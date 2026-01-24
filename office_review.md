# Office Package Review & Improvement Recommendations

**Review Date:** 2026-01-12
**Package Location:** `packages/rooms/office/`
**Files Reviewed:** `office.yaml` (1629 lines), `steam.yaml` (44 lines)

---

## Executive Summary

The office package is **functionally rich** but suffers from:
- **Critical bugs** (duplicate automation IDs, incorrect timer messages)
- **Structural issues** (file too large at 1629 lines)
- **Complexity** that could be simplified with better patterns
- **Missing entity definitions** (helpers, timers, groups)

**Overall Assessment:** 6/10 - Works but needs refactoring for maintainability

---

## Critical Issues (Fix Immediately)

### 1. **DUPLICATE AUTOMATION ID** ⚠️
**Location:** Lines 587 and 627
```yaml
# Line 587
- id: "1622374233312"
  alias: "Office: Close Office Blinds At Night 2"

# Line 627
- id: "1622374233310"  # Different ID but...
  alias: "Office: Close Office Blinds At Night 2"  # SAME ALIAS
```

**Impact:** Confusing automation traces, potential automation conflicts
**Fix:** Rename one to "Office: Close Office Blinds At Night 3" or merge them

### 2. **Timer Duration Mismatch**
**Location:** Lines 257-265
```yaml
# Line 257: Says "2 minutes"
message: >-
  🚷 No motion in the office. Starting :hourglass_flowing_sand: timer for 2 minutes
  before turning lights off.

# Line 265: Actually sets 1 minute
duration: "00:01:00"
```

**Fix:**
```yaml
message: >-
  🚷 No motion in the office. Starting timer for 1 minute before turning lights off.
duration: "00:01:00"
```

### 3. **Incorrect Log Message**
**Location:** Line 117
```yaml
message: >-
  🐾 💡 🔆 Motion detected in the office
  and bright ({{ states('sensor.office_motion_2_illuminance') }} <
  {{ states('input_number.office_light_level_threshold', with_unit=True) }}).
  Turning office lights off.
```

The message says "bright" but the operator is `<` (less than), meaning it's actually **dark**.

**Fix:**
```yaml
message: >-
  🐾 💡 🔆 Motion detected in the office
  and dark ({{ states('sensor.office_motion_2_illuminance') }} <
  {{ states('input_number.office_light_level_threshold', with_unit=True) }}).
  Turning office lights off.
```

---

## Structural Issues

### 1. **File Too Large** (1629 lines)

**Problem:** Single file contains:
- 40+ automations
- 13 scenes
- 3 scripts
- 10+ history_stats sensors

**Recommendation:** Split into separate files:

```
packages/rooms/office/
├── office.yaml              # Main automations & helpers
├── office_lights.yaml       # Lighting automations
├── office_blinds.yaml       # Blind automations (300+ lines)
├── office_climate.yaml      # Temperature/fan automations
├── office_computer.yaml     # Computer-related automations
├── office_scenes.yaml       # Scene definitions
├── office_sensors.yaml      # History stats sensors
└── steam.yaml              # Keep as-is
```

### 2. **Missing Entity Definitions**

**Referenced but not defined:**
```yaml
input_boolean:
  - enable_office_motion_triggers
  - enable_office_blind_automations
  - enable_steam_notifications

input_number:
  - office_light_level_threshold
  - blind_low_brightness_threshold
  - blind_high_brightness_threshold
  - office_blinds_morning_sun_azimuth_threshold
  - office_blinds_afternoon_sun_azimuth_threshold
  - office_blinds_afternoon_sun_elevation_threshold

timer:
  - office_lights_off

group:
  - jd_computer
  - dannys_work_computer
  - tracked_people
```

**Fix:** Add these definitions to the package or document where they're defined.

---

## Motion Detection Automations (Lines 4-291)

### Problem: Two Separate Automations for Light State

**Current Structure:**
- Automation 1 (lines 4-148): "Motion Detected And Light Is On"
- Automation 2 (lines 150-233): "Motion Detected And Light Is Off"

**Issue:**
- Duplicated logic (400+ lines)
- Split due to dynamic attribute access issue
- Complex nested conditions

### Recommended Refactor:

**Create a centralized script:**

```yaml
script:
  office_handle_motion:
    alias: Office Handle Motion
    sequence:
      - variables:
          illuminance: "{{ states('sensor.office_motion_2_illuminance') | float }}"
          threshold: "{{ states('input_number.office_light_level_threshold') | float }}"
          light_2_on: "{{ is_state('light.office_2', 'on') }}"
          light_3_on: "{{ is_state('light.office_3', 'on') }}"
          bright_enough: "{{ illuminance > threshold }}"
          before_sunset: "{{ state_attr('sun.sun', 'elevation') > -1 }}"

      - choose:
          # Case 1: Bright enough, don't turn on
          - conditions:
              - "{{ bright_enough and before_sunset }}"
            sequence:
              - action: script.send_to_home_log
                data:
                  message: >-
                    🐾 Motion detected but bright enough
                    ({{ illuminance }}lx > {{ threshold }}lx). Skipping.
                  title: "🏢 Office"
                  log_level: "Debug"
              - action: timer.cancel
                target:
                  entity_id: timer.office_lights_off

          # Case 2: Dark, turn on lights
          - conditions:
              - "{{ not bright_enough }}"
              - or:
                  - "{{ not light_2_on }}"
                  - "{{ not light_3_on }}"
                  - "{{ state_attr('light.office_2', 'brightness') | int(0) < 200 }}"
                  - "{{ state_attr('light.office_3', 'brightness') | int(0) < 200 }}"
            sequence:
              - parallel:
                  - action: scene.turn_on
                    target:
                      entity_id: scene.office_main_light_on
                    data:
                      transition: 1
                  - action: script.send_to_home_log
                    data:
                      message: >-
                        🐾 Motion detected and dark ({{ illuminance }}lx < {{ threshold }}lx).
                        Turning lights on.
                      title: "🏢 Office"
                      log_level: "Debug"
              - action: timer.cancel
                target:
                  entity_id: timer.office_lights_off
```

**Then simplify automations:**

```yaml
automation:
  - id: "1606428361967"
    alias: "Office: Motion Detected"
    triggers:
      - trigger: state
        entity_id: binary_sensor.office_motion_2_presence
        to: "on"
      - trigger: numeric_state
        entity_id: sensor.office_motion_2_target_distance
        above: 0.1
    conditions:
      - condition: state
        entity_id: input_boolean.enable_office_motion_triggers
        state: "on"
    actions:
      - action: script.office_handle_motion
    mode: queued
    max: 10
```

**Benefits:**
- Reduces from 400+ lines to ~100 lines
- Single source of truth for motion logic
- Easier to test and maintain
- Variables make logic clearer

---

## Blind Automations (Lines 512-935)

### Issues:
1. **10+ separate automations** for blind control
2. **Repeated conditions** across automations
3. **Hardcoded tilt positions** (0, 25, 50)
4. **Complex sun position logic** repeated

### Recommended Improvements:

**1. Create Helper Input Numbers:**

```yaml
input_number:
  office_blind_position_closed:
    name: Office Blind Position - Closed
    min: 0
    max: 100
    step: 5
    initial: 0
    unit_of_measurement: "%"

  office_blind_position_partial:
    name: Office Blind Position - Partial
    min: 0
    max: 100
    step: 5
    initial: 25
    unit_of_measurement: "%"

  office_blind_position_open:
    name: Office Blind Position - Open
    min: 0
    max: 100
    step: 5
    initial: 50
    unit_of_measurement: "%"
```

**2. Create Centralized Blind Scripts:**

```yaml
script:
  office_set_blinds_for_brightness:
    alias: Office Set Blinds For Brightness
    description: Adjust blinds based on illuminance and sun position
    sequence:
      - variables:
          illuminance: "{{ states('sensor.front_garden_motion_illuminance') | float }}"
          low_threshold: "{{ states('input_number.blind_low_brightness_threshold') | float }}"
          high_threshold: "{{ states('input_number.blind_high_brightness_threshold') | float }}"
          sun_azimuth: "{{ state_attr('sun.sun', 'azimuth') | float }}"
          sun_elevation: "{{ state_attr('sun.sun', 'elevation') | float }}"
          morning_azimuth: "{{ states('input_number.office_blinds_morning_sun_azimuth_threshold') | float }}"
          afternoon_azimuth: "{{ states('input_number.office_blinds_afternoon_sun_azimuth_threshold') | float }}"
          afternoon_elevation: "{{ states('input_number.office_blinds_afternoon_sun_elevation_threshold') | float }}"
          window_closed: "{{ is_state('binary_sensor.office_windows', 'off') }}"
          computer_on: "{{ is_state('group.jd_computer', 'home') or is_state('group.dannys_work_computer', 'home') }}"

      - choose:
          # Very bright - close blinds
          - conditions:
              - "{{ illuminance > high_threshold }}"
              - "{{ sun_azimuth > morning_azimuth }}"
              - "{{ sun_azimuth < afternoon_azimuth }}"
              - "{{ window_closed }}"
              - "{{ computer_on }}"
            sequence:
              - action: script.send_to_home_log
                data:
                  message: "☀️ Very bright ({{ illuminance }}lx). Closing blinds to {{ states('input_number.office_blind_position_closed') }}%."
                  title: "🏢 Office"
              - action: cover.set_cover_tilt_position
                target:
                  entity_id: cover.office_blinds
                data:
                  tilt_position: "{{ states('input_number.office_blind_position_closed') | int }}"

          # Moderately bright - partial
          - conditions:
              - "{{ illuminance > low_threshold }}"
              - "{{ illuminance <= high_threshold }}"
              - "{{ computer_on }}"
            sequence:
              - action: script.send_to_home_log
                data:
                  message: "🌤️ Moderately bright ({{ illuminance }}lx). Partially closing blinds to {{ states('input_number.office_blind_position_partial') }}%."
                  title: "🏢 Office"
              - action: cover.set_cover_tilt_position
                target:
                  entity_id: cover.office_blinds
                data:
                  tilt_position: "{{ states('input_number.office_blind_position_partial') | int }}"

          # Dark enough - open
          - conditions:
              - "{{ illuminance <= low_threshold }}"
            sequence:
              - action: script.office_open_blinds
```

**3. Consolidate Time-Based Automations:**

Instead of separate automations at 08:00, sunset, sunset+1hr, merge into single automation with appropriate conditions:

```yaml
automation:
  - id: "1622374444832"
    alias: "Office: Adjust Blinds Throughout Day"
    triggers:
      - trigger: time
        at: "08:00:00"
      - trigger: sun
        event: sunset
      - trigger: sun
        event: sunset
        offset: "01:00:00"
      - trigger: numeric_state
        entity_id: sensor.front_garden_motion_illuminance
        above: input_number.blind_high_brightness_threshold
        for: "00:01:00"
      - trigger: numeric_state
        entity_id: sensor.front_garden_motion_illuminance
        below: input_number.blind_low_brightness_threshold
        for: "00:05:00"
    conditions:
      - condition: state
        entity_id: input_boolean.enable_office_blind_automations
        state: "on"
    actions:
      - action: script.office_set_blinds_for_brightness
    mode: queued
    max: 5
```

---

## Temperature/Fan Automation (Lines 293-393)

### Issues:
1. **Three separate trigger thresholds** (26°C, 29°C, 31°C) in one automation
2. **Inconsistent notification logic**
3. **No actionable notification handler**

### Improvements:

**1. Add Missing Handler:**

```yaml
automation:
  - id: "switch_on_office_fan_handler"
    alias: "Office: Handle Fan Notification Action"
    triggers:
      - trigger: event
        event_type: mobile_app_notification_action
        event_data:
          action: "switch_on_office_fan"
    actions:
      - parallel:
          - action: script.send_to_home_log
            data:
              message: "User confirmed fan turn on via notification."
              title: "🏢 Office"
          - action: switch.turn_on
            target:
              entity_id: switch.office_fan
    mode: single
```

**2. Simplify Temperature Logic:**

```yaml
input_number:
  office_fan_auto_threshold:
    name: Office Fan Auto-On Threshold
    min: 20
    max: 35
    step: 0.5
    initial: 26
    unit_of_measurement: "°C"

  office_fan_notify_threshold:
    name: Office Fan Notify Threshold
    min: 20
    max: 35
    step: 0.5
    initial: 29
    unit_of_measurement: "°C"

  office_fan_emergency_threshold:
    name: Office Fan Emergency Threshold
    min: 20
    max: 35
    step: 0.5
    initial: 31
    unit_of_measurement: "°C"

automation:
  - id: "1622584959878"
    alias: "Office: Temperature Management"
    triggers:
      - trigger: numeric_state
        entity_id: sensor.office_area_mean_temperature
        above: input_number.office_fan_auto_threshold
        for: "00:01:00"
    conditions:
      - condition: state
        entity_id: switch.office_fan
        state: "off"
    actions:
      - choose:
          # Emergency: Just turn on
          - conditions:
              - condition: numeric_state
                entity_id: sensor.office_area_mean_temperature
                above: input_number.office_fan_emergency_threshold
            sequence:
              - parallel:
                  - action: script.send_to_home_log
                    data:
                      message: "🚨♨️ Emergency! Temperature {{ states('sensor.office_area_mean_temperature') }}°C. Turning fan on."
                      title: "🏢 Office"
                      log_level: "Normal"
                  - action: switch.turn_on
                    target:
                      entity_id: switch.office_fan

          # High: Ask user
          - conditions:
              - condition: numeric_state
                entity_id: sensor.office_area_mean_temperature
                above: input_number.office_fan_notify_threshold
            sequence:
              - action: script.send_actionable_notification_with_2_buttons
                data:
                  message: "Temperature is {{ states('sensor.office_area_mean_temperature') }}°C. Turn on fan?"
                  title: "♨️🏢 Office High Temperature"
                  people:
                    entity_id:
                      - person.danny
                  action1_title: "Yes"
                  action1_name: switch_on_office_fan
                  action2_title: "No"
                  action2_name: ignore

          # Normal: Auto if home during day
          - conditions:
              - condition: state
                entity_id: group.tracked_people
                state: "home"
              - condition: time
                after: "08:30:00"
                before: "22:00:00"
            sequence:
              - parallel:
                  - action: script.send_to_home_log
                    data:
                      message: "♨️ Temperature {{ states('sensor.office_area_mean_temperature') }}°C. Turning fan on."
                      title: "🏢 Office"
                  - action: switch.turn_on
                    target:
                      entity_id: switch.office_fan
    mode: single
```

---

## Computer Automations (Lines 394-510)

### Issues:
1. **Inconsistent delay times** (1 min, 5 min, 10 min)
2. **Script called but not defined** (`ecoflow_office_turn_off_plug`)
3. **Multiple automations for same trigger**

### Improvements:

**1. Add Missing Scripts:**

```yaml
script:
  ecoflow_office_turn_off_plug:
    alias: EcoFlow Office Turn Off Plug
    sequence:
      - condition: state
        entity_id: switch.ecoflow_office_plug
        state: "on"
      - action: script.send_to_home_log
        data:
          message: "🔌 Turning off EcoFlow office plug"
          log_level: "Debug"
      - action: switch.turn_off
        target:
          entity_id: switch.ecoflow_office_plug
    mode: single
```

**2. Consolidate Computer Off Automations:**

Instead of 3 separate automations (lines 415, 449, 478), create one with better logic:

```yaml
automation:
  - id: "1606256309890"
    alias: "Office: Computer State Changed"
    triggers:
      - trigger: state
        entity_id: group.jd_computer
        from: "home"
        to: "not_home"
    conditions: []
    actions:
      # Immediate actions (within 1 minute)
      - if:
          - condition: state
            entity_id: group.dannys_work_computer
            state: "not_home"
        then:
          - action: script.send_to_home_log
            data:
              message: "Computer turned off. Turning monitor light off."
              title: "🏢 Office"

      # After 5 minutes - close blinds if daytime
      - wait_for_trigger:
          - trigger: state
            entity_id: group.jd_computer
            to: "not_home"
            for: "00:05:00"
        timeout: "00:05:00"
        continue_on_timeout: false

      - if:
          - condition: state
            entity_id: input_boolean.enable_office_blind_automations
            state: "on"
          - condition: sun
            after: sunrise
          - condition: sun
            before: sunset
          - condition: time
            after: "08:00:30"
        then:
          - action: script.office_open_blinds

      # After 10 minutes - power down accessories
      - wait_for_trigger:
          - trigger: state
            entity_id: group.jd_computer
            to: "not_home"
            for: "00:10:00"
        timeout: "00:05:00"
        continue_on_timeout: false

      - parallel:
          - action: script.send_to_home_log
            data:
              message: "Computer off for 10+ min. Powering down accessories."
              title: "💻 Computer"
          - action: script.office_turn_off_backup_drive
          - action: script.ecoflow_office_turn_off_plug
    mode: restart
```

---

## Scene Definitions (Lines 1085-1442)

### Issues:
1. **Hardcoded attributes** in scenes
2. **Scenes in package file** instead of global scenes.yaml
3. **Duplicate metadata** (effect_list, supported_features repeated)

### Recommendations:

**Option 1: Keep in package but simplify**

```yaml
scene:
  - id: "1600795089307"
    name: "Office: Main Light On"
    entities:
      light.office_2:
        state: "on"
        brightness: 255
        color_temp: 285
      light.office_3:
        state: "on"
        brightness: 255
        color_temp: 285
    icon: mdi:lightbulb

  - id: "1606247204381"
    name: "Office: Main Light Off"
    entities:
      light.office_2:
        state: "off"
      light.office_3:
        state: "off"
      light.office_4:
        state: "off"
```

Remove `effect_list`, `supported_features`, `friendly_name`, `min_mireds`, `max_mireds` - these are static attributes that don't need to be in scenes.

**Option 2: Move to global scenes.yaml**

Move scene definitions to `/homeassistant-config/scenes.yaml` for better organization.

---

## Minor Issues & Best Practices

### 1. **Hardcoded Device IDs**
**Lines 1011, 1035:**
```yaml
device_id: 589ffdf441f33bc8f72a6f9faf153da2
```

**Fix:** Use entity_id instead or add comment explaining what device this is:
```yaml
# Remote: Office MQTT Button (589ffdf441f33bc8f72a6f9faf153da2)
```

### 2. **Repeated Clock Emoji Template**
**Lines 543, 566, 580, etc.:**
```yaml
:clock{{ now().strftime('%I') | int }}{% if now().minute | int > 25 and now().minute | int < 35 %}30{% else %}{% endif %}:
```

**Fix:** Create a template sensor or remove (not adding value):
```yaml
message: "Opening blinds at {{ now().strftime('%H:%M') }}."
```

### 3. **Missing `mode:` on Some Automations**

Add explicit mode to all automations:
```yaml
mode: single  # or queued, restart, parallel
```

### 4. **Inconsistent Log Titles**

Some use `:office:`, some use "🏢 Office". Standardize:
```yaml
title: "🏢 Office"  # Preferred (emoji + text)
```

### 5. **Script Validation**
**Line 1448-1461:**
```yaml
script:
  office_turn_off_backup_drive:
    sequence:
      - and:  # ❌ Invalid syntax
          - condition: state
```

**Fix:**
```yaml
script:
  office_turn_off_backup_drive:
    sequence:
      - condition: and  # ✅ Correct
        conditions:
          - condition: state
            entity_id: switch.external_hdd
            state: "on"
          - condition: state
            entity_id: group.jd_computer
            state: "not_home"
      - action: script.send_to_home_log
        data:
          message: "💾 Turning off external HDD"
          log_level: "Debug"
      - action: switch.turn_off
        target:
          entity_id: switch.external_hdd
```

---

## Proposed File Structure

Split the 1629-line file into:

### `/packages/rooms/office/office.yaml` (Main Config)
```yaml
# Helper entities
input_boolean:
  enable_office_motion_triggers:
    name: Enable Office Motion Triggers
    icon: mdi:motion-sensor
  enable_office_blind_automations:
    name: Enable Office Blind Automations
    icon: mdi:blinds

input_number:
  office_light_level_threshold:
    name: Office Light Level Threshold
    min: 0
    max: 500
    step: 10
    unit_of_measurement: lux

timer:
  office_lights_off:
    name: Office Lights Off Timer
    duration: "00:01:00"

# Include other files
automation: !include_dir_merge_list office/automations/
script: !include_dir_merge_named office/scripts/
scene: !include_dir_merge_list office/scenes/
```

### `/packages/rooms/office/automations/`
- `motion.yaml` - Motion detection
- `blinds.yaml` - Blind control
- `climate.yaml` - Temperature/fan
- `computer.yaml` - Computer state
- `lights.yaml` - Light control

### `/packages/rooms/office/scripts/`
- `lights.yaml`
- `blinds.yaml`
- `computer.yaml`

### `/packages/rooms/office/scenes/`
- `office_scenes.yaml`

---

## Priority Action Items

### High Priority (Fix Now):
1. ✅ Fix duplicate automation ID (line 587 vs 627)
2. ✅ Fix timer duration message mismatch
3. ✅ Fix incorrect "bright" message (should be "dark")
4. ✅ Add missing notification handler for `switch_on_office_fan`
5. ✅ Fix script syntax error (line 1448)

### Medium Priority (This Week):
1. 🔄 Consolidate motion detection automations
2. 🔄 Create centralized blind management script
3. 🔄 Add missing entity definitions
4. 🔄 Simplify temperature logic

### Low Priority (Nice to Have):
1. 📋 Split into multiple files
2. 📋 Remove hardcoded scene attributes
3. 📋 Standardize emoji usage
4. 📋 Add script documentation

---

## Testing Checklist

After making changes, test:
- [ ] Motion detection triggers lights correctly
- [ ] Lights turn off after timer expires
- [ ] Blinds adjust based on sun position
- [ ] Fan turns on at correct temperatures
- [ ] Computer off sequence works (1 min, 5 min, 10 min)
- [ ] Notification actions work
- [ ] All helpers are accessible in UI
- [ ] No errors in Home Assistant logs

---

## Estimated Effort

- **Quick fixes** (critical issues): 30 minutes
- **Motion refactor**: 2 hours
- **Blind refactor**: 3 hours
- **File splitting**: 2 hours
- **Testing**: 2 hours

**Total: ~10 hours** for complete refactor

---

## Questions for User

1. Are `group.jd_computer` and `group.dannys_work_computer` defined elsewhere?
2. Should scenes stay in package or move to global scenes.yaml?
3. What is `switch.ecoflow_office_plug` - should it be defined?
4. Do you want to keep history_stats sensors or move to InfluxDB/Grafana?
5. Is the remote button (device_id: 589ff...) documented anywhere?

---

This review provides a roadmap for improving the office package while maintaining all existing functionality.
