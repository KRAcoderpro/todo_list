from aiogram.fsm.state import StatesGroup, State


class ShowTaskSG(StatesGroup):
    menu = State()
    category_type = State()
    by_category = State()
