"""Chroma bridge."""

from __future__ import annotations

import aiohttp
import logging
from typing import Any

from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import UpdateFailed

from aiochroma import AIOChroma
from .const import CONF_DEVICES, CONF_LAYOUT, DEFAULT_LAYOUT, SENSORS_TYPE_LIGHT

_LOGGER = logging.getLogger(__name__)


class ChromaBridge:
    """Bridge for AIOChroma library."""

    def __init__(
        self,
        hass: HomeAssistant,
        configs: dict[str, Any],
        options: dict[str, Any] = dict(),
    ) -> None:
        """Initialize bridge."""

        self._configs = configs.copy()
        self._configs.update(options)

        session = async_get_clientsession(hass)
        self._api = self._get_api(self._configs, session)
        self._host = self._configs[CONF_HOST]
        self._identity: dict[str, Any] | None = None

    @staticmethod
    def _get_api(
        configs: dict[str, Any],
        session: aiohttp.ClientSession,
    ) -> AIOChroma:
        """Get Chroma API."""

        return AIOChroma(
            host=configs[CONF_HOST],
            targets=configs.get(CONF_DEVICES),
            layout=configs.get(CONF_LAYOUT, DEFAULT_LAYOUT),
            session=session,
        )

    @property
    def is_connected(self) -> bool:
        """Get connection status."""

        return self._api.connected

    async def async_connect(self) -> None:
        """Connect to the device."""

        try:
            await self._api.async_connect()
            await self._api.async_initialize(self._configs[CONF_DEVICES])
            self._identity = self._api.identity
        except Exception as ex:
            raise ConfigEntryNotReady from ex

    async def async_disconnect(self) -> None:
        """Disconnect from the device."""

        await self._api.async_disconnect()

    async def async_get_available_sensors(self) -> dict[str, dict[str, Any]]:
        """Get a dictionary of available sensors."""

        sensors_types = {
            SENSORS_TYPE_LIGHT: {
                "sensors": self._configs[CONF_DEVICES],
                "method": self._get_light,
            },
        }

        return sensors_types

    async def _get_light(self) -> dict[str, Any]:
        """Get lights data from the device."""

        try:
            data = await self._api.async_get_state()
            _LOGGER.debug(f"Sensors. Light data: {data}")
        except Exception as ex:
            raise UpdateFailed(ex) from ex

        return data
