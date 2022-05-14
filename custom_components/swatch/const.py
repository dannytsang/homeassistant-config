"""Constants for the swatch integration."""

from homeassistant.const import Platform

NAME = "Swatch"
DOMAIN = "swatch"

# Attributes
ATTR_CONFIG = "config"
ATTR_CLIENT = "client"
ATTR_CLIENT_ID = "client_id"
ATTR_COORDINATOR = "coordinator"

# Platforms
PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR]

# Services
SERVICE_DETECT_OBJECT = "detect_object"

STARTUP_MESSAGE = """
-------------------------------------------------------------------
{title}
Integration Version: {integration_version}
This is a custom integration!
If you have any issues with this you need to open an issue here:
https://github.com/blakeblackshear/frigate-hass-integration/issues
-------------------------------------------------------------------
"""
