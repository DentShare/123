from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from dentshare_bot.states import RegistrationStates
from dentshare_bot.database import async_session
from dentshare_bot.models import User
from dentshare_bot.config import ADMIN_SECRET
from dentshare_bot.keyboards.main_menu import get_dentist_main_menu, get_technician_main_menu

router = Router()

# Старт — выбор роли
@router.message(F.text == "/start")
async def reg_start(message: Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🦷 Я стоматолог"),
                KeyboardButton(text="🏭 Я техник")
            ]
        ],
        resize_keyboard=True
    )
    await state.set_state(RegistrationStates.choosing_role)
    await message.answer("Добро пожаловать! Выберите вашу роль:", reply_markup=kb)

# FSM: выбор роли
@router.message(RegistrationStates.choosing_role)
async def reg_choose_role(message: Message, state: FSMContext):
    role = None
    text = message.text.lower()
    if "стоматолог" in text:
        role = "dentist"
    elif "техник" in text:
        role = "technician"
    elif "администратор" in text:
        role = "admin"
    else:
        await message.answer("Пожалуйста, выберите одну из ролей кнопкой.")
        return

    await state.update_data(role=role)
    if role == "admin":
        await state.set_state(RegistrationStates.confirming)
        await message.answer("Введите секретный ключ администратора:", reply_markup=ReplyKeyboardRemove())
    else:
        await state.set_state(RegistrationStates.entering_full_name)
        await message.answer("Введите ФИО:", reply_markup=ReplyKeyboardRemove())

# FSM: ФИО
@router.message(RegistrationStates.entering_full_name)
async def reg_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(RegistrationStates.entering_phone)
    await message.answer("Введите основной телефон:")

# FSM: основной телефон
@router.message(RegistrationStates.entering_phone)
async def reg_phone(message: Message, state: FSMContext):
    await state.update_data(phone_main=message.text)
    skip_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Пропустить")]],
        resize_keyboard=True
    )
    await state.set_state(RegistrationStates.entering_extra_phones)
    await message.answer("Дополнительные телефоны (можно пропустить):", reply_markup=skip_kb)

# FSM: доп. телефоны
@router.message(RegistrationStates.entering_extra_phones)
async def reg_extra_phones(message: Message, state: FSMContext):
    if "пропустить" in message.text.lower():
        await state.update_data(phone_extra="")
    else:
        await state.update_data(phone_extra=message.text)
    await state.set_state(RegistrationStates.entering_org_name)
    await message.answer("Название клиники/лаборатории:", reply_markup=ReplyKeyboardRemove())

# FSM: организация
@router.message(RegistrationStates.entering_org_name)
async def reg_org_name(message: Message, state: FSMContext):
    await state.update_data(clinic_lab_name=message.text)
    await state.set_state(RegistrationStates.entering_org_addresses)
    await message.answer("Адрес(а) клиники/лаборатории:")

# FSM: адреса
@router.message(RegistrationStates.entering_org_addresses)
async def reg_org_addr(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    text = (
        "Проверьте ваши данные:\n"
        f"Роль: {data.get('role', '-')}\n"
        f"ФИО: {data.get('full_name', '-')}\n"
        f"Телефон: {data.get('phone_main', '-')}\n"
        f"Доп. телефоны: {data.get('phone_extra', '-')}\n"
        f"Организация: {data.get('clinic_lab_name', '-')}\n"
        f"Адрес: {data.get('address', '-')}"
    )
    confirm_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Подтвердить")],
            [KeyboardButton(text="Отмена")]
        ],
        resize_keyboard=True
    )
    await state.set_state(RegistrationStates.confirming)
    await message.answer(text, reply_markup=confirm_kb)

# FSM: подтверждение регистрации
@router.message(RegistrationStates.confirming)
async def reg_confirm(message: Message, state: FSMContext):
    data = await state.get_data()
    text = message.text.lower().strip()
    role = data.get("role")

    if role == "admin":
        # обработка админа
        pass
    elif "подтверд" in text:
        # здесь размещай отправку меню!
        await state.clear()
        if role == "dentist":
            await message.answer(
                "Регистрация завершена! Вот ваше меню стоматолога:",
                reply_markup=get_dentist_main_menu()
            )
        elif role == "technician":
            await message.answer(
                "Регистрация завершена! Вот ваше меню техника:",
                reply_markup=get_technician_main_menu()
            )
        else:
            await message.answer("Регистрация завершена!", reply_markup=ReplyKeyboardRemove())
    else:
        await state.clear()
        await message.answer("Регистрация отменена.", reply_markup=ReplyKeyboardRemove())