# app/main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dentshare_bot.config import BOT_TOKEN
from dentshare_bot.handlers import registration, dentist, technician, admin

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(registration.router)
    dp.include_router(dentist.router)
    dp.include_router(technician.router)
    dp.include_router(admin.router)
    print("DentShare бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
