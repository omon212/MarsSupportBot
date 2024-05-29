from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

fullname_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Ism Familyani Yuborish 👤", request_contact=True)
        ]
    ],
    resize_keyboard=True
)

admin_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Yangi Savol qo`shish 🆕"),
            KeyboardButton("Savollarni Ko'rish 👀"),
            KeyboardButton("Savollarni O'chirish ❌")
        ]
    ],
    resize_keyboard=True
)

savollar_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Savollar 👀")
        ]
    ],
    resize_keyboard=True
)