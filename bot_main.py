import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import asyncio
from datetime import datetime


from hidden import tokenfile

API_TOKEN = tokenfile.TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_ids = set()


@dp.message()
async def echo(message: Message):
    user_ids.add(message.chat.id)
    await message.answer(message.text)


async def send_time():
    now = datetime.now().strftime("%H:%M:%S")
    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=user_id, text=f"Текущее время: {now}")
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

# Запуск планировщика
scheduler = AsyncIOScheduler()
scheduler.add_job(send_time, CronTrigger(minute=1))
scheduler.start()

async def main():
    # Инициализация планировщика
    scheduler = AsyncIOScheduler()
    # Запуск задачи для отправки в отведенный период времени
    scheduler.add_job(send_time, IntervalTrigger(minutes=5), max_instances=2)  # Увеличиваем max_instances до 2
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
