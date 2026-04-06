[<- Back to Integrations README](../README.md) · [Packages README](../../README.md) · [Main README](../../../README.md)

# Zigbee

Coordinator availability monitoring for the Zigbee2MQTT bridge.

---

## Overview

A single automation notifies Danny when the Zigbee2MQTT bridge connection becomes unavailable, with a 1-minute delay to avoid alerts from brief restarts.

---

## Automations

| ID | Alias | Trigger | Delay | Action |
|----|-------|---------|-------|--------|
| `1741294780206` | Zigbee Coordinator Unavailable | `binary_sensor.zigbee2mqtt_bridge_connection_state` → `unavailable` for 1 min | 1 minute | Direct notification to Danny |

---

## Entities

| Entity | Description |
|--------|-------------|
| `binary_sensor.zigbee2mqtt_bridge_connection_state` | Zigbee2MQTT bridge connection status |

---

## Dependencies

- **Integration:** [Zigbee2MQTT](https://www.zigbee2mqtt.io/) via MQTT
- **Scripts:** `script.send_direct_notification`
- **Person:** `person.danny` (notification recipient)

---

*Last updated: 2026-04-05*
