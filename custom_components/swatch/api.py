"""Swatch API Client."""

import asyncio
import logging
import socket
from typing import Any, Dict, cast

import aiohttp
import async_timeout
from yarl import URL

TIMEOUT = 10

_LOGGER: logging.Logger = logging.getLogger(__name__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class SwatchApiClientError(Exception):
    """General SwatchApiClient error."""


class SwatchApiClient:
    """Swatch API client."""

    def __init__(self, host: str, session: aiohttp.ClientSession) -> None:
        """Construct API Client."""
        self._host = host
        self._session = session

    async def async_get_version(self) -> str:
        """Get data from the API."""
        return cast(
            str,
            await self.api_wrapper(
                "get", str(URL(self._host) / "api/version"), decode_json=False
            ),
        )

    async def async_get_config(self) -> dict[str, Any]:
        """Get data from the API."""
        return cast(
            Dict[str, Any],
            await self.api_wrapper("get", str(URL(self._host) / "api/config")),
        )

    async def async_detect_camera(
        self,
        camera_name,
        image_url: str = None,
    ) -> dict[str, Any]:
        """Get data from the API."""
        if image_url:
            return cast(
                Dict[str, Any],
                await self.api_wrapper(
                    "post",
                    str(
                        URL(self._host) / f"api/{camera_name}/detect",
                    ),
                    {"imageUrl": image_url},
                ),
            )
        else:
            return cast(
                Dict[str, Any],
                await self.api_wrapper(
                    "post", str(URL(self._host) / f"api/{camera_name}/detect")
                ),
            )

    async def async_get_object_state(self, object_name: str) -> dict[str, Any]:
        """Get latest object state from the API."""
        return cast(
            Dict[str, Any],
            await self.api_wrapper(
                "get", str(URL(self._host) / f"api/{object_name}/latest")
            ),
        )

    async def api_wrapper(
        self,
        method: str,
        url: str,
        data: dict = None,
        headers: dict = None,
        decode_json: bool = True,
    ) -> Any:
        """Get information from the API."""
        if data is None:
            data = {}
        if headers is None:
            headers = {}

        try:
            async with async_timeout.timeout(TIMEOUT):
                if method == "get":
                    response = await self._session.get(
                        url, headers=headers, raise_for_status=True
                    )
                    if decode_json:
                        return await response.json()
                    return await response.text()

                if method == "put":
                    await self._session.put(url, headers=headers, json=data)

                elif method == "patch":
                    await self._session.patch(url, headers=headers, json=data)

                elif method == "post":
                    response = await self._session.post(url, headers=headers, json=data)

                    if response:
                        return await response.json()

        except asyncio.TimeoutError as exc:
            _LOGGER.error(
                "Timeout error fetching information from %s: %s",
                url,
                exc,
            )
            raise SwatchApiClientError from exc

        except (KeyError, TypeError) as exc:
            _LOGGER.error(
                "Error parsing information from %s: %s",
                url,
                exc,
            )
            raise SwatchApiClientError from exc
        except (aiohttp.ClientError, socket.gaierror) as exc:
            _LOGGER.error(
                "Error fetching information from %s: %s",
                url,
                exc,
            )
            raise SwatchApiClientError from exc
