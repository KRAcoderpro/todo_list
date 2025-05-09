from aiogram_dialog import DialogManager


async def get_confirmed_data(dialog_manager: DialogManager, **kwargs):
    category_name = dialog_manager.dialog_data["category_name"]

    confirmed_text = f"<b>{category_name}</b>"

    return {"confirmed_text": confirmed_text}


