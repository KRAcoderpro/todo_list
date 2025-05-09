from aiogram_dialog import DialogManager
from aiogram.types import Message, CallbackQuery

from bot.dialogs.edit_catagory.states import EditCategorySG
from bot.services import api
from bot.handlers.error import handle_errors_callback, handle_errors_message


@handle_errors_message
async def on_category_entered(
    message: Message, widget,
    dialog_manager: DialogManager,
    title: str
):
    dialog_manager.dialog_data["category_name"] = title
    await dialog_manager.switch_to(EditCategorySG.confirm)


@handle_errors_callback
async def on_confirm(
    callback: CallbackQuery,
    widget,
    dialog_manager: DialogManager,
):
    user_id = str(dialog_manager.event.from_user.id)
    category_name = dialog_manager.dialog_data["category_name"]

    resp = await api.update_category(
        telegram_id=user_id,
        category_id=dialog_manager.start_data["category_id"],
        name=category_name
    )

    await callback.answer(f"Категория успешно изменена")
    await callback.message.answer(f"Категория  успешно изменена")

    await dialog_manager.done()
