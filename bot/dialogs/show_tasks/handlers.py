from datetime import datetime
from aiogram_dialog import DialogManager
from aiogram.types import CallbackQuery
from bot.dialogs.show_tasks.states import ShowTaskSG
from bot.services import api
from bot import keyboards
from bot.handlers.error import handle_errors_callback


def _format_date(iso_string: str) -> str:
    dt = datetime.fromisoformat(iso_string)

    return dt.strftime("%d %B %Y, %H:%M")


def _format_task(task: dict) -> str:
    new_line_character = "\n\n"
    result = ""
    result += f"<b>📝 {task['title']}</b>{new_line_character}"
    if task_category := task.get('category'):
        result += f"🏷 {task_category['name']}{new_line_character}"
    result += f"📅 {_format_date(task['created_at'])}{new_line_character}"
    if due_date := task['due_date']:
        result += f"⏰ {_format_date(due_date)}{new_line_character}"
    if task.get('finished'):
        result += f"🔚 Завершена"
    else:
        result += f"🕐 В процессе"

    return result


@handle_errors_callback
async def _show_tasks(callback_query: CallbackQuery, tasks: list[dict]):
    if not tasks:
        await callback_query.answer("Задачи не найдены.")
        await callback_query.message.answer(
            "🤔 У вас пока нет задач.\n"
            "Не проблема, создайте их, нажав на кнопку ниже 👇."
        )
        return
    for task in tasks:
        task_text = _format_task(task)
        await callback_query.message.answer(
            task_text,
            reply_markup=keyboards.tasks.task_inline_keyboard(
                task['id'],
                task["finished"]
            ),
            parse_mode="HTML"
        )


@handle_errors_callback
async def on_show_task_type_chosen(
    callback: CallbackQuery,
    widget,
    dialog_manager: DialogManager,
    item_id: str
):
    user_id = str(dialog_manager.event.from_user.id)
    await callback.answer("Тип задач выбран.")
    match item_id:
        case "all":
            await callback.message.answer(
                "<b>Все ваши задачи:</b>",
                parse_mode="HTML"
            )
            tasks = await api.get_tasks(telegram_id=user_id)
            await _show_tasks(callback, tasks)
        case "finished":
            await callback.message.answer(
                "<b>Завершенные задачи:</b>",
                parse_mode="HTML"
            )
            tasks = await api.get_tasks_by_status(telegram_id=user_id, finished="true")
            await _show_tasks(callback, tasks)
        case "in_progress":
            await callback.message.answer(
                "<b>Задачи в процессе:</b>",
                parse_mode="HTML"
            )
            tasks = await api.get_tasks_by_status(telegram_id=user_id, finished="false")
            await _show_tasks(callback, tasks)
        case "by_category":
            await dialog_manager.switch_to(ShowTaskSG.category_type)
            return

    await dialog_manager.done()


@handle_errors_callback
async def on_category_type_chosen(
    callback: CallbackQuery,
    widget,
    dialog_manager: DialogManager,
    item_id: str
):

    dialog_manager.dialog_data["category_type"] = item_id
    await callback.answer("Тип категории выбран.")
    await dialog_manager.switch_to(ShowTaskSG.by_category)


@handle_errors_callback
async def on_category_chosen(
    callback: CallbackQuery,
    widget,
    dialog_manager: DialogManager,
    item_id: str
):
    user_id = str(dialog_manager.event.from_user.id)
    await callback.answer("Категория выбрана.")

    await callback.message.answer(
        "<b>Задачи по выбранной категории:</b>",
        parse_mode="HTML"
    )
    tasks = await api.get_tasks_by_category(telegram_id=user_id, category_id=item_id)
    await _show_tasks(callback, tasks)

    await dialog_manager.done()

