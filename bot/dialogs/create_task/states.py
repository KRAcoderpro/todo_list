from aiogram.fsm.state import StatesGroup, State


class CreateTaskSG(StatesGroup):
    title = State()
    category_type = State()
    category = State()
    due_date = State()
    due_time = State()
    confirm = State()
