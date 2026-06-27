[<- Back to Packages README](../README.md) · [Main README](../../README.md)

# Integrations

Last reviewed: 2026-06-27

Integration-specific configuration organized by functional domain. Each package is self-contained where practical, with UI integration setup and secrets handled separately.

## Current Inventory

| Metric | Count |
|--------|-------|
| Integration YAML files | 45 |
| Integration automations | 130 |
| Integration scripts | 77 |
| Integration sensors | 36 |
| Integration template blocks | 30 |
| Integration groups | 4 |
| Integration MQTT entries | 122 |
| REST commands | 3 |
| Shell commands | 2 |
| Conversation blocks | 1 |
| Intent scripts | 13 |

## Integration Categories

| Category | YAML files | Current package contents | Documentation |
|----------|------------|--------------------------|---------------|
| **Energy** | 8 | 38 automations, 28 scripts, 12 sensors, 16 template blocks, 4 groups, 1 conversation block, 13 intent scripts | [README](energy/README.md) |
| **HVAC** | 3 | 16 automations, 12 scripts, 16 sensors, 7 template blocks, 1 schedule, 1 input number, 1 utility meter | [README](hvac/README.md) |
| **Messaging** | 7 | 5 automations, 23 scripts, 2 notify services | [README](messaging/README.md) |
| **Transport** | 2 | 2 automations, 2 scripts, 4 template blocks, 122 MQTT entries | [README](transport/README.md) |
| **Weather** | 3 | 6 automations, 2 REST blocks | [README](weather/README.md) |

## Energy Documentation

| Package | Current package contents | Document |
|---------|--------------------------|----------|
| `energy/energy.yaml` | 14 automations, 9 scripts, 4 groups, 4 template blocks | [README](energy/energy_README.md) |
| `energy/ecoflow.yaml` | 11 automations, 10 scripts, 4 template blocks | [README](energy/ecoflow_README.md) |
| `energy/energy_conversations.yaml` | 1 conversation block, 13 intent scripts | [README](energy/README.md) |
| `energy/octopus_energy.yaml` | 3 automations, 1 script | [README](energy/octopus_energy_README.md) |
| `energy/predbat.yaml` | 2 automations | [README](energy/predbat_README.md) |
| `energy/solar_assistant.yaml` | 1 automation, 6 scripts, 12 sensors, 8 template blocks | [README](energy/solar_assistant_README.md) |
| `energy/solcast.yaml` | 1 automation, 1 script | [README](energy/solcast_README.md) |
| `energy/zappi.yaml` | 6 automations, 1 script | [README](energy/zappi_README.md) |

## Transport Sub-Integrations

| Package | Current package contents | Document |
|---------|--------------------------|----------|
| `transport/tesla.yaml` | 2 automations, 122 MQTT entries, 1 script, 2 template blocks | [README](transport/tesla_README.md) |
| `transport/google_travel.yaml` | 1 script, 2 template blocks | [README](transport/google_travel_README.md) |

## Device & Media Integrations

| Integration | Current package contents | Documentation |
|-------------|--------------------------|---------------|
| **Alexa** | 2 scripts | [README](alexa_README.md) |
| **Chromecast** | 2 automations, 1 script | [README](chromecast_README.md) |
| **LG** | 4 automations | [README](lg_README.md) |
| **Spotify** | 1 automation | [README](spotify_README.md) |

## Household & Appliances

| Integration | Current package contents | Documentation |
|-------------|--------------------------|---------------|
| **Bins** | 2 automations, 5 sensors, 1 template block | [README](bins_README.md) |
| **Cleaning** | 3 automations, 1 REST command | [README](cleaning_README.md) |
| **Grocy** | 2 REST commands, 2 sensors | [README](grocy_README.md) |
| **Paperless** | 1 automation, 1 sensor | [README](paperless_README.md) |

## Security & Safety

| Integration | Current package contents | Documentation |
|-------------|--------------------------|---------------|
| **Alarm** | 8 automations, 4 scripts | [README](alarm_README.md) |
| **Nuki** | 3 automations, 2 scripts | [README](nuki_README.md) |
| **Smoke Alarm** | 6 automations | [README](smoke_alarm_README.md) |
| **UniFi Protect** | 4 automations | [README](unifi_protect_README.md) |
| **Water** | 2 automations, 1 template block | [README](water_README.md) |

## Infrastructure & Monitoring

| Integration | Current package contents | Documentation |
|-------------|--------------------------|---------------|
| **ESPHome** | 2 automations | [README](esphome_README.md) |
| **OwnTracks** | 3 automations | [README](owntracks_README.md) |
| **SFTPGo** | 1 shell command | [README](sftpgo_README.md) |
| **Supervisor** | 13 automations, 1 script | [README](supervisor_README.md) |
| **UPS** | 4 automations, 1 template block | [README](ups_README.md) |
| **Zigbee** | 1 automation | [README](zigbee_README.md) |

## Calendar, CI/CD & Automation

| Integration | Current package contents | Documentation |
|-------------|--------------------------|---------------|
| **Calendar** | 3 automations, 2 scripts | [README](calendar_README.md) |
| **Git** | 1 automation | [README](git_README.md) |
| **N8N** | 1 shell command | [README](n8n_README.md) |

## Weather

| Integration | Current package contents | Documentation |
|-------------|--------------------------|---------------|
| **Weather** | 5 automations, 1 REST block | [README](weather/README.md) |
| **Ecowitt** | 1 automation | [README](weather/README.md) |
| **Carbon Intensity UK** | 1 REST block | [README](weather/README.md) |

## Related Documentation

- [Rooms](../rooms/README.md) - Room-specific configuration
- [Main Packages README](../README.md) - Overview of the packages architecture
- [Setup Statistics](../../setup_statistics.md) - Current package counts and analysis
