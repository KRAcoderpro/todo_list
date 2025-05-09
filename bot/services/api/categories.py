import aiohttp
from bot.config import API_URL

from .handlers import handle_api_errors
from .exceptions import APIException


@handle_api_errors
async def create_category(telegram_id: str, name: str) -> None:
    async with aiohttp.ClientSession() as session:
        headers = {"X-Telegram-ID": str(telegram_id)}
        data = {
            "name": name,
        }
        async with session.post(
                f"{API_URL}/categories/", json=data, headers=headers
        ) as resp:
            resp.raise_for_status()

            if resp.status == aiohttp.http.HTTPStatus.CREATED:
                return None

            raise APIException(
                message="Something went wrong during creating category",
                status_code=resp.status
            )


@handle_api_errors
async def get_default_categories(telegram_id: str) -> list:
    async with aiohttp.ClientSession() as session:
        headers = {"X-Telegram-ID": str(telegram_id)}
        async with session.get(
            f"{API_URL}/categories/default/", headers=headers
        ) as resp:
            resp.raise_for_status()

            if resp.status == aiohttp.http.HTTPStatus.OK:
                return await resp.json()

            raise APIException(
                message="Something went wrong during getting default categories",
                status_code=resp.status
            )


@handle_api_errors
async def get_user_categories(telegram_id: str) -> list:
    async with aiohttp.ClientSession() as session:
        headers = {"X-Telegram-ID": str(telegram_id)}
        async with session.get(f"{API_URL}/categories/", headers=headers) as resp:
            resp.raise_for_status()

            if resp.status == aiohttp.http.HTTPStatus.OK:
                return await resp.json()

            raise APIException(
                message="Something went wrong during getting user categories",
                status_code=resp.status
            )


@handle_api_errors
async def update_category(telegram_id: str, category_id: str, name: str) -> None:
    async with aiohttp.ClientSession() as session:
        headers = {"X-Telegram-ID": str(telegram_id)}
        data = {
            "name": name,
        }
        async with session.patch(
                f"{API_URL}/categories/{category_id}/", json=data, headers=headers
        ) as resp:
            resp.raise_for_status()

            if resp.status == aiohttp.http.HTTPStatus.OK:
                return None

            raise APIException(
                message="Something went wrong during updating category",
                status_code=resp.status
            )


@handle_api_errors
async def delete_user_category(telegram_id, category_id) -> None:
    async with aiohttp.ClientSession() as session:
        headers = {"X-Telegram-ID": str(telegram_id)}
        async with session.delete(
                f"{API_URL}/categories/{category_id}/", headers=headers
        ) as resp:
            resp.raise_for_status()

            if resp.status == aiohttp.http.HTTPStatus.NO_CONTENT:
                return None

            raise APIException(
                message="Something went wrong during deleting category",
                status_code=resp.status
            )
