# app/handlers/dentist.py

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from dentshare_bot.states import DentistMenuStates, OrderFSM
from dentshare_bot.crud import get_orders_by_dentist, create_order, add_lab
from dentshare_bot.models import Order

router = Router()

# --- Создание нового наряда ---

@router.message(F.text == "📝 Новый наряд")
async def new_order_start(message: Message, state: FSMContext):
    await state.set_state(OrderFSM.choose_lab)
    await message.answer("Введите ID лаборатории для отправки наряда:")

@router.message(OrderFSM.choose_lab)
async def order_choose_lab(message: Message, state: FSMContext):
    await state.update_data(lab_id=message.text)
    kb = ReplyKeyboardMarkup([["На зубах", "На имплантах"]], resize_keyboard=True)
    await state.set_state(OrderFSM.choose_location_type)
    await message.answer("Выберите место установки:", reply_markup=kb)

@router.message(OrderFSM.choose_location_type)
async def order_choose_location_type(message: Message, state: FSMContext):
    await state.update_data(place_type=message.text)
    kb = ReplyKeyboardMarkup([["Коронка", "Мост"]], resize_keyboard=True)
    await state.set_state(OrderFSM.choose_construction_type)
    await message.answer("Выберите тип конструкции:", reply_markup=kb)

@router.message(OrderFSM.choose_construction_type)
async def order_choose_construction_type(message: Message, state: FSMContext):
    await state.update_data(construction_type=message.text)
    await state.set_state(OrderFSM.choose_teeth)
    await message.answer("Укажите номера зубов (например, 11,12,13):", reply_markup=ReplyKeyboardRemove())

@router.message(OrderFSM.choose_teeth)
async def order_choose_teeth(message: Message, state: FSMContext):
    nums = [int(x.strip()) for x in message.text.split(",") if x.strip().isdigit()]
    await state.update_data(teeth_numbers=nums)
    kb = ReplyKeyboardMarkup([["Циркон", "E.Max"], ["PMMA", "Металлокерамика"], ["Рефрактор"]], resize_keyboard=True)
    await state.set_state(OrderFSM.choose_material)
    await message.answer("Выберите материал:", reply_markup=kb)

@router.message(OrderFSM.choose_material)
async def order_choose_material(message: Message, state: FSMContext):
    await state.update_data(material=message.text)
    kb = ReplyKeyboardMarkup(
        [["A1", "A2", "B1", "B2"], ["C1", "C2", "Bleach"]], resize_keyboard=True
    )
    await state.set_state(OrderFSM.choose_color)
    await message.answer("Выберите цвет:", reply_markup=kb)

@router.message(OrderFSM.choose_color)
async def order_choose_color(message: Message, state: FSMContext):
    await state.update_data(color=message.text)
    skip_kb = ReplyKeyboardMarkup([[KeyboardButton("Пропустить")]], resize_keyboard=True)
    await state.set_state(OrderFSM.upload_files)
    await message.answer("Загрузите файл (можно пропустить):", reply_markup=skip_kb)

@router.message(OrderFSM.upload_files)
async def order_upload_files(message: Message, state: FSMContext):
    has_file = not ("пропустить" in message.text.lower())
    await state.update_data(has_file=has_file)
    skip_kb = ReplyKeyboardMarkup([[KeyboardButton("Пропустить")]], resize_keyboard=True)
    await state.set_state(OrderFSM.add_comment)
    await message.answer("Комментарий к наряду (можно пропустить):", reply_markup=skip_kb)

@router.message(OrderFSM.add_comment)
async def order_add_comment(message: Message, state: FSMContext):
    comment = "" if "пропустить" in message.text.lower() else message.text
    await state.update_data(comment=comment)
    data = await state.get_data()
    text = (
        "Проверьте наряд:\n"
        f"Лаборатория: {data['lab_id']}\n"
        f"Установка: {data['place_type']}\n"
        f"Тип: {data['construction_type']}\n"
        f"Зубы: {', '.join(map(str, data['teeth_numbers']))}\n"
        f"Материал: {data['material']}\n"
        f"Цвет: {data['color']}\n"
        f"Комментарий: {data['comment']}\n"
        f"Файл: {'да' if data['has_file'] else 'нет'}"
    )
    kb = ReplyKeyboardMarkup(
        [[KeyboardButton("Подтвердить")], [KeyboardButton("Редактировать")]],
        resize_keyboard=True
    )
    await state.set_state(OrderFSM.preview)
    await message.answer(text, reply_markup=kb)

@router.message(OrderFSM.preview, F.text == "Подтвердить")
async def order_confirm(message: Message, state: FSMContext):
    data = await state.get_data()
    order_dict = {
        "dentist_id": message.from_user.id,
        "lab_id": int(data["lab_id"]),
        "comment": data["comment"],
        "status": "new"
        # Позиции и файлы добавляются отдельно через другие CRUD-функции
    }
    await create_order(order_dict)
    await state.clear()
    await message.answer("Заказ отправлен!", reply_markup=ReplyKeyboardRemove())

@router.message(OrderFSM.preview, F.text == "Редактировать")
async def order_edit(message: Message, state: FSMContext):
    await state.set_state(OrderFSM.choose_lab)
    await message.answer("Введите ID лаборатории для отправки наряда:")

# --- Просмотр заказов ---

@router.message(F.text == "📋 Мои заказы")
async def dentist_my_orders(message: Message, state: FSMContext):
    orders = await get_orders_by_dentist(message.from_user.id)
    if not orders:
        await message.answer("У вас нет заказов.")
        return
    text = "\n".join([f"#{o.id}: {o.status}" for o in orders])
    await message.answer("Ваши заказы:\n" + text)

# --- Добавление лаборатории ---

@router.message(F.text == "🏭 Мои лаборатории")
async def dentist_labs(message: Message, state: FSMContext):
    await message.answer("Функционал лабораторий будет реализован в следующей версии.")

# --- Настройки ---

@router.message(F.text == "⚙️ Настройки")
async def dentist_settings(message: Message, state: FSMContext):
    await message.answer("Здесь будут настройки профиля.")

# --- Обратная связь ---

@router.message(F.text == "✉️ Обратная связь")
async def dentist_feedback(message: Message, state: FSMContext):
    await message.answer("Введите ваше сообщение или вопрос. Мы обязательно ответим!")
