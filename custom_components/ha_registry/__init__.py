"""The Home Assistant Registry integration."""
import logging

import homeassistant.core as ha
import voluptuous as vol
from homeassistant.auth.permissions.const import CAT_ENTITIES
from homeassistant.auth.permissions.const import POLICY_EDIT
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_AREA_ID
from homeassistant.const import ATTR_DEVICE_CLASS
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.const import ATTR_ICON
from homeassistant.const import ATTR_NAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import NoEntitySpecifiedError
from homeassistant.exceptions import Unauthorized
from homeassistant.exceptions import UnknownUser
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_registry import RegistryEntryDisabler
from homeassistant.helpers.entity_registry import RegistryEntryHider

from .const import ATTR_ALIASES
from .const import ATTR_DISABLED
from .const import ATTR_DISABLED_BY
from .const import ATTR_HIDDEN
from .const import ATTR_HIDDEN_BY
from .const import ATTR_NEW_ENTITY_ID
from .const import ATTR_OPTIONS
from .const import ATTR_OPTIONS_DOMAIN
from .const import DOMAIN
from .const import SERVICE_REMOVE_ENTITY
from .const import SERVICE_UPDATE_ENTITY


SCHEMA_REMOVE_ENTITY = vol.Schema(
    {
        vol.Required(ATTR_ENTITY_ID): cv.entity_ids,
    }
)
SCHEMA_UPDATE_ENTITY = vol.Schema(
    {
        vol.Required(ATTR_ENTITY_ID): cv.entity_ids,
        vol.Optional(ATTR_ALIASES): vol.All(cv.ensure_list_csv, [cv.string]),
        vol.Optional(ATTR_AREA_ID): vol.Any(None, str),
        vol.Optional(ATTR_DEVICE_CLASS): vol.Any(None, str),
        vol.Optional(ATTR_ICON): vol.Any(None, str),
        vol.Optional(ATTR_NAME): vol.Any(None, str),
        vol.Optional(ATTR_NEW_ENTITY_ID): cv.string,
        vol.Inclusive(ATTR_OPTIONS_DOMAIN, "entity_option"): vol.Any(None, str),
        vol.Inclusive(ATTR_OPTIONS, "entity_option"): vol.Any(None, dict),
        vol.Optional(ATTR_DISABLED): bool,
        vol.Optional(ATTR_HIDDEN): bool,
    }
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Home Assistant Registry from a config entry."""

    async def check_permissions_and_entities(
        entity_registry, entities, context
    ) -> None:
        """Check user has permissions to edit entities and that entity registries exist."""
        if context.user_id:
            user = await hass.auth.async_get_user(context.user_id)

            if user is None:
                raise UnknownUser(
                    context=context,
                    permission=POLICY_EDIT,
                    user_id=context.user_id,
                )

            for entity_id in entities:
                if not user.permissions.check_entity(entity_id, POLICY_EDIT):
                    raise Unauthorized(
                        context=context,
                        permission=POLICY_EDIT,
                        user_id=context.user_id,
                        perm_category=CAT_ENTITIES,
                    )

        not_found_entities = [
            entity_id
            for entity_id in entities
            if not entity_registry.async_is_registered(entity_id)
        ]
        if len(not_found_entities) > 0:
            raise NoEntitySpecifiedError(
                f"Entity registries not found: {not_found_entities}"
            )

    async def async_remove_entity(call: ha.ServiceCall) -> None:
        """Remove entity."""
        entity_ids = call.data[ATTR_ENTITY_ID]
        registry = er.async_get(hass)

        await check_permissions_and_entities(registry, entity_ids, call.context)

        for entity_id in entity_ids:
            _LOGGER.debug("Removing entity %s", entity_id)
            registry.async_remove(entity_id)

    hass.services.async_register(
        DOMAIN,
        SERVICE_REMOVE_ENTITY,
        async_remove_entity,
        schema=SCHEMA_REMOVE_ENTITY,
    )

    async def async_update_entity(call):
        """Update entity"""
        entities = call.data[ATTR_ENTITY_ID]
        entity_registry = er.async_get(hass)

        await check_permissions_and_entities(entity_registry, entities, call.context)

        changes = {ATTR_ICON: None}
        for key in (
            ATTR_AREA_ID,
            ATTR_DEVICE_CLASS,
            ATTR_ICON,
            ATTR_NAME,
            ATTR_NEW_ENTITY_ID,
        ):
            if key in call.data:
                value = call.data[key]
                if type(value) is str and value.strip() == "":
                    value = None
                _LOGGER.debug("Service call {%s:%s}", key, value)
                changes[key] = value

        aliases = call.data.get(ATTR_ALIASES)
        if aliases is not None:
            changes[ATTR_ALIASES] = set(aliases)

        disabled = call.data.get(ATTR_DISABLED)
        if disabled is not None:
            changes[ATTR_DISABLED_BY] = RegistryEntryDisabler.USER if disabled else None
            if disabled is False:
                device_registry = dr.async_get(hass)
                disabled_entities = []
                for entity_id in entities:
                    entity_entry = entity_registry.async_get(entity_id)
                    if entity_entry.device_id:
                        device = device_registry.async_get(entity_entry.device_id)
                        if device and device.disabled:
                            disabled_entities.append(entity_id)
                if len(disabled_entities) > 0:
                    raise ValueError(
                        "Can not enable entities wtih disabled devices: {disabled_entities}"
                    )

        hidden = call.data.get(ATTR_HIDDEN)
        if hidden is not None:
            changes[ATTR_HIDDEN_BY] = RegistryEntryHider.USER if hidden else None

        for entity_id in entities:
            if ATTR_OPTIONS_DOMAIN in call.data:
                _LOGGER.debug("Updating entity %s options", entity_id)
                entity_entry = entity_registry.async_update_entity_options(
                    entity_id, call.data[ATTR_OPTIONS_DOMAIN], call.data[ATTR_OPTIONS]
                )

            if changes:
                _LOGGER.debug("Updating entity %s", entity_id)
                entity_registry.async_update_entity(entity_id, **changes)

    hass.services.async_register(
        DOMAIN, SERVICE_UPDATE_ENTITY, async_update_entity, schema=SCHEMA_UPDATE_ENTITY
    )

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    return True
