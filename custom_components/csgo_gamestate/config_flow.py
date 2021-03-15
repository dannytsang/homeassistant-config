"""Config flow for csgo_gamestate."""
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN

config_entry_flow.register_webhook_flow(
    DOMAIN, "Webhook", {"docs_url": "https://github.com/lociii/homeassistant-csgo/blob/master/info.md"},
)
