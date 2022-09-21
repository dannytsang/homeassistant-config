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
