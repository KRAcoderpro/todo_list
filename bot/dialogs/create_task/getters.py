from aiogram_dialog import DialogManager
from bot.services import api


async def get_category_types(**kwargs):
    return {
        "category_types": [
            {"id": "default", "name": "По умолчанию"},
            {"id": "user", "name": "Личные"},
            {"id": "null", "name": "Без категории"},
        ]
    }


async def get_categories(dialog_manager: DialogManager, **kwargs):
    user_id = str(dialog_manager.event.from_user.id)
    category_type = dialog_manager.dialog_data.get("category_type")

    if category_type == "default":
        categories = await api.get_default_categories(user_id)
    else:
        categories = await api.get_user_categories(user_id)

    dialog_manager.dialog_data["available_categories"] = len(categories)
    await dialog_manager.answer_callback()

    return {
        "categories": [
            {"id": category["id"], "name": category["name"]}
            for category in categories
        ]
    }


async def get_confirmed_data(dialog_manager: DialogManager, **kwargs):
    title = dialog_manager.dialog_data["title"]

    confirmed_text = f"<b>{title}</b>"

    return {"confirmed_text": confirmed_text}


