# app/handlers/settings.py
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(F.text == "⚙️ Настройки")
async def settings_menu(message: Message, state: FSMContext):
    await message.answer(
        "Здесь будут настройки профиля (изменить ФИО, телефон, язык и др.)",
        reply_markup=ReplyKeyboardRemove()
    )
