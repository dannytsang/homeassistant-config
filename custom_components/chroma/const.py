"""Chroma constants."""

from __future__ import annotations

from homeassistant.const import Platform

# Main integrartion info
DOMAIN = "chroma"
DATA_CHROMA = DOMAIN
PLATFORMS = [
    Platform.LIGHT,
]
KEY_COORDINATOR = "coordinator"

CONF_CONFIRM = "confirm"
CONF_DEVICES = "devices"
CONF_LAYOUT = "layout"
CONF_REQ_RELOAD = [
    CONF_DEVICES,
]

SENSORS_TYPE_LIGHT = "light"

RESULT_SUCCESS = "success"

CHROMA_DEVICES = [
    "chromalink",
    "headset",
    "keyboard",
    "keypad",
    "mouse",
    "mousepad",
]
CHROMA_LAYOUTS = {
    "EN_US": "English (US)",
}
DEFAULT_LAYOUT = "EN_US"
DEFAULT_SCAN_INTERVAL = 5

# Defaults for services
DEFAULT_MESSAGE_BACKGROUND = [0, 0, 0]
DEFAULT_MESSAGE_BRIGHTNESS = 255
DEFAULT_MESSAGE_REPEATS = 1
DEFAULT_MESSAGE_SLEEP = 0.5
DEFAULT_MESSAGE_SPACING = 0.5
DEFAULT_MESSAGE_TAIL = 0

ICONS = {
    "headset": "mdi:headset",
    "keyboard": "mdi:keyboard-outline",
    "mouse": "mdi:rodent",
}
ICONS_ON = {
    "chromalink": "mdi:lightbulb-on-outline",
}
ICONS_OFF = {
    "chromalink": "mdi:lightbulb-outline",
}
