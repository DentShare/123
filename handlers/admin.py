# app/handlers/admin.py
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from dentshare_bot.models import User
from dentshare_bot.crud import get_user_by_tg_id

router = Router()

@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    # Проверим, что пользователь — админ (есть в базе и role == admin)
    user = await get_user_by_tg_id(str(message.from_user.id))
    if user and user.role == "admin":
        await message.answer(
            "Панель администратора:\n"
            "Пока что: просмотр пользователей и заказов (заглушка)\n"
            "План: вывод статистики, управление пользователями/заказами",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer("Доступ запрещён. Вы не администратор.", reply_markup=ReplyKeyboardRemove())
