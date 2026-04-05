[<- Back to Packages README](../README.md) · [Main README](../../README.md)

# Time

*Last updated: 2026-04-05*

Time-based automations covering scheduled maintenance tasks, end-of-night safety checks, morning routine management, bedtime announcements, and a fallback lights-off schedule. These are house-wide, time-driven automations that don't belong to a specific room or device.

---

## Contents

- [Automations](#automations)
- [Scripts](#scripts)

---

## Automations

### `Time: Warn Doors or Windows Still Open At Night`

| Property | Value |
|---|---|
| ID | `1622667704047` |
| Trigger | Daily at **22:00** |
| Condition | `binary_sensor.alarmed_doors_and_windows` is `on` (at least one open) |
| Mode | Single |

If any alarmed doors or windows are still open at 22:00 a warning is written to the home log. The log entry lists every open entrance by friendly name. No notification is pushed to phones — this is a log-only alert.

---

### `Time: Delete Old Camera Files`

| Property | Value |
|---|---|
| ID | `1619466600288` |
| Trigger | Every 2 hours (`/2` time pattern) |
| Condition | None |
| Mode | Single |

Calls `delete.files_in_folder` against `/config/camera/` (with subfolders, not removing subdirectory structure) to remove files older than **4 hours** (14400 seconds). The following files are preserved regardless of age:

- `.gitignore`, `README.md`
- DeepStack latest/none reference images: `deepstack_object_*_latest.png` and `deepstack_object_*_none.png` for conservatory, driveway, front door, kitchen, lounge, and upstairs

Logs the deletion attempt to the home log.

---

### `Time: Reset Morning Run`

| Property | Value |
|---|---|
| ID | `1588859384208` |
| Trigger | Daily at **04:59** |
| Condition | None |
| Mode | Single |

Turns on `input_boolean.enable_morning_routine` so the morning routine is available to fire when motion is first detected after sunrise. Runs in parallel with a debug log entry.

---

### `Timed: Turn Off Downstairs Lights at 2am`

| Property | Value |
|---|---|
| ID | `1582406380123` |
| Triggers | **02:00** (id: `2am`), **03:00**, **04:00** |
| Condition | Excludes Sunday at 02:00 (the 02:00 trigger is skipped on Sundays) |
| Mode | Single |

Fallback automation that ensures downstairs lights are off during the small hours in case of connectivity or automation failures. Activates `scene.turn_off_downstairs_lights` in parallel with a debug log entry.

The Sunday exclusion on the 02:00 trigger reflects that late Saturday nights are a legitimate use case.

---

### `Time: Announce Bed Time`

| Property | Value |
|---|---|
| ID | `1745396436913` |
| Triggers | `input_datetime.childrens_bed_time` **minus 1h 15 min** (id: `1h`) and **minus 15 min** (id: `0h`) |
| Conditions | Leo or Ashlee is home; home mode is not "No Children"; weekday is Mon–Thu or Sun |
| Mode | Single |

Before announcing, the automation queries `calendar.tsang_children` for tomorrow's events. If any event title matches `half term`, `holidays`, or `occasional day` (case-insensitive), the announcement is skipped and a log entry explains why.

Otherwise:

| Trigger | Alexa message |
|---|---|
| 1h 15 min before bedtime (`1h`) | "It's one hour before bedtime." |
| 15 min before bedtime (`0h`) | "It's bed time." |

`suppress_if_quiet: true` — announcements are suppressed during quiet hours.

---

## Scripts

### `script.morning_script`

**Alias:** Morning Script
**Mode:** `single`

Runs when motion is first detected in the lounge in the morning (called from the lounge motion automation when `input_boolean.enable_morning_routine` is `on`). Sequence:

1. Turns off `input_boolean.enable_morning_routine` (prevents re-running).
2. In **parallel**:
   - Logs "Motion detected in the Lounge in the morning. Running morning routine."
   - Calls `script.set_alarm_to_disarmed_mode` — disarms the house alarm.
   - Logs "Morning routine complete."
   - Calls `script.announce_delayed_notifications` — delivers any notifications queued overnight.

---

## Dependencies

| Entity | Purpose |
|---|---|
| `binary_sensor.alarmed_doors_and_windows` | Aggregate open-door/window check |
| `input_boolean.enable_morning_routine` | Flag controlling morning routine eligibility |
| `input_datetime.childrens_bed_time` | Configurable children's bedtime used as trigger offset |
| `calendar.tsang_children` | School holiday calendar consulted before bed announcements |
| `scene.turn_off_downstairs_lights` | Scene activated by the 2am fallback automation |
| `script.set_alarm_to_disarmed_mode` | Disarms the house alarm |
| `script.announce_delayed_notifications` | Delivers queued/delayed notifications |
| `script.alexa_announce` | Household Alexa announcement |
| `script.get_clock_emoji` | Clock emoji for log messages |
| `script.send_to_home_log` | Home log writer |
