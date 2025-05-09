import aiohttp
from bot.config import API_URL
from .exceptions import APIException

from .handlers import handle_api_errors


@handle_api_errors
async def register_user(telegram_id: str) -> int:
    async with aiohttp.ClientSession() as session:
        data = {"telegram_id": telegram_id}

        async with session.post(f"{API_URL}/register/", json=data) as resp:
            resp.raise_for_status()

            if (
                resp.status in
                [aiohttp.http.HTTPStatus.CREATED, aiohttp.http.HTTPStatus.OK]
            ):
                return resp.status

            raise APIException(
                message="Something went wrong during user registration",
                status_code=resp.status
            )
