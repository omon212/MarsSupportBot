from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from states.state import States
from utils.databace import connect, cursor, UserRegister
from keyboards.default.default import fullname_button


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Assalomu aleykum {message.from_user.first_name}")
    await message.answer("""
Avval to'liq Ism Familyangizni yuboring,
yoki <b>Omonullo Raimkulov</b> ko'rinishida yozing.
    """, reply_markup=fullname_button)
    await States.fullname.set()


@dp.message_handler(content_types="contact", state=States.fullname)
async def fulname(message: types.Message, state: FSMContext):
    try:
        a = await UserRegister(message.from_user.id, message.contact.full_name)
        print(a)
        await message.answer("Sizni qanday savollar qiynayabdi ?")
    except Exception as e:
        print(e)
        await state.finish()
