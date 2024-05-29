from loader import dp
from aiogram import types
from states.state import States
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


# @dp.message_handler(state=States.admin_state)
# async def admin_welcome(message: types.Message):
#     await message.answer('Assalomu aleykum')
#     button = ReplyKeyboardMarkup(resize_keyboard=True)
#     button.add(KeyboardButton('Yangi Savol qo`shish'))
#     await message.answer('Siz admin paneldasiz !', reply_markup=button)


@dp.message_handler(state=States.admin_state, text='Yangi Savol qo`shish')
async def adder_savol(message: types.Message):
    await message.answer('Savolni yuboring',reply_markup=ReplyKeyboardRemove())
    await States.admin_savol.set()


@dp.message_handler(state=States.admin_savol, content_types=types.ContentType.TEXT)
async def savol_func(message: types.Message):
    savol_text = message.text
    await message.answer('Video Jo`nating !')
    await States.video_yes_no.set()

    @dp.message_handler(state=States.video_yes_no, content_types=types.ContentType.VIDEO)
    async def video_saver(message: types.Message):
        video_id = message.video['file_id']
        print(video_id)
        await message.answer_video(video_id)
        await States.video_caption.set()
        await message.answer('Video uchun yozuv qoldiring !')

        @dp.message_handler(state=States.video_caption, content_types=types.ContentType.TEXT)
        async def caption_saver(message: types.Message):
            caption_user = message.text
            print(caption_user)
