from loader import dp
from aiogram import types
from states.state import States
from ..users.start import cursor, connect
from keyboards.default.default import admin_button
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery


@dp.message_handler(state=States.admin_state, text='Yangi Savol qo`shish 🆕')
async def adder_savol(message: types.Message):
    await message.answer('Savolni yuboring ❔', reply_markup=ReplyKeyboardRemove())
    await States.admin_savol.set()


@dp.message_handler(state=States.admin_savol, content_types=types.ContentType.TEXT)
async def savol_func(message: types.Message):
    question = message.text
    print(question)
    await message.answer('Video Jo`nating 📹')
    await States.video_yes_no.set()

    @dp.message_handler(state=States.video_yes_no, content_types=types.ContentType.VIDEO)
    async def video_saver(message: types.Message):
        video = message.video['file_id']
        print(video)
        await States.video_caption.set()
        await message.answer('Video uchun yozuv qoldiring 💬')

        @dp.message_handler(state=States.video_caption, content_types=types.ContentType.TEXT)
        async def caption_saver(message: types.Message, state: FSMContext):
            caption = message.text
            print(caption)
            cursor.execute("INSERT INTO questions (question, video, caption) VALUES (?, ?, ?)",
                           (question, video, caption))
            connect.commit()
            await state.finish()
            await States.admin_state.set()
            await message.answer("Savol Muvofaqiyatli Qo'shildi ✅", reply_markup=admin_button)


@dp.message_handler(text="Savollarni Ko'rish 👀", state=States.admin_state)
async def savolarni_korish_func(message: types.Message, state: FSMContext):
    questions = cursor.execute("SELECT * FROM questions").fetchall()
    a = []
    if questions == a:
        await message.answer("Savollar Mavjud Emas !")
    else:
        await state.update_data(offset=0)

        questions_btn = InlineKeyboardMarkup()
        for i, question in enumerate(questions[:5], start=1):
            questions_btn.add(InlineKeyboardButton(text=question[1], callback_data=question[0]))

        questions_btn.add(
            InlineKeyboardButton("Orqaga ⬅️", callback_data="back"),
            InlineKeyboardButton("Oldinga ➡️", callback_data="next"),
        )
        await message.answer("Savollar:", reply_markup=questions_btn)


@dp.callback_query_handler(text="next", state=States.admin_state)
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
        InlineKeyboardButton("Orqaga ⬅️", callback_data="back"),
        InlineKeyboardButton("Oldinga ➡️", callback_data="next"),
    )

    await call.message.edit_reply_markup(reply_markup=questions_btn)


@dp.callback_query_handler(text="back", state=States.admin_state)
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
        InlineKeyboardButton("Orqaga ⬅️", callback_data="back"),
        InlineKeyboardButton("Oldinga ➡️", callback_data="next"),
    )

    await call.message.edit_reply_markup(reply_markup=questions_btn)


@dp.callback_query_handler(state=States.admin_state)
async def next_button_handler(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back":
        pass
    elif call.data == "next":
        pass
    else:
        await call.message.delete()
        id = int(call.data)
        print(id)
        data = cursor.execute("SELECT * FROM questions WHERE id = ?", (id,)).fetchone()
        print(data[2])
        await call.message.answer_video(video=data[2], caption=f"""
<b>Savol</b> : {data[1]}

<b>Javob</b> : {data[3]}        
        """)


@dp.message_handler(text="Savollarni O'chirish ❌", state=States.admin_state)
async def savollarni_ochirish(message: types.Message, state: FSMContext):
    questions = cursor.execute("SELECT * FROM questions").fetchall()
    await state.update_data(offset=0)

    questions_btn = InlineKeyboardMarkup()
    for i, question in enumerate(questions[:5], start=1):
        questions_btn.add(InlineKeyboardButton(text=question[1], callback_data=f"del{question[0]}"))

    questions_btn.add(
        InlineKeyboardButton("Orqaga ⬅️", callback_data="delete_back"),
        InlineKeyboardButton("Oldinga ➡️", callback_data="delete_next"),
    )
    await message.answer("O'chirish Uchun Savol Tanlang:", reply_markup=questions_btn)
    await state.finish()
    await States.delete_savollar.set()


@dp.callback_query_handler(text="delete_next", state=States.delete_savollar)
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
        questions_btn.add(InlineKeyboardButton(text=question[1], callback_data=f"del{question_id}"))

    questions_btn.add(
        InlineKeyboardButton("Orqaga ⬅️", callback_data="delete_back"),
        InlineKeyboardButton("Oldinga ➡️", callback_data="delete_next"),
    )

    await call.message.edit_reply_markup(reply_markup=questions_btn)


@dp.callback_query_handler(text="delete_back", state=States.delete_savollar)
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
        questions_btn.add(InlineKeyboardButton(text=question[1], callback_data=f"del{question_id}"))

    questions_btn.add(
        InlineKeyboardButton("Orqaga ⬅️", callback_data="delete_back"),
        InlineKeyboardButton("Oldinga ➡️", callback_data="delete_next"),
    )

    await call.message.edit_reply_markup(reply_markup=questions_btn)


@dp.callback_query_handler(state=States.delete_savollar)
async def next_button_handler(call: types.CallbackQuery, state: FSMContext):
    if call.data == "delete_next":
        pass
    if call.data == "delete_back":
        pass
    else:
        await call.message.delete()
        id = int(call.data[3])
        print(id)
        data = cursor.execute("SELECT * FROM questions WHERE id = ?", (id,)).fetchone()
        print(data)
        cursor.execute("DELETE FROM questions WHERE id = ?", (id,))
        await call.message.answer(f"""
<b>{data[1]}</b>

Nomli Savol O'chirildi
        """)
        await state.finish()
        await States.admin_state.set()


