from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_dentist_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Новый наряд")],
            [KeyboardButton(text="📋 Мои заказы")],
            [KeyboardButton(text="🏭 Мои лаборатории")],
            [KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="✉️ Обратная связь")]
        ],
        resize_keyboard=True
    )

def get_technician_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Заказы")],
            [KeyboardButton(text="👩‍⚕️ Стоматолог")],
            [KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="✉️ Обратная связь")]
        ],
        resize_keyboard=True
    )
