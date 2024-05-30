from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
import sqlite3
from loader import dp
from states.state import States
from keyboards.default.default import fullname_button
from data.config import DATABASE_PATH
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

connect = sqlite3.connect(DATABASE_PATH)
cursor = connect.cursor()
from data.config import ADMINS
from keyboards.default.default import *


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        await message.answer(f'Assalomu aleykum <b>{message.from_user.full_name}</b>')
        await message.answer('Siz admin paneldasiz 👤🎛', reply_markup=admin_button)
        await States.admin_state.set()
    else:
        user = cursor.execute("SELECT * FROM support WHERE user_id = ?", (message.from_user.id,)).fetchone()
        if user is not None:
            await message.answer(f"Assalomu aleykum <b>{message.from_user.first_name}</b>")
            await message.answer("Sizni qanday savollar qiynamoqda", reply_markup=savollar_btn)
            await States.savollar.set()
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
    await message.answer("Sizni qanday savollar qiynamoqda ?", reply_markup=savollar_btn)
    await States.savollar.set()


@dp.message_handler(text="Savollar 👀", state=States.savollar)
async def savollar(message: types.Message, state: FSMContext):
    questions = cursor.execute("SELECT * FROM questions").fetchall()
    await state.update_data(offset=0)

    questions_btn = InlineKeyboardMarkup()
    for i, question in enumerate(questions[:5], start=1):
        questions_btn.add(InlineKeyboardButton(text=question[1], callback_data=question[0]))

    questions_btn.add(
        InlineKeyboardButton("Orqaga ⬅️", callback_data="question_back"),
        InlineKeyboardButton("Oldinga ➡️", callback_data="question_next"),
    )
    await message.answer("<b>Savollar</b> : ", reply_markup=questions_btn)


@dp.callback_query_handler(text="question_next", state=States.savollar)
async def next_button_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_offset = data.get("offset", 0)
    questions = cursor.execute("SELECT * FROM questions").fetchall()
    remaining_questions = questions[current_offset + 5:]

    if not remaining_questions:
        await call.answer("Boshqa savol qolmagan")
        return

    await state.update_data(offset=current_offset + 5)
    questions_btn = InlineKeyboardMarkup()
    for i, question in enumerate(remaining_questions[:5], start=current_offset + 6):
        question_id = question[0]
        questions_btn.add(InlineKeyboardButton(text=question[1], callback_data=f"{question_id}"))

    questions_btn.add(
        InlineKeyboardButton("Orqaga ⬅️", callback_data="question_back"),
        InlineKeyboardButton("Oldinga ➡️", callback_data="question_next"),
    )

    await call.message.edit_reply_markup(reply_markup=questions_btn)


@dp.callback_query_handler(text="question_back", state=States.savollar)
async def back_button_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_offset = data.get("offset", 0)
    new_offset = max(current_offset - 5, 0)
    questions = cursor.execute("SELECT * FROM questions").fetchall()
    previous_questions = questions[new_offset:new_offset + 5]

    await state.update_data(offset=new_offset)
    questions_btn = InlineKeyboardMarkup()
    for i, question in enumerate(previous_questions, start=new_offset + 1):
        question_id = question[0]
        questions_btn.add(InlineKeyboardButton(text=question[1], callback_data=f"{question_id}"))

    questions_btn.add(
        InlineKeyboardButton("Orqaga ⬅️", callback_data="question_back"),
        InlineKeyboardButton("Oldinga ➡️", callback_data="question_next"),
    )

    await call.message.edit_reply_markup(reply_markup=questions_btn)


@dp.callback_query_handler(state=States.savollar)
async def next_button_handler(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back":
        pass
    elif call.data == "next":
        pass
    else:
        await call.message.delete()
        id = int(call.data)
        data = cursor.execute("SELECT * FROM questions WHERE id = ?", (id,)).fetchone()
        await call.message.answer_video(video=data[2], caption=f"""
<b>Yechim</b> : {data[3]}        
        """)
        await state.finish()
