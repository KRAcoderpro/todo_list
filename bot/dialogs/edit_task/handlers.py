from datetime import date, datetime
from aiogram_dialog import DialogManager
from aiogram.types import Message, CallbackQuery
from aiogram_dialog.widgets.kbd import Calendar
from bot.dialogs.edit_task.states import EditTaskSG
from bot.services import api
from bot.handlers.error import handle_errors_callback, handle_errors_message


@handle_errors_message
async def on_title_entered(
    message: Message, widget,
    dialog_manager: DialogManager,
    title: str
):
    dialog_manager.dialog_data["title"] = title
    await dialog_manager.switch_to(EditTaskSG.category_type)


@handle_errors_callback
async def on_category_type_chosen(
    callback: CallbackQuery,
    widget,
    dialog_manager: DialogManager,
    item_id: str
):
    if item_id == "null":
        await callback.answer("Без категории.")
        dialog_manager.dialog_data["category"] = None
        await dialog_manager.switch_to(EditTaskSG.due_date)
        return

    dialog_manager.dialog_data["category_type"] = item_id
    await callback.answer("Тип категории выбран.")
    await dialog_manager.switch_to(EditTaskSG.category)


@handle_errors_callback
async def on_category_chosen(
    callback: CallbackQuery,
    widget,
    dialog_manager: DialogManager,
    item_id: str
):
    await callback.answer("Категория выбрана.")
    dialog_manager.dialog_data["category"] = item_id
    await dialog_manager.switch_to(EditTaskSG.due_date)


@handle_errors_callback
async def on_date_selected(
    callback: CallbackQuery,
    widget: Calendar,
    dialog_manager: DialogManager,
    selected_date: date,
):
    dialog_manager.dialog_data["due_date"] = selected_date.strftime("%Y-%m-%d")
    await callback.answer("Дата выбрана.")
    await dialog_manager.switch_to(EditTaskSG.due_time)


@handle_errors_callback
async def on_no_date_selected(
    callback: CallbackQuery,
    widget,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["due_date"] = None
    await callback.answer("Без даты.")
    await dialog_manager.switch_to(EditTaskSG.confirm)


@handle_errors_callback
async def on_time_entered(
    message: Message,
    widget,
    dialog_manager: DialogManager,
    time: str
):
    try:
        due_datetime = datetime.strptime(
            f"{dialog_manager.dialog_data['due_date']} {time}", "%Y-%m-%d %H:%M"
        )
    except ValueError:
        await message.answer("Дата и Время указаны неверно. Попробуйте еще раз.")
        return

    dialog_manager.dialog_data["due_date"] = due_datetime.isoformat()
    await dialog_manager.switch_to(EditTaskSG.confirm)


@handle_errors_callback
async def on_no_time_entered(
    callback: CallbackQuery,
    widget,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["due_date"] = dialog_manager.dialog_data["date"]
    await callback.answer("Без времени.")
    await dialog_manager.switch_to(EditTaskSG.confirm)


@handle_errors_callback
async def on_confirm(
    callback: CallbackQuery,
    widget,
    dialog_manager: DialogManager,
):
    user_id = str(dialog_manager.event.from_user.id)
    title = dialog_manager.dialog_data.get("title")
    category = dialog_manager.dialog_data.get("category")
    due_date = dialog_manager.dialog_data.get("due_date")

    await api.update_task(
        telegram_id=user_id,
        task_id=dialog_manager.start_data["task_id"],
        title=title,
        category_id=category,
        due_date=due_date
    )

    await callback.answer(f"Задача успешно изменена")
    await callback.message.answer(f"Задача успешно изменена")

    await dialog_manager.done()
