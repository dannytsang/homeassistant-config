"""Chroma configuration flow."""

from __future__ import annotations

import logging
import socket
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import (
    CHROMA_DEVICES,
    CHROMA_LAYOUTS,
    CONF_DEVICES,
    CONF_LAYOUT,
    DEFAULT_LAYOUT,
    DOMAIN,
    RESULT_SUCCESS,
)

_LOGGER = logging.getLogger(__name__)


def _check_host(
    host: str,
) -> str | None:
    """Get the IP address from the hostname."""

    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None


def _check_errors(
    errors: dict[str, Any],
) -> bool:
    """Check for errors."""

    if (
        "base" in errors
        and errors["base"] != RESULT_SUCCESS
        and errors["base"] != str()
    ):
        return True

    return False


def _create_form_discovery(
    user_input: dict[str, Any] = dict(),
) -> vol.Schema:
    """Create a form for the 'discovery' step."""

    schema = {
        vol.Required(CONF_HOST, default=user_input.get(CONF_HOST, "")): cv.string,
    }

    return vol.Schema(schema)


def _create_form_devices(
    user_input: dict[str, Any] = dict(),
    default: list[str] = list(),
) -> vol.Schema:
    """Create a form for the 'devices' step."""

    schema = {
        vol.Required(
            CONF_DEVICES,
            default=default,
        ): cv.multi_select({k: k for k in user_input[CONF_DEVICES]}),
    }

    return vol.Schema(schema)


def _create_form_layout(
    user_input: dict[str, Any] = dict(),
    default: list[str] = list(),
) -> vol.Schema:
    """Create a form for the 'layout' step."""

    schema = {
        vol.Required(
            CONF_LAYOUT,
            default=user_input.get(CONF_LAYOUT, DEFAULT_LAYOUT),
        ): vol.In(CHROMA_LAYOUTS),
    }

    return vol.Schema(schema)


def _create_form_name(
    user_input: dict[str, Any] = dict(),
) -> vol.Schema:
    """Create a form for the 'name' step."""

    schema = {
        vol.Optional(CONF_NAME, default=user_input.get(CONF_NAME, "")): cv.string,
    }

    return vol.Schema(schema)


class ChromaFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for Chroma."""

    VERSION = 1

    def __init__(self):
        """Initialize config flow."""

        self._configs = dict()
        self._options = dict()
        self._unique_id: str | None = None

        self._steps = {
            "discovery": self.async_step_devices,
            "devices": self.async_step_layout,
            "layout": self.async_step_name,
            "name": self.async_step_finish,
        }

    async def async_select_step(
        self,
        last_step: str | None = None,
        errors: dict[str, Any] = dict(),
    ) -> FlowResult:
        """Step selector."""

        if last_step:
            if last_step in self._steps:
                if _check_errors(errors):
                    return await self._steps[f"{last_step}_error"](errors=errors)
                else:
                    return await self._steps[last_step]()
            else:
                raise ValueError(f"Unknown value of last_step: {last_step}")
        else:
            raise ValueError("Step name was not provided")

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Flow initiated by user."""

        return await self.async_step_discovery(user_input)

    # Step #1 - discover the device
    async def async_step_discovery(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Device discovery step."""

        step_id = "discovery"

        errors = dict()

        if user_input:
            # Check if host can be resolved
            ip = await self.hass.async_add_executor_job(
                _check_host, user_input[CONF_HOST]
            )
            if not ip:
                errors["base"] = "cannot_resolve_host"

            if not errors:
                self._configs.update(user_input)
                return await self.async_select_step(step_id, errors)

        if not user_input:
            user_input = dict()

        return self.async_show_form(
            step_id=step_id,
            data_schema=_create_form_discovery(user_input),
            errors=errors,
        )

    # Step #2 - devices to control
    async def async_step_devices(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Step to select devices to control."""

        step_id = "devices"

        if not user_input:
            user_input = self._options.copy()
            user_input[CONF_DEVICES] = CHROMA_DEVICES
            return self.async_show_form(
                step_id=step_id,
                data_schema=_create_form_devices(user_input),
            )

        self._options.update(user_input)

        return await self.async_select_step(step_id)

    # Step #3 (optional) - select keyboard layout
    async def async_step_layout(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Step to select keyboard layout."""

        step_id = "layout"

        if (
            self._options.get(CONF_DEVICES)
            and "keyboard" in self._options[CONF_DEVICES]
        ):
            if not user_input:
                user_input = self._options.copy()
                user_input[CONF_LAYOUT] = CHROMA_LAYOUTS
                return self.async_show_form(
                    step_id=step_id,
                    data_schema=_create_form_layout(user_input),
                )

            self._options.update(user_input)

        return await self.async_select_step(step_id)

    # Step #4 - select device name
    async def async_step_name(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Name the device step."""

        step_id = "name"

        if not user_input:
            user_input = dict()
            return self.async_show_form(
                step_id=step_id,
                data_schema=_create_form_name(user_input),
            )

        self._options.update(user_input)

        return await self.async_select_step(step_id)

    # Step Finish
    async def async_step_finish(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Finish setup."""

        return self.async_create_entry(
            title=self._options[CONF_NAME],
            data=self._configs,
            options=self._options,
        )
