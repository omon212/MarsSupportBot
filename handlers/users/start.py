from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
import sqlite3
from loader import dp
from states.state import States
from keyboards.default.default import fullname_button
from data.config import DATABASE_PATH

connect = sqlite3.connect(DATABASE_PATH)
cursor = connect.cursor()
from data.config import ADMINS
from keyboards.default.default import *


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    print(ADMINS)
    if str(message.from_user.id) in ADMINS:
        await message.answer(f'Assalomu aleykum <b>{message.from_user.full_name}</b>')
        await message.answer('Siz admin paneldasiz 👤🎛', reply_markup=admin_button)
        await States.admin_state.set()
    else:
        user = cursor.execute("SELECT * FROM support WHERE user_id = ?", (message.from_user.id,)).fetchone()
        print(user)
        if user is not None:
            await message.answer(f"Assalomu aleykum <b>{message.from_user.first_name}</b>")
            await message.answer('Sizni qanday Savollar qiynayapti ?')
        else:
            await message.answer(f"Assalomu aleykum {message.from_user.first_name}")
            await message.answer("""
Avval to'liq <b>Ism Familyangizni</b> yuboring,
                        """, reply_markup=fullname_button)
            await States.fullname.set()


@dp.message_handler(content_types="contact", state=States.fullname)
async def fulname(message: types.Message, state: FSMContext):
    cursor.execute("INSERT INTO support (user_id, fullname) VALUES (?, ?)",
                   (message.from_user.id, message.contact.full_name))
    connect.commit()
    await message.answer('Sizni qanday Savollar qiynayapti ?')
