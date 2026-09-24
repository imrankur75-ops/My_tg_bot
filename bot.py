import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from g4f.client import Client

# Включаем логирование
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

BOT_TOKEN = "8273788160:AAFmJvdaERDtp_Xx2y7cNQ7FcvU6ONUuvmU"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
ai_client = Client()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я твой безлимитный ИИ-ассистент. Я готов искать для тебя всё что угодно!")

@dp.message()
async def handle_message(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    models_to_try = ["llama-3.1-70b", "gpt-4o", "mixtral-8x7b"]
    answer = None
    
    for model in models_to_try:
        try:
            response = ai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message.text}],
                web_search=True
            )
            answer = response.choices.message.content
            if answer and not "Error" in answer:
                break
        except Exception as e:
            continue
            
    if answer:
        await message.answer(answer)
    else:
        await message.answer("Все бесплатные сервера сейчас заняты. Попробуй еще раз через минуту!")

async def main():
    # Запускаем бота, предварительно удалив старые зависшие запросы
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Правильный запуск бесконечного цикла на сервере
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")
        
