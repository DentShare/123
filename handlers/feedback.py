# app/handlers/feedback.py
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(F.text == "✉️ Обратная связь")
async def feedback_start(message: Message, state: FSMContext):
    await message.answer("Введите ваш вопрос или сообщение:", reply_markup=ReplyKeyboardRemove())
    await state.set_state("feedback_waiting")

@router.message(F.state == "feedback_waiting")
async def feedback_receive(message: Message, state: FSMContext):
    # Здесь можно отправить сообщение админу через бот или сохранить в базу
    await message.answer("Спасибо! Ваше сообщение передано администрации.")
    await state.clear()
