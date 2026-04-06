[<- Back to README](../../README.md)

# /packages Folder

This directory contains Home Assistant configuration organized as [packages](https://www.home-assistant.io/docs/configuration/packages/#create-a-packages-folder). Packages allow related configuration (automations, sensors, scripts) to be grouped together in a single YAML file.

## Why Packages?

The main reason for using packages is to better manage configurations in a way that makes logical sense — grouping by room or integration rather than by entity type. This comes at the cost of not being able to edit some entities from the UI (Lovelace), but makes the configuration more maintainable and portable.

### Automation Naming Convention

Automations stored in packages use a caret (`^`) prefix to denote they cannot be edited from the UI. For example: `^Kitchen: Motion Detected`.

## Documentation Index

| Category | Document | Description |
|----------|----------|-------------|
| **Rooms Overview** | [rooms/README.md](rooms/README.md) | All room packages with quick links |
| **Integrations Overview** | [integrations/README.md](integrations/README.md) | All integration packages |
| **This File** | [packages/README.md](README.md) | Package architecture guide |

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

See [Rooms Overview](rooms/README.md) for detailed room documentation.

| Room | Description | Documentation | Setup Guide |
|------|-------------|---------------|-------------|
| `office/` | Office automation with motion lighting, blind control, computer presence | [README](rooms/office/README.md) | [SETUP](rooms/office/OFFICE-SETUP.md) |
| `kitchen/` | Kitchen with appliance monitoring, oven, dishwasher, smoke alarm | [README](rooms/kitchen/README.md) | [SETUP](rooms/kitchen/KITCHEN-SETUP.md) |
| `porch/` | Front door, motion lighting, lock status, NFC entry | [README](rooms/porch/README.md) | [SETUP](rooms/porch/PORCH-SETUP.md) |
| `stairs/` | Motion lighting with children's door integration, Magic Mirror | [README](rooms/stairs/README.md) | [SETUP](rooms/stairs/STAIRS-SETUP.md) |
| `living_room/` | RGB lighting, TV/media control, blind automation | [README](rooms/living_room/README.md) | [SETUP](rooms/living_room/LIVING-ROOM-SETUP.md) |
| `bedroom/` | Sleep As Android, AWTRIX, blind control | [README](rooms/bedroom/README.md) | [SETUP](rooms/bedroom/BEDROOM-SETUP.md) |
| `utility/` | Washing machine, fridge/freezer monitoring | [README](rooms/utility_README.md) | - |
| `conservatory/` | Airer, OctoPrint 3D printer, climate | [README](rooms/conservatory/README.md) | - |
| `bathroom.yaml` | Bathroom automation | [README](rooms/bathroom_README.md) | - |
| `bedroom2.yaml` | Bedroom 2 (Leo's room) | [README](rooms/bedroom2_README.md) | - |
| `bedroom3.yaml` | Bedroom 3 (Ashlee's room) | [README](rooms/bedroom3_README.md) | - |
| `attic.yaml` | Attic | [README](rooms/attic_README.md) | - |
| `front_garden.yaml` | Front garden | [README](rooms/front_garden_README.md) | - |
| `back_garden.yaml` | Back garden and shed | [README](rooms/back_garden_README.md) | - |

---

## Integrations

Configuration organized by integration. Each integration package is self-contained — removing the integration only requires deleting its package file.

See [Integrations Overview](integrations/README.md) for detailed integration documentation.

### Energy & Power

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| `energy/` | Core energy management, solar forecasting, battery control | [README](integrations/energy/README.md) |
| `energy/ecoflow.yaml` | EcoFlow power stations | [README](integrations/energy/README.md) |
| `energy/solar_assistant.yaml` | Solar inverter monitoring | [README](integrations/energy/solar_assistant_README.md) |
| `energy/zappi.yaml` | MyEnergi Zappi EV charger | [README](integrations/energy/zappi/README.md) |
| `energy/eddi.yaml` | MyEnergi Eddi solar diverter | [README](integrations/hvac/README.md) |
| `energy/predbat.yaml` | Predbat battery optimization | [README](integrations/energy/predbat/README.md) |
| `energy/solcast.yaml` | Solar forecasting | [README](integrations/energy/solcast/README.md) |
| `energy/octopus_energy.yaml` | Octopus Agile tariff | [README](integrations/energy/octopus_energy/README.md) |

### Transport & Vehicles

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| `transport/tesla.yaml` | Tesla vehicle integration (TeslaMate) | [README](integrations/transport/README.md) |
| `transport/google_travel.yaml` | Google Travel time | [README](integrations/transport/google_travel/README.md) |

### Messaging & Notifications

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| `messaging/notifications.yaml` | Core notification system | [README](integrations/messaging/README.md) |
| `messaging/slack.yaml` | Slack integration | [README](integrations/messaging/README.md) |
| `messaging/discord.yaml` | Discord integration | [README](integrations/messaging/README.md) |
| `messaging/telegram.yaml` | Telegram integration | [README](integrations/messaging/README.md) |
| `messaging/home_assistant_mobile.yaml` | Mobile app notifications | [README](integrations/messaging/README.md) |
| `messaging/callmebot.yaml` | WhatsApp via CallMeBot | [README](integrations/messaging/README.md) |

### Climate & HVAC

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| `hvac/hive.yaml` | Hive heating control | [README](integrations/hvac/README.md) |
| `hvac/hvac.yaml` | General HVAC automation | [README](integrations/hvac/README.md) |
| `hvac/eddi.yaml` | Eddi solar diverter | [README](integrations/hvac/README.md) |

### Other Integrations

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| `alarm.yaml` | House alarm system | [README](integrations/alarm_README.md) |
| `alexa.yaml` | Amazon Echo TTS announcements | [README](integrations/alexa/README.md) |
| `bins.yaml` | Bin collection tracking | [README](integrations/bins/README.md) |
| `calendar.yaml` | Google Calendar event notifications with travel time | [README](integrations/calendar/README.md) |
| `chromecast.yaml` | Chromecast / Magic Mirror / Google TV | [README](integrations/chromecast/README.md) |
| `cleaning.yaml` | Deebot robot vacuum | [README](integrations/cleaning/README.md) |
| `esphome.yaml` | ESPHome firmware updates and recovery | [README](integrations/esphome/README.md) |
| `git.yaml` | GitHub CI/CD config auto-deploy | [README](integrations/git/README.md) |
| `grocy.yaml` | Grocy inventory management | [README](integrations/grocy/README.md) |
| `lg.yaml` | LG WebOS TV monitoring | [README](integrations/lg/README.md) |
| `n8n.yaml` | N8N workflow integration | [README](integrations/n8n_README.md) |
| `nuki.yaml` | Nuki smart door lock | [README](integrations/nuki/README.md) |
| `owntracks.yaml` | OwnTracks location publishing | [README](integrations/owntracks/README.md) |
| `paperless.yaml` | Paperless-NGX document notifications | [README](integrations/paperless/README.md) |
| `pihole.yaml` | Pi-hole DNS ad filtering | [README](integrations/pihole_README.md) |
| `sftpgo.yaml` | SFTPGo file server commands | [README](integrations/sftpgo/README.md) |
| `smoke_alarm.yaml` | Nest Protect smoke / CO detection | [README](integrations/smoke_alarm_README.md) |
| `spotify.yaml` | Spotify playback logging | [README](integrations/spotify/README.md) |
| `supervisor.yaml` | Add-on lifecycle and auto-disable | [README](integrations/supervisor/README.md) |
| `unifi_protect.yaml` | UniFi Protect camera events | [README](integrations/unifi_protect/README.md) |
| `ups.yaml` | UPS monitoring via NUT | [README](integrations/ups/README.md) |
| `water.yaml` | Leak detection and alerts | [README](integrations/water/README.md) |
| `zigbee.yaml` | Zigbee2MQTT coordinator monitoring | [README](integrations/zigbee/README.md) |
| `weather/` | Forecasts, warnings, carbon intensity, Ecowitt | [README](integrations/weather/README.md) |

---

## Root Folder Files

Files that don't fit into the room or integration categories:

| File | Description | Documentation |
|------|-------------|---------------|
| `home.yaml` | Home modes, global device control, lock/alarm scripts | [README](home_README.md) |
| `tracker.yaml` | Presence detection, arrival/departure, music follow | [README](tracker_README.md) |
| `home_assistant.yaml` | HA lifecycle, backups, upgrades, purge | [README](home_assistant_README.md) |
| `time.yaml` | Scheduled automations, bedtime announcements | [README](time_README.md) |
| `smoke_alarms.yaml` | Smoke alarm coordination, camera snapshots | [README](smoke_alarms_README.md) |
| `shared_helpers.yaml` | Shared template sensors (motion+dark helpers) | [README](shared_helpers_README.md) |
| `recorder.yaml` | Database and history configuration | - |
| `logger.yaml` | Logging configuration | - |
| `rest.yaml` | REST command definitions | - |
| `shell.yaml` | Shell command definitions | - |
| `template.yaml` | Global template sensors | - |
| `command_line.yaml` | Command line sensors | - |
| `mqtt.yaml` | MQTT configuration | - |
| `notify.yaml` | Notification services | - |
| `group.yaml` | Group definitions | - |
| `zone.yaml` | Zone definitions | - |
| `timer.yaml` | Global timers | - |
| `counter.yaml` | Global counters | - |
| `input_*.yaml` | Input helpers (booleans, numbers, selects, etc.) | - |

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [Rooms Overview](rooms/README.md) | Detailed documentation for all room packages |
| [Integrations Overview](integrations/README.md) | Detailed documentation for all integration packages |

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
- Links to related setup guides or external documentation
