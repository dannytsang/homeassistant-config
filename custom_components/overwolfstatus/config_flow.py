"""Config flow for overwolf_status."""
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN, TITLE


config_entry_flow.register_webhook_flow(
    DOMAIN,
    TITLE,
    {
        "docs_url": "https://github.com/lociii/homeassistant-overwolf-status/blob/master/info.md",
        "overwolf_url": "https://TBD",
    },
    False,
)
