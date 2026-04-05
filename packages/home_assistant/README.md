[<- Back to Packages README](../README.md) · [Main README](../../README.md)

# Home Assistant

*Last updated: 2026-04-05*

Core Home Assistant lifecycle management: startup checks, shutdown logging, automated backups, database maintenance, and version upgrade workflows with interactive approval.

---

## Contents

- [Automations](#automations)
- [Scripts](#scripts)
- [Template Sensors](#template-sensors)

---

## Automations

### `Home Assistant: Shutdown`

| Property | Value |
|---|---|
| ID | `1608489438291` |
| Trigger | `homeassistant` event: `shutdown` |
| Mode | Single |

Writes a shutdown log entry to the home log. No other actions — this acts as an audit trail in the log timeline.

---

### `Home Assistant: Start Up`

| Property | Value |
|---|---|
| ID | `1608489396143` |
| Trigger | `homeassistant` event: `start` |
| Mode | Single |

Comprehensive startup check running the following **in parallel**:

| Step | What it does |
|---|---|
| Log | Writes "Started." to the home log |
| Solar Assistant | Calls `script.solar_assistant_check_charging_mode` with current Octopus import/export rates |
| Zappi EV charger | If `input_boolean.enable_zappi_automations` is on and an EV is connected, calls `script.zappi_check_ev_charge` with current electricity rates |
| Terina's work laptop | Calls `script.check_terinas_work_laptop_status` to adjust living room light thresholds |
| 3D printer light | Calls `script.3d_printer_check_turn_off_light` |
| Magic Mirror | If someone is home (or Guest mode) and alarm is not `armed_away`, casts the `lovelace-magicmirror/home` dashboard to `media_player.stairs_chromecast` |
| Porch light | If the front door is closed (`binary_sensor.front_door` = `off`), turns off the porch light and all `dedicate_notification_light` label lights |

---

### `Home Assistant: Update Available`

| Property | Value |
|---|---|
| ID | `1664657264986` |
| Trigger | `update.home_assistant_core_update` changes from `off` to `on` |
| Condition | `input_select.home_assistant_automatic_upgrade` is not `Disabled` |
| Mode | Single |

Calls `script.upgrade_home_assistant` when a new HA Core version is detected.

---

### `Home Assistant: Weekday Backup`

| Property | Value |
|---|---|
| ID | `1738875026613` |
| Trigger | Daily at **17:00** |
| Condition | Monday–Friday only |
| Mode | Single |

Triggers a full compressed backup via `hassio.backup_full`.

---

### `Home Assistant: Weekend Backup`

| Property | Value |
|---|---|
| ID | `1738875026614` |
| Trigger | Daily at **11:00** |
| Condition | Saturday–Sunday only |
| Mode | Single |

Triggers a full compressed backup via `hassio.backup_full`.

---

### `Home Assistant: Purge Noisy Entities`

| Property | Value |
|---|---|
| ID | `1759178231254` |
| Trigger | Every **Saturday at 04:00** |
| Condition | None |
| Mode | Single |

Calls `recorder.purge` with `repack: true` and `keep_days: 7` targeting the entity domains listed below. This keeps the database compact by removing high-volume history from domains that don't benefit from long-term retention.

**Purged domains (7-day retention):**

`calendar`, `camera`, `counter`, `event`, `image_processing`, `media_player`, `notify`, `siren`, `sun`, `timer`, `vacuum`

---

## Scripts

### `script.upgrade_home_assistant`

**Alias:** Upgrade Home Assistant
**Mode:** `single`

Determines the type of version change by comparing `installed_version` and `latest_version` from `update.home_assistant_core_update`, then sends an interactive 2-button notification to `person.danny` requesting approval.

| `input_select.home_assistant_automatic_upgrade` | Version change detected | Notification sent |
|---|---|---|
| Any value except `Disabled` | Patch only (major and minor unchanged) | "Patch update from X to Y?" |
| `Minor Versions` | Minor version changed (major unchanged) | "Minor update from X to Y?" |
| `Major Versions` | Major version changed | "Major update from X to Y?" (titled "Home Assistant Supervisor") |

Buttons: **Yes** (`update_home_assistant`) / **No** (`ignore`). No automatic action is taken — the upgrade only proceeds if Danny approves via the notification.

---

### `script.upgrade_home_assistant_supervisor`

**Alias:** Upgrade Home Assistant Supervisor
**Mode:** `single`

Identical approval flow to `upgrade_home_assistant` but reads from `update.home_assistant_supervisor_update`. Sends the same 2-button actionable notification to `person.danny`.

| `input_select.home_assistant_automatic_upgrade` | Version change detected | Notification sent |
|---|---|---|
| Any value except `Disabled` | Patch only | "Patch update from X to Y?" |
| `Minor Versions` | Minor changed | "Minor update from X to Y?" |
| `Major Versions` | Major changed | "Major update from X to Y?" |

---

## Template Sensors

### `sensor.total_sensors`

**Icon:** `mdi:radio-tower`

Reports the total count of all entities registered in Home Assistant. The `break_down` attribute provides a per-domain entity count list.

| Attribute | Description |
|---|---|
| `state` | Total entity count across all domains |
| `break_down` | List of `{"domain": count}` objects for every domain |

---

## Dependencies

| Entity | Purpose |
|---|---|
| `update.home_assistant_core_update` | HA Core update state and version attributes |
| `update.home_assistant_supervisor_update` | HA Supervisor update state and version attributes |
| `input_select.home_assistant_automatic_upgrade` | Controls which update types trigger approval prompts |
| `input_boolean.enable_zappi_automations` | Guards Zappi startup check |
| `sensor.octopus_energy_electricity_current_rate` | Current import rate passed to solar/Zappi checks |
| `sensor.octopus_energy_electricity_export_current_rate` | Current export rate passed to solar/Zappi checks |
| `sensor.myenergi_zappi_plug_status` | EV connection state |
| `group.tracked_people` | Determines if someone is home for Magic Mirror cast |
| `alarm_control_panel.house_alarm` | Guards Magic Mirror cast (skips if armed away) |
| `media_player.stairs_chromecast` | Magic Mirror display target |
| `binary_sensor.front_door` | Guards porch light off on startup |
| `script.solar_assistant_check_charging_mode` | Solar battery charging mode check |
| `script.zappi_check_ev_charge` | Zappi EV charge check |
| `script.check_terinas_work_laptop_status` | Living room light threshold adjuster |
| `script.3d_printer_check_turn_off_light` | 3D printer enclosure light check |
| `script.send_actionable_notification_with_2_buttons` | Upgrade approval notification |
| `script.send_to_home_log` | Home log writer |
