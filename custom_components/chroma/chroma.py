"""Chroma module."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any, Awaitable, Callable, TypeVar

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, ServiceCall, callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from aiochroma import Color
from .bridge import ChromaBridge
from .const import (
    CONF_REQ_RELOAD,
    DEFAULT_MESSAGE_BACKGROUND,
    DEFAULT_MESSAGE_BRIGHTNESS,
    DEFAULT_MESSAGE_REPEATS,
    DEFAULT_MESSAGE_SLEEP,
    DEFAULT_MESSAGE_SPACING,
    DEFAULT_MESSAGE_TAIL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    KEY_COORDINATOR,
)

_LOGGER = logging.getLogger(__name__)


_T = TypeVar("_T")


class ChromaSensorHandler:
    """Data handler for Chroma sensors."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: ChromaBridge,
        scan_interval: int = DEFAULT_SCAN_INTERVAL,
    ) -> None:
        """Initialise data handler."""

        self._hass = hass
        self._api = api
        self._connected_devices = 0
        self._connected_devices_list: list[str] = list()
        self._scan_interval = timedelta(seconds=scan_interval)

    async def get_coordinator(
        self,
        sensor_type: str,
        update_method: Callable[[], Awaitable[_T]] | None = None,
    ) -> DataUpdateCoordinator:
        """Find coordinator for the sensor type."""

        should_poll = True

        if update_method is not None:
            method = update_method
        else:
            raise RuntimeError(f"Unknown sensor type: {sensor_type}")

        coordinator = DataUpdateCoordinator(
            self._hass,
            _LOGGER,
            name=sensor_type,
            update_method=method,
            update_interval=self._scan_interval if should_poll else None,
        )
        await coordinator.async_refresh()

        return coordinator


class Chroma:
    """Representation of Chroma."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize Chroma."""

        self.hass = hass
        self._config_entry = config_entry

        self._api: ChromaBridge | None = None

        self._options = config_entry.options.copy()

        self._host: str = config_entry.data[CONF_HOST]

        self._name: str = self._options[CONF_NAME]

        self._model: str = "ChromaSDK"
        self._vendor: str = "Razer Inc."
        self._firmware: str | None = None

        self._sensors_data_handler: ChromaSensorHandler | None = None
        self._sensors_coordinator: dict[str, Any] = {}

        self._on_close: list[Callable] = list()

    async def setup(self) -> None:
        """Setup Chroma."""

        self._api = ChromaBridge(
            self.hass, dict(self._config_entry.data), self._options
        )

        try:
            await self._api.async_connect()
        except OSError as ex:
            raise ConfigEntryNotReady from ex

        # Services -->
        async def async_service_send_message(service: ServiceCall):
            """Send message to the keyboard."""

            data = service.data

            _LOGGER.debug(f"Calling service Send Message with parameters: {data}")

            (r, g, b) = data.get("color")
            color = Color(r, g, b)
            (r, g, b) = data.get("background", DEFAULT_MESSAGE_BACKGROUND)
            background = Color(r, g, b)

            await self._api._api.async_keyboard_sequence(
                message=data.get("message"),
                color=color,
                background=background,
                brightness=data.get("brightness", DEFAULT_MESSAGE_BRIGHTNESS),
                tail=data.get("tail", DEFAULT_MESSAGE_TAIL),
                repeats=data.get("repeats", DEFAULT_MESSAGE_REPEATS),
                spacing=data.get("spacing", DEFAULT_MESSAGE_SPACING),
                sleep=data.get("sleep", DEFAULT_MESSAGE_SLEEP),
            )

        if "keyboard" in self._options["devices"]:
            self.hass.services.async_register(
                DOMAIN, "service_send_message", async_service_send_message
            )
        # <-- Services

        self._firmware = self._api._identity["version"]

        if self._model is not None:
            if self._name is None or self._name == "":
                self._name = self._model

        # Initialise sensors
        await self.init_sensors_coordinator()

    async def init_sensors_coordinator(self) -> None:
        """Initialize Chroma sensors coordinators."""

        if self._sensors_data_handler:
            return

        self._sensors_data_handler = ChromaSensorHandler(
            self.hass, self._api, DEFAULT_SCAN_INTERVAL
        )

        sensors_types = await self._api.async_get_available_sensors()

        for sensor_type, sensor_def in sensors_types.items():
            if not (sensor_names := sensor_def.get("sensors")):
                continue
            coordinator = await self._sensors_data_handler.get_coordinator(
                sensor_type, update_method=sensor_def.get("method")
            )
            self._sensors_coordinator[sensor_type] = {
                KEY_COORDINATOR: coordinator,
                sensor_type: sensor_names,
            }

    async def close(self) -> None:
        """Close the connection."""

        if self._api is not None:
            await self._api.async_disconnect()
        self._api = None

        for func in self._on_close:
            func()
        self._on_close.clear()

    @callback
    def async_on_close(
        self,
        func: CALLBACK_TYPE,
    ) -> None:
        """Functions on close."""

        self._on_close.append(func)

    def update_options(
        self,
        new_options: dict,
    ) -> bool:
        """Update Chroma options."""

        req_reload = False
        for name, new_opt in new_options.items():
            if name in CONF_REQ_RELOAD:
                old_opt = self._options.get(name)
                if not old_opt or old_opt != new_opt:
                    req_reload = True
                    break

        self._options.update(new_options)
        return req_reload

    @property
    def device_info(self) -> DeviceInfo:
        """Device information."""

        return DeviceInfo(
            identifiers={(DOMAIN, self._name)},
            name=self._name,
            model=self._model,
            manufacturer=self._vendor,
            sw_version=self._firmware,
        )

    @property
    def host(self) -> str:
        """Chroma hostname."""

        return self._host

    @property
    def api(self) -> ChromaBridge:
        """Chroma API."""

        return self._api
