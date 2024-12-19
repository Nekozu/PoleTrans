from telebot.async_telebot import AsyncTeleBot
import dl_translate as dlt
from fast_langdetect import detect
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import json
import os
import pytesseract
import speech_recognition as sr
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN') # load the bot token from env

bot = AsyncTeleBot(TOKEN)# Fasttext model load
dl = dlt.TranslationModel("nllb200", device="cpu") # you can change it as cpu, cuda, or auto. prefer to cpu

def load_user_settings():
    if os.path.exists('user_settings.json'):
        with open('user_settings.json', 'r') as f:
            return json.load(f)
    return {}

def save_user_settings(settings):
    with open('user_settings.json', 'w') as f:
        json.dump(settings, f)

# MESSAGE
# CUSTOMIZE AS YOU NEED
START_MSG = """
🌟 Welcome to the PoleTrans Bot! 🌍

I can help you translate text, photos, and voice messages into multiple languages! 🎯

Here's what I can do:
📝 Text Translation
📸 Photo Text Translation  
🗣 Voice Message Translation

Commands:
/lang - Set your preferred language
/help - Show help menu

Just send me any text, photo, or voice message to get started! ✨
"""
HELP_MSG = """
Here is guide for using this bots:
📝 Text Translation:
- Simply send any text message to translate it
- The bot will detect the language and translate to your selected language

📸 Photo Text Translation:
- Send a photo containing text
- The bot will extract and translate the text
- You can also get audio pronunciation of the translation

🗣 Voice Message Translation:
- Send a voice message
- The bot will convert speech to text
- Then translate it to your preferred language

⚙️ Settings:
/lang - Choose your preferred target language
/help - Show this help menu

Note: Make sure to select your preferred language first using /lang command!

💡 Tips:
- For best results, send clear photos of text
- Speak clearly when sending voice messages
- You can change your language anytime using /lang
"""

@bot.message_handler(commands=["start"])
async def start(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔧 Help", callback_data="help"),
        InlineKeyboardButton("🌍 Select Language", callback_data="lang")
    )
    await bot.reply_to(message, START_MSG, reply_markup=keyboard)

@bot.message_handler(commands=["help"])
async def help(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Back", callback_data="back")
    )
    await bot.reply_to(message, HELP_MSG, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "help")
async def helpcall(call):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Back", callback_data="back")
    )
    await bot.edit_message_text(text=HELP_MSG, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: call.data == "back")
async def back(call):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔧 Help", callback_data="help"),
        InlineKeyboardButton("🌍 Select Language", callback_data="lang")
    )
    await bot.edit_message_text(text=START_MSG, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "lang")
async def langcall(call):
    user_settings = load_user_settings()
    current_lang = user_settings.get(str(call.from_user.id))
    
    getlang = dlt.utils.get_lang_code_map()
    lang_code_to_name = {code: name.upper() for name, code in getlang.items()}
    
    msg_text = "Please select your preferred language:"
    if current_lang and current_lang in lang_code_to_name:
        msg_text = f"🈷️ Current language: {lang_code_to_name[current_lang]} ({current_lang})\n\nSelect a language:"
    
    buttons = []
    row = []
    count = 0
    
    lang_items = list(getlang.items())
    total_pages = (len(lang_items) + 49) // 50
    current_page = 1
    
    page_langs = lang_items[:50]
    
    for lang_name, lang_code in page_langs:
        display_text = f"{lang_name} ({lang_code})"
        row.append(InlineKeyboardButton(display_text, callback_data=f"setlang_{lang_code}"))
        count += 1
        
        if count % 3 == 0:
            buttons.append(row)
            row = []
    
    if row:
        buttons.append(row)
        
    if total_pages > 1:
        buttons.append([InlineKeyboardButton("Next ➡️", callback_data=f"langpage_{current_page + 1}")])
    
    keyboard = InlineKeyboardMarkup(buttons)

    try:
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=msg_text,
            reply_markup=keyboard
        )
    except Exception as e:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=msg_text,
            reply_markup=keyboard
        )

@bot.message_handler(commands=["lang"])
async def lang(message):
    user_settings = load_user_settings()
    current_lang = user_settings.get(str(message.from_user.id))
    
    getlang = dlt.utils.get_lang_code_map()
    lang_code_to_name = {code: name.upper() for name, code in getlang.items()}
    
    msg_text = "Please select your preferred language:"
    if current_lang and current_lang in lang_code_to_name:
        msg_text = f"🈷️ Current language: {lang_code_to_name[current_lang]} ({current_lang})\n\nSelect a language:"
    
    buttons = []
    row = []
    count = 0
    
    lang_items = list(getlang.items())
    total_pages = (len(lang_items) + 49) // 50
    current_page = 1
    
    page_langs = lang_items[:50]
    
    for lang_name, lang_code in page_langs:
        display_text = f"{lang_name} ({lang_code})"
        row.append(InlineKeyboardButton(display_text, callback_data=f"setlang_{lang_code}"))
        count += 1
        
        if count % 3 == 0:
            buttons.append(row)
            row = []
            
    if row:
        buttons.append(row)
        
    if total_pages > 1:
        buttons.append([InlineKeyboardButton("Next ➡️", callback_data=f"langpage_{current_page + 1}")])
    
    keyboard = InlineKeyboardMarkup(buttons)
    await bot.reply_to(message, msg_text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("setlang_"))
async def callback_set_language(call):
    lang_code = call.data.split("_")[1]
    
    user_settings = load_user_settings()
    user_settings[str(call.from_user.id)] = lang_code
    save_user_settings(user_settings)
    
    getlang = dlt.utils.get_lang_code_map()
    lang_code_to_name = {code: name.upper() for name, code in getlang.items()}
    lang_name = lang_code_to_name.get(lang_code, lang_code)
    
    await bot.answer_callback_query(call.id, f"Language set to {lang_name} ({lang_code})")

@bot.callback_query_handler(func=lambda call: call.data.startswith("langpage_"))
async def callback_language_page(call):
    page = int(call.data.split("_")[1])
    getlang = dlt.utils.get_lang_code_map()
    lang_items = list(getlang.items())
    total_pages = (len(lang_items) + 49) // 50
    
    start_idx = (page - 1) * 50
    end_idx = start_idx + 50
    page_langs = lang_items[start_idx:end_idx]
    
    buttons = []
    row = []
    count = 0
    
    for lang_name, lang_code in page_langs:
        display_text = f"{lang_name} ({lang_code})"
        row.append(InlineKeyboardButton(display_text, callback_data=f"setlang_{lang_code}"))
        count += 1
        
        if count % 3 == 0:
            buttons.append(row)
            row = []
    
    if row:
        buttons.append(row)
        
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"langpage_{page-1}"))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"langpage_{page+1}"))
    if nav_buttons:
        buttons.append(nav_buttons)
    
    keyboard = InlineKeyboardMarkup(buttons)
    await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyboard)

async def translate_text(text: str, target_lang: str) -> str:
    try:
        # Load language codes
        with open('languages.json', 'r') as f:
            langcode = json.load(f)
            
        # Detect source language
        teks = text.replace("\n", " ")
        detection_result = await asyncio.to_thread(detect, teks)
        src = detection_result['lang']
        
        # Convert language codes
        src_iso3 = langcode.get(src) 
        tgt_iso3 = langcode.get(target_lang.lower())
        
        if not (src_iso3 and tgt_iso3):
            return "Unsupported language combination. Please check the language codes."
            
        # Translate using NLLB
        translated = await asyncio.to_thread(dl.translate, text, source=src_iso3, target=tgt_iso3)
        return translated
        
    except Exception as e:
        import traceback
        print(traceback.print_exc())
        print(f"Translation error: {str(e)}")
        return "An error occurred during translation."
# Text translator
@bot.message_handler(content_types=['text'])
async def handle_text(message):
    if message.text.startswith('/'):
        return
    user_settings = load_user_settings()
    target_lang = user_settings.get(str(message.from_user.id))
    
    if not target_lang:
        await bot.reply_to(message, "Please set your preferred language first using /lang command!")
        return

    try:
        translation = await translate_text(message.text, target_lang)
        response = f"📝 Translation ({target_lang.upper()}):\n\n{translation}"
        await bot.reply_to(message, response)
    except Exception as e:
        await bot.reply_to(message, f"❌ Translation error: {str(e)}")
# Photo translation
@bot.message_handler(content_types=['photo'])
async def handle_photo(message):
    user_settings = load_user_settings()
    target_lang = user_settings.get(str(message.from_user.id))
    
    if not target_lang:
        await bot.reply_to(message, "Please set your preferred language first using /lang command!")
        return
    
    try:
        file_info = await bot.get_file(message.photo[-1].file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        
        with open("temp_image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        
        text = pytesseract.image_to_string("temp_image.jpg")
        os.remove("temp_image.jpg")
        
        if not text.strip():
            await bot.reply_to(message, "❌ No text detected in the image!")
            return
            
        translation = await translate_text(text, target_lang)
        
        response = f"📷 Extracted Text:\n{text}\n\n"
        response += f"📝 Translation ({target_lang.upper()}):\n\n"
        response += f"{translation}"
        
        await bot.reply_to(message, response)
    except Exception as e:
        await bot.reply_to(message, f"❌ Error processing image: {str(e)}")
# Voice translation. But maybe sometimes not accurate :D
@bot.message_handler(content_types=['voice'])
async def handle_voice(message):
    user_settings = load_user_settings()
    target_lang = user_settings.get(str(message.from_user.id))
    
    if not target_lang:
        await bot.reply_to(message, "Please set your preferred language first using /lang command!")
        return
    
    try:
        file_info = await bot.get_file(message.voice.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        
        with open("temp_voice.ogg", 'wb') as new_file:
            new_file.write(downloaded_file)
        
        os.system("ffmpeg -i temp_voice.ogg temp_voice.wav -y")
        
        r = sr.Recognizer()
        with sr.AudioFile('temp_voice.wav') as source:
            audio = r.record(source)
            text = r.recognize_sphinx(audio)
        
        os.remove("temp_voice.ogg")
        os.remove("temp_voice.wav")
        
        translation = await translate_text(text, target_lang)
        
        response = f"🎤 Transcribed Text:\n{text}\n\n"
        response += f"📝 Translation ({target_lang.upper()}):\n\n"
        response += f"{translation}"
        
        await bot.reply_to(message, response)
    except Exception as e:
        await bot.reply_to(message, f"❌ Error processing voice message: {str(e)}")

if __name__ == "__main__":
    asyncio.run(bot.polling())
