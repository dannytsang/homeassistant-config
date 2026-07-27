[<- Back to Packages README](../README.md) · [Main README](../../README.md)

# Integrations

Last reviewed against YAML: 2026-07-19

Integration-specific configuration organized by functional domain. Each package is self-contained where practical, with UI integration setup and secrets handled separately.

## Current Inventory

| Metric | Count |
|--------|-------|
| Integration YAML files | 45 |
| Integration automations | 130 |
| Integration scripts | 78 |
| Integration sensors | 36 |
| Integration template blocks | 30 |
| Integration groups | 4 |
| Integration MQTT entries | 122 |
| REST commands | 3 |
| Shell commands | 2 |
| Conversation blocks | 1 |
| Intent scripts | 13 |

## Integration Categories

Each package's README is its implementation guide. The source YAML is linked beside it below so a reader can move directly between the documentation, exact triggers/conditions/actions, and Home Assistant traces.

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
| [energy.yaml](energy/energy.yaml) | 14 automations, 9 scripts, 4 groups, 4 template blocks | [README](energy/energy_README.md) |
| [ecoflow.yaml](energy/ecoflow.yaml) | 11 automations, 10 scripts, 4 template blocks | [README](energy/ecoflow_README.md) |
| [energy_conversations.yaml](energy/energy_conversations.yaml) | 1 conversation block, 13 intent scripts | [README](energy/README.md) |
| [octopus_energy.yaml](energy/octopus_energy.yaml) | 3 automations, 1 script | [README](energy/octopus_energy_README.md) |
| [predbat.yaml](energy/predbat.yaml) | 2 automations | [README](energy/predbat_README.md) |
| [solar_assistant.yaml](energy/solar_assistant.yaml) | 1 automation, 6 scripts, 12 sensors, 8 template blocks | [README](energy/solar_assistant_README.md) |
| [solcast.yaml](energy/solcast.yaml) | 1 automation, 1 script | [README](energy/solcast_README.md) |
| [zappi.yaml](energy/zappi.yaml) | 6 automations, 1 script | [README](energy/zappi_README.md) |

## Transport Sub-Integrations

| Package | Current package contents | Document |
|---------|--------------------------|----------|
| [tesla.yaml](transport/tesla.yaml) | 2 automations, 122 MQTT entries, 1 script, 2 template blocks | [README](transport/tesla_README.md) |
| [google_travel.yaml](transport/google_travel.yaml) | 1 script, 2 template blocks | [README](transport/google_travel_README.md) |

## Device & Media Integrations

| Integration | Current package contents | Documentation |
|-------------|--------------------------|---------------|
| **[Alexa](alexa.yaml)** | 2 scripts | [README](alexa_README.md) |
| **[Chromecast](chromecast.yaml)** | 2 automations, 1 script | [README](chromecast_README.md) |
| **[LG](lg.yaml)** | 4 automations | [README](lg_README.md) |
| **[Spotify](spotify.yaml)** | 1 automation | [README](spotify_README.md) |

## Household & Appliances

| Integration | Current package contents | Documentation |
|-------------|--------------------------|---------------|
| **[Bins](bins.yaml)** | 2 automations, 5 sensors, 1 template block | [README](bins_README.md) |
| **[Cleaning](cleaning.yaml)** | 3 automations, 1 REST command | [README](cleaning_README.md) |
| **[Grocy](grocy.yaml)** | 2 REST commands, 2 sensors | [README](grocy_README.md) |
| **[Paperless](paperless.yaml)** | 1 automation, 1 sensor | [README](paperless_README.md) |

## Security & Safety

| Integration | Current package contents | Documentation |
|-------------|--------------------------|---------------|
| **[Alarm](alarm.yaml)** | 8 automations, 5 scripts | [README](alarm_README.md) |
| **[Nuki](nuki.yaml)** | 3 automations, 2 scripts | [README](nuki_README.md) |
| **[Smoke Alarm](smoke_alarm.yaml)** | 6 automations | [README](smoke_alarm_README.md) |
| **[UniFi Protect](unifi_protect.yaml)** | 4 automations | [README](unifi_protect_README.md) |
| **[Water](water.yaml)** | 2 automations, 1 template block | [README](water_README.md) |

## Infrastructure & Monitoring

| Integration | Current package contents | Documentation |
|-------------|--------------------------|---------------|
| **[ESPHome](esphome.yaml)** | 2 automations | [README](esphome_README.md) |
| **[OwnTracks](owntracks.yaml)** | 3 automations | [README](owntracks_README.md) |
| **[SFTPGo](sftpgo.yaml)** | 1 shell command | [README](sftpgo_README.md) |
| **[Supervisor](supervisor.yaml)** | 13 automations, 1 script | [README](supervisor_README.md) |
| **[UPS](ups.yaml)** | 4 automations, 1 template block | [README](ups_README.md) |
| **[Zigbee](zigbee.yaml)** | 1 automation | [README](zigbee_README.md) |

## Calendar, CI/CD & Automation

| Integration | Current package contents | Documentation |
|-------------|--------------------------|---------------|
| **[Calendar](calendar.yaml)** | 3 automations, 2 scripts | [README](calendar_README.md) |
| **[Git](git.yaml)** | 1 automation | [README](git_README.md) |
| **[N8N](n8n.yaml)** | 1 shell command | [README](n8n_README.md) |

## Weather

| Integration | Current package contents | Documentation |
|-------------|--------------------------|---------------|
| **[Weather](weather/weather.yaml)** | 5 automations, 1 REST block | [README](weather/README.md) |
| **[Ecowitt](weather/ecowitt.yaml)** | 1 automation | [README](weather/README.md) |
| **[Carbon Intensity UK](weather/carbon_intensity_uk.yaml)** | 1 REST block | [README](weather/README.md) |

## Related Documentation

- [Rooms](../rooms/README.md) - Room-specific configuration
- [Main Packages README](../README.md) - Overview of the packages architecture
- [Setup Statistics](../../setup_statistics.md) - Current package counts and analysis
