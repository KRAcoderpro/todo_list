from aiogram_dialog import DialogManager, Dialog

from bot.handlers import start


async def show_main_menu(start_data: dict, manager: DialogManager):
    await manager.event.message.answer(
        "🏠 Главное меню:",
        reply_markup=start.main_inline_kb()
    )


def dialog_with_main_menu(*windows, **kwargs):
    return Dialog(*windows, **kwargs, on_close=show_main_menu)
