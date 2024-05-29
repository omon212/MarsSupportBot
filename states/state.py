from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class States(StatesGroup):
    fullname = State()
    admin_state = State()
    admin_savol = State()
    video_yes_no = State()
    video_caption = State()
