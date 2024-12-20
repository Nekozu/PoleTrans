# 🐾 PoleTrans

A powerful **Telegram Bot** for translating text, voice, and images using **NLLB-200** with **dl-translate**!

---

## ✨ Features

### 📝 Text Translation
- Translate text messages seamlessly into multiple languages.
- Powered by **NLLB-200**, ensuring high-quality and more accurate translations.

### 🎤 Voice Translation
- Supports speech-to-text and translation for audio messages.
- Utilizes **Speech Recognition** for extracting text from voice.

### 🖼️ Image Translation
- Extract and translate text from images.
- Leverages **Tesseract OCR** for reliable text detection.

---

## 🛠️ Library used

| Library         | Purpose                          |
|--------------------|----------------------------------|
| **NLLB-200**      | High-quality language translation |
| **dl-translate**  | Lightweight translation toolkit   |
| **SpeechRecognition** | Convert voice to text          |
| **Tesseract OCR** | Extract text from images         |
| **PyTelegramBotAPI** | Telegram bot functionality     |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Telegram Bot Token
- Disk space upt o 5 GB+ and ram 2 GB+ (for NLLB running)
- Dependencies installed via `requirements.txt`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/nekozu-translator-bot.git
   cd nekozu-translator-bot
   ```

2. Install dependencies:
   ```bash
   sudo apt install tesseract-ocr ffmpeg
   pip install -r requirements.txt
   ```

3. Set up your `.env` file with your Telegram bot token:
   ```env
   TOKEN=your-telegram-bot-token
   ```

4. Run the bot:
   ```bash
   python main.py
   ```

---

## 📚 How It Works

1. **Text Translation**: Send a text message, and the bot will reply with the translated text in your chosen language.

2. **Voice Translation**: Send a voice message, and the bot will transcribe and translate it.

3. **Image Translation**: Send an image, and the bot will extract and translate the text it contains.

---

## 🌐 Supported Languages
With the power of **NLLB-200**, the bot supports **200+ languages**!

---

## 🧑‍💻 Contributing

We welcome contributions to make this project even better! Here's how you can help:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add a new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## ⭐️ Stars
Don't forget to give a star!

<h2 id="star_hist">Star History</h2>

<a href="https://star-history.com/#Nekozu/PoleTrans&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Nekozu/PoleTrans&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Nekozu/PoleTrans&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Nekozu/PoleTrans&type=Date"/>
 </picture>
</a>
