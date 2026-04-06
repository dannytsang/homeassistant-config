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
| **Octopus Energy** | Agile tariff integration | [README](energy/octopus_energy_README.md) | 2026-04-01 |
| **Predbat** | Battery optimization | [README](energy/predbat_README.md) | 2026-04-01 |
| **Solcast** | Solar forecasting service | [README](energy/solcast_README.md) | 2026-04-01 |
| **Solar Assistant** | Growatt inverter monitoring | [README](energy/solar_assistant_README.md) | 2026-04-01 |
| **Zappi** | MyEnergi EV charger | [README](energy/zappi_README.md) | 2026-04-01 |

## Transport Sub-Integrations

| Topic | Description | Document | Last Updated |
|-------|-------------|----------|--------------|
| **TeslaMate** | Tesla vehicle telemetry | [README](transport/README.md) | 2026-04-01 |
| **Google Travel** | Travel time estimates | [README](transport/google_travel_README.md) | 2026-04-01 |

## Device & Media Integrations

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| **Alexa** | Amazon Echo TTS announcements | [README](alexa_README.md) |
| **Chromecast** | Magic Mirror casting and Google TV monitoring | [README](chromecast_README.md) |
| **LG** | LG WebOS TV monitoring and long-use alerts | [README](lg_README.md) |
| **Spotify** | Playback logging | [README](spotify_README.md) |

## Household & Appliances

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| **Bins** | Bin collection distance tracking and notifications | [README](bins_README.md) |
| **Cleaning** | Deebot robot vacuum monitoring | [README](cleaning_README.md) |
| **Grocy** | Inventory management (tablets, salt) | [README](grocy_README.md) |
| **Paperless** | Document management notifications | [README](paperless_README.md) |

## Security & Safety

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| **Alarm** | House alarm system | [README](alarm_README.md) |
| **Nuki** | Smart door lock control and monitoring | [README](nuki_README.md) |
| **Smoke Alarm** | Nest Protect smoke and CO detection | [README](smoke_alarm_README.md) |
| **UniFi Protect** | Camera event processing (vehicles, faces) | [README](unifi_protect_README.md) |
| **Water** | Leak detection and critical alerts | [README](water_README.md) |

## Infrastructure & Monitoring

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| **ESPHome** | ESP device firmware updates and recovery | [README](esphome_README.md) |
| **OwnTracks** | Location publishing to MQTT | [README](owntracks_README.md) |
| **Pi-hole** | DNS ad filtering across 3 instances | [README](pihole_README.md) |
| **SFTPGo** | File server shell commands | [README](sftpgo_README.md) |
| **Supervisor** | Add-on lifecycle and auto-disable | [README](supervisor_README.md) |
| **UPS** | Uninterruptible power supply monitoring | [README](ups_README.md) |
| **Zigbee** | Zigbee2MQTT coordinator availability | [README](zigbee_README.md) |

## Calendar & Notifications

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| **Calendar** | Google Calendar event notifications with travel time | [README](calendar_README.md) |

## CI/CD & Automation

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| **Git** | GitHub Actions webhook → config auto-deploy | [README](git_README.md) |
| **N8N** | N8N workflow integration | [README](n8n_README.md) |

## Weather

| Integration | Description | Documentation |
|-------------|-------------|---------------|
| **Weather** | Forecasts, warnings, storm detection, carbon intensity, Ecowitt station | [README](weather/README.md) |

## Related Documentation

- [Rooms](../rooms/README.md) - Room-specific configuration
- [Main Packages README](../README.md) - Overview of the packages architecture
