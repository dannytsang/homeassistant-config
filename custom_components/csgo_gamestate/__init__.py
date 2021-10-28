from http import HTTPStatus
import logging

from aiohttp import web
import voluptuous as vol

from homeassistant.const import CONF_WEBHOOK_ID
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN
from .gamestate import GameState
from .schema import WEBHOOK_SCHEMA

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, hass_config):
    """Set up the csgo_gamestate component."""
    return True


async def async_setup_entry(hass, entry):
    """Configure based on config entry."""
    hass.components.webhook.async_register(
        DOMAIN, "CS:GO game state listener", entry.data[CONF_WEBHOOK_ID], handle_webhook
    )
    hass.data.setdefault(DOMAIN, GameState(hass=hass).dump())
    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    hass.components.webhook.async_unregister(entry.data[CONF_WEBHOOK_ID])
    return True


async def handle_webhook(hass, webhook_id, request):
    """Handle incoming webhook from CSGO."""
    # parse request data
    try:
        data = WEBHOOK_SCHEMA(await request.json())
    except vol.MultipleInvalid as error:
        _LOGGER.warn(f"csgo: failed to parse message '{error.error_message}''")
        # always reply 200 so that csgo keeps sending data
        return web.Response(text="OK", status=HTTPStatus.OK)

    # load current gamestate
    gamestate = GameState(hass=hass)
    gamestate.load(data=hass.data[DOMAIN])

    # check for updates and fire signals
    gamestate.update(data=data)

    # store updated gamestate
    hass.data[DOMAIN] = gamestate.dump()

    # acknowledge
    return web.Response(text="OK", status=HTTPStatus.OK)


# pylint: disable=invalid-name
async_remove_entry = config_entry_flow.webhook_async_remove_entry
