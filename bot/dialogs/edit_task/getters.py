from datetime import datetime
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

    return {
        "categories": [
            {"id": category["id"], "name": category["name"]}
            for category in categories
        ]
    }


async def get_confirmed_data(dialog_manager: DialogManager, **kwargs):
    user_id = str(dialog_manager.event.from_user.id)
    task_id = dialog_manager.start_data.get("task_id")
    task = await api.get_task(user_id, task_id)

    confirmed_text = f"<b>{task['title']}</b>"

    return {"confirmed_text": confirmed_text}


async def _format_datetime_to_date(iso_datetime_test: str) -> str:
    dt = datetime.fromisoformat(iso_datetime_test)

    return dt.strftime('%Y-%m-%d')


async def set_prev_task_data(data: dict, dialog_manager: DialogManager) -> None:
    user_id = str(dialog_manager.event.from_user.id)
    task_id = dialog_manager.start_data.get("task_id")
    task = await api.get_task(user_id, task_id)

    dialog_manager.dialog_data["title"] = task["title"]
    dialog_manager.dialog_data["category"] = (
        category.get("id") if (category := task["category"]) else None
    )
    dialog_manager.dialog_data["due_date"] = await _format_datetime_to_date(
        due_date
    ) if (due_date := task["due_date"]) else None
