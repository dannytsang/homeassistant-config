"""Chroma dataclasses."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntityDescription
from homeassistant.components.light import LightEntityDescription
from homeassistant.helpers.entity import EntityDescription


@dataclass
class ChromaEntityDescription(EntityDescription):
    """Describe Chroma entity."""

    key_group: Callable[[dict], str] | None = None
    value: Callable[[Any], Any] = lambda val: val
    extra_state_attributes: dict[str, Any] | None = None


@dataclass
class ChromaBinaryDescription(ChromaEntityDescription, BinarySensorEntityDescription):
    """Describe Chroma binary entity."""

    icon_on: str | None = None
    icon_off: str | None = None


@dataclass
class ChromaLightDescription(ChromaBinaryDescription, LightEntityDescription):
    """Describe Chroma light."""
