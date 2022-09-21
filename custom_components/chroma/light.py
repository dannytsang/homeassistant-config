"""Chroma lights."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.light import ColorMode, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from aiochroma import Color
from .chroma import Chroma
from .compilers import list_lights
from .const import CONF_DEVICES
from .dataclass import ChromaLightDescription
from .entity import ChromaBinaryEntity, async_setup_chroma_entry

_LOGGER = logging.getLogger(__name__)


LIGHTS = {}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup Chroma lights."""

    LIGHTS.update(list_lights(config_entry.options[CONF_DEVICES]))

    await async_setup_chroma_entry(
        hass, config_entry, async_add_entities, LIGHTS, ChromaLight
    )


class ChromaLight(ChromaBinaryEntity, LightEntity):
    """Chroma light."""

    _attr_supported_color_modes = {ColorMode.RGB}
    _attr_color_mode = ColorMode.RGB

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        chroma: Chroma,
        description: ChromaLightDescription,
    ) -> None:
        """Initialize Chroma light."""

        super().__init__(coordinator, chroma, description)
        self._target = description.key

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""

        _LOGGER.debug(f"Command `turn_off` with args: `{kwargs}`")

        await self.api.async_turn_off(self._target)

        self.async_schedule_update_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the light."""

        _LOGGER.debug(f"Command `turn_on` with args: `{kwargs}`")

        color: int | None = None
        brightness: float | None = None

        if "rgb_color" in kwargs:
            (r, g, b) = kwargs["rgb_color"]
            color = Color(r, g, b)
        elif "brightness" in kwargs:
            brightness = kwargs["brightness"]

        await self.api.async_turn_on(self._target, color, brightness)

        self.async_schedule_update_ha_state()

    @property
    def is_on(self) -> bool:
        """Return state of the light."""

        return self.coordinator.data.get(self._target).get("state")

    @property
    def brightness(self) -> int:
        """Return brightness of the light."""

        return self.coordinator.data.get(self._target).get("brightness")

    @property
    def rgb_color(self) -> tuple[int, int, int]:
        """Return RGB color of the light."""

        color = self.coordinator.data.get(self._target).get("color")
        return (color.r, color.g, color.b)
