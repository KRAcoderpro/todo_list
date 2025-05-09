from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import (
    Group,
    ScrollingGroup,
    Select
)
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.show_tasks.states import ShowTaskSG
from .. import common_buttons
from . import getters, handlers

task_types_window = Window(
    Const("Какие задачи:"),
    Group(
        Select(
            Format("{item[name]}"),
            id="show_task_types",
            item_id_getter=lambda item: str(item["id"]),
            items="task_types",
            on_click=handlers.on_show_task_type_chosen
        ),
        id="scrolling_task_types",
        width=2,
    ),
    common_buttons.cancel_button,
    state=ShowTaskSG.menu,
    getter=getters.get_show_task_types
)
category_type_window = Window(
    Const("Выберите тип категории:"),
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
    common_buttons.back_button,
    common_buttons.cancel_button,
    state=ShowTaskSG.category_type,
    getter=getters.get_category_types
)

by_category_window = Window(
    Const("Выберите категорию:"),
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
    common_buttons.back_button,
    common_buttons.cancel_button,
    state=ShowTaskSG.by_category,
    getter=getters.get_categories
)
