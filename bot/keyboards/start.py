from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def main_inline_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📅 Мои задачи", callback_data="my_tasks"
                ),
                InlineKeyboardButton(
                    text="🗂 Мои категории", callback_data="my_categories"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📝 Добавить задачу", callback_data="add_task"
                ),
                InlineKeyboardButton(
                    text="🏷 Добавить категорию", callback_data="add_category"
                )
            ],
        ]
    )
