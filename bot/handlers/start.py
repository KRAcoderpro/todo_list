from aiogram import Dispatcher, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart
from bot.services.api import register_user
from bot.keyboards.start import main_inline_kb

from .error import handle_errors_message

start_router = Router()


@start_router.message(CommandStart())
@handle_errors_message
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    user_id = str(message.from_user.id)
    resp = await register_user(telegram_id=user_id)

    if resp == 201:
        await message.answer("Вы успешно зарегистрированы!")

    await message.answer(
        "👋 Добро пожаловать!\n"
        "Используйте клавиатуру ниже, чтобы взаимодействовать со своими задачами 📅.",
        reply_markup=main_inline_kb()
    )


def register_handlers(dp: Dispatcher):
    dp.include_router(start_router)
