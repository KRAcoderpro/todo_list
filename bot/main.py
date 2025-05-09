import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram_dialog import setup_dialogs
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import start, tasks, categories
from dialogs.dialogs import (
    create_task_dialog,
    edit_task_dialog,
    create_category_dialog,
    edit_category_dialog,
    show_tasks_dialog
)

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)

start.register_handlers(dp)
tasks.register_handlers(dp)
categories.register_handlers(dp)

dp.include_router(create_task_dialog)
dp.include_router(edit_task_dialog)
dp.include_router(create_category_dialog)
dp.include_router(edit_category_dialog)
dp.include_router(show_tasks_dialog)
setup_dialogs(dp)


async def setup_bot_commands():
    await bot.set_my_description("Нажмите /start, чтобы начать работу")
    await bot.set_my_commands([
        BotCommand(command="start", description="Начать работу с ботом"),
        # можешь добавить и другие команды
    ])


async def main() -> None:
    await setup_bot_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
