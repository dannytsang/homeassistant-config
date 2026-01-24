# Home Assistant Automation YAML Reference

**Source:** https://www.home-assistant.io/docs/automation/yaml/
**Date:** 2026-01-22
**Purpose:** Comprehensive guide to writing automations in YAML format

---

## Automation Fundamentals

Automations are sequences of actions triggered by events, state changes, or time-based events. They can be created via UI or written directly in YAML.

### Basic Structure

```yaml
automation:
  - id: "1234567890001"
    alias: "Human-readable name"
    description: "What this automation does"

    triggers:
      - trigger: state              # Trigger type
        entity_id: entity.name
        to: "on"

    conditions:
      - condition: state
        entity_id: entity.other
        state: "on"

    actions:
      - action: service.name
        target:
          entity_id: entity.target
        data:
          param: value
```

### Required vs Optional

**REQUIRED:**
- `triggers:` - What starts the automation
- `actions:` - What happens when triggered

**OPTIONAL:**
- `id:` - Unique identifier (required for UI editing)
- `alias:` - Friendly name
- `description:` - Documentation
- `conditions:` - Additional requirements
- `variables:` - Template variables available in conditions/actions
- `initial_state:` - Startup behavior

### Automatic Properties

Home Assistant automatically adds:
- `mode: single` (default)
- `conditions: []` (no conditions = always execute)
- `variables:` (optional, empty by default)

---

## Triggers

Triggers are the events that start the automation. Multiple triggers are OR'd together (any trigger fires = automation starts).

### 1. State Trigger

Execute when entity state changes:

```yaml
triggers:
  - trigger: state
    entity_id: binary_sensor.motion
    to: "on"
    for: "00:00:30"              # Optional: wait 30s of continuous state
```

**With "from" condition (specific state transition):**

```yaml
triggers:
  - trigger: state
    entity_id: light.kitchen
    from: "off"
    to: "on"
```

**Multiple entities:**

```yaml
triggers:
  - trigger: state
    entity_id:
      - binary_sensor.motion_1
      - binary_sensor.motion_2
      - binary_sensor.motion_3
    to: "on"
```

**State value checks:**
- `to: "on"` - New state is "on"
- `to: "off"` - New state is "off"
- `from: "unavailable"` - Old state was unavailable
- `attribute: brightness` - Check specific attribute (not just state)

### 2. Numeric State Trigger

Execute when numeric entity crosses threshold:

```yaml
triggers:
  - trigger: numeric_state
    entity_id: sensor.temperature
    above: 25              # Trigger when temp > 25
    below: 35              # Trigger when temp < 35
    for: "00:05:00"        # Must be in range for 5 minutes
```

**Variants:**

```yaml
# Only check above
- trigger: numeric_state
  entity_id: sensor.battery
  below: 20               # Low battery alert

# Only check below
- trigger: numeric_state
  entity_id: sensor.battery
  above: 80               # High battery

# Check attribute instead of state
- trigger: numeric_state
  entity_id: light.lamp
  attribute: brightness
  above: 100              # When brightness > 100
```

### 3. Time Trigger

Execute at specific time:

```yaml
# At specific time daily
- trigger: time
  at: "14:30:00"

# Multiple times
- trigger: time
  at:
    - "08:00:00"
    - "14:00:00"
    - "20:00:00"
```

**Time pattern (more flexible):**

```yaml
# Every 30 minutes
- trigger: time_pattern
  minutes: "*/30"         # 0, 30

# Every hour at :15
- trigger: time_pattern
  minutes: 15

# Every Monday at 8 AM
- trigger: time_pattern
  weekday: mon
  hour: 8
  minute: 0

# Valid patterns: hour, minute, second, day (month), month, weekday
# Use */N for every N, 0-4 for range, comma for list
```

### 4. Sun Trigger

Execute based on solar events:

```yaml
# At sunrise
- trigger: sun
  event: sunrise
  id: morning

# 30 minutes before sunset
- trigger: sun
  event: sunset
  offset: "-00:30:00"
  id: pre_sunset

# 1 hour after sunset
- trigger: sun
  event: sunset
  offset: "01:00:00"
  id: post_sunset
```

**Sunrise/Sunset with offset:**
- Positive offset: after event
- Negative offset: before event
- Format: `HH:MM:SS`

### 5. Event Trigger

Execute when custom event fires:

```yaml
# Any event of type
- trigger: event
  event_type: timer.finished
  event_data:
    entity_id: timer.kitchen

# Mobile app notification action
- trigger: event
  event_type: mobile_app_notification_action
  event_data:
    action: door_unlocked

# Custom event
- trigger: event
  event_type: my_custom_event
  event_data:
    device: "kitchen"
```

### 6. MQTT Trigger

Execute on MQTT message:

```yaml
- trigger: mqtt
  topic: home/kitchen/motion
  payload: "on"
  value_template: "{{ value }}"  # Optional: transform payload
```

### 7. Webhook Trigger

Execute from HTTP POST request:

```yaml
- trigger: webhook
  webhook_id: my_webhook_id

# Access webhook data in actions
# trigger.json - JSON payload
# trigger.data - Form data
# trigger.query - Query parameters
```

### 8. Home Assistant Trigger

Execute on HA events:

```yaml
# Home Assistant startup
- trigger: homeassistant
  event: start

# Configuration reload
- trigger: homeassistant
  event: shutdown
```

### 9. Template Trigger

Execute when template evaluates true:

```yaml
- trigger: template
  value_template: "{{ states('sensor.temperature') | float(0) > 25 }}"

# With ID for branching
- trigger: template
  value_template: "{{ is_state('light.kitchen', 'on') }}"
  id: lights_on
```

### 10. Device Trigger

Execute from device automation:

```yaml
- trigger: device
  device_id: device_abc123
  domain: motion_sensor
  type: motion
  subtype: motion_detected
```

### 11. Conversation Trigger

Execute from voice assistant:

```yaml
- trigger: conversation
  command: "turn on the lights"
```

### Trigger with IDs (for branching)

```yaml
triggers:
  - trigger: state
    entity_id: binary_sensor.motion
    to: "on"
    id: motion_detected
  - trigger: state
    entity_id: binary_sensor.motion
    to: "off"
    id: motion_stopped
  - trigger: time
    at: "23:00:00"
    id: nighttime

actions:
  - choose:
      - conditions:
          - condition: trigger
            id: motion_detected
        sequence:
          - action: light.turn_on
      - conditions:
          - condition: trigger
            id: motion_stopped
        sequence:
          - action: light.turn_off
      - conditions:
          - condition: trigger
            id: nighttime
        sequence:
          - action: light.turn_on
            data:
              brightness_pct: 25
```

---

## Conditions

Conditions are requirements that must be true to execute actions. If trigger fires but conditions fail, automation stops (no actions run).

### ⚠️ CRITICAL: Condition Syntax Constraints

**Condition objects support `alias:` parameter ONLY**

Condition objects do NOT support `description:` parameter. Using `description:` will cause syntax errors.

```yaml
# ❌ WRONG: description not supported on conditions
conditions:
  - alias: "Motion detected"
    description: "This checks for motion"  # INVALID SYNTAX
    condition: state
    entity_id: binary_sensor.motion
    state: "on"

# ✅ CORRECT: Use alias only
conditions:
  - alias: "Motion detected - bright room"
    condition: state
    entity_id: binary_sensor.motion
    state: "on"
```

**Supported Condition Parameters:**
- `alias:` - Brief label for documentation (SUPPORTED)
- `condition:` - Condition type (REQUIRED)
- `entity_id:`, `state:`, etc. - Condition-specific parameters
- `description:` - NOT SUPPORTED (will cause syntax error)

### State Condition

```yaml
conditions:
  - condition: state
    entity_id: input_boolean.enable_motion_triggers
    state: "on"

# Multiple states (OR'd)
- condition: state
  entity_id: light.kitchen
  state:
    - "on"
    - "unavailable"

# Match value with attribute
- condition: state
  entity_id: light.kitchen
  attribute: brightness
    state: 255
```

### Numeric State Condition

```yaml
conditions:
  # Check above threshold
  - condition: numeric_state
    entity_id: sensor.temperature
    above: 25

  # Check range
  - condition: numeric_state
    entity_id: sensor.temperature
    above: 20
    below: 30

  # Check attribute
  - condition: numeric_state
    entity_id: light.lamp
    attribute: brightness
    below: 100
```

### Time Condition

```yaml
conditions:
  # Specific time of day
  - condition: time
    after: "07:00:00"
    before: "22:00:00"

  # Specific days
  - condition: time
    weekday:
      - mon
      - tue
      - wed
      - thu
      - fri

  # Date range
  - condition: time
    after: "2026-01-01"
    before: "2026-12-31"
```

### Sun Condition

```yaml
conditions:
  # After sunrise
  - condition: sun
    after: sunrise

  # Before sunset
  - condition: sun
    before: sunset

  # After sunset with offset
  - condition: sun
    after: sunset
    after_offset: "01:00:00"
```

### Template Condition

```yaml
conditions:
  - condition: template
    value_template: "{{ states('sensor.temperature') | float(0) > 25 }}"

  # Complex logic
  - condition: template
    value_template: >
      {% set temp = states('sensor.temperature') | float(0) %}
      {% set humidity = states('sensor.humidity') | float(0) %}
      {{ temp > 25 and humidity > 60 }}
```

### Zone Condition

```yaml
conditions:
  - condition: zone
    entity_id: person.danny
    zone: zone.home
```

### Device Condition

```yaml
conditions:
  - condition: device
    device_id: device_abc123
    domain: motion_sensor
    type: motion
    subtype: motion_detected
```

### Trigger Condition (with trigger IDs)

```yaml
conditions:
  - condition: trigger
    id: motion_detected
```

### And/Or/Not Conditions

```yaml
conditions:
  # AND (all must be true)
  - condition: state
    entity_id: light.kitchen
    state: "on"
  - condition: numeric_state
    entity_id: sensor.temperature
    above: 25

  # OR (any one can be true)
  - or:
      - condition: state
        entity_id: light.kitchen
        state: "on"
      - condition: state
        entity_id: light.bedroom
        state: "on"

  # NOT (condition must be false)
  - not:
      - condition: state
        entity_id: switch.maintenance_mode
        state: "on"

  # Complex nesting
  - and:
      - condition: state
        entity_id: input_boolean.enable_motion
        state: "on"
      - or:
          - condition: time
            after: "22:00:00"
          - condition: time
            before: "06:00:00"
      - not:
          - condition: state
            entity_id: light.kitchen
            state: "off"
```

---

## Actions

Actions are the sequence of operations performed when trigger + conditions are met.

### ⚠️ CRITICAL: Entity Domain Validation

**Action domain MUST match target entity domain**

When calling actions on entities, the action domain (first part before `.`) MUST match the target entity domain. Mismatches will cause logic errors or silent failures.

```yaml
# ❌ WRONG: Action domain doesn't match entity domain
actions:
  - action: light.turn_on
    target:
      entity_id: input_boolean.some_bool  # Wrong: boolean, not light

  - action: switch.turn_off
    target:
      entity_id: light.some_light  # Wrong: light, not switch

# ✅ CORRECT: Action domain matches entity domain
actions:
  - action: light.turn_on
    target:
      entity_id: light.some_light  # Correct: light matches light

  - action: input_boolean.turn_on
    target:
      entity_id: input_boolean.some_bool  # Correct: boolean matches boolean
```

**Domain Matching Rules:**
- `light.turn_on` → requires `light.*` entity_id
- `switch.turn_on` → requires `switch.*` entity_id
- `input_boolean.turn_on` → requires `input_boolean.*` entity_id
- `climate.set_temperature` → requires `climate.*` entity_id
- etc.

**Always verify:**
1. Entity exists in Home Assistant
2. Entity domain matches action domain
3. Entity supports the action being called

### Service Call Action

Call any Home Assistant service:

```yaml
actions:
  - action: light.turn_on
    target:
      entity_id: light.kitchen
    data:
      brightness_pct: 100
      color_temp_kelvin: 4000
```

**Multiple entities:**

```yaml
- action: light.turn_on
  target:
    entity_id:
      - light.kitchen
      - light.bedroom
      - light.living_room
  data:
    brightness_pct: 75
```

**Using groups:**

```yaml
- action: light.turn_off
  target:
    entity_id: group.all_lights
```

### Delay Action

```yaml
# Simple delay
- delay: "00:00:30"              # 30 seconds
- delay: "00:05:00"              # 5 minutes
- delay: "01:30:00"              # 1 hour 30 minutes

# Object format
- delay:
    hours: 1
    minutes: 30
    seconds: 15
    milliseconds: 500

# Template delay (dynamic)
- delay:
    seconds: "{{ states('input_number.delay_seconds') | int(5) }}"
```

### Condition Check in Action

Stop if condition fails:

```yaml
actions:
  - if:
      - condition: state
        entity_id: light.kitchen
        state: "on"
    then:
      - action: light.turn_off
        target:
          entity_id: light.kitchen
    else:
      - action: light.turn_on
        target:
          entity_id: light.kitchen
```

### Choose Action (Branching)

Execute first matching branch:

```yaml
actions:
  - choose:
      # Branch 1: Check first
      - conditions:
          - condition: numeric_state
            entity_id: sensor.temperature
            above: 30
        sequence:
          - action: climate.set_temperature
            data:
              temperature: 18

      # Branch 2: Check second
      - conditions:
          - condition: numeric_state
            entity_id: sensor.temperature
            below: 10
        sequence:
          - action: climate.set_temperature
            data:
              temperature: 24

    # Default: if no conditions match
    default:
      - action: script.send_to_home_log
        data:
          message: "Temperature normal"
```

**KEY PATTERN:** First matching condition wins - order matters!

### Parallel Action

Run multiple actions simultaneously:

```yaml
actions:
  - parallel:
      - action: light.turn_on
        target:
          entity_id: light.kitchen
      - action: script.send_to_home_log
        data:
          message: "Lights turned on"
      - action: switch.turn_on
        target:
          entity_id: switch.coffee_maker
```

### Script Execution

```yaml
actions:
  - action: script.my_script
    data:
      param1: "value1"
      param2: 42

  # With response variables
  - action: script.get_clock_emoji
    data:
      hour: "{{ now().strftime('%I') | int }}"
      minute: "{{ now().minute | int }}"
    response_variables:
      clock_emoji: "{{ response.emoji }}"

  - action: script.send_notification
    data:
      message: "{{ clock_emoji }} Notification"
```

### Repeat Action

```yaml
# Fixed iterations
- repeat:
    count: 5
    sequence:
      - action: light.turn_on
        target:
          entity_id: "light.lamp_{{ repeat.index }}"

# Loop over list
- repeat:
    for_each:
      - light.kitchen
      - light.bedroom
      - light.living_room
    sequence:
      - action: light.turn_on
        target:
          entity_id: "{{ repeat.item }}"

# While condition
- repeat:
    while:
      - condition: numeric_state
        entity_id: sensor.battery
        below: 50
    sequence:
      - action: script.charge_device
      - delay: "00:05:00"

# Until condition
- repeat:
    until:
      - condition: state
        entity_id: light.kitchen
        state: "on"
    sequence:
      - action: light.turn_on
        target:
          entity_id: light.kitchen
      - delay: "00:02:00"
```

### Wait Action

```yaml
# Wait for template
- wait_template: "{{ states('light.kitchen') == 'on' }}"
  timeout: "00:05:00"
  continue_on_timeout: false

# Wait for trigger
- wait_for_trigger:
    - trigger: state
      entity_id: binary_sensor.motion
      to: "on"
  timeout: "00:10:00"

# Access wait results
- if:
    - condition: template
      value_template: "{{ wait.completed }}"
  then:
    - action: script.send_notification
      data:
        message: "Condition met"
  else:
    - action: script.send_notification
      data:
        message: "Timeout reached"
```

### Stop Action

Halt automation sequence:

```yaml
actions:
  - if:
      - condition: state
        entity_id: input_boolean.maintenance_mode
        state: "on"
    then:
      - stop:
          response_variable: result
          value:
            status: "Script skipped - maintenance mode"
```

### Event Action

```yaml
actions:
  - action: events.fire
    event_type: my_custom_event
    event_data:
      device: "kitchen"
      status: "motion_detected"
      timestamp: "{{ now() }}"
```

### Scene Action

```yaml
actions:
  - action: scene.turn_on
    target:
      entity_id: scene.movie_time
    data:
      transition: 2  # Seconds for lights to adjust
```

### Notification Action

```yaml
actions:
  - action: notify.mobile_app_danny
    data:
      message: "Motion detected"
      title: "Kitchen Alert"
      data:
        actions:
          - action: UNLOCK_DOOR
            title: "Unlock"
          - action: LOCK_DOOR
            title: "Lock"
```

---

## Variables

Variables are defined once and available in templates within conditions and actions:

```yaml
automation:
  - id: "1234567890001"
    alias: "Temperature Check"

    variables:
      current_temp: "{{ states('sensor.temperature') | float(0) }}"
      target_temp: "{{ states('input_number.target_temperature') | float(20) }}"
      temp_difference: "{{ (current_temp - target_temp) | abs }}"

    triggers:
      - trigger: numeric_state
        entity_id: sensor.temperature
        above: 25

    actions:
      - action: script.send_notification
        data:
          message: "Current: {{ current_temp }}°, Target: {{ target_temp }}°, Diff: {{ temp_difference }}°"
```

**Variable scope:**
- Defined at automation level: available throughout
- Defined in conditional blocks: accessible after definition
- Defined in parallel blocks: only within that block

---

## Automation Modes

Control how automation behaves when triggered multiple times:

### Mode: single (default)

```yaml
mode: single  # Don't start if already running
```

**Behavior:**
- If automation is running and trigger fires again, issue warning
- New run doesn't start until current completes
- Use for: Simple automations, no re-entrance needed

### Mode: restart

```yaml
mode: restart  # Stop current run and restart
```

**Behavior:**
- Stop current execution
- Start new run from beginning
- Use for: Actions that should restart immediately

### Mode: queued

```yaml
mode: queued
max: 10  # Queue up to 10 runs
```

**Behavior:**
- Queue new runs (up to `max:`)
- Execute sequentially when previous finishes
- Use for: Motion sensors, frequent triggers (e.g., light adjustments)

### Mode: parallel

```yaml
mode: parallel
max: 5  # Allow up to 5 concurrent runs
```

**Behavior:**
- Run multiple instances simultaneously
- Each run independent
- Use for: Non-blocking operations, independent scenarios

---

## Initial State

Control automation startup behavior:

```yaml
initial_state: true   # Run automation on startup (default)
initial_state: false  # Don't run on startup (must be manually enabled)
```

**Use cases:**
- `false` for testing automations without affecting system
- `false` for experimental features being tested
- `true` for production automations

---

## Trace Configuration

Debug automation execution:

```yaml
automation:
  - id: "1234567890001"
    alias: "My Automation"
    stored_traces: 10  # Store last 10 traces (default: 5)

    triggers: [...]
    actions: [...]
```

**Access traces:**
- Home Assistant UI → Automations → Click automation → Traces tab
- Shows condition evaluation, action execution, timing
- Helps debug complex automations

---

## Practical Patterns

### Pattern 1: Motion-Triggered Lights with Context

```yaml
automation:
  - id: "1606158191303"
    alias: "Kitchen: Motion Detected"
    description: "Turn on lights when motion detected in dark kitchen"

    variables:
      is_dark: "{{ states('binary_sensor.kitchen_motion_dark') == 'on' }}"
      motion_enabled: "{{ states('input_boolean.enable_kitchen_motion_triggers') == 'on' }}"

    triggers:
      - trigger: state
        entity_id: binary_sensor.kitchen_area_motion
        to: "on"

    conditions:
      - condition: template
        value_template: "{{ motion_enabled and is_dark }}"

    actions:
      - parallel:
          - action: script.send_to_home_log
            data:
              message: "🐾 Motion detected. Turning lights on."
              title: "🧑‍🍳 Kitchen"
              log_level: "Debug"
          - action: scene.turn_on
            target:
              entity_id: scene.kitchen_lights_on
          - action: timer.cancel
            target:
              entity_id: timer.kitchen_lights_off

    mode: queued
    max: 10
```

### Pattern 2: Time-Based Trigger with Multiple Branches

```yaml
automation:
  - id: "1632156425622"
    alias: "Morning Routine"

    triggers:
      - trigger: time
        at: "06:00:00"
        id: weekday
      - trigger: time
        at: "08:00:00"
        id: weekend

    conditions:
      - condition: state
        entity_id: input_boolean.enable_automations
        state: "on"

    actions:
      - choose:
          - conditions:
              - condition: trigger
                id: weekday
              - condition: time
                weekday:
                  - mon
                  - tue
                  - wed
                  - thu
                  - fri
            sequence:
              - action: script.weekday_morning

          - conditions:
              - condition: trigger
                id: weekend
              - condition: time
                weekday:
                  - sat
                  - sun
            sequence:
              - action: script.weekend_morning
```

### Pattern 3: Rate-Limited Automation

```yaml
automation:
  - id: "1625924056779"
    alias: "Occupancy: Update Home Mode"

    triggers:
      - trigger: state
        entity_id: binary_sensor.people_home
        for: "00:05:00"  # Only trigger if state stable for 5 min

    conditions:
      - condition: state
        entity_id: input_select.home_mode
        state: "Normal"

    actions:
      - choose:
          - conditions:
              - condition: state
                entity_id: binary_sensor.people_home
                state: "on"
            sequence:
              - action: input_select.select_option
                target:
                  entity_id: input_select.home_mode
                data:
                  option: "Home"

          - conditions:
              - condition: state
                entity_id: binary_sensor.people_home
                state: "off"
            sequence:
              - action: input_select.select_option
                target:
                  entity_id: input_select.home_mode
                data:
                  option: "Away"

    mode: single
```

### Pattern 4: Complex Conditional Logic

```yaml
automation:
  - id: "1592062695452"
    alias: "Climate: Adjust Based on Conditions"

    variables:
      current_temp: "{{ states('sensor.temperature') | float(0) }}"
      target_temp: "{{ states('input_number.target_temperature') | float(20) }}"
      is_home: "{{ is_state('group.people', 'home') }}"
      is_night: "{{ now().hour < 6 or now().hour > 22 }}"

    triggers:
      - trigger: numeric_state
        entity_id: sensor.temperature
        above: 25
      - trigger: numeric_state
        entity_id: sensor.temperature
        below: 15
      - trigger: state
        entity_id: group.people
        to: "home"
      - trigger: state
        entity_id: group.people
        to: "not_home"

    actions:
      - choose:
          # Case 1: Too hot and people home
          - conditions:
              - condition: template
                value_template: "{{ current_temp > target_temp + 3 and is_home }}"
            sequence:
              - action: climate.set_temperature
                target:
                  entity_id: climate.thermostat
                data:
                  temperature: 18
              - action: script.send_notification
                data:
                  message: "Too warm. Cooling to 18°."

          # Case 2: Too cold and people home
          - conditions:
              - condition: template
                value_template: "{{ current_temp < target_temp - 3 and is_home }}"
            sequence:
              - action: climate.set_temperature
                target:
                  entity_id: climate.thermostat
                data:
                  temperature: 22
              - action: script.send_notification
                data:
                  message: "Too cold. Heating to 22°."

          # Case 3: Nobody home
          - conditions:
              - condition: template
                value_template: "{{ not is_home }}"
            sequence:
              - action: climate.set_temperature
                target:
                  entity_id: climate.thermostat
                data:
                  temperature: 16  # Away mode

          # Default: Normal operation
          default:
            - action: climate.set_temperature
              target:
                entity_id: climate.thermostat
              data:
                temperature: "{{ target_temp }}"

    mode: single
```

---

## Common Mistakes to Avoid

| Mistake | Problem | Solution |
|---------|---------|----------|
| Missing `id:` field | Can't edit in UI, debug traces unavailable | Always add unique 13-digit ID |
| `triggers:` is singular | YAML parsing error | Use `triggers:` (plural) |
| `conditions:` is singular | YAML parsing error | Use `conditions:` (plural) |
| `actions:` is singular | YAML parsing error | Use `actions:` (plural) |
| No quotes on single-line template | YAML parse error | Use `"{{ ... }}"` |
| State comparison without string match | Type mismatch (string vs number) | Use exact state string like `"on"` |
| Multiple conditions without AND/OR | Implicit AND confuses readability | Use explicit `- and:` or `- or:` |
| `for:` on wrong trigger type | Only works with state triggers | Check trigger type supports `for:` |
| Wrong entity_id format | Entity not found | Use lowercase, underscores: `light.kitchen` |
| Conditions checking impossible states | Automation never runs | Verify conditions can be true together |
| Using `action: service.` (deprecated) | May not work in newer versions | Use `action: domain.service` format |
| Too many parallel actions | Performance impact | Keep parallel actions lightweight |
| Infinite loops | System crash/high CPU | Add conditions to prevent re-triggering |
| Order-dependent choose branches | Wrong branch executes | Remember first match wins |

---

## Motion Detection Semantics

### Critical Rule: Timer Cancellation is Unconditional

Motion detection automation represents **"I am present"** — this semantic meaning has implications for timer/shutdown logic.

**Principle:** Any timer set to eventually turn off/dim/shutdown must be canceled unconditionally whenever motion is detected, regardless of whether the lighting conditions warrant adjustment.

### Correct Pattern: Unconditional Timer Cancellation

```yaml
automation:
  - id: "1234567890001"
    alias: "Motion Detected - Lights"
    triggers:
      - trigger: state
        entity_id: binary_sensor.motion
        to: "on"
        id: motion_on
    actions:
      - parallel:
          # Timer cancellation ALWAYS runs (unconditional)
          - action: script.cancel_room_timers

          # Light control runs conditionally
          - if:
              - condition: numeric_state
                entity_id: sensor.illuminance
                below: 100
            then:
              - action: light.turn_on
                target:
                  entity_id: light.room
              - action: script.send_to_home_log
                data:
                  title: "Room"
                  message: "Motion detected and dark"
                  log_level: "Debug"
```

**Why this matters:**
- User present → Don't turn off/dim lights
- User present → Cancel ALL pending shutdown operations
- Timer cancellation must happen ALWAYS, not conditionally
- Light adjustment can be conditional, timer cancellation cannot

### Wrong Pattern: Conditional Timer Cancellation

```yaml
# ❌ WRONG: Timer only canceled if conditions met
actions:
  - if:
      - condition: numeric_state
        entity_id: sensor.illuminance
        below: 100
    then:
      - action: script.cancel_room_timers  # Only runs if dark!
      - action: light.turn_on
        target:
          entity_id: light.room
```

**Problem:** If motion detected when it's bright, timer continues running. Pending shutdown timer will fire, dimming/turning off lights while user is still present.

### Implementation Pattern

```yaml
# Semantic separation of concerns:
actions:
  - parallel:
      # Layer 1: Presence indication (unconditional)
      - action: script.cancel_all_room_timers

      # Layer 2: Presence-based adjustments (conditional)
      - if: [conditions]
        then:
          - action: light.turn_on
            target:
              entity_id: light.room

      # Layer 3: Notifications (optional)
      - action: script.send_to_home_log
        data:
          message: "Motion detected"
```

---

## Best Practices

### DO:
✅ **Use descriptive aliases** - Clear what automation does
✅ **Add descriptions** - Document why automation exists
✅ **Use unique 13-digit IDs** - Enables UI editing
✅ **Test with stored_traces** - Easier debugging
✅ **Order choose branches by priority** - Most specific first
✅ **Use parallel for independent actions** - Light + logging together
✅ **Set appropriate mode** - Single for simple, queued for frequent
✅ **Use variables for repeated values** - DRY principle
✅ **Add logging** - Use send_to_home_log for visibility
✅ **Handle edge cases** - Unavailable sensors, etc.

### DON'T:
❌ **Mix deprecated service syntax** - Use action: domain.service format
❌ **Create impossible conditions** - Automation never runs if conditions can't both be true
❌ **Trigger on every small change** - Use `for:` duration to debounce
❌ **Create circular automations** - Automation A triggers B which triggers A
❌ **Ignore mode settings** - Wrong mode causes missed triggers or queue overflow
❌ **Use regex in state conditions** - Use template condition instead
❌ **Assume entity always available** - Always check for unavailable/unknown
❌ **Skip error handling** - Use `continue_on_error: true` for unreliable actions
❌ **Create massive choose blocks** - Consider multiple automations instead
❌ **Forget to test time-based automations** - May not trigger as expected

---

## Debugging Techniques

### 1. Enable Automation Traces

```yaml
automation:
  - id: "1234567890001"
    alias: "Debug Test"
    stored_traces: 50  # Store more traces for analysis
    triggers: [...]
    actions: [...]
```

**View traces in UI:**
- Settings → Automations & Scenes → Automations
- Click automation → Traces tab
- See each step execution with timing

### 2. Add Logging

```yaml
actions:
  - action: script.send_to_home_log
    data:
      message: "Debug: {{ variable_name }}"
      title: "Automation Name"
      log_level: "Debug"
```

### 3. Test Conditions Manually

Use Developer Tools → States to verify conditions:
- Check entity states match expected values
- Verify template conditions evaluate correctly
- Test time conditions work as expected

### 4. Use Template Conditions for Complex Logic

```yaml
conditions:
  - condition: template
    value_template: >
      {% set test = states('sensor.value') | float(0) %}
      {{ test > 10 and test < 30 }}
```

### 5. Check Recent Automations

Settings → Automations & Scenes → Automations:
- Recent automations column shows last run time
- Verify automation actually ran when expected

---

## Real-World Examples from Your Config

### Example 1: Kitchen Motion with Multiple Branches

```yaml
automation:
  - id: "kitchen_motion_lights_on"
    alias: "Kitchen: Motion Detected - Lights"
    description: "Consolidated motion detection for all kitchen light zones"
    triggers:
      - trigger: state
        entity_id:
          - binary_sensor.kitchen_area_motion
          - binary_sensor.kitchen_motion_ld2412_presence
          - binary_sensor.kitchen_motion_ld2450_presence
          - binary_sensor.kitchen_motion_2_occupancy
        to: "on"

    conditions:
      - condition: state
        entity_id: input_boolean.enable_kitchen_motion_triggers
        state: "on"

    actions:
      - choose:
          - alias: "Table Lights - Off or Dim"
            conditions:
              - or:
                  - condition: state
                    entity_id: light.kitchen_table_white
                    state: "off"
                  - and:
                      - condition: state
                        entity_id: light.kitchen_table_white
                        state: "on"
                      - condition: numeric_state
                        entity_id: light.kitchen_table_white
                        attribute: brightness
                        below: 100
            sequence:
              - parallel:
                  - action: script.send_to_home_log
                    data:
                      message: "🐾 Motion detected. Turning table 💡 🔆 lights on."
                      title: "🧑‍🍳 Kitchen"
                      log_level: "Debug"
                  - action: scene.turn_on
                    target:
                      entity_id: scene.kitchen_table_lights_on
                  - action: script.kitchen_cancel_all_light_timers

    mode: queued
    max: 10
```

### Example 2: Porch Trigger ID Branching

```yaml
automation:
  - id: "porch_motion_handler"
    alias: "Porch: Motion Detected (On/Off)"
    description: "Consolidated motion handling with trigger IDs"

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
          - alias: "Motion Detected - Turn On Light"
            conditions:
              - condition: trigger
                id: motion_on
            sequence:
              - parallel:
                  - action: light.turn_on
                    target:
                      entity_id: light.porch
                    data:
                      brightness_pct: 100
                  - action: timer.cancel
                    target:
                      entity_id: timer.porch_light

          - alias: "No Motion - Start Timer"
            conditions:
              - condition: trigger
                id: motion_off
            sequence:
              - parallel:
                  - action: script.send_to_home_log
                    data:
                      message: "No motion. Starting 💡 light timer."
                      title: "🚪 Porch"
                      log_level: "Debug"
                  - action: timer.start
                    target:
                      entity_id: timer.porch_light
                    data:
                      duration: "00:01:00"

    mode: single
```

---

## Key Takeaways

1. **Triggers are OR'd** - Any trigger starting automation
2. **Conditions are AND'd** - All must be true
3. **First choose branch wins** - Order matters critically
4. **Use trigger IDs for branching** - Cleaner than multiple automations
5. **Always use unique IDs** - Required for UI editing and traces
6. **Mode affects re-entrance behavior** - Choose carefully
7. **Variables are template-available** - Use for repeated calculations
8. **Parallel for independent actions** - Light + logging together
9. **Test conditions before deployment** - Use Developer Tools
10. **Add logging for visibility** - Easy debugging later
11. **Handle unavailable entities** - Not all sensors always available
12. **Document automation purpose** - Comments help future you
