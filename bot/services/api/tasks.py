import aiohttp
from bot.config import API_URL
from .exceptions import APIException

from .handlers import handle_api_errors


@handle_api_errors
async def create_task(
        telegram_id: str, category: str, title: str, due_date: str
) -> None:
    async with aiohttp.ClientSession() as session:
        headers = {"X-Telegram-ID": str(telegram_id)}
        data = {
            "title": title,
            "category_id": category,
            "due_date": due_date,
        }

        async with session.post(
                f"{API_URL}/tasks/", json=data, headers=headers
        ) as resp:
            resp.raise_for_status()

            if resp.status == aiohttp.http.HTTPStatus.CREATED:
                return None

            raise APIException(
                message="Something went wrong during creating task",
                status_code=resp.status
            )


@handle_api_errors
async def get_tasks(telegram_id: str) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        headers = {"X-Telegram-ID": str(telegram_id)}
        async with session.get(
                f"{API_URL}/tasks/", headers=headers
        ) as resp:
            resp.raise_for_status()

            if resp.status == aiohttp.http.HTTPStatus.OK:
                return await resp.json()

            raise APIException(
                message="Something went wrong during getting tasks",
                status_code=resp.status
            )


@handle_api_errors
async def get_task(telegram_id: str, task_id: str) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = {"X-Telegram-ID": str(telegram_id)}
        async with session.get(
                f"{API_URL}/tasks/{task_id}/", headers=headers
        ) as resp:
            resp.raise_for_status()

            if resp.status == aiohttp.http.HTTPStatus.OK:
                return await resp.json()

            raise APIException(
                message="Something went wrong during getting task",
                status_code=resp.status
            )


@handle_api_errors
async def get_tasks_by_status(telegram_id: str, finished: str) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        headers = {"X-Telegram-ID": str(telegram_id)}
        params = {'finished': finished}
        async with session.get(
            f"{API_URL}/tasks/", headers=headers, params=params
        ) as resp:
            resp.raise_for_status()

            if resp.status == aiohttp.http.HTTPStatus.OK:
                return await resp.json()

            raise APIException(
                message="Something went wrong during getting task by status",
                status_code=resp.status
            )


@handle_api_errors
async def get_tasks_by_category(telegram_id: str, category_id: str) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        headers = {"X-Telegram-ID": str(telegram_id)}
        params = {'category': category_id}
        async with session.get(
            f"{API_URL}/tasks/", headers=headers, params=params
        ) as resp:
            resp.raise_for_status()

            if resp.status == aiohttp.http.HTTPStatus.OK:
                return await resp.json()

            raise APIException(
                message="Something went wrong during getting task by category",
                status_code=resp.status
            )


@handle_api_errors
async def update_task(
        telegram_id: str,
        task_id: str,
        category_id: str,
        title: str,
        due_date: str,
        finished: bool = False
) -> None:
    async with aiohttp.ClientSession() as session:
        headers = {"X-Telegram-ID": str(telegram_id)}
        data = {
            "category_id": category_id,
            "finished": finished,
            "due_date": due_date
        }

        if title is not None:
            data.update({"title": title})

        async with session.patch(
                f"{API_URL}/tasks/{task_id}/", json=data, headers=headers
        ) as resp:
            resp.raise_for_status()

            if resp.status == aiohttp.http.HTTPStatus.OK:
                return None

            raise APIException(
                message="Something went wrong during updating task",
                status_code=resp.status
            )


@handle_api_errors
async def set_task_status(telegram_id: str, task_id: str, finished: bool) -> None:
    async with aiohttp.ClientSession() as session:
        headers = {"X-Telegram-ID": str(telegram_id)}
        data = {
            "finished": finished
        }

        async with session.patch(
                f"{API_URL}/tasks/{task_id}/", json=data, headers=headers
        ) as resp:
            resp.raise_for_status()

            if resp.status == aiohttp.http.HTTPStatus.OK:
                return None

            raise APIException(
                message="Something went wrong during setting task status",
                status_code=resp.status
            )


@handle_api_errors
async def delete_task(telegram_id, task_id) -> None:
    async with aiohttp.ClientSession() as session:
        headers = {"X-Telegram-ID": str(telegram_id)}
        async with session.delete(
                f"{API_URL}/tasks/{task_id}/", headers=headers
        ) as resp:
            resp.raise_for_status()

            if resp.status == aiohttp.http.HTTPStatus.NO_CONTENT:
                return None

            raise APIException(
                message="Something went wrong during deleting task",
                status_code=resp.status
            )
