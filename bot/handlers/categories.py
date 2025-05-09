from aiogram import Dispatcher, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import DialogManager, StartMode, ShowMode
from bot.services import api
from bot import keyboards


from bot.dialogs.create_catagory.states import CreateCategorySG
from bot.dialogs.edit_catagory.states import EditCategorySG

from .error import handle_errors_callback

create_category_router = Router()


class CreateCategoryState(StatesGroup):
    name = State()


@create_category_router.callback_query(F.data == "add_category")
@handle_errors_callback
async def start_create_category(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(
        CreateCategorySG.name,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND
    )


@create_category_router.callback_query(F.data.startswith("edit_category_"))
@handle_errors_callback
async def start_edit_category(callback: CallbackQuery, dialog_manager: DialogManager):
    category_id = callback.data.replace("edit_category_", "")
    await dialog_manager.start(
        EditCategorySG.name,
        mode=StartMode.RESET_STACK, data={"category_id": category_id},
        show_mode=ShowMode.SEND
    )


@create_category_router.callback_query(F.data == "my_categories")
@handle_errors_callback
async def show_categories(callback_query: CallbackQuery):
    user_id = str(callback_query.from_user.id)
    categories = await api.get_user_categories(user_id)

    if not categories:
        await callback_query.answer("Категории не найдены.")
        await callback_query.message.answer(
            "🤔 У вас пока нет категорий.\n"
            "Не проблема, создайте их, нажав на кнопку ниже 👇.",
            reply_markup=keyboards.start.main_inline_kb()
        )
        return
    for category in categories:
        category_text = f"🏷 {category['name']}"
        await callback_query.message.answer(
            category_text,
            reply_markup=keyboards.categories.category_inline_keyboard(category['id']),
            parse_mode="HTML"
        )

    await callback_query.answer(f"Категории получены")
    await callback_query.message.answer(
        f"Вот все ваши категории ☝️",
        reply_markup=keyboards.start.main_inline_kb()
    )


@create_category_router.callback_query(F.data.startswith("delete_category_"))
@handle_errors_callback
async def handle_delete_category(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    category_id = callback_query.data.replace("delete_category_", "")
    await api.delete_user_category(telegram_id=user_id, category_id=category_id)

    await callback_query.answer("Категория удалена!")
    await callback_query.message.edit_text("Категория успешно удалена!")


def register_handlers(dp: Dispatcher):
    dp.include_router(create_category_router)
