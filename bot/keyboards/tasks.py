from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder


def task_inline_keyboard(task_id: str, is_finished: bool):
    kb = InlineKeyboardBuilder()
    
    kb.add(
        InlineKeyboardButton(
            text="🗑 Удалить", callback_data=f"delete_task_{task_id}"
        )
    )
    if not is_finished:
        kb.add(
            InlineKeyboardButton(
                text="✏️ Изменить", callback_data=f"edit_task_{task_id}"
            )
        )
        kb.add(
            InlineKeyboardButton(
                text="🔚 Завершить", callback_data=f"finish_task_{task_id}"
            )
        )

    kb.adjust(2)
    return kb.as_markup()
