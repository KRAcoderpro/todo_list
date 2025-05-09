from datetime import date

from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Select,
    Calendar,
    ScrollingGroup,
    CalendarConfig
)
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.edit_task.states import EditTaskSG
from bot.dialogs import common_buttons

from . import getters, handlers

title_window = Window(
    Const("Введите новое название задачи:"),
    TextInput(id="title_input", on_success=handlers.on_title_entered),
    common_buttons.next_button,
    common_buttons.cancel_button,
    state=EditTaskSG.title,
)

category_type_window = Window(
    Const("Выберите новый тип категории:"),
    ScrollingGroup(
        Select(
            Format("{item[name]}"),
            id="category_type",
            item_id_getter=lambda item: str(item["id"]),
            items="category_types",
            on_click=handlers.on_category_type_chosen
        ),
        id="scrolling_category_type",
        width=4,
        height=2,
    ),
    common_buttons.next_button,
    common_buttons.back_button,
    common_buttons.cancel_button,
    state=EditTaskSG.category_type,
    getter=getters.get_category_types
)

category_window = Window(
    Const("Выберите новую категорию:"),
    ScrollingGroup(
        Select(
            Format("{item[name]}"),
            id="category",
            item_id_getter=lambda x: x["id"],
            items="categories",
            on_click=handlers.on_category_chosen
        ),
        id="scrolling_category",
        width=4,
        height=2,
    ),
    common_buttons.next_button,
    common_buttons.back_button,
    common_buttons.cancel_button,
    state=EditTaskSG.category,
    getter=getters.get_categories
)

due_date_window = Window(
    Const("Выберите новую дату:"),
    Calendar(
        id="due_datecalendar",
        on_click=handlers.on_date_selected,
        config=CalendarConfig(
                firstweekday=0,
                min_date=date.today()
            )
    ),
    Button(
        Const("Без даты"),
        id="no_date_button",
        on_click=handlers.on_no_date_selected
    ),
    common_buttons.next_button,
    common_buttons.back_button,
    common_buttons.cancel_button,
    state=EditTaskSG.due_date,
)

due_time_window = Window(
    Const("Введите новое время (например 14:00):"),
    TextInput(
        id="due_time_input",
        on_success=handlers.on_time_entered
    ),
    Button(
        Const("Без времени"),
        id="no_date_time_button",
        on_click=handlers.on_no_time_entered
    ),
    common_buttons.next_button,
    common_buttons.back_button,
    common_buttons.cancel_button,
    state=EditTaskSG.due_time,
)

confirm_window = Window(
    Format("Изменить задачу:\n{confirmed_text}"),
    Button(Const("✅ Да"), id="task_confirm", on_click=handlers.on_confirm),
    common_buttons.back_button,
    common_buttons.cancel_button,
    parse_mode="HTML",
    state=EditTaskSG.confirm,
    getter=getters.get_confirmed_data
)
