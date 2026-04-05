[<- Back to Integrations README](../README.md) · [Packages README](../../README.md) · [Main README](../../../README.md)

# ESPHome Device Management

*Last updated: 2026-04-05*

Manages ESPHome-based devices across the house: automatically installs firmware updates for bed presence sensors and recovers ESP plugs that have gone offline.

## Automations

| Automation | Trigger | Mode | Description |
|------------|---------|------|-------------|
| ESPHome: Firmware Update | `update.bed_firmware` or `update.leos_bed_firmware` → `on` | Queued (max 15) | Calls `update.install` on the triggering entity and logs the update |
| ESPHome: ESP Plug Turned Off | Any monitored ESP plug → `off` for 5 minutes | Queued (max 10) | Turns the plug back on and logs a debug entry |

### Monitored ESP Plugs

| Entity | Location |
|--------|----------|
| `switch.bedroom_esp_plug` | Bedroom |
| `switch.ashlee_s_bedroom_esp_plug` | Ashlee's room |
| `switch.kitchen_esp_plug` | Kitchen |
| `switch.leo_s_bedroom_esp_plug` | Leo's room |
| `switch.conservatory_extension_2` | Conservatory |

### Firmware Update Entities

| Entity | Device |
|--------|--------|
| `update.bed_firmware` | Bed presence sensor |
| `update.leos_bed_firmware` | Leo's bed presence sensor |

## Notes

- The 5-minute `for:` delay on the plug recovery automation avoids acting on brief, intentional power interruptions.
- Both automations use the `trigger.entity_id` template variable so the same action block handles all monitored entities without duplication.
- Firmware updates are queued (max 15) to handle multiple devices updating simultaneously without collisions.
