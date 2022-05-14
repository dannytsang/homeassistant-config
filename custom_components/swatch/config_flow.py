"""Config flow for swatch integration."""
from __future__ import annotations

import logging
from typing import Any

import requests
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from yarl import URL

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL): str,
    }
)


def get_config_entry_title(url_str: str) -> str:
    """Get the title of a config entry from the URL."""
    # Strip the scheme from the URL as it's not that interesting in the title
    # and space is limited on the integrations page.
    url = URL(url_str)
    return str(url).replace("http://", "")


def validate_host(host) -> bool:
    """Validate if Swatch host is valid."""
    resp = requests.get(host)

    if not resp or resp.status_code != 200:
        return False
    else:
        return True


async def validate_input(
    hass: HomeAssistant,
    data: dict[str, Any],
) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with
    values provided by the user.
    """
    host = data[CONF_URL]

    host_is_valid = await hass.async_add_executor_job(validate_host, host)

    if not host_is_valid:
        raise CannotConnect

    # Return info that you want to store in the config entry.
    return {"title": get_config_entry_title(host), CONF_URL: host}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for swatch."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(
                title=info["title"],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
