[<- Back to Packages README](../README.md) · [Main README](../../README.md)

# Integrations 🖧

Integration-specific configuration organized by functional domain. Each package is self-contained — removing an integration only requires deleting its package file.

## Integration Categories

| Category | Description | Documentation | Last Updated |
|----------|-------------|---------------|--------------|
| **Energy** | Solar, battery, grid monitoring, EV charging, Octopus Agile | [README](energy/README.md) | 2026-04-01 |
| **HVAC** | Heating, ventilation, air conditioning (Hive, Eddi) | [README](hvac/README.md) | 2026-04-01 |
| **Messaging** | Notifications (Slack, Discord, Telegram, Mobile) | [README](messaging/README.md) | 2026-04-01 |
| **Transport** | Tesla vehicles (TeslaMate integration) | [README](transport/README.md) | 2026-04-01 |

## Detailed Energy Documentation

| Topic | Description | Document | Last Updated |
|-------|-------------|----------|--------------|
| **Energy Core** | Solar forecasting, battery management, grid monitoring | [README](energy/README.md) | 2026-04-01 |
| **Octopus Energy** | Agile tariff integration | [README](energy/octopus_energy/README.md) | 2026-04-01 |
| **Predbat** | Battery optimization | [README](energy/predbat/README.md) | 2026-04-01 |
| **Solcast** | Solar forecasting service | [README](energy/solcast/README.md) | 2026-04-01 |
| **Solar Assistant** | Growatt inverter monitoring | [README](energy/solar_assistant_README.md) | 2026-04-01 |
| **Zappi** | MyEnergi EV charger | [README](energy/zappi/README.md) | 2026-04-01 |

## Transport Sub-Integrations

| Topic | Description | Document | Last Updated |
|-------|-------------|----------|--------------|
| **TeslaMate** | Tesla vehicle telemetry | [README](transport/README.md) | 2026-04-01 |
| **Google Travel** | Travel time estimates | [README](transport/google_travel/README.md) | 2026-04-01 |

## Device & Media Integrations

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| **Alexa** | Amazon Echo TTS announcements | [README](alexa/README.md) |
| **Chromecast** | Magic Mirror casting and Google TV monitoring | [README](chromecast/README.md) |
| **LG** | LG WebOS TV monitoring and long-use alerts | [README](lg/README.md) |
| **Spotify** | Playback logging | [README](spotify/README.md) |

## Household & Appliances

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| **Bins** | Bin collection distance tracking and notifications | [README](bins/README.md) |
| **Cleaning** | Deebot robot vacuum monitoring | [README](cleaning/README.md) |
| **Grocy** | Inventory management (tablets, salt) | [README](grocy/README.md) |
| **Paperless** | Document management notifications | [README](paperless/README.md) |

## Security & Safety

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| **Alarm** | House alarm system | [README](alarm/README.md) |
| **Nuki** | Smart door lock control and monitoring | [README](nuki/README.md) |
| **Smoke Alarm** | Nest Protect smoke and CO detection | [README](smoke_alarm/README.md) |
| **UniFi Protect** | Camera event processing (vehicles, faces) | [README](unifi_protect/README.md) |
| **Water** | Leak detection and critical alerts | [README](water/README.md) |

## Infrastructure & Monitoring

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| **ESPHome** | ESP device firmware updates and recovery | [README](esphome/README.md) |
| **OwnTracks** | Location publishing to MQTT | [README](owntracks/README.md) |
| **Pi-hole** | DNS ad filtering across 3 instances | [README](pihole/README.md) |
| **SFTPGo** | File server shell commands | [README](sftpgo/README.md) |
| **Supervisor** | Add-on lifecycle and auto-disable | [README](supervisor/README.md) |
| **UPS** | Uninterruptible power supply monitoring | [README](ups/README.md) |
| **Zigbee** | Zigbee2MQTT coordinator availability | [README](zigbee/README.md) |

## Calendar & Notifications

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| **Calendar** | Google Calendar event notifications with travel time | [README](calendar/README.md) |

## CI/CD & Automation

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| **Git** | GitHub Actions webhook → config auto-deploy | [README](git/README.md) |
| **N8N** | N8N workflow integration | [README](n8n/README.md) |

## Weather

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| **Weather** | Forecasts, warnings, storm detection, carbon intensity, Ecowitt station | [README](weather/README.md) |

## Related Documentation

- [Rooms](../rooms/README.md) - Room-specific configuration
- [Main Packages README](../README.md) - Overview of the packages architecture
