# Automation Consolidation Opportunities

**Purpose:** Document reusable automation patterns identified during code reviews for future templating and consolidation work.

**Source:** Office.yaml review (2026-01-19) and living_room.yaml review (2026-01-15)

**Status:** Planning phase - patterns documented, implementation pending

---

## High Priority Patterns (Ready for Templating)

### 1. Motion Detection with Illuminance Logic

**Pattern Source:** office.yaml (lines 4-136), living_room.yaml (similar)

**Current State:** Duplicated across multiple rooms with slight variations

**Pattern Description:**
- Dual-trigger motion detection (binary_sensor + numeric_state for distance)
- 4-branch choose block based on illuminance levels
- Conditional light control based on current brightness
- Timer cancellation when motion detected

**Core Logic:**
```yaml
triggers:
  - trigger: state
    entity_id: binary_sensor.{room}_motion_presence
    to: "on"
  - trigger: numeric_state
    entity_id: sensor.{room}_motion_target_distance
    above: 0.1

variables:
  light_1: "{{ state_attr('light.{room}_1', 'brightness') | int(0) }}"
  light_2: "{{ state_attr('light.{room}_2', 'brightness') | int(0) }}"

choose:
  - conditions: # Branch 1: Bright enough, skip
      - condition: numeric_state
        entity_id: sensor.{room}_illuminance
        above: input_number.{room}_brightness_threshold
    sequence: []

  - conditions: # Branch 2: Dark, lights dim, turn on
      - condition: numeric_state
        entity_id: sensor.{room}_illuminance
        below: input_number.{room}_brightness_threshold
      - condition: template
        value_template: "{{ light_1 < 200 and light_2 < 200 }}"
    sequence:
      - action: scene.turn_on
        target:
          entity_id: scene.{room}_main_light_on

  - conditions: # Branch 3: Bright, lights dim, turn off
      - condition: numeric_state
        entity_id: sensor.{room}_illuminance
        above: input_number.{room}_brightness_threshold
      - condition: template
        value_template: "{{ light_1 < 200 and light_2 < 200 }}"
    sequence:
      - action: light.turn_off

  - conditions: # Branch 4: Timer active, turn off
      - condition: state
        entity_id: timer.{room}_lights_off
        state: "active"
    sequence:
      - action: light.turn_off
      - action: timer.cancel
```

**Parameterization Required:**
- Room name (e.g., "office", "living_room")
- Motion sensor entities (binary_sensor, numeric_state)
- Light entities (array of lights to control)
- Illuminance sensor entity
- Brightness threshold input_number
- Scene entity for "lights on"
- Timer entity for "lights off"
- Brightness check value (default: 200)
- Distance threshold (default: 0.1)

**Rooms Applicable:**
- Office (implemented)
- Living room (implemented, slight variation)
- Bedroom
- Kitchen
- Conservatory

**Estimated Reuse:** 15+ automations across 5+ rooms

**Implementation Effort:** Medium (requires script or automation template)

**Benefits:**
- Eliminates ~500 lines of duplicated code
- Consistent behavior across rooms
- Single point for bug fixes
- Easy to add to new rooms

---

### 2. No Motion Timer Pattern

**Pattern Source:** office.yaml (lines 138-166, 167-191)

**Current State:** Duplicated across multiple rooms

**Pattern Description:**
- Two-phase timer system for delayed light turnoff
- Phase 1: No motion detected → start grace timer
- Phase 2: Timer finishes → turn off lights
- Configurable timer duration per room

**Core Logic:**

**Automation 1: Start Timer**
```yaml
triggers:
  - trigger: numeric_state
    entity_id: sensor.{room}_motion_target_distance
    below: 0.01
    for: "00:02:00"

conditions:
  - condition: state
    entity_id: input_boolean.enable_{room}_motion_triggers
    state: "on"
  - condition: state
    entity_id: binary_sensor.{room}_motion_presence
    state: "off"

actions:
  - parallel:
      - action: script.send_to_home_log
        data:
          message: >-
            🚷 No motion in {room_display} for 2 minutes.
            Starting timer for 1 minute before turning lights off.
          title: ":{room_emoji}: {room_display}"
          log_level: "Debug"
      - action: timer.start
        target:
          entity_id: timer.{room}_lights_off
        data:
          duration: "00:01:00"
```

**Automation 2: Timer Finished**
```yaml
triggers:
  - trigger: event
    event_type: timer.finished
    event_data:
      entity_id: timer.{room}_lights_off

conditions:
  - condition: state
    entity_id: input_boolean.enable_{room}_motion_triggers
    state: "on"

actions:
  - parallel:
      - action: script.send_to_home_log
        data:
          message: "💤 {room_display} lights off timer finished. Turning lights off."
          title: ":{room_emoji}: {room_display}"
          log_level: "Debug"
      - action: scene.turn_on
        target:
          entity_id: scene.{room}_main_light_off
```

**Parameterization Required:**
- Room name (e.g., "office")
- Room display name (e.g., "Office")
- Room emoji (e.g., "office")
- Motion sensor entities
- Timer entity
- Scene entity for "lights off"
- Enable toggle (input_boolean)
- No motion duration (default: 2 minutes)
- Timer duration (default: 1 minute)

**Rooms Applicable:**
- Office (2 automations)
- Living room (similar pattern)
- Bedroom
- Kitchen
- Any room with motion-based lighting

**Estimated Reuse:** 10+ automation pairs (20+ automations)

**Implementation Effort:** Low-Medium (could be script or template)

**Benefits:**
- Consistent grace period behavior
- Prevents abrupt light turnoff
- Configurable delays per room
- ~40 lines of code per room → single template

---

### 3. Sunrise/Sunset Blind Control

**Pattern Source:** office.yaml (lines 414-843) - 8 distinct automations

**Current State:** Implemented in office, likely duplicated with variations in other rooms

**Pattern Description:**
- Sun-based blind positioning (open/close/tilt)
- Multiple trigger types: time, sun events, illuminance
- Common safety checks: enable toggle, window contact, current position
- Tilt positions standardized: 0 (closed), 25 (partially), 50 (open)

**Core Template Structure:**
```yaml
triggers:
  - trigger: {type}  # time, sun, numeric_state (illuminance)
    # ... trigger-specific config

conditions:
  - condition: state
    entity_id: input_boolean.enable_{room}_blind_automations
    state: "on"
  - condition: state
    entity_id: binary_sensor.{room}_windows
    state: "off"  # Windows must be closed
  - condition: numeric_state
    entity_id: cover.{room}_blinds
    attribute: current_tilt_position
    {above/below}: {threshold}  # Don't act if already in position

actions:
  - parallel:
      - action: script.send_to_home_log
        data:
          message: "{emoji} {reason}. {action_description}."
          title: ":{room_emoji}: {room_display}"
          log_level: "Debug"
      - action: cover.set_cover_tilt_position
        target:
          entity_id: cover.{room}_blinds
        data:
          tilt_position: {0/25/50}
```

**Automation Types Identified:**

1. **Morning Open** (Time trigger @ 8:00 AM)
   - Opens blinds if bright outside
   - Partially opens if moderately bright
   - Keeps closed if very bright (computer glare prevention)

2. **Sunset Partial Close** (Sun event: sunset)
   - Tilts to 25% for privacy

3. **Night Full Close** (Sun event: sunset + 1 hour)
   - Fully closes blinds (tilt to 0%)

4. **Window Closed at Night** (State trigger: window closed)
   - Closes blinds if window closed after sunset

5. **No Direct Sun** (Sun azimuth/elevation triggers)
   - Opens blinds when sun not facing window
   - Two variations: morning and afternoon

6. **Brightness-Based** (Illuminance triggers with duration)
   - Closes blinds when very bright (25% tilt)
   - Fully closes when extremely bright (0% tilt)
   - Opens when outside gets darker (50% tilt)

**Parameterization Required:**
- Room name, display name, emoji
- Blind entity (cover.{room}_blinds)
- Window contact sensor
- Illuminance sensor (optional)
- Enable toggle input_boolean
- Sun azimuth thresholds (optional)
- Sun elevation thresholds (optional)
- Brightness thresholds (optional)
- Tilt positions (0, 25, 50 or custom)
- Time triggers (morning open time)
- Computer presence check (optional, office-specific)

**Rooms Applicable:**
- Office (8 automations implemented)
- Bedroom (likely has similar)
- Living room (likely has similar)
- Any room with motorized blinds

**Estimated Reuse:** 40+ automations across rooms with blinds

**Implementation Effort:** High (complex, many variations)

**Benefits:**
- Massive code reduction (8 automations × multiple rooms)
- Consistent blind behavior
- Easy to add new rooms with blinds
- Centralized configuration for sun angles

**Challenges:**
- Many variations and optional features
- Room-specific logic (e.g., computer glare in office)
- Need good parameter structure

---

### 4. Temperature-Based Device Control

**Pattern Source:** office.yaml (lines 194-278)

**Current State:** Implemented in office, potentially applicable to other rooms

**Pattern Description:**
- 3-priority graduated response system
- Priority 1 (26°C): Auto-on during daytime with people home
- Priority 2 (31°C): Emergency override, always on
- Priority 3 (29°C): Warning notification with user interaction
- Uses actionable notifications for user control

**Core Logic:**
```yaml
triggers:
  - trigger: numeric_state
    entity_id: sensor.{room}_temperature
    above: 26
  - trigger: numeric_state
    entity_id: sensor.{room}_temperature
    above: 29
  - trigger: numeric_state
    entity_id: sensor.{room}_temperature
    above: 31

conditions:
  - condition: state
    entity_id: switch.{room}_{device}
    state: "off"

choose:
  # Priority 1: Auto-on (26°C + conditions)
  - conditions:
      - condition: numeric_state
        entity_id: sensor.{room}_temperature
        above: 26
      - condition: time
        after: "08:30:00"
        before: "22:00:00"
      - or:
          - condition: state
            entity_id: group.{presence_group}
            state: "home"
    sequence:
      - action: switch.turn_on
        target:
          entity_id: switch.{room}_{device}

  # Priority 2: Emergency (31°C always)
  - conditions:
      - condition: numeric_state
        entity_id: sensor.{room}_temperature
        above: 31
    sequence:
      - action: switch.turn_on
        target:
          entity_id: switch.{room}_{device}

  # Priority 3: Warning (29°C with notification)
  - conditions:
      - condition: numeric_state
        entity_id: sensor.{room}_temperature
        above: 29
    sequence:
      - action: script.send_actionable_notification_with_2_buttons
        data:
          message: "Temperature in {room} is {{ states('sensor.{room}_temperature') }}°C"
          button_1: "Turn on {device}"
          button_2: "Ignore"
          # ... callback handling
```

**Parameterization Required:**
- Room name, display name
- Temperature sensor entity
- Device entity (switch/fan)
- Presence group (optional)
- Temperature thresholds (26°C, 29°C, 31°C)
- Time window for auto-on (08:30-22:00)
- Notification preferences

**Rooms Applicable:**
- Office (implemented for fan)
- Bedroom (fan/heater control)
- Living room (fan control)
- Conservatory (heater control)
- Kitchen (extractor fan)

**Estimated Reuse:** 8+ automations across rooms

**Implementation Effort:** Medium (actionable notification complexity)

**Benefits:**
- Graduated response prevents nuisance activations
- Emergency override for extreme temperatures
- User control via notifications
- Prevents overnight device operation
- ~85 lines per room → single template

**Use Cases Beyond Temperature:**
- Humidity control (dehumidifier)
- Air quality (air purifier)
- CO2 levels (ventilation)

---

### 5. Message/Logging Patterns

**Pattern Source:** office.yaml (32 send_to_home_log calls)

**Current State:** Consistent structure but manually typed each time

**Pattern Description:**
- Standard message format: emoji + context + sensor values + action
- Consistent title structure with room emoji
- Standardized log levels (Debug for routine, Normal for alerts)
- Sensor values include units for user-friendliness

**Standard Message Structure:**
```yaml
action: script.send_to_home_log
data:
  message: >-
    {emoji} {context_description}
    {optional_sensor_values}
    {action_taken}
  title: ":{room_emoji}: {room_display}"
  log_level: "{Debug|Normal}"
```

**Message Pattern Examples:**

**Motion Detection:**
```yaml
message: >-
  🐾 💡 🔆 Motion detected in the {room}.
  Illuminance: {{ states('sensor.{room}_illuminance', with_unit=True) }}.
  Turning on lights.
```

**No Motion:**
```yaml
message: >-
  🚷 No motion in the {room} for 2 minutes.
  Starting timer for 1 minute before turning lights off.
```

**Temperature Alert:**
```yaml
message: >-
  🌡️ 🔥 {priority_level} {room} temperature at
  {{ states('sensor.{room}_temperature') }}°C.
  {action_description}.
```

**Blind Control:**
```yaml
message: >-
  {{ clock_result.emoji }} {reason_for_action}.
  Azimuth: {{ state_attr('sun.sun', 'azimuth') }}
  ({{ states('input_number.{room}_azimuth_threshold') }}).
  {blind_action}.
```

**Parameterization Required:**
- Room name, display name, emoji
- Message components (emoji, context, action)
- Sensor entities for value inclusion
- Log level (default: "Debug")
- Optional: clock emoji integration

**Standardization Opportunity:**

Create helper script: `script.send_room_log`
```yaml
send_room_log:
  fields:
    room: {description: "Room name"}
    room_emoji: {description: "Room emoji"}
    emoji: {description: "Action emoji"}
    context: {description: "What triggered this"}
    sensors: {description: "Array of sensor entities to include"}
    action: {description: "What action was taken"}
    log_level: {description: "Debug or Normal", default: "Debug"}
  sequence:
    - action: script.send_to_home_log
      data:
        message: >-
          {{ emoji }} {{ context }}
          {% for sensor in sensors %}
          {{ state_attr(sensor, 'friendly_name') }}: {{ states(sensor, with_unit=True) }}
          {% endfor %}
          {{ action }}
        title: ":{{ room_emoji }}: {{ room }}"
        log_level: "{{ log_level }}"
```

**Benefits:**
- Consistent message formatting across all automations
- Easier to read logs
- Centralized format changes
- Reduces typing/copy-paste errors
- ~10 lines per call → 3 lines

**Estimated Reuse:** 500+ send_to_home_log calls across entire system

**Implementation Effort:** Low (simple script wrapper)

---

### 6. Light Timeout Detection

**Pattern Source:** office.yaml (lines 845-885)

**Current State:** Implemented in office, likely applicable to other rooms

**Pattern Description:**
- Detects lights left on during bright daylight
- Suggests user error (forgot to turn off)
- Automatically turns off after extended duration
- Prevents energy waste

**Core Logic:**
```yaml
triggers:
  - trigger: state
    entity_id: light.{room}_area_lights
    to: "on"
    for: "01:00:00"  # 1 hour

conditions:
  - condition: sun
    before: sunset
    after: sunrise
  - condition: numeric_state
    entity_id: sensor.{room}_illuminance
    above: input_number.{room}_light_level_threshold

actions:
  - parallel:
      - action: script.send_to_home_log
        data:
          message: >-
            💡 ⏰ {room_display} lights have been on for 1 hour during
            bright daylight ({{ states('sensor.{room}_illuminance', with_unit=True) }}).
            Turning off to save energy.
          title: ":{room_emoji}: {room_display}"
          log_level: "Debug"
      - action: light.turn_off
        target:
          entity_id:
            - light.{room}_light_1
            - light.{room}_light_2
```

**Parameterization Required:**
- Room name, display name, emoji
- Light entities (array)
- Illuminance sensor
- Brightness threshold input_number
- Duration (default: 1 hour)

**Rooms Applicable:**
- Office (implemented)
- Living room
- Bedroom
- Kitchen
- Any room with illuminance sensor

**Estimated Reuse:** 5-8 automations

**Implementation Effort:** Low (simple pattern)

**Benefits:**
- Energy savings
- Prevents forgotten lights
- User-friendly notification
- ~15 lines per room → single template

---

## Medium Priority Patterns

### 7. Remote Control Device Toggle

**Pattern Source:** office.yaml (lines 912-959)

**Description:** MQTT device triggers for remote control buttons

**Reuse Potential:** Medium (requires MQTT remotes)

### 8. Scheduled Device Shutdown

**Pattern Source:** office.yaml (lines 280-295)

**Description:** Time-based device turnoff (e.g., fan at 3 AM)

**Reuse Potential:** Medium (simple, but varies by device)

---

## Implementation Strategy

### Phase 1: Quick Wins (Low Effort, High Impact)
1. **Message/Logging Standardization** (Pattern #5)
   - Create `script.send_room_log` helper
   - Migrate 10-20 calls as proof of concept
   - Measure impact on readability

### Phase 2: Timer Patterns (Medium Effort, High Impact)
2. **No Motion Timer** (Pattern #2)
   - Create generic automation template
   - Migrate office and living room
   - Document parameters

### Phase 3: Complex Patterns (High Effort, Very High Impact)
3. **Motion Detection with Illuminance** (Pattern #1)
   - Create comprehensive template
   - Test in one room thoroughly
   - Roll out to remaining rooms

4. **Blind Control** (Pattern #3)
   - Break into sub-patterns (morning, sunset, brightness)
   - Create modular templates
   - Parameterize per room

5. **Temperature Control** (Pattern #4)
   - Generalize to any graduated response pattern
   - Support multiple thresholds
   - Add humidity/air quality variants

### Phase 4: Cleanup
6. **Light Timeout Detection** (Pattern #6)
   - Simple template
   - Quick migration

---

## Success Metrics

**Code Reduction:**
- Target: Eliminate 1,500+ lines of duplicated automation code
- Estimated: 40% reduction in automation YAML across room packages

**Maintenance:**
- Bug fixes apply to all instances automatically
- New rooms can be added in <30 minutes
- Consistent behavior across all rooms

**Consistency:**
- Same timing delays across rooms
- Same message formats
- Same condition checks

---

## Next Steps

1. **Review this document with user** - Confirm priorities
2. **Implement Pattern #5 (Message Logging)** - Quick win to prove concept
3. **Create template directory** - `.claude/templates/` for reusable patterns
4. **Document each template** - Usage examples, parameters, migration guide
5. **Gradual migration** - One pattern at a time, test thoroughly

---

**Document Status:** Planning complete, awaiting implementation approval
**Last Updated:** 2026-01-19
