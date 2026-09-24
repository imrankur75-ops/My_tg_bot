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
GROQ_API_KEY = "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"  # Ваш ключ подставится сам, если стерся — вставьте заново gsk_...

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
groq_client = Groq(api_key=GROQ_API_KEY)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я твой безлимитный ИИ-ассистент. Я исправил модели и готов отвечать пулей!")

@dp.message()
async def handle_message(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # Список САМЫХ АКТУАЛЬНЫХ моделей Groq на выбор (Meta Llama 3.3 и Google Gemma 2)
    models_to_try = ["llama-3.3-70b-specdec", "llama3-70b-8192", "gemma2-9b-it"]
    answer = None
    
    for model in models_to_try:
        try:
            completion = groq_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Ты полезный ИИ-ассистент. Отвечай на русском языке."},
                    {"role": "user", "content": message.text}
                ],
                temperature=0.7
            )
            answer = completion.choices.message.content
            if answer:
                break  # Если модель ответила успешно, выходим из цикла
        except Exception as e:
            logging.error(f"Модель {model} выдала ошибку: {e}. Пробую следующую...")
            continue
            
    if answer:
        await message.answer(answer)
    else:
        await message.answer("В данный момент сервера Groq обновляются. Попробуй написать еще раз через пару минут!")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")

        
