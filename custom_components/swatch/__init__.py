"""The swatch integration."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_MODEL, CONF_URL
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.loader import async_get_integration
from homeassistant.util import slugify

from .api import SwatchApiClient, SwatchApiClientError
from .const import (
    ATTR_CLIENT,
    ATTR_CONFIG,
    ATTR_COORDINATOR,
    DOMAIN,
    NAME,
    PLATFORMS,
    STARTUP_MESSAGE,
)

_LOGGER: logging.Logger = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=5)


def get_swatch_device_identifier(
    entry: ConfigEntry, camera_name: str | None = None
) -> tuple[str, str]:
    """Get a device identifier."""
    if camera_name:
        return (DOMAIN, f"{entry.entry_id}:{slugify(camera_name)}")
    else:
        return (DOMAIN, entry.entry_id)


def get_swatch_entity_unique_id(
    config_entry_id: str,
    type_name: str,
    name: str,
) -> str:
    """Get the unique_id for a Swatch entity."""
    return f"{config_entry_id}:{type_name}:{name}"


def get_friendly_name(name: str) -> str:
    """Get a friendly version of a name."""
    return name.replace("_", " ").title()


def get_zones_and_objects(
    config: dict[str, Any],
) -> set[tuple[str, str, str]]:
    """Get cameras and tracking object tuples."""
    zone_objects = set()
    for cam_name, cam_config in config["cameras"].items():
        for zone_name, zone_config in cam_config["zones"].items():
            for obj in zone_config["objects"]:
                zone_objects.add((cam_name, zone_name, obj))

    return zone_objects


def get_cameras_and_zones(config: dict[str, Any]) -> set[str]:
    """Get cameras and zones."""
    cameras_zones = set()
    for camera in config.get("cameras", {}).keys():
        cameras_zones.add(camera)
        for zone in config["cameras"][camera].get("zones", {}).keys():
            cameras_zones.add(zone)
    return cameras_zones


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Set up this integration using YAML is not supported."""
    integration = await async_get_integration(hass, DOMAIN)
    _LOGGER.info(
        STARTUP_MESSAGE.format(
            title=NAME,
            integration_version=integration.version,
        )
    )

    hass.data.setdefault(DOMAIN, {})

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up swatch from a config entry."""
    # TODO Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)

    client = SwatchApiClient(
        entry.data.get(CONF_URL),
        async_get_clientsession(hass),
    )
    coordinator = SwatchDataUpdateCoordinator(hass, client=client)
    await coordinator.async_config_entry_first_refresh()
    model = f"{(await async_get_integration(hass, DOMAIN)).version}/1.0.0"

    try:
        config = await client.async_get_config()
    except SwatchApiClientError:
        return False

    hass.data[DOMAIN][entry.entry_id] = {
        ATTR_CLIENT: client,
        ATTR_CONFIG: config,
        ATTR_COORDINATOR: coordinator,
        ATTR_MODEL: model,
    }

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    ):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class SwatchEntity(Entity):  # type: ignore[misc]
    """Base class for Swatch entities."""

    def __init__(self, config_entry: ConfigEntry):
        """Construct a SwatchEntity."""
        Entity.__init__(self)

        self._config_entry = config_entry
        self._available = True

    @property
    def available(self) -> bool:
        """Return the availability of the entity."""
        return self._available

    def _get_model(self) -> str:
        """Get the Swatch device model string."""
        return str(
            self.hass.data[DOMAIN][self._config_entry.entry_id][ATTR_MODEL],
        )


class SwatchDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage updating entities latest state from API."""

    def __init__(self, hass: HomeAssistant, client: SwatchApiClient):
        """Initialize."""
        self._api = client
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            return await self._api.async_get_object_state("all")
        except SwatchApiClientError as exc:
            raise exc
