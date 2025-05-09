import functools
import aiohttp
import asyncio
from .exceptions import APIException


def handle_api_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except aiohttp.ClientResponseError as e:
            raise APIException(
                f"API returned error: {e.message or e.status}", status_code=e.status
            )

        except aiohttp.ClientConnectionError:
            raise APIException("API Server connection error", status_code=503)

        except asyncio.TimeoutError:
            raise APIException("Timeout Error while connecting to API", status_code=504)

        except aiohttp.ClientError:
            raise APIException("Client Error during API request", status_code=500)

        except Exception:
            raise APIException("Unexpected", status_code=500)

    return wrapper
