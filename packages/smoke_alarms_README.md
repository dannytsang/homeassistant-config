[<- Back to Packages README](README.md) · [Main README](../README.md)

# Smoke Alarms

*Reviewed against YAML: 2026-10-24*

Central smoke and CO alarm coordination. This package complements the Nest Protect integration at `packages/integrations/smoke_alarm.yaml`, which handles the physical device integration. This package implements the response logic: capturing camera evidence, notifying occupants via Alexa and mobile push, and repeating alerts until the condition clears.

---

## Contents

- [Automations](#automations)
- [Scripts](#scripts)
- [Detection Flow](#detection-flow)
- [Camera Coverage](#camera-coverage)

---

## Automations

### `Timer: Check Smoke Alarms Complete`

| Property | Value |
|---|---|
| ID | `1757836826542` |
| Trigger | `timer.check_smoke_alarms` finishes (`timer.finished` event) |
| Condition | None |
| Action | Calls `script.check_smoke_alarms` |
| Mode | Single |

This automation forms the repeat loop: the script starts the timer, and when the timer finishes this automation calls the script again. The script itself checks the aggregate alarm state before repeating notifications.

---

## Scripts

### `script.check_smoke_alarms`

**Alias:** Check Smoke Alarms
**Mode:** `single`

The core response script. It iterates over every entity listed in `binary_sensor.smoke_alarms` and for each one:

1. For every active sensor, takes a timestamped camera snapshot.
2. Saves each image to a path constructed from `input_text.camera_external_folder_path` and a subdirectory matching that sensor's location.
3. If one or more sensors are active, runs the following **in parallel**:
   - Alexa announcement naming all active alarm areas (always plays, `suppress_if_quiet: false`).
   - Mobile push notification to all household members with high priority.
   - Starts `timer.check_smoke_alarms` for 1 minute — triggering the repeat loop via the automation above.
4. If no sensors are active, logs that the alarm is clear and does not restart the timer.

#### Camera Snapshot Mapping

| Smoke sensor | Camera | Subdirectory |
|---|---|---|
| `binary_sensor.kitchen_smoke_alarm_smoke` | `camera.kitchen_high_resolution_channel` | `kitchen/` |
| `binary_sensor.nest_protect_living_room_smoke_status` | `camera.living_room_high_resolution_channel` | `lounge/` |
| `binary_sensor.nest_protect_office_smoke_status` | `camera.office_high_resolution_channel` | `office/` |
| `binary_sensor.nest_protect_upstairs_smoke_status` | `camera.stairs_high_resolution_channel` | `stairs/` |

Snapshot filenames use the format `YYYY-MM-DD HH.MM.SS.jpg`.

---

## Detection Flow

```mermaid
flowchart TD
    A[Smoke/CO sensor triggers] --> B[binary_sensor.smoke_alarms ON]
    B --> C[script.check_smoke_alarms called]
    C --> D{Iterate each sensor\nin smoke_alarms group}
    D --> E[Take camera snapshot\nfor that location]
    E --> D
    D -->|All sensors processed| F[Parallel actions]
    F --> G[Alexa announces\naffected rooms]
    F --> H[Push notification\nhigh priority\nto all people]
    F --> I[Start timer.check_smoke_alarms\n1 minute]
    I --> J[Timer fires]
    J --> K[Automation: Timer Check\nSmoke Alarms Complete]
    K --> C
    C -->|No active sensor| L[Log all clear\nand stop repeating]
```

> **Note:** The timer only restarts while a member of `binary_sensor.smoke_alarms` is active. It stops naturally after the next check once all members are clear.

---

## Dependencies

| Entity | Purpose |
|---|---|
| `binary_sensor.smoke_alarms` | Group sensor; `entity_id` attribute lists all member sensors |
| `timer.check_smoke_alarms` | 1-minute repeat timer |
| `input_text.camera_external_folder_path` | Root path for snapshot storage |
| `script.alexa_announce` | Household Alexa announcement |
| `script.send_direct_notification` | Mobile push to named people |
