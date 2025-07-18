# app/handlers/technician.py
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from dentshare_bot.states import TechnicianMenuStates
from dentshare_bot.crud import get_orders_by_technician
from dentshare_bot.models import Order

router = Router()

@router.message(F.text == "📋 Заказы")
async def view_orders(message: Message, state: FSMContext):
    orders = await get_orders_by_technician(message.from_user.id)
    if not orders:
        await message.answer("Нет заказов для вашей лаборатории.")
        return
    order = orders[0]  # Для MVP — только первый
    await state.update_data(order_id=order.id)
    kb = ReplyKeyboardMarkup([["Принять"], ["Отклонить"]], resize_keyboard=True)
    text = (
        f"Заказ #{order.id}\n"
        f"Стоматолог: {order.dentist_id}\n"
        f"Комментарий: {order.comment}\n"
        f"Принять или отклонить?"
    )
    await state.set_state(TechnicianMenuStates.accept_order)
    await message.answer(text, reply_markup=kb)

@router.message(TechnicianMenuStates.accept_order, F.text == "Принять")
async def accept_order(message: Message, state: FSMContext):
    # Здесь ты бы обновил статус заказа
    await state.set_state(TechnicianMenuStates.comment)
    skip_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Пропустить")]],
        resize_keyboard=True
    )
    await message.answer("Комментарий к заказу (можно пропустить):", reply_markup=skip_kb)

@router.message(TechnicianMenuStates.accept_order, F.text == "Отклонить")
async def decline_order(message: Message, state: FSMContext):
    await state.set_state(TechnicianMenuStates.decline_order)
    await message.answer("Укажите причину отказа:")

@router.message(TechnicianMenuStates.comment)
async def tech_comment(message: Message, state: FSMContext):
    # Можно обработать комментарий, сохранить его в историю
    finish_kb = ReplyKeyboardMarkup([[KeyboardButton("Завершить работу")]], resize_keyboard=True)
    await state.set_state(TechnicianMenuStates.finish_work)
    await message.answer("Когда работа будет готова — нажмите 'Завершить работу'.", reply_markup=finish_kb)

@router.message(TechnicianMenuStates.finish_work, F.text == "Завершить работу")
async def tech_finish_work(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Работа завершена, стоматолог уведомлен.", reply_markup=ReplyKeyboardRemove())
