# Home Assistant Setup Statistics & Analysis

Generated: 2026-06-27

## Overview

This Home Assistant configuration has **383 YAML-defined automations** in the repository: **381 in packages** and **2 deprecated UI automations** in `automations.yaml`. The package system is now the production source of truth, with room, integration, and root/global packages covering the current automations, scripts, scenes, sensors, helpers, MQTT entities, REST commands, shell commands, conversations, and intent scripts.

State counts are tracked separately in [statistics.md](statistics.md), because they come from the live Home Assistant state machine and include UI-created entities, integration-provided entities, disabled entities, and runtime-only entities that are not all represented in YAML.

---

## YAML Configuration Summary

| Metric | Count |
|--------|-------|
| Package YAML files | 71 |
| Package README files | 66 |
| Package automations | 381 |
| UI automations in `automations.yaml` | 2 deprecated water leak automations |
| Package scripts | 133 |
| UI scripts in `scripts.yaml` | 6 |
| Package scenes | 64 |
| UI scenes in `scenes.yaml` | 3 |
| Package sensors | 83 |
| Package template blocks | 46 |
| Package groups | 16 |
| Package MQTT entries | 122 |
| REST commands | 3 |
| Shell commands | 3 |
| Conversation blocks | 1 |
| Intent scripts | 13 |

### Architecture Quality

**Excellent** - production automations are organized in packages. The only automations left in `automations.yaml` are two deprecated water leak automations that point to the replacement logic in `packages/integrations/water.yaml`.

---

## Automation Distribution

| Area | Automations | Notes |
|------|-------------|-------|
| Room packages | 212 | Physical-room behavior, lighting, blinds, appliance monitoring, presence, media, and local alerts |
| Integration packages | 130 | Energy, HVAC, messaging, safety, transport, infrastructure, weather, and service integrations |
| Root/global packages | 39 | Home modes, time routines, tracker/presence, HA lifecycle, shared safety helpers |
| UI legacy file | 2 | Deprecated water leak automations retained for reference |
| **Total YAML automations** | **383** | 381 package automations plus 2 UI automations |

---

## Room Package Breakdown

| Room/package | Automations | Other YAML features |
|--------------|-------------|---------------------|
| `rooms/attic.yaml` | 3 | Attic hatch lighting |
| `rooms/back_garden.yaml` | 3 | Garden and shed automation |
| `rooms/bathroom.yaml` | 9 | 1 script, 1 sensor |
| `rooms/bedroom/bedroom.yaml` | 24 | 5 scenes, 8 scripts, 5 sensors, 1 template block |
| `rooms/bedroom/awtrix_light.yaml` | 0 | 1 AWTRIX script |
| `rooms/bedroom/sleep_as_android.yaml` | 8 | 1 template block |
| `rooms/bedroom2.yaml` | 15 | 2 scenes, 1 script, 1 sensor, 1 template block |
| `rooms/bedroom3.yaml` | 10 | 1 script, 1 sensor, 1 template block |
| `rooms/conservatory/airer.yaml` | 2 | 1 script |
| `rooms/conservatory/conservatory.yaml` | 9 | 2 scenes, 1 script, 1 sensor |
| `rooms/conservatory/octoprint.yaml` | 6 | 3 scenes, 3 scripts |
| `rooms/front_garden.yaml` | 5 | 1 shell command |
| `rooms/kitchen/kitchen.yaml` | 27 | 16 scenes, 6 scripts, 13 sensors, 6 template blocks |
| `rooms/kitchen/meater.yaml` | 2 | MEATER cook monitoring |
| `rooms/living_room/living_room.yaml` | 23 | 12 scenes, 5 scripts, 11 sensors, 1 template block |
| `rooms/office/office.yaml` | 27 | 8 scenes, 4 scripts, 9 sensors |
| `rooms/office/steam.yaml` | 2 | Steam-related office automation |
| `rooms/porch/porch.yaml` | 12 | 6 scenes, 5 scripts, 1 template block |
| `rooms/stairs/stairs.yaml` | 14 | 9 scenes |
| `rooms/utility.yaml` | 11 | 1 script, 5 sensors, 1 template block |

---

## Integration Package Breakdown

| Integration/package | Automations | Other YAML features |
|---------------------|-------------|---------------------|
| `integrations/alarm.yaml` | 8 | 4 scripts |
| `integrations/alexa.yaml` | 0 | 2 scripts |
| `integrations/bins.yaml` | 2 | 5 sensors, 1 template block |
| `integrations/calendar.yaml` | 3 | 2 scripts |
| `integrations/chromecast.yaml` | 2 | 1 script |
| `integrations/cleaning.yaml` | 3 | 1 REST command |
| `integrations/energy/ecoflow.yaml` | 11 | 10 scripts, 4 template blocks |
| `integrations/energy/energy.yaml` | 14 | 4 groups, 9 scripts, 4 template blocks |
| `integrations/energy/energy_conversations.yaml` | 0 | 1 conversation block, 13 intent scripts |
| `integrations/energy/octopus_energy.yaml` | 3 | 1 script |
| `integrations/energy/predbat.yaml` | 2 | Battery optimization automations |
| `integrations/energy/solar_assistant.yaml` | 1 | 6 scripts, 12 sensors, 8 template blocks |
| `integrations/energy/solcast.yaml` | 1 | 1 script |
| `integrations/energy/zappi.yaml` | 6 | 1 script |
| `integrations/esphome.yaml` | 2 | ESPHome update and recovery automation |
| `integrations/git.yaml` | 1 | GitHub Actions deployment hook |
| `integrations/grocy.yaml` | 0 | 2 REST commands, 2 sensors |
| `integrations/hvac/eddi.yaml` | 4 | 4 scripts, 1 input number, 1 utility meter |
| `integrations/hvac/hive.yaml` | 10 | 1 schedule, 8 scripts, 12 sensors |
| `integrations/hvac/hvac.yaml` | 2 | 4 sensors, 7 template blocks |
| `integrations/lg.yaml` | 4 | LG appliance and TV monitoring |
| `integrations/messaging/callmebot.yaml` | 0 | 2 notify services, 1 script |
| `integrations/messaging/discord.yaml` | 0 | 3 scripts |
| `integrations/messaging/home_assistant_mobile.yaml` | 0 | 4 scripts |
| `integrations/messaging/message_callback.yaml` | 1 | Action callback handling |
| `integrations/messaging/notifications.yaml` | 0 | 10 shared notification scripts |
| `integrations/messaging/slack.yaml` | 1 | 3 scripts |
| `integrations/messaging/telegram.yaml` | 3 | 2 scripts |
| `integrations/n8n.yaml` | 0 | 1 shell command |
| `integrations/nuki.yaml` | 3 | 2 scripts |
| `integrations/owntracks.yaml` | 3 | OwnTracks location publishing |
| `integrations/paperless.yaml` | 1 | 1 sensor |
| `integrations/sftpgo.yaml` | 0 | 1 shell command |
| `integrations/smoke_alarm.yaml` | 6 | Nest Protect safety handling |
| `integrations/spotify.yaml` | 1 | Playback logging |
| `integrations/supervisor.yaml` | 13 | 1 script |
| `integrations/transport/google_travel.yaml` | 0 | 1 script, 2 template blocks |
| `integrations/transport/tesla.yaml` | 2 | 122 MQTT entries, 1 script, 2 template blocks |
| `integrations/unifi_protect.yaml` | 4 | Camera event processing |
| `integrations/ups.yaml` | 4 | 1 template block |
| `integrations/water.yaml` | 2 | 1 template block |
| `integrations/weather/carbon_intensity_uk.yaml` | 0 | 1 REST sensor/config block |
| `integrations/weather/ecowitt.yaml` | 1 | Ecowitt weather station automation |
| `integrations/weather/weather.yaml` | 5 | 1 REST sensor/config block |
| `integrations/zigbee.yaml` | 1 | Zigbee2MQTT monitoring |

---

## Root/Global Package Breakdown

| Package | Automations | Other YAML features |
|---------|-------------|---------------------|
| `home.yaml` | 11 | 1 scene, 7 scripts, 1 template block |
| `home_assistant.yaml` | 6 | 2 scripts, 1 template block |
| `shared_helpers.yaml` | 0 | 1 helper script, 1 template block |
| `smoke_alarms.yaml` | 1 | 1 script |
| `time.yaml` | 5 | 1 script |
| `tracker.yaml` | 16 | 12 groups, 6 scripts |

---

## Notable Current Features

1. **Energy management remains the flagship system**
   - EcoFlow, Solar Assistant, Octopus Energy, Predbat, Solcast, Zappi, and core energy packages work together for battery, solar, EV, tariff, and grid-aware behavior.

2. **Room packages are now broadly complete**
   - Living room, kitchen, porch, stairs, bedroom, office, conservatory, utility, front/back garden, bathroom, attic, and children bedroom packages all exist.

3. **Notification routing is script-centric**
   - The messaging packages mostly expose reusable scripts and callback handling rather than large numbers of channel-specific automations.

4. **Transport and weather are dedicated package groups**
   - Tesla/TeslaMate MQTT configuration, Google Travel helpers, weather forecasts, carbon intensity, and Ecowitt station logic are now documented package areas.

5. **Legacy UI automations are effectively retired**
   - `automations.yaml` contains only two deprecated water leak automations, superseded by `packages/integrations/water.yaml`.

---

## Documentation Currency Notes

- `packages/README.md`, `packages/rooms/README.md`, and `packages/integrations/README.md` should be treated as the navigation entry points for package documentation.
- Detailed package READMEs remain useful for behavior and entity references, but count totals should be regenerated from YAML when accuracy matters.
- Live entity totals in `statistics.md` are separate from YAML package counts and should be refreshed from Developer Tools using the template included in that file.
