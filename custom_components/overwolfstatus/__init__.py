from aiohttp import web

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_WEBHOOK_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN, EVENT_NAME, TITLE


async def handle_webhook(
    hass: HomeAssistant, webhook_id: str, request: web.Request
) -> web.Response:
    """Fire Overwolf data 1:1 as a Home Assistant event."""
    try:
        data = await request.json()
    except Exception:
        return web.Response(text="Failed to parse payload", status=400)

    hass.bus.async_fire(EVENT_NAME, data)
    return web.Response(text="OK")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configure based on config entry."""
    hass.components.webhook.async_register(
        DOMAIN, TITLE, entry.data[CONF_WEBHOOK_ID], handle_webhook
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.components.webhook.async_unregister(entry.data[CONF_WEBHOOK_ID])
    return True


async_remove_entry = config_entry_flow.webhook_async_remove_entry
