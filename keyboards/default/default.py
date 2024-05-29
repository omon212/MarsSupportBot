from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

fullname_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Ism Familyangizni Jo'natish", request_contact=True)
        ]
    ]
)
