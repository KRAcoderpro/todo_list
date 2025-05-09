import functools
from aiogram.types import Message, CallbackQuery
from bot.services.api import exceptions


def handle_errors_message(func):
    @functools.wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        try:
            return await func(message, *args, **kwargs)

        except exceptions.APIException as exc:
            await message.answer(
                f"<b>⚠️ Ошибка ({exc.status_code}):</b>\n{exc.message}",
                parse_mode="HTML"
            )
        except Exception as exc:
            await message.answer(
                f"<b>⛔ Что-то пошло не так:</b>\n{exc}",
                parse_mode="HTML"
            )

    return wrapper


def handle_errors_callback(func):
    @functools.wraps(func)
    async def wrapper(callback: CallbackQuery, *args, **kwargs):
        try:
            return await func(callback, *args, **kwargs)

        except exceptions.APIException as exc:
            await callback.answer("Произошла ошибка")
            await callback.message.answer(
                f"<b>⚠️ Ошибка ({exc.status_code}):</b>\n{exc.message}",
                parse_mode="HTML"
            )
        except Exception as exc:
            await callback.answer("Произошла ошибка")
            await callback.message.answer(
                f"<b>⛔ Что-то пошло не так:</b>\n{exc}",
                parse_mode="HTML"
            )

    return wrapper
