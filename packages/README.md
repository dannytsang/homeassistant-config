[<- Back to README](../README.md)

# /packages Folder

Last reviewed against YAML: 2026-07-19

This directory contains Home Assistant configuration organized as [packages](https://www.home-assistant.io/docs/configuration/packages/#create-a-packages-folder). Packages group related automations, scripts, scenes, sensors, helpers, commands, and integration configuration by room or functional area.

## Current Inventory

| Metric | Count |
|--------|-------|
| Package YAML files | 71 |
| Package README files | 66 |
| Package automations | 383 |
| Package scripts | 135 |
| Package scenes | 64 |
| Package sensors | 83 |
| Package template blocks | 46 |
| Package groups | 16 |
| Package MQTT entries | 122 |
| REST commands | 3 |
| Shell commands | 3 |
| Conversation blocks | 1 |
| Intent scripts | 13 |

## Why Packages?

Packages keep related configuration together by room or integration rather than by entity type. This makes the configuration easier to review, move, and remove, at the cost of some entities not being editable through the Home Assistant UI.

### Automation Naming Convention

Automations stored in packages use a caret (`^`) prefix to denote they cannot be edited from the UI. For example: `^Kitchen: Motion Detected`.

## Documentation Index

| Category | Document | Description |
|----------|----------|-------------|
| **Rooms Overview** | [rooms/README.md](rooms/README.md) | All room packages with quick links and package counts |
| **Integrations Overview** | [integrations/README.md](integrations/README.md) | All integration packages with package counts |
| **Setup Statistics** | [../setup_statistics.md](../setup_statistics.md) | Current package inventory and automation analysis |
| **This File** | [packages/README.md](README.md) | Package architecture guide |

## Folder Structure

Configuration is split into three categories, in priority order:

1. **`rooms/`** - Highest priority. Settings based on physical rooms in the house.
2. **`integrations/`** - Integration-specific configuration. Self-contained per integration.
3. **Root folder** - Catch-all for files that do not fit the above categories.

### Priority Example

A new light in the lounge would go into `/packages/rooms/living_room/` rather than `/packages/integrations/` because room-based organization takes precedence.

---

## Rooms

Configuration organized by physical rooms in the house. Each room package contains automations, scenes, scripts, sensors, and templates specific to that area.

See [Rooms Overview](rooms/README.md) for detailed room documentation.

| Source YAML | Description | Documentation | Setup Guide |
|-------------|-------------|---------------|-------------|
| [office.yaml](rooms/office/office.yaml), [steam.yaml](rooms/office/steam.yaml) | Office automation with motion lighting, blind control, computer presence, Steam monitoring | [README](rooms/office/README.md) | [SETUP](rooms/office/OFFICE-SETUP.md) |
| [kitchen.yaml](rooms/kitchen/kitchen.yaml), [meater.yaml](rooms/kitchen/meater.yaml) | Kitchen with appliance monitoring, oven, dishwasher, smoke alarm, MEATER monitoring | [README](rooms/kitchen/README.md) | [SETUP](rooms/kitchen/KITCHEN-SETUP.md) |
| [porch.yaml](rooms/porch/porch.yaml) | Front door, motion lighting, lock status, NFC entry | [README](rooms/porch/README.md) | [SETUP](rooms/porch/PORCH-SETUP.md) |
| [stairs.yaml](rooms/stairs/stairs.yaml) | Motion lighting with children's door integration, Magic Mirror | [README](rooms/stairs/README.md) | [SETUP](rooms/stairs/STAIRS-SETUP.md) |
| [living_room.yaml](rooms/living_room/living_room.yaml) | RGB lighting, TV/media control, blind automation | [README](rooms/living_room/README.md) | [SETUP](rooms/living_room/LIVING-ROOM-SETUP.md) |
| [bedroom.yaml](rooms/bedroom/bedroom.yaml), [sleep_as_android.yaml](rooms/bedroom/sleep_as_android.yaml), [awtrix_light.yaml](rooms/bedroom/awtrix_light.yaml) | Sleep As Android, AWTRIX, blind control | [README](rooms/bedroom/README.md) | [SETUP](rooms/bedroom/BEDROOM-SETUP.md) |
| [utility.yaml](rooms/utility.yaml) | Washing machine, fridge/freezer monitoring | [README](rooms/utility_README.md) | - |
| [conservatory.yaml](rooms/conservatory/conservatory.yaml), [airer.yaml](rooms/conservatory/airer.yaml), [octoprint.yaml](rooms/conservatory/octoprint.yaml) | Airer, OctoPrint 3D printer, climate | [README](rooms/conservatory/README.md) | - |
| [bathroom.yaml](rooms/bathroom.yaml) | Bathroom automation | [README](rooms/bathroom_README.md) | - |
| [bedroom2.yaml](rooms/bedroom2.yaml) | Bedroom 2 (Leo's room) | [README](rooms/bedroom2_README.md) | - |
| [bedroom3.yaml](rooms/bedroom3.yaml) | Bedroom 3 (Ashlee's room) | [README](rooms/bedroom3_README.md) | - |
| [attic.yaml](rooms/attic.yaml) | Attic | [README](rooms/attic_README.md) | - |
| [front_garden.yaml](rooms/front_garden.yaml) | Front garden | [README](rooms/front_garden_README.md) | - |
| [back_garden.yaml](rooms/back_garden.yaml) | Back garden and shed | [README](rooms/back_garden_README.md) | - |

---

## Integrations

Configuration organized by integration. Each integration package is self-contained; removing the integration normally only requires deleting its package file and any related UI integration setup.

See [Integrations Overview](integrations/README.md) for detailed integration documentation.

### Energy & Power

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| [energy.yaml](integrations/energy/energy.yaml) | Core energy management, groups, grid/battery scripts | [README](integrations/energy/energy_README.md) |
| [ecoflow.yaml](integrations/energy/ecoflow.yaml) | EcoFlow power stations | [README](integrations/energy/ecoflow_README.md) |
| [solar_assistant.yaml](integrations/energy/solar_assistant.yaml) | Solar inverter monitoring | [README](integrations/energy/solar_assistant_README.md) |
| [zappi.yaml](integrations/energy/zappi.yaml) | MyEnergi Zappi EV charger | [README](integrations/energy/zappi_README.md) |
| [predbat.yaml](integrations/energy/predbat.yaml) | Predbat battery optimization | [README](integrations/energy/predbat_README.md) |
| [solcast.yaml](integrations/energy/solcast.yaml) | Solar forecasting | [README](integrations/energy/solcast_README.md) |
| [octopus_energy.yaml](integrations/energy/octopus_energy.yaml) | Octopus Energy tariff and dispatching | [README](integrations/energy/octopus_energy_README.md) |
| [energy_conversations.yaml](integrations/energy/energy_conversations.yaml) | Energy conversation intents | [README](integrations/energy/README.md) |

### Transport & Vehicles

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| [tesla.yaml](integrations/transport/tesla.yaml) | Tesla vehicle integration (TeslaMate MQTT) | [README](integrations/transport/tesla_README.md) |
| [google_travel.yaml](integrations/transport/google_travel.yaml) | Google Travel time helpers | [README](integrations/transport/google_travel_README.md) |

### Messaging & Notifications

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| [notifications.yaml](integrations/messaging/notifications.yaml) | Core notification scripts | [README](integrations/messaging/README.md) |
| [slack.yaml](integrations/messaging/slack.yaml) | Slack integration | [README](integrations/messaging/README.md) |
| [discord.yaml](integrations/messaging/discord.yaml) | Discord integration | [README](integrations/messaging/README.md) |
| [telegram.yaml](integrations/messaging/telegram.yaml) | Telegram integration | [README](integrations/messaging/README.md) |
| [home_assistant_mobile.yaml](integrations/messaging/home_assistant_mobile.yaml) | Mobile app notifications | [README](integrations/messaging/README.md) |
| [callmebot.yaml](integrations/messaging/callmebot.yaml) | WhatsApp via CallMeBot | [README](integrations/messaging/README.md) |
| [message_callback.yaml](integrations/messaging/message_callback.yaml) | Actionable notification callback handling | [README](integrations/messaging/README.md) |

### Climate & HVAC

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| [hive.yaml](integrations/hvac/hive.yaml) | Hive heating control | [README](integrations/hvac/hive_README.md) |
| [hvac.yaml](integrations/hvac/hvac.yaml) | General HVAC automation and templates | [README](integrations/hvac/hvac_README.md) |
| [eddi.yaml](integrations/hvac/eddi.yaml) | MyEnergi Eddi solar diverter | [README](integrations/hvac/eddi_README.md) |

### Other Integrations

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| [alarm.yaml](integrations/alarm.yaml) | House alarm system | [README](integrations/alarm_README.md) |
| [alexa.yaml](integrations/alexa.yaml) | Amazon Echo TTS announcements | [README](integrations/alexa_README.md) |
| [bins.yaml](integrations/bins.yaml) | Bin collection tracking | [README](integrations/bins_README.md) |
| [calendar.yaml](integrations/calendar.yaml) | Google Calendar event notifications with travel time | [README](integrations/calendar_README.md) |
| [chromecast.yaml](integrations/chromecast.yaml) | Chromecast / Magic Mirror / Google TV | [README](integrations/chromecast_README.md) |
| [cleaning.yaml](integrations/cleaning.yaml) | Deebot robot vacuum | [README](integrations/cleaning_README.md) |
| [esphome.yaml](integrations/esphome.yaml) | ESPHome firmware updates and recovery | [README](integrations/esphome_README.md) |
| [git.yaml](integrations/git.yaml) | GitHub CI/CD config auto-deploy | [README](integrations/git_README.md) |
| [grocy.yaml](integrations/grocy.yaml) | Grocy inventory management | [README](integrations/grocy_README.md) |
| [lg.yaml](integrations/lg.yaml) | LG WebOS TV monitoring | [README](integrations/lg_README.md) |
| [n8n.yaml](integrations/n8n.yaml) | N8N workflow integration | [README](integrations/n8n_README.md) |
| [nuki.yaml](integrations/nuki.yaml) | Nuki smart door lock | [README](integrations/nuki_README.md) |
| [owntracks.yaml](integrations/owntracks.yaml) | OwnTracks location publishing | [README](integrations/owntracks_README.md) |
| [paperless.yaml](integrations/paperless.yaml) | Paperless-NGX document notifications | [README](integrations/paperless_README.md) |
| [sftpgo.yaml](integrations/sftpgo.yaml) | SFTPGo file server commands | [README](integrations/sftpgo_README.md) |
| [smoke_alarm.yaml](integrations/smoke_alarm.yaml) | Nest Protect smoke / CO detection | [README](integrations/smoke_alarm_README.md) |
| [spotify.yaml](integrations/spotify.yaml) | Spotify playback logging | [README](integrations/spotify_README.md) |
| [supervisor.yaml](integrations/supervisor.yaml) | Add-on lifecycle and auto-disable | [README](integrations/supervisor_README.md) |
| [unifi_protect.yaml](integrations/unifi_protect.yaml) | UniFi Protect camera events | [README](integrations/unifi_protect_README.md) |
| [ups.yaml](integrations/ups.yaml) | UPS monitoring via NUT | [README](integrations/ups_README.md) |
| [water.yaml](integrations/water.yaml) | Leak detection and alerts | [README](integrations/water_README.md) |
| [zigbee.yaml](integrations/zigbee.yaml) | Zigbee2MQTT coordinator monitoring | [README](integrations/zigbee_README.md) |
| [weather.yaml](integrations/weather/weather.yaml), [carbon_intensity_uk.yaml](integrations/weather/carbon_intensity_uk.yaml), [ecowitt.yaml](integrations/weather/ecowitt.yaml) | Forecasts, warnings, carbon intensity, Ecowitt | [README](integrations/weather/README.md) |

---

## Root Folder Files

Files that do not fit into the room or integration categories:

| File | Description | Documentation |
|------|-------------|---------------|
| [home.yaml](home.yaml) | Home modes, global device control, lock/alarm scripts | [README](home_README.md) |
| [tracker.yaml](tracker.yaml) | Presence detection, arrival/departure, music follow | [README](tracker_README.md) |
| [home_assistant.yaml](home_assistant.yaml) | HA lifecycle, backups, upgrades, purge | [README](home_assistant_README.md) |
| [time.yaml](time.yaml) | Scheduled automations, bedtime announcements | [README](time_README.md) |
| [smoke_alarms.yaml](smoke_alarms.yaml) | Smoke alarm coordination, camera snapshots | [README](smoke_alarms_README.md) |
| [shared_helpers.yaml](shared_helpers.yaml) | Shared logging and motion/dark helpers | [README](shared_helpers_README.md) |

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [Rooms Overview](rooms/README.md) | Detailed documentation for all room packages |
| [Integrations Overview](integrations/README.md) | Detailed documentation for all integration packages |
| [Setup Statistics](../setup_statistics.md) | Current counts and package inventory |

## Adding New Packages

When adding new configuration:

1. **Room-based first** - If it is specific to a room, add it to that room's package.
2. **Integration second** - If it is integration-specific, create an integration package.
3. **Root last** - Only use root for truly global configuration.

### Documentation

When creating significant new packages, add or update a README in the same folder documenting:
- Overview of what the package does
- Key automations and their triggers
- Important sensors and their purposes
- Configuration options such as input booleans, numbers, and selects
- Entity reference
- Links to related setup guides or external documentation
