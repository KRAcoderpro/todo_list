from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def category_inline_keyboard(category_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Изменить", callback_data=f"edit_category_{category_id}"
                ),
                InlineKeyboardButton(
                    text="🗑 Удалить", callback_data=f"delete_category_{category_id}"
                )
            ]
        ]
    )
