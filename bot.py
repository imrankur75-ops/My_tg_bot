

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from g4f.client import Client

logging.basicConfig(level=logging.INFO)

# КЛЮЧ БОТА (Строго ваш токен из BotFather)
BOT_TOKEN = "8273788160:AAFmJvdaERDtp_Xx2y7cNQ7FcvU6ONUuvmU"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
ai_client = Client()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я твой безлимитный ИИ-ассистент. Я обновил настройки и готов искать для тебя всё что угодно!")

@dp.message()
async def handle_message(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # Список надежных бесплатных моделей на выбор
    models_to_try = ["llama-3.1-70b", "gpt-4o", "mixtral-8x7b"]
    answer = None
    
    for model in models_to_try:
        try:
            # Запрос к ИИ с веб-поиском в реальном времени
            response = ai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message.text}],
                web_search=True
            )
            answer = response.choices.message.content
            if answer and not "Error" in answer:
                break # Если получили хороший ответ, выходим из цикла
        except Exception as e:
            logging.error(f"Модель {model} не ответила, пробуем следующую...")
            continue
            
    if answer:
        await message.answer(answer)
    else:
        await message.answer("Все бесплатные сервера сейчас сильно загружены. Попробуй переформулировать вопрос или написать через минуту!")

# Запуск бота
print("Бот успешно перезапущен на стабильных серверах!")
await dp.start_polling(bot)
