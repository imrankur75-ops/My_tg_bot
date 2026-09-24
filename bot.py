import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from groq import Groq

# Настройки логирования
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# ТОКЕНЫ
TELEGRAM_TOKEN = "8273788160:AAFmJvdaERDtp_Xx2y7cNQ7FcvU6ONUuvmU"
GROQ_API_KEY = "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"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
groq_client = Groq(api_key=GROQ_API_KEY)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я твой безлимитный ИИ-ассистент. Всё настроено, задавай любой вопрос!")

@dp.message()
async def handle_message(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        # Используем основную и стабильную бесплатную модель Groq
        completion = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "Ты полезный ИИ-ассистент. Отвечай на русском языке."},
                {"role": "user", "content": message.text}
            ],
            temperature=0.7
        )
        answer = completion.choices.message.content
        await message.answer(answer)
    except Exception as e:
        logging.error(f"Ошибка Groq: {e}")
        await message.answer("Сеть немного занята. Пожалуйста, попробуй отправить запрос еще раз через пару секунд!")

async def main():
    # Эта строчка сбрасывает старые конфликты запусков при перезапуске сервера
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")

            
