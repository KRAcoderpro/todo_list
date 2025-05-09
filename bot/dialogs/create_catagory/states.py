from aiogram.fsm.state import StatesGroup, State


class CreateCategorySG(StatesGroup):
    name = State()
    confirm = State()
