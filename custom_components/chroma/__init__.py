"""Support for Chroma devices."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.core import HomeAssistant

from .chroma import Chroma
from .const import DATA_CHROMA, DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
) -> bool:
    """Setup Chroma platform."""

    chroma = Chroma(hass, config_entry)
    await chroma.setup()

    chroma.async_on_close(config_entry.add_update_listener(update_listener))

    async def async_close_connnection(event):
        """Close Chroma connection on HA stop."""

        await chroma.close()

    stop_listener = hass.bus.async_listen_once(
        EVENT_HOMEASSISTANT_STOP, async_close_connnection
    )

    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = {
        DATA_CHROMA: chroma,
        "stop_listener": stop_listener,
    }

    hass.config_entries.async_setup_platforms(config_entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
) -> bool:
    """Unload config entry."""

    unload = await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)

    if unload:
        hass.data[DOMAIN][config_entry.entry_id]["stop_listener"]()
        chroma = hass.data[DOMAIN][config_entry.entry_id][DATA_CHROMA]
        await chroma.close()

        hass.data[DOMAIN].pop(config_entry.entry_id)

    return unload


async def update_listener(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
) -> None:
    """Update on config_entry update."""

    chroma = hass.data[DOMAIN][config_entry.entry_id][DATA_CHROMA]

    if chroma.update_options(config_entry.options):
        await hass.config_entries.async_reload(config_entry.entry_id)

    return
