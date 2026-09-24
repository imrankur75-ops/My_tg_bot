import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from groq import Groq

# Настройки логирования
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# ТОКЕНЫ (Вставь свои ключи внутрь кавычек!)
TELEGRAM_TOKEN = "8273788160:AAFmJvdaERDtp_Xx2y7cNQ7FcvU6ONUuvmU"
GROQ_API_KEY = "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"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Инициализируем официальный клиент Groq
groq_client = Groq(api_key=GROQ_API_KEY)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я твой обновленный ИИ-ассистент на движке Groq. Теперь я отвечаю пулей и никогда не зависаю!")

@dp.message()
async def handle_message(message: types.Message):
    # Анимация "печатает..."
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    try:
        # Делаем сверхбыстрый официальный запрос к модели Llama 3.1
        completion = groq_client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": "Ты полезный ИИ-ассистент. Отвечай на русском языке."},
                {"role": "user", "content": message.text}
            ],
            temperature=0.7
        )
        
        answer = completion.choices[0].message.content
        await message.answer(answer)
        
    except Exception as e:
        logging.error(f"Ошибка Groq: {e}")
        await message.answer("Произошла ошибка при генерации ответа. Попробуй еще раз!")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")
        
