[<- Back to Packages README](../README.md) · [Main README](../../README.md)

# Rooms

Last reviewed: 2026-06-14

Room-specific automations, scripts, scenes, templates, sensors, and commands organized by physical location in the house.

## Current Inventory

| Metric | Count |
|--------|-------|
| Room YAML files | 20 |
| Room automations | 213 |
| Room scenes | 64 |
| Room scripts | 41 |
| Room sensors | 48 |
| Room template blocks | 14 |
| Room shell commands | 1 |

## Subfolder Rooms

| Room | YAML files | Current package contents | README | Setup Guide |
|------|------------|--------------------------|--------|-------------|
| **Bedroom** | `bedroom.yaml`, `sleep_as_android.yaml`, `awtrix_light.yaml` | 32 automations, 5 scenes, 9 scripts, 5 sensors, 2 template blocks | [README](bedroom/README.md) | [SETUP](bedroom/BEDROOM-SETUP.md) |
| **Kitchen** | `kitchen.yaml`, `meater.yaml` | 29 automations, 16 scenes, 6 scripts, 13 sensors, 6 template blocks | [README](kitchen/README.md) | [SETUP](kitchen/KITCHEN-SETUP.md) |
| **Living Room** | `living_room.yaml` | 23 automations, 12 scenes, 5 scripts, 11 sensors, 1 template block | [README](living_room/README.md) | [SETUP](living_room/LIVING-ROOM-SETUP.md) |
| **Office** | `office.yaml`, `steam.yaml` | 29 automations, 8 scenes, 4 scripts, 9 sensors | [README](office/README.md) | [SETUP](office/OFFICE-SETUP.md) |
| **Porch** | `porch.yaml` | 12 automations, 6 scenes, 5 scripts, 1 template block | [README](porch/README.md) | [SETUP](porch/PORCH-SETUP.md) |
| **Stairs** | `stairs.yaml` | 14 automations, 9 scenes | [README](stairs/README.md) | [SETUP](stairs/STAIRS-SETUP.md) |
| **Conservatory** | `conservatory.yaml`, `airer.yaml`, `octoprint.yaml` | 17 automations, 5 scenes, 5 scripts, 1 sensor | [README](conservatory/README.md) | — |

## Single-File Rooms

| Room | YAML File | Current package contents | README |
|------|-----------|--------------------------|--------|
| **Attic** | [attic.yaml](attic.yaml) | 3 automations | [README](attic_README.md) |
| **Back Garden** | [back_garden.yaml](back_garden.yaml) | 3 automations | [README](back_garden_README.md) |
| **Bathroom** | [bathroom.yaml](bathroom.yaml) | 9 automations, 1 script, 1 sensor | [README](bathroom_README.md) |
| **Bedroom 2** | [bedroom2.yaml](bedroom2.yaml) | 15 automations, 2 scenes, 1 script, 1 sensor, 1 template block | [README](bedroom2_README.md) |
| **Bedroom 3** | [bedroom3.yaml](bedroom3.yaml) | 10 automations, 1 script, 1 sensor, 1 template block | [README](bedroom3_README.md) |
| **Front Garden** | [front_garden.yaml](front_garden.yaml) | 5 automations, 1 shell command | [README](front_garden_README.md) |
| **Utility** | [utility.yaml](utility.yaml) | 12 automations, 1 script, 5 sensors, 1 template block | [README](utility_README.md) |

## Package Notes

- Kitchen, living room, office, porch, stairs, bedroom, and conservatory now all have dedicated package folders.
- `utility.yaml` remains a single-file room package rather than a folder.
- Current counts are derived from YAML files and do not include entities created only through the Home Assistant UI or by integrations at runtime.

## Related Documentation

- [Integrations](../integrations/README.md) - Integration-specific configuration
- [Main Packages README](../README.md) - Overview of the packages architecture
- [Setup Statistics](../../setup_statistics.md) - Current package counts and analysis
