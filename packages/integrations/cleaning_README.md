[<- Back to Integrations README](README.md) · [Packages README](../README.md) · [Main README](../../README.md)

# Cleaning — Deebot Vacuum

Monitoring and logging automations for the Deebot T8 robot vacuum, using the [Deebot-4-Home-Assistant](https://github.com/DeebotUniverse/Deebot-4-Home-Assistant) HACS integration.

---

## Overview

Three automations cover the key vacuum lifecycle events — error states, charging completion, and cleaning completion. A REST command allows the Deebot integration to be reloaded via the Home Assistant API.

---

## Automations

| ID | Alias | Trigger | Action |
|----|-------|---------|--------|
| `1650387098757` | Deebot: Error | `vacuum.t8` state → `error` | Logs warning to home log (Normal) |
| `1650387098756` | Deebot: Fully Charged | `vacuum.t8` battery_level > 99 | Logs fully charged (Debug) |
| `1654865901253` | Deebot: Finished Cleaning | `vacuum.t8` state → `docked` for 1 min (not from `unavailable`) | Logs completion with map image URL |

### Deebot: Finished Cleaning — detail

When the vacuum docks and has been docked for at least 1 minute, the automation calls `script.send_home_log_with_url` including a direct link to the latest cleaned-area map image:

```
{external_url}{image.t8_map entity_picture}
```

---

## REST Command

| Command | Purpose |
|---------|---------|
| `rest_command.reload_deebot` | Reloads the Deebot integration via HA REST API (POST with auth token) |

The reload URL and auth token are stored in secrets (`deebot_restcommand_reload_url`, `deebot_restcommand_reload_token`).

---

## Entities

| Entity | Description |
|--------|-------------|
| `vacuum.t8` | Deebot T8 vacuum robot |
| `image.t8_map` | Latest cleaned-area map image |
| `input_text.external_url` | Home Assistant external URL (used to build map image link) |

---

## Dependencies

- **HACS Integration:** [Deebot-4-Home-Assistant](https://github.com/DeebotUniverse/Deebot-4-Home-Assistant)
- **Scripts:** `script.send_to_home_log`, `script.send_home_log_with_url`

---

*Last updated: 2026-04-05*
