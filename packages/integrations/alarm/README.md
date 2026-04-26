[<- Back to Alarm README](../README.md) · [Packages README](../../README.md) · [Main README](../../../README.md)

# Alarm Package Documentation

This package manages alarm automation including 8 automations and 0 scripts.

---

## Table of Contents

- [Overview](#overview)
- [Design Decisions](#design-decisions)
- [Automations](#automations)
- [Entity Reference](#entity-reference)

---

## Overview

The alarm automation system provides intelligent control and monitoring.

```mermaid
flowchart TB
    subgraph Inputs["📥 Inputs"]
        binary_sensor_alarmed_doors_and_windows["alarmed_doors_and_wi"]
    end
    subgraph Logic["🧠 Logic"]
        AlarmDisarmed["Alarm: Disarmed"]
        AlarmArmOvernightHom["Alarm: Arm Overnight Home Mode"]
        AlarmArmOvernightHom["Alarm: Arm Overnight Home Mode"]
        AlarmArmOvernightWhe["Alarm: Arm Overnight When Door"]
        AlarmArmed["Alarm: Armed"]
    end
    subgraph Outputs["📤 Outputs"]
        alias: Turn on bedroom light to warn not all doors/windows are closed_[""]
        light_under_bed_left["under_bed_left"]
        light_under_bed_right["under_bed_right"]
        light_bedroom_lamp_left["bedroom_lamp_left"]
        light_bedroom_lamp_right["bedroom_lamp_right"]
    end
    binary_sensor_alarmed_doors_and_windows --> AlarmDisarmed
    AlarmDisarmed --> alias: Turn on bedroom light to warn not all doors/windows are closed_
    AlarmDisarmed --> light_under_bed_left
    AlarmDisarmed --> light_under_bed_right
```

### File Structure

```
packages/integrations/
├── alarm.yaml      # Main package file
└── README.md             # This documentation
```

---

## Design Decisions

Key architectural decisions captured from the YAML configuration:

- **Alarm: Disarmed** has a master enable switch for easy disabling
- **Alarm: Arm Overnight Home Mode** triggers on state transitions (edge detection) rather than continuous state
- **Alarm: Arm Overnight Home Mode** has a master enable switch for easy disabling
- **Alarm: Arm Overnight Home Mode Final Check** uses scheduled times for predictable daily routines
- **Alarm: Arm Overnight When Doors And Windows Shut** triggers on state transitions (edge detection) rather than continuous state

---

## Automations

### Alarm: Disarmed
**ID:** `1628956688014`

**Triggers:**
- When `House Alarm` changes to 'disarmed'

**Conditions:**
- `Enable Alarm Automations` is enabled

**Actions:**
- Execute actions in parallel

### Alarm: Arm Overnight Home Mode
**ID:** `1587680439012`

**Triggers:**
- When `Alarm Scheduled Home Mode` changes from 'off' to 'on'

**Conditions:**
- `House Alarm` is 'disarmed'
- `Enable Alarm Automations` is enabled

**Actions:**
- Execute actions in parallel
- Conditional action selection

### Alarm: Arm Overnight Home Mode Final Check
**ID:** `1587680439015`

**Triggers:**
- At 02:05:00

**Conditions:**
- `House Alarm` is 'disarmed'

**Actions:**
- Turn on Under Bed Left, Under Bed Right
- Execute actions in parallel
- Conditional action selection

### Alarm: Arm Overnight When Doors And Windows Shut
**ID:** `1587680439013`

**Triggers:**
- When `Alarmed Doors And Windows` changes from 'on' to 'off'

**Conditions:**
- `Adult People` is 'home'
- `Alarmed Doors And Windows` is 'off'
- `Enable Alarm Automations` is enabled

**Actions:**
- *See YAML for action details*

### Alarm: Armed
**ID:** `1630366065607`

**Triggers:**
- When `House Alarm` changes to 'armed_away'

**Conditions:**
- `Enable Alarm Automations` is enabled

**Actions:**
- Execute actions in parallel

### Alarm: Disconnected
**ID:** `1614197981954`

**Triggers:**
- When `House Alarm` changes to 'unavailable'

**Conditions:**
- `Enable Alarm Automations` is enabled

**Actions:**
- Execute actions in parallel

### Alarm: Disconnected For A Period Of Time
**ID:** `1658658845650`

**Triggers:**
- When `House Alarm` changes to 'unavailable'

**Conditions:**
- `Enable Alarm Automations` is enabled

**Actions:**
- Conditional action selection

### Alarm: Triggered
**ID:** `1589026420341`

**Triggers:**
- When `House Alarm` changes to 'triggered'

**Conditions:**
- `Enable Alarm Automations` is enabled

**Actions:**
- Execute actions in parallel

---

---

## Scripts

### set_alarm_to_away_mode
Sets the alarm to away mode. Only acts if alarm is not already in away mode.

### set_alarm_to_disarmed_mode
Sets the alarm to disarmed mode. Only acts if alarm is not already disarmed.

### set_alarm_to_home_mode
Sets the alarm to home mode. Only acts if alarm is not already in home mode.

### arm_alarm_overnight
Complex overnight arming logic with people-aware behavior:
- **Already locked + armed:** Skip
- **Everyone home:** Arm home + lock door
- **Someone not far:** Log and retry later
- **Someone home, rest far:** Arm home + lock door (after 22:59 or before 02:00)
- **Otherwise:** Notify and retry later

---

## Entity Reference

### Alarm Panel

| Entity | Purpose |
|--------|---------|
| `alarm_control_panel.house_alarm` | Main house alarm panel |

### Binary Sensors

| Entity | Purpose |
|--------|---------|
| `binary_sensor.alarmed_doors_and_windows` | Combined door/window sensor group |

### People

| Entity | Purpose |
|--------|---------|
| `person.danny` | Danny's presence |
| `person.terina` | Terina's presence |
| `person.leo` | Leo's presence |

### Locks

| Entity | Purpose |
|--------|---------|
| `lock.front_door` | Front door lock |

### Schedules

| Entity | Purpose |
|--------|---------|
| `schedule.alarm_scheduled_home_mode` | Scheduled arming schedule |

### Input Booleans

| Entity | Purpose |
|--------|---------|
| `input_boolean.enable_alarm_automations` | Master switch for alarm automations |

### Input Numbers

| Entity | Purpose |
|--------|---------|
| `input_number.long_distance_away_from_home` | Distance threshold for "far away" detection |

### Lights (Indicators)

| Entity | Purpose |
|--------|---------|
| `light.under_bed_left` | Under-bed indicator light |
| `light.under_bed_right` | Under-bed indicator light |
| `light.bedroom_lamp_left` | Bedroom lamp |
| `light.bedroom_lamp_right` | Bedroom lamp |

---

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [Integrations Overview](../README.md) | Overview of all integration packages |
| [Main Packages README](../../README.md) | Architecture and organization guidelines |

---

## Maintenance Notes

### Troubleshooting

| Issue | Check |
|-------|-------|
| Automation not triggering | Entity states and conditions |
| Script failing | Service calls and entity availability |

*Last updated: 2026-04-08*
