"""Chroma compilers."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.entity import EntityCategory

from .const import ICONS, ICONS_OFF, ICONS_ON, SENSORS_TYPE_LIGHT
from .dataclass import ChromaLightDescription


def list_lights(devices: list[str] | None = None) -> dict[str, Any]:
    """Compile a list of lights."""

    lights = dict()

    if not devices:
        return lights

    for device in devices:
        light = device
        lights.update(
            {
                (SENSORS_TYPE_LIGHT, light): ChromaLightDescription(
                    key=light,
                    key_group=SENSORS_TYPE_LIGHT,
                    name=light,
                    icon=ICONS[light] if light in ICONS else None,
                    icon_on=ICONS_ON[light] if light in ICONS_ON else None,
                    icon_off=ICONS_OFF[light] if light in ICONS_OFF else None,
                    entity_category=EntityCategory.CONFIG,
                    entity_registry_enabled_default=True,
                )
            }
        )

    return lights
