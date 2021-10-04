"""The Hildebrand Glow integration."""
import asyncio
import logging
from typing import Any, Dict

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import APP_ID, DOMAIN
from .glow import Glow, InvalidAuth, NoCADAvailable

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: Dict[str, Any]) -> bool:
    """Set up the Hildebrand Glow component."""
    hass.data[DOMAIN] = {}

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hildebrand Glow from a config entry."""
    glow = Glow(APP_ID, entry.data["username"], entry.data["password"])

    try:
        await hass.async_add_executor_job(glow.authenticate)
        await hass.async_add_executor_job(glow.retrieve_cad_hardwareId)
        await hass.async_add_executor_job(glow.connect_mqtt)

        while not glow.broker_active:
            continue

    except InvalidAuth:
        _LOGGER.error("Couldn't login with the provided username/password.")

        return False

    except NoCADAvailable:
        _LOGGER.error("Couldn't find any CAD devices (e.g. Glow Stick)")

        return False

    hass.data[DOMAIN][entry.entry_id] = glow

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
