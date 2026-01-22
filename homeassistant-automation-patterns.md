# Home Assistant Automation Patterns & Reference

**Last Updated:** 2026-01-22
**Scope:** Automation IDs, Patterns, Consolidation, Real-world Examples

---

## Automation ID Uniqueness Validation

**Purpose:** Ensure all new automation IDs are unique across the entire configuration before creation

**Why It Matters:**
- Home Assistant requires unique automation IDs
- Duplicate IDs cause automation failures and configuration errors
- Manual checking is error-prone
- Systematic validation prevents issues at creation time

### Implementation Pattern (Grep-Based)

**Approach:** Use Grep tool to validate candidate automation IDs before creation

**Workflow:**
1. Generate random 13-digit ID candidate
2. Run Grep search to check for existing ID
3. If unique, create automation with verified ID
4. If duplicate found, retry with new ID (max 3 attempts)

### Automation ID Format Reference

**Format:** 13-digit random numbers
```
Examples:
- "1625924056779" (existing, from message_callback.yaml)
- "1736794523847" (example candidate)
- "1234567890123" (example candidate)
```

**Generation Method:**
```
Using random number in range: 1000000000000 to 9999999999999
Collision probability: ~1 in 9 trillion (negligible)
```

### Implementation Steps

**When Creating New Automations:**
1. Generate candidate ID: `random(1000000000000, 9999999999999)`
2. Search for duplicates using Grep pattern: `id: "[candidate_id]"`
3. If `files_with_matches` returns empty, ID is unique → proceed
4. If matches found, generate new ID and retry (max 3 attempts)
5. Create automation with verified unique ID

**Token Cost:** ~50-100 tokens per Grep search (highly efficient)

### Existing Automation IDs Reference

For verification, here are known automation IDs in the configuration:
- `message_callback.yaml`: `"1625924056779"` (Mobile Notification Action Router)
- `bedroom2.yaml`: Various circadian lighting automations (PR #175)
- `living_room.yaml`: 35+ automations with unique IDs

---

## Notable Automation Patterns

### 1. Dynamic Illuminance Thresholds

Living room motion automation changes brightness thresholds based on Terina's work laptop:
- Laptop ON: 81 and 65 lux (need brighter light)
- Laptop OFF: 30 and 25 lux (okay with dimmer light)

**Pattern:** Use nested conditions or variables to dynamically adjust thresholds

### 2. Sophisticated Bed Occupancy

- 4-point pressure sensors (ADS1115)
- BME680 air quality sensor for breathing detection
- Custom IAQ calculation
- Distinguishes between "in bed" and "asleep"

### 3. Multi-Layer Safety Interlocks

- Window contact check before closing blinds (3-hour wait)
- Door closure verification before arming alarm
- Heating state checks before adjusting radiators
- Motion detection disabled during "Naughty Step Mode"

### 4. Solar-Aware Scheduling

- Forecast-based scheduling (tomorrow's generation)
- Rate-aware switching (Agile tariff prices)
- Battery SoC monitoring
- Inverter mode validation

### 5. Context-Aware Automation

- Music playback follows Danny's BLE location
- Different automation behaviors based on home mode
- Alarm automations consider time of day
- Kitchen light levels adjust based on laptop status

### 6. Fake Presence During Holiday

Random light selection during away periods:
- Downstairs: up to 3 lights ON simultaneously
- Upstairs: 1 light ON
- 15-minute intervals from sunset to 22:00
- Only when far away and armed_away

### 7. NFC Tag Integration

- **Front door tag** → unlock + log
- **Bedroom right tag** → turn everything off
- User context preserved (logs who scanned)

---

## Real-World Consolidation Examples

### Motion Detection with Context-Aware Responses

Motion detection often requires different actions based on context (room brightness, occupant presence, etc.). Use multi-branch automations with descriptive aliases:

```yaml
automation:
  - id: "1736794523847"
    alias: "Room: Motion Detected"
    description: "Multi-branch automation with different responses based on room state"
    triggers:
      - trigger: state
        entity_id: binary_sensor.room_motion
        to: "on"
    conditions:
      - condition: state
        entity_id: input_boolean.enable_room_motion_triggers
        state: "on"
    actions:
      - choose:
          # Branch 1: Dark room - turn on lights normally
          - alias: "Room Dark - Turn Lights On"
            conditions:
              - condition: numeric_state
                entity_id: sensor.room_illuminance
                below: 30
            sequence:
              - parallel:
                  - action: script.send_to_home_log
                    data:
                      message: "🐾 Motion detected. Room dark. Turning lights on."
                      title: "Room Name"
                  - action: scene.turn_on
                    target:
                      entity_id: scene.room_lights_on

          # Branch 2: Bright room - Flash lights as motion signal
          - alias: "Room Bright - Flash Motion Signal"
            conditions:
              - condition: numeric_state
                entity_id: sensor.room_illuminance
                above: 30
            sequence:
              - parallel:
                  - action: script.send_to_home_log
                    data:
                      message: >-
                        🐾 Motion detected. Room already bright ({{ states('sensor.room_illuminance') }} lux).
                        Flashing lights as motion signal. Yellow flash indicates motion but no action needed.
                      title: "Room Name"
                      log_level: "Debug"
                  - action: script.flash_lights_yellow
                    data: {}

        default:
          - action: script.send_to_home_log
            data:
              message: "🐾 Motion detected but no matching conditions."
              title: "Room Name"
              log_level: "Debug"
    mode: queued
    max: 10
```

**Key Points:**
- Visual flash signals (yellow, red) provide user feedback when lights don't turn on
- Append context to log messages rather than replacing original message
- Use descriptive aliases for each branch (helps with automation traces)
- Flash signals are intentional features, not bugs

### Log Message Best Practice - Append vs Replace

When adding clarification to an automation's log message, **append new information** rather than replacing the original detailed message:

```yaml
# WRONG - Replaces informative message with less detail
message: "Motion detected - room bright, flashing lights as signal."

# CORRECT - Appends clarification while preserving context
message: >-
  🐾 Motion detected and it's dark
  ({{ states('sensor.apollo_r_pro_1_w_ef755c_ltr390_light') }} &
  {{ states('sensor.living_room_motion_illuminance') }} <
  {{ states('input_number.living_room_light_level_threshold') }})
  and Terina's work computer is on. Flashing lights as signal (room bright enough).
```

**Rationale:** The original message provides sensor values and thresholds that help debug automation behavior. Appending clarification preserves this diagnostic information while explaining intent.

---

## Common Automation Patterns

### 1. Motion-Based Lighting with Illuminance

```yaml
automation:
  - alias: "Room: Motion Detected"
    triggers:
      - trigger: state
        entity_id: binary_sensor.room_motion
        to: "on"
    conditions:
      - condition: state
        entity_id: input_boolean.enable_room_motion_triggers
        state: "on"
    actions:
      - choose:
          - conditions:
              - condition: numeric_state
                entity_id: sensor.room_illuminance
                below: input_number.room_light_threshold
            sequence:
              - parallel:
                  - action: script.send_to_home_log
                    data:
                      message: "Motion detected. Turning lights on."
                      title: "Room Name"
                      log_level: "Debug"
                  - action: scene.turn_on
                    target:
                      entity_id: scene.room_lights_on
                    data:
                      transition: 1
      - action: timer.cancel
        target:
          entity_id: timer.room_lights_off
    mode: queued
    max: 10
```

**Key Pattern Elements:**
- Enable/disable toggle with `input_boolean.enable_*`
- Illuminance threshold check with `input_number.*_threshold`
- Parallel execution for logging + action
- Timer cancellation to prevent premature turn-off
- `mode: queued` with `max: 10` for handling rapid triggers

### 2. No Motion Timer Pattern

```yaml
automation:
  - alias: "Room: No Motion"
    triggers:
      - trigger: state
        entity_id: binary_sensor.room_motion
        to: "off"
    conditions:
      - condition: state
        entity_id: input_boolean.enable_room_motion_triggers
        state: "on"
    actions:
      - parallel:
          - action: script.send_to_home_log
            data:
              message: "No motion. Starting timer."
          - action: timer.start
            target:
              entity_id: timer.room_lights_off
            data:
              duration: "00:05:00"
```

### 3. Trigger ID Branching Pattern

Consolidate multiple automations with different responses using trigger IDs:

```yaml
automation:
  - id: "porch_motion_handler"
    alias: "Porch: Motion Detected (On/Off)"
    triggers:
      - trigger: state
        entity_id: binary_sensor.porch_motion_occupancy
        to: "on"
        for: "00:02:00"
        id: motion_on
      - trigger: state
        entity_id: binary_sensor.porch_motion_occupancy
        to: "off"
        for: "00:01:00"
        id: motion_off
    actions:
      - choose:
          - conditions:
              - condition: trigger
                id: motion_on
            sequence:
              - action: light.turn_on
                target:
                  entity_id: light.porch
          - conditions:
              - condition: trigger
                id: motion_off
            sequence:
              - action: timer.start
                target:
                  entity_id: timer.porch_light_off
```

**Benefits:**
- Consolidates 2+ automations into 1
- Clearer logic with explicit trigger branching
- Reduces automation count and improves maintainability

### 4. Rate/Cost-Based Automation

```yaml
automation:
  - alias: "Device: Check Cost Before Running"
    sequence:
      - variables:
          current_rate: "{{ states('sensor.octopus_energy_electricity_current_rate') }}"
      - choose:
          - conditions:
              - condition: template
                value_template: "{{ current_rate | float <= 0 }}"
            sequence:
              - action: switch.turn_on
                target:
                  entity_id: switch.device
          - conditions:
              - condition: template
                value_template: "{{ current_rate | float > 0 }}"
            sequence:
              - action: script.send_to_home_log
                data:
                  message: "Rate too high. Not running device."
```

### 5. Home Mode Conditional Logic

```yaml
automation:
  - alias: "Automation with Home Mode Check"
    conditions:
      - condition: state
        entity_id: input_select.home_mode
        state: "Normal"
      - condition: not
        conditions:
          - condition: state
            entity_id: input_select.home_mode
            state: "Holiday"
```

### 6. Temperature Automation with Multiple Thresholds

When using multiple temperature thresholds, order conditions by priority (first match wins):

```yaml
automation:
  - alias: "Device: Temperature Management"
    triggers:
      - trigger: numeric_state
        entity_id: sensor.temperature
        above: 26  # Lowest threshold triggers automation
      - trigger: numeric_state
        entity_id: sensor.temperature
        above: 29
        for: "00:01:00"
      - trigger: numeric_state
        entity_id: sensor.temperature
        above: 31
        for: "00:01:00"
    conditions:
      - condition: state
        entity_id: switch.device
        state: "off"
    actions:
      - choose:
          # Priority 1: Time/presence conditions (if specified)
          - conditions:
              - condition: state
                entity_id: group.people
                state: "home"
              - condition: time
                after: "08:30:00"
                before: "22:00:00"
            sequence:
              - action: script.send_to_home_log
                data:
                  message: "Temperature high ({{ states('sensor.temperature') }}°C). Auto-turning on."
              - action: switch.turn_on
                target:
                  entity_id: switch.device

          # Priority 2: Highest temperature (emergency)
          - conditions:
              - condition: numeric_state
                entity_id: sensor.temperature
                above: 31
            sequence:
              - action: script.send_to_home_log
                data:
                  message: "🚨 Emergency! Temperature above 31°C. Forcing on."
                  log_level: "Normal"
              - action: switch.turn_on
                target:
                  entity_id: switch.device

          # Priority 3: Medium temperature (notify)
          - conditions:
              - condition: numeric_state
                entity_id: sensor.temperature
                above: 29
            sequence:
              - action: script.send_direct_notification
                data:
                  message: "Temperature {{ states('sensor.temperature') }}°C. Turn on device?"
```

**Key Principles:**
- First condition in `choose:` wins - order matters!
- Put time/presence conditions first if they should override temperature
- Order temperature checks from highest to lowest after priority conditions
- Use `for:` duration on triggers to prevent rapid cycling
