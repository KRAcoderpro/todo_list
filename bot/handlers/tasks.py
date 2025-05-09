from aiogram import Dispatcher, Router, F
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram.types import CallbackQuery
from bot.services.api import delete_task, set_task_status
from bot.dialogs.create_task.states import CreateTaskSG
from bot.dialogs.edit_task.states import EditTaskSG
from bot.dialogs.show_tasks.states import ShowTaskSG

from .error import handle_errors_callback

tasks_router = Router()


@tasks_router.callback_query(F.data == "add_task")
@handle_errors_callback
async def start_create_task(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(
        CreateTaskSG.title,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )


@tasks_router.callback_query(F.data.startswith("edit_task_"))
@handle_errors_callback
async def start_edit_task(callback: CallbackQuery, dialog_manager: DialogManager):
    task_id = callback.data.replace("edit_task_", "")
    await dialog_manager.start(
        EditTaskSG.title,
        mode=StartMode.RESET_STACK,
        data={"task_id": task_id},
        show_mode=ShowMode.SEND
    )


@tasks_router.callback_query(F.data == "my_tasks")
@handle_errors_callback
async def start_show_tasks(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(
        ShowTaskSG.menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND
    )


@tasks_router.callback_query(F.data.startswith("delete_task_"))
@handle_errors_callback
async def handle_delete_task(callback_query: CallbackQuery):
    task_id = callback_query.data.replace("delete_task_", "")
    await delete_task(callback_query.from_user.id, task_id)

    await callback_query.answer("Задача удалена!")
    await callback_query.message.edit_text("Задача успешно удалена!")


@tasks_router.callback_query(F.data.startswith("finish_task_"))
@handle_errors_callback
async def handle_finish_task(callback_query: CallbackQuery):
    user_id = str(callback_query.from_user.id)
    task_id = callback_query.data.split("_")[-1]
    await set_task_status(telegram_id=user_id, task_id=task_id, finished=True)

    await callback_query.answer("Задача завершена!")
    await callback_query.message.answer("Задача успешно завершена!")


def register_handlers(dp: Dispatcher):
    dp.include_router(tasks_router)
