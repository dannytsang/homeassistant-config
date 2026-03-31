# /packages Folder

This directory contains Home Assistant configuration organized as [packages](https://www.home-assistant.io/docs/configuration/packages/#create-a-packages-folder). Packages allow related configuration (automations, sensors, scripts) to be grouped together in a single YAML file.

## Why Packages?

The main reason for using packages is to better manage configurations in a way that makes logical sense — grouping by room or integration rather than by entity type. This comes at the cost of not being able to edit some entities from the UI (Lovelace), but makes the configuration more maintainable and portable.

### Automation Naming Convention

Automations stored in packages use a caret (`^`) prefix to denote they cannot be edited from the UI. For example: `^Kitchen: Motion Detected`.

## Folder Structure

Configuration is split into three categories, in priority order:

1. **`rooms/`** - Highest priority. Settings based on physical rooms in the house.
2. **`integrations/`** - Integration-specific configuration. Self-contained per integration.
3. **Root folder** - Catch-all for files that don't fit the above categories.

### Priority Example

A new light in the lounge would go into `/packages/rooms/living_room/` rather than `/packages/integrations/` because room-based organization takes precedence.

---

## Rooms

Configuration organized by physical rooms in the house. Each room package contains automations, scenes, scripts, and sensors specific to that area.

| Room | Description | Documentation |
|------|-------------|---------------|
| `office/` | Office automation with motion lighting, blind control, computer presence | [README](rooms/office/README.md) |
| `kitchen/` | Kitchen with appliance monitoring, oven, dishwasher, smoke alarm | [README](rooms/kitchen/README.md) |
| `porch/` | Front door, motion lighting, lock status, NFC entry | [README](rooms/porch/README.md) |
| `stairs/` | Motion lighting with children's door integration, Magic Mirror | [README](rooms/stairs/README.md) |
| `living_room/` | RGB lighting, TV/media control, blind automation | [README](rooms/living_room/README.md) |
| `bedroom/` | Sleep As Android, AWTRIX, blind control | [README](rooms/bedroom/README.md) |
| `utility/` | Washing machine, fridge/freezer monitoring | [README](rooms/utility/README.md) |
| `conservatory/` | Airer, OctoPrint 3D printer, climate | [README](rooms/conservatory/README.md) |
| `bathroom.yaml` | Bathroom automation | - |
| `bedroom2.yaml` | Bedroom 2 | - |
| `bedroom3.yaml` | Bedroom 3 | - |
| `attic.yaml` | Attic | - |
| `front_garden.yaml` | Front garden | - |
| `back_garden.yaml` | Back garden | - |

---

## Integrations

Configuration organized by integration. Each integration package is self-contained — removing the integration only requires deleting its package file.

### Energy & Power

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| `energy/` | Core energy management, solar forecasting, battery control | [README](integrations/energy/README.md) |
| `energy/ecoflow.yaml` | EcoFlow power stations | [README](integrations/energy/README.md) |
| `energy/solar_assistant.yaml` | Solar inverter monitoring | [README](integrations/energy/solar_assistant_README.md) |
| `energy/zappi.yaml` | MyEnergi Zappi EV charger | - |
| `energy/eddi.yaml` | MyEnergi Eddi solar diverter | - |
| `energy/predbat.yaml` | Predbat battery optimization | - |
| `energy/solcast.yaml` | Solar forecasting | - |
| `energy/octopus_energy.yaml` | Octopus Agile tariff | - |

### Transport & Vehicles

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| `transport/tesla.yaml` | Tesla vehicle integration | [README](integrations/transport/README.md) |
| `transport/google_travel.yaml` | Google Travel time | - |

### Messaging & Notifications

| Integration | Description |
|-------------|-------------|
| `messaging/notifications.yaml` | Core notification system |
| `messaging/slack.yaml` | Slack integration |
| `messaging/discord.yaml` | Discord integration |
| `messaging/telegram.yaml` | Telegram integration |
| `messaging/home_assistant_mobile.yaml` | Mobile app notifications |

### Climate & HVAC

| Integration | Description |
|-------------|-------------|
| `hvac/hive.yaml` | Hive heating control |
| `hvac/hvac.yaml` | General HVAC automation |
| `hvac/eddi.yaml` | Eddi solar diverter |

### Other Integrations

| Integration | Description |
|-------------|-------------|
| `alarm.yaml` | House alarm system |
| `alexa.yaml` | Amazon Alexa integration |
| `chromecast.yaml` | Chromecast devices |
| `esphome.yaml` | ESPHome devices |
| `grocy.yaml` | Grocy inventory management |
| `lg.yaml` | LG appliances |
| `owntracks.yaml` | Location tracking |
| `paperless.yaml` | Paperless-ngx document management |
| `pihole.yaml` | Pi-hole DNS management |
| `smoke_alarm.yaml` | Smoke alarm integration |
| `spotify.yaml` | Spotify control |
| `supervisor.yaml` | Home Assistant Supervisor |
| `ups.yaml` | UPS monitoring |
| `water.yaml` | Leak detection |
| `zigbee.yaml` | Zigbee2MQTT configuration |
| `git.yaml` | Git integration |
| `calendar.yaml` | Calendar integration |
| `cleaning.yaml` | Cleaning schedules |

---

## Root Folder Files

Files that don't fit into the room or integration categories:

| File | Description |
|------|-------------|
| `tracker.yaml` | Device and person tracking |
| `homeassistant.yaml` | Core Home Assistant configuration |
| `recorder.yaml` | Database and history configuration |
| `logger.yaml` | Logging configuration |
| `rest.yaml` | REST command definitions |
| `shell.yaml` | Shell command definitions |
| `template.yaml` | Global template sensors |
| `command_line.yaml` | Command line sensors |
| `mqtt.yaml` | MQTT configuration |
| `notify.yaml` | Notification services |
| `group.yaml` | Group definitions |
| `zone.yaml` | Zone definitions |
| `timer.yaml` | Global timers |
| `counter.yaml` | Global counters |
| `input_*.yaml` | Input helpers (booleans, numbers, selects, etc.) |

---

## Adding New Packages

When adding new configuration:

1. **Room-based first** - If it's specific to a room, add it to that room's package
2. **Integration second** - If it's integration-specific, create an integration package
3. **Root last** - Only use root for truly global configuration

### Documentation

When creating significant new packages, consider adding a README.md in the same folder documenting:
- Overview of what the package does
- Key automations and their triggers
- Important sensors and their purposes
- Configuration options (input booleans, numbers, etc.)
- Entity reference
