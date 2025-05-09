from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Back, Cancel, Next


async def cancel_logic(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await callback.answer("Действие отменено!")
    await callback.message.answer("Вы отменили действе.")


next_button = Next(Const("➡️ Вперед"))
back_button = Back(Const("⬅️ Назад"))
cancel_button = Cancel(Const("❌ Отмена"), on_click=cancel_logic)
