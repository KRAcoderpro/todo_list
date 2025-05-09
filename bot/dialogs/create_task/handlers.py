from datetime import date, datetime
from aiogram_dialog import DialogManager
from aiogram.types import Message, CallbackQuery
from aiogram_dialog.widgets.kbd import Calendar
from bot.dialogs.create_task.states import CreateTaskSG
from bot.services import api
from bot.handlers.error import handle_errors_callback, handle_errors_message


@handle_errors_message
async def on_title_entered(
    message: Message, widget,
    dialog_manager: DialogManager,
    title: str
):
    dialog_manager.dialog_data["title"] = title
    await dialog_manager.switch_to(CreateTaskSG.category_type)


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
        await dialog_manager.switch_to(CreateTaskSG.due_date)
        return

    dialog_manager.dialog_data["category_type"] = item_id
    await callback.answer("Тип категории выбран.")
    await dialog_manager.switch_to(CreateTaskSG.category)


@handle_errors_callback
async def on_category_chosen(
    callback: CallbackQuery,
    widget,
    dialog_manager: DialogManager,
    item_id: str
):
    await callback.answer("Категория выбрана.")
    dialog_manager.dialog_data["category"] = item_id
    await dialog_manager.switch_to(CreateTaskSG.due_date)


@handle_errors_callback
async def on_date_selected(
    callback: CallbackQuery,
    widget: Calendar,
    dialog_manager: DialogManager,
    selected_date: date,
):
    dialog_manager.dialog_data["due_date"] = selected_date.strftime("%Y-%m-%d")
    await callback.answer("Дата выбрана.")
    await dialog_manager.switch_to(CreateTaskSG.due_time)


@handle_errors_callback
async def on_no_date_selected(
    callback: CallbackQuery,
    widget,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data["due_date"] = None
    await callback.answer("Без даты.")
    await dialog_manager.switch_to(CreateTaskSG.confirm)


@handle_errors_message
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
        await message.answer("Время указано неверно. Попробуйте еще раз.")
        return

    dialog_manager.dialog_data["due_date"] = due_datetime.isoformat()
    await dialog_manager.switch_to(CreateTaskSG.confirm)


@handle_errors_callback
async def on_no_time_entered(
    callback: CallbackQuery,
    widget,
    dialog_manager: DialogManager,
):
    await callback.answer("Без времени.")
    await dialog_manager.switch_to(CreateTaskSG.confirm)


@handle_errors_callback
async def on_confirm(
    callback: CallbackQuery,
    widget,
    dialog_manager: DialogManager,
):
    user_id = str(dialog_manager.event.from_user.id)
    title = dialog_manager.dialog_data["title"]
    category = dialog_manager.dialog_data["category"]
    due_date = dialog_manager.dialog_data["due_date"]

    resp = await api.create_task(
        telegram_id=user_id,
        title=title,
        category=category,
        due_date=due_date
    )

    await callback.answer(f"Задача успешно создана")
    await callback.message.edit_text(
        f"Задача успешно создана:\n<b>{title}</b> ",
        parse_mode="HTML"
    )

    await dialog_manager.done()
