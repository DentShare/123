# app/handlers/file.py
from aiogram import Router, F
from aiogram.types import Message
from pathlib import Path

router = Router()

@router.message(F.content_type.in_({"document", "photo"}))
async def save_file(message: Message):
    # Сохраняет файл локально, путь для MVP
    file = message.document or message.photo[-1]
    file_id = file.file_id
    file_info = await message.bot.get_file(file_id)
    file_path = Path("files") / (file.file_unique_id + "_" + (file.file_name if hasattr(file, "file_name") else ".jpg"))
    await message.bot.download_file(file_info.file_path, file_path)
    await message.answer("Файл сохранён!")
