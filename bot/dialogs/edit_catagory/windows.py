from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.edit_catagory.states import EditCategorySG
from .. import common_buttons
from . import getters, handlers

name_window = Window(
    Const("Введите новое название категории:"),
    TextInput(id="category_input", on_success=handlers.on_category_entered),
    common_buttons.cancel_button,
    state=EditCategorySG.name,
)

confirm_window = Window(
    Format("Изменить категорию на:\n{confirmed_text}"),
    Button(Const("✅ Да"), id="category_confirm", on_click=handlers.on_confirm),
    common_buttons.back_button,
    common_buttons.cancel_button,
    parse_mode="HTML",
    state=EditCategorySG.confirm,
    getter=getters.get_confirmed_data
)
