import os
import io
from PIL import Image
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

def apply_overlay(image_bytes):
    user_img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    overlay = Image.open("overlay.png").convert("RGBA")

    overlay = overlay.resize(user_img.size)
    result = Image.alpha_composite(user_img, overlay)

    buf = io.BytesIO()
    result.save(buf, "PNG")
    buf.seek(0)
    return buf

@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded = bot.download_file(file_info.file_path)

        result = apply_overlay(downloaded)
        bot.send_photo(message.chat.id, result)

    except Exception as e:
        bot.send_message(message.chat.id, "❌ Ошибка обработки изображения")

@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "📷 Отправь фото")

bot.infinity_polling()
