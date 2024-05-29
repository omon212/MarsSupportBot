from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
import sqlite3
from loader import dp
from states.state import States
from utils.database import connect, cursor, UserRegister
from keyboards.default.default import fullname_button

connect = sqlite3.connect('/home/sharif/PycharmProjects/MarsSupportBot/support.db')
cursor = connect.cursor()
from data.config import ADMINS
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    print(ADMINS)
    if str(message.from_user.id) in ADMINS:
        await message.answer('Assalomu aleykum')
        button = ReplyKeyboardMarkup(resize_keyboard=True)
        button.add(KeyboardButton('Yangi Savol qo`shish'))
        await message.answer('Siz admin paneldasiz !', reply_markup=button)
        await States.admin_state.set()
    else:

        await message.answer(f"Assalomu aleykum {message.from_user.first_name}")
        await message.answer("""
    Avval to'liq Ism Familyangizni yuboring,
    yoki <b>Omonullo Raimkulov</b> ko'rinishida yozing.
        """, reply_markup=fullname_button)
        await States.fullname.set()


@dp.message_handler(content_types="contact", state=States.fullname)
async def fulname(message: types.Message, state: FSMContext):
    cursor.execute("INSERT INTO support (user_id, fullname) VALUES (?, ?)",
                   (message.from_user.id, message.contact.full_name))
    connect.commit()
    await message.answer('Sizni qanday Savollar qiynayapti')
