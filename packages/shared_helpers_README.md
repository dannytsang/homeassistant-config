[<- Back to Packages README](README.md) · [Main README](../README.md)

# Shared Helpers

*Last updated: 2026-04-05*

Cross-cutting template sensors and utility scripts shared by room and automation packages throughout the configuration. Nothing in this package controls hardware directly — it provides building blocks consumed by other packages.

---

## Contents

- [Scripts](#scripts)
- [Template Binary Sensors](#template-binary-sensors)

---

## Scripts

### `script.log_with_clock`

**Alias:** Send Log Message with Clock Emoji

Wraps `script.send_to_home_log` with an automatic clock emoji that reflects the current hour and minute. Callers pass a title, message body, and optional log level; the script calls `script.get_clock_emoji` to resolve the correct emoji and prepends it to the message before forwarding to the home log.

| Field | Required | Default | Description |
|---|---|---|---|
| `title` | Yes | — | Log message title (e.g. `🧑‍🍳 Kitchen`) |
| `message` | Yes | — | Log message body (multi-line supported) |
| `log_level` | No | `Debug` | Filter level: `Debug`, `Normal`, or `Important` |

**Mode:** `single`

---

## Template Binary Sensors

Each sensor compares the illuminance reading from a room-specific motion sensor against a configurable threshold `input_number`. When the illuminance falls below the threshold the sensor is `on` (dark), allowing lighting automations to decide whether to switch lights on when motion is detected.

| Entity ID | Illuminance sensor | Threshold input |
|---|---|---|
| `binary_sensor.kitchen_motion_dark` | `sensor.kitchen_motion_illuminance` | `input_number.kitchen_light_level_threshold` (default 500) |
| `binary_sensor.kitchen_motion_2_dark` | `sensor.kitchen_motion_2_illuminance` | `input_number.kitchen_light_level_2_threshold` (default 500) |
| `binary_sensor.stairs_motion_dark` | `sensor.stairs_motion_illuminance` | `input_number.stairs_light_level_threshold` (default 500) |
| `binary_sensor.back_garden_motion_dark` | `sensor.back_garden_motion_illuminance` | `input_number.back_garden_light_level_threshold` (default 500) |
| `binary_sensor.porch_motion_dark` | `sensor.porch_motion_illuminance` | `input_number.porch_light_level_threshold` (default 500) |

**Icon:** `mdi:brightness-5`

The kitchen has two variants (`kitchen_motion_dark` and `kitchen_motion_2_dark`) to cover the two separate motion sensors covering different parts of the kitchen.

---

## Dependencies

| Entity | Purpose |
|---|---|
| `script.get_clock_emoji` | Resolves a Unicode clock emoji for the current hour/minute |
| `script.send_to_home_log` | Writes log entries to the home log notification channel |
| `input_number.*_light_level_threshold` | Per-room illuminance thresholds, configurable via UI |
