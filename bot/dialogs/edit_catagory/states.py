from aiogram.fsm.state import StatesGroup, State


class EditCategorySG(StatesGroup):
    name = State()
    confirm = State()
