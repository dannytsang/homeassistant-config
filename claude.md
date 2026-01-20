# Home Assistant Configuration Analysis

**Date:** 2026-01-12
**Analysis by:** Claude Sonnet 4.5

---

## Overview

This is a **professional-grade smart home automation system** demonstrating advanced home automation engineering with sophisticated energy management, comprehensive security, and intelligent comfort automation.

### Key Statistics
- **6,902 total states** across the system
- **384 automations** (20 in main automations.yaml, 431 in packages)
- **137 scripts** (105 unique called scripts)
- **75 scenes** with complex lighting presets
- **73 lights** across multiple rooms
- **25 covers** (blinds, roller shades)
- **493 switches** (power monitoring and control)
- **3,077 sensors** (extensive monitoring)
- **685 binary sensors** (presence, occupancy, contact sensors)

---

## Architecture

### Configuration Structure
- **Split configuration** with packages for organization
- **Room-based packages** (bedroom, kitchen, living room, office, etc.)
- **Integration-based packages** (energy, HVAC, messaging, etc.)
- **UI automation file** + YAML-based automations
- **Git-tracked with CI/CD** (Git pull addon)

### Infrastructure
- **Host OS:** Unraid (custom-built computer)
- **Database:** InfluxDB 2.0 (30-day recorder retention)
- **MQTT:** EMQX (external broker)
- **Analytics:** Grafana (external dashboards)
- **ESPHome:** 13 custom devices with OTA updates

---

## Network & Core Infrastructure

### Networking
- **Ubiquiti Unifi Dream Machine Pro** (network hub, NVR)
- **Aruba networking** (replaced Unifi for PPSK controllerless setup)
- **SMLIGHT SLZB-06** (Zigbee hub)
- Multiple Unifi switches with PoE

### Power Infrastructure
- **3 UPS systems** (Living Room, Server, Computer) with battery runtime monitoring
- **Shelly switches** (EM, Plus 1PM, Plus 1PM Mini)
- **TP-Link Kasa Smart plugs** (HS110, KP115, KP303)
- **Sonoff USB adapters** (WiFi and Zigbee variants)
- **Samsung SmartThings plugs** (power monitoring)

---

## Energy Management System (Flagship Feature)

### Solar & Battery Infrastructure
- **Growatt SPH3000-6000 Solar Inverter** + **GBLI Battery**
- **Solar Assistant** for local/faster solar data (replaces Growatt integration)
- **Solcast** for solar forecasting
- **myEnergi Zappi** (EV charger)
- **myEnergi Eddi** (solar diverter/relay for water heating)
- **EcoFlow** battery system with power monitoring
- Real-time grid import/export monitoring

### Energy Integrations
- **Octopus Energy** integration (UK Agile tariff tracking)
- **Predbat** integration for intelligent battery prediction and scheduling
- Rate-aware automation and cost optimization

### Intelligent Energy Features
1. **Battery Mode Switching:**
   - "Battery First" mode (use stored energy)
   - "Load First" mode (use grid when needed)
   - "Grid First" mode (charge battery from grid on cheap rates)
   - Mode validation alerts if inverter not in correct mode

2. **Solar Optimization:**
   - Monitor battery state of charge
   - Forecast excess solar → notify user
   - Track consecutive low-forecast days
   - Daily Predbat summary notifications

3. **Hot Water Control:**
   - Turn off boiler in morning if hot day expected
   - Turn on boiler in afternoon based on forecast
   - Eddi (solar diverter) cuts off boiler when enough solar heating done
   - Tracks consecutive low-generation days

4. **EV Charging (Zappi):**
   - Integrated with solar forecasting
   - Rate-based charging decisions
   - Smart charge scheduling

5. **Cost-Aware Appliance Automation:**
   - Conservatory airer runs only on:
     - Free solar energy
     - Cheap electricity rates (<£0/kWh threshold)
     - Within operation schedule
     - Temperature/humidity suitable for drying

---

## Lighting System

### Hardware
- **Philips Hue** (motion sensors, bulbs)
- **LIFX** (candles, color bulbs, mini white)
- **Innr Smart Bulbs** (E14)
- **Elgato Key Light** (studio lighting)

### Automation Features
- **Scene-based automation** with 75 pre-configured scenes
- **Motion-based triggering** with illuminance thresholds
- **Adaptive lighting** (color temp changes based on time)
- **Dynamic thresholds** - Living room changes from 81 to 30 lux based on Terina's work laptop status

### Motion-Based Patterns
- Living room motion → check light level + work laptop status → adjust thresholds
- Kitchen motion on different zones (table lights, cooker lights)
- Conservatory motion with door open detection
- Porch/front door occupancy detection

---

## Climate Control (HVAC)

### Hardware
- **Hive Active Heating** (SLT3) - central heating hub
- **TRV radiators** across 6+ rooms (Tuya-based)
- **Eddi solar diverter** - intelligent hot water heating from excess solar
- **Temperature sensors** in fridge and freezers (TuYa)

### Automation
- **Dynamic heating scheduling** based on presence and weather
- Conservatory below 3°C → boost heating
- Radiators below target temperature (by room) → alert
- Heating turn-on checks (office window open, etc.)
- Set to home mode when people arrive
- Off when no one home
- Radiator TRV synchronization with thermostat

---

## Security & Monitoring

### Security Hardware
- **Ring Doorbell 2** + **Ring Alarm System** (1st gen with 2nd gen sensors)
- **Reolink RLC-520A** camera
- **Ubiquiti Protect** cameras (G4 Instant, G5 Flex, G6 Instant, G6 Turret)
- **Nest Protect** smoke/CO detectors
- **Nuki smart lock** (front door)
- **NFC tag scanning** for automation triggers (bedroom, front door)
- **Contact sensors** on all doors/windows

### Alarm Automations
- **Armed States:** Armed Away, Armed Home, Disarmed
- Motion detected in office/kitchen while armed_home (logs alert)
- Door armed (NFC tag triggers office door alarm)
- Overnight arm (midnight with various retry times 00:00, 01:00, 02:00)
- Checks all doors/windows are closed before arming
- Sets heating to home mode when disarmed
- Auto-disarm when approaching home
- Auto-lock house when everyone leaves

---

## Presence Detection & Home Modes

### Multi-Layer Presence Tracking
- **GPS-based distance sensors** (heading towards home, close to home, far away)
- **Network-based device tracking** (computers, Nintendo Switch)
- **Multiple people tracked:** Danny, Terina, Leo, Ashlee
- **Family calendar integration** (holiday detection)

### Home Modes
1. **Normal** - Everyone home
2. **Holiday** - Long distance away, fake presence lights
3. **No Children** - Kids away, different automation rules
4. **Naughty Step Mode** - Discipline mode (disables motion triggers in certain areas)

### Presence Automations
- Auto-disarm alarm when approaching home
- Turn on lights when arriving in the dark
- Announce delayed notifications
- Auto-lock house when everyone leaves
- Holiday fake presence (random lights 17:00-22:00)
- Children home in "No Children" mode → auto-switch to Normal

---

## Smart Home Connectivity

### Voice Assistants
- **Alexa Media Player** (custom component v5.9.0)
  - 5 Echo devices (1st Gen, Dot 2nd/3rd Gen, Show 10 2nd Gen, Show 5 1st Gen)
- **Home Assistant Mobile App** with notification actions

### Media
- **Google Chromecast** devices (Chromecast Ultra, Google TV)
- **Spotify integration** with source-following automation
- **Music follows Danny** via BLE area detection

---

## ESPHome Custom Devices (13 devices)

### Occupancy & Presence Detection
- **bed.yaml** - 4-point ADS1115 pressure sensors + BME680 air quality
  - Custom IAQ calculation: `log(gas_resistance) + 0.04 * humidity`
- **ashlees-bed.yaml** - Ashlee's bedroom sensors
- **leos-bed.yaml** - Leo's bedroom sensors
- **bathroom-motion.yaml** - Motion detection
- **conservatory-motion.yaml** - Conservatory motion
- **living-room-motion.yaml** - Living room occupancy
- **everything-presence-one/lite** - mmWave presence detection
- **apollo-r-pro-1-eth-ef755c.yaml** - Multi-sensor device

### Monitoring Devices
- **office.yaml** - Office environment sensors
- **boiler.yaml** - Boiler monitoring
- **central-heating.yaml** - Heating control
- **water-softener.yaml** - Water softener status

### Common Packages
- `esp32-base.yaml` - ESP32 configuration
- `bluetooth-base.yaml` - Bluetooth support

---

## Blind & Cover Automation

### Hardware
- **IKEA FYRTUR/KADRILJ** roller blinds with repeaters
- **SwitchBot Blind Tilt** + Hub Mini

### Automation Logic
- **Weather-based:**
  - Close blinds when temperature drops (cold protection)
  - Close blinds before sunset in bedrooms
  - Adjust blind positions based on sun angle

- **Presence-based:**
  - Close bedroom blinds when occupant in bed after sunset
  - Open blinds when waking up
  - Leo's bed occupancy triggers blind closing (with window safety check)
  - **Safety interlock:** Waits up to 3 hours for window to close before closing blinds

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

**Log Message Best Practice - Append vs Replace:**

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
  and Terina's work :computer: computer is on. Flashing lights as signal (room bright enough).
```

**Rationale:** The original message provides sensor values and thresholds that help debug automation behavior. Appending clarification preserves this diagnostic information while explaining intent.

**Real-world example:** Fixed in living_room.yaml lines 21-120 where motion automation branches now have clear aliases and flash intent is documented.

### Blind Tilt Position Conventions

When controlling blind tilt positions, use these conventions consistently:

```yaml
# Tilt position reference (SwitchBot Blind Tilt)
# 0    = Fully closed (no light through)
# 25   = Partially open (angled, some light, some privacy)
# 50   = Half open (maximum airflow while maintaining privacy)
# 75   = Mostly open (primarily for light/view)
# 100  = Fully open (no obstruction)
```

**Example: Conditional blind opening based on position**

```yaml
automation:
  - alias: "Blinds: Set to Half Open"
    sequence:
      # Only adjust if blinds are below 50 (more closed than half-open)
      - if:
          - condition: numeric_state
            entity_id: cover.blind_left
            attribute: current_tilt_position
            below: 50
        then:
          - action: cover.set_cover_tilt_position
            data:
              tilt_position: 50
            target:
              entity_id:
                - cover.blind_left
                - cover.blind_middle
                - cover.blind_right
```

**Pattern:** Group multiple blinds in a single action rather than separate if/then blocks. This reduces code duplication and prevents redundant checks.

**Consolidation Pattern - Eliminate Redundant Conditions:**

When an action checks the same condition multiple times (once in the condition block, again in nested if/then within the action), consolidate into a single action:

```yaml
# WRONG - Redundant condition checking (condition checked, then re-checked in action)
conditions:
  - condition: numeric_state
    entity_id: cover.blind_left
    attribute: current_tilt_position
    below: 50
actions:
  - parallel:
      - if:
          - condition: numeric_state
            entity_id: cover.blind_left
            attribute: current_tilt_position
            below: 50
        then:
          - action: cover.set_cover_tilt_position
            data:
              tilt_position: 50
            target:
              entity_id: cover.blind_left
      # ... 2 more identical if blocks for middle and right blinds

# CORRECT - Single action targeting all blinds
conditions:
  - condition: numeric_state
    entity_id: cover.blind_left
    attribute: current_tilt_position
    below: 50
actions:
  - action: cover.set_cover_tilt_position
    data:
      tilt_position: 50
    target:
      entity_id:
        - cover.blind_left
        - cover.blind_middle
        - cover.blind_right
```

**Benefit:** Reduces from 37 lines to 8 lines while maintaining exact behavior. The condition ensures at least one blind needs adjustment, and the action applies to all blinds.

**Real-world fix:** Simplified living_room.yaml lines 1072-1088, removed 29 lines of repetitive condition/action blocks by consolidating into single action with multiple target entities.

---

## Specialized Devices & Integrations

### Personal Devices
- **Garmin Epix Pro Gen 2** (smartwatch sync)
- **Oral-B Electric Toothbrush** (Bluetooth)

### Kitchen & Cooking
- **MEATER Plus** (meat thermometer)
- Fridge/freezer temperature alerts

### Maker & Hobbies
- **3D Printer monitoring** via OctoPrint
  - Print started → log + turn on light
  - 50% complete → notification
  - Finished → notification + turn off light
  - Paused mid-print → alert
  - **Left unattended → immediate alert** (runs when no one home)

### Weather
- **Ecowitt Wittboy** weather station

### IR/RF Control
- **Broadlink RM4 Pro** (IR/RF remote replacement)

---

## Notification System

### Multi-Channel Delivery
- Direct notifications (Mobile App, Slack, Discord, Telegram)
- Home log (in-app logging with debug/normal levels)
- Delayed announcement queue
- Mobile app action buttons

### Notification Features
- **Interactive buttons:**
  - Blind position adjustments
  - Fan on/off
  - Appliance toggling (fridge, freezer)
  - Server fan control
- Mobile app action router with button mapping
- Delayed notification buffering and announcement
- Fridge/freezer temperature alerts
- **Quiet hours with smart exceptions** (keyword-based bypass)

---

## Smart Notification Patterns

### Smart Quiet Hours with Keyword Exceptions

**Purpose:** Allow critical messages to bypass quiet hours while respecting sleep/focus time

**Implementation Location:** `packages/integrations/messaging/notifications.yaml` lines 115-151

**Keywords (Hardcoded):**
```yaml
# Bypass keywords for quiet hours exceptions
# Safety: emergency, fire, gas, water, leak
# Security: intruder, alarm, breach, danger, alert
# Priority: critical, urgent
```

**Condition Logic in send_direct_notification (lines 115-151):**

The quiet hours check uses an OR condition with multiple branches:

```yaml
115:      - if:
116:          - or:
117:              - alias: "Quiet time is OFF"
118:                condition: state
119:                entity_id: schedule.notification_quiet_time
120:                state: "off"
121:
122:              - alias: "Quiet time ON but suppress_if_quiet is FALSE"
123:                and:
124:                  - condition: state
125:                    entity_id: schedule.notification_quiet_time
126:                    state: "on"
127:                  - condition: template
128:                    value_template: "{{ not v_suppress_if_quiet }}"
129:
130:              - alias: "Quiet time ON but message contains bypass keyword"
131:                and:
132:                  - condition: state
133:                    entity_id: schedule.notification_quiet_time
134:                    state: "on"
135:                  - condition: template
136:                    value_template: >
137:                      {%- set keywords = ['emergency', 'fire', 'gas', 'water', 'leak', 'intruder', 'alarm', 'breach', 'danger', 'alert', 'critical', 'urgent'] %}
138:                      {%- for keyword in keywords %}
139:                        {%- if keyword.lower() in message.lower() %}
140:                          true
141:                        {%- endif %}
142:                      {%- endfor %}
143:
144:              - alias: "Quiet time ON but priority is NOT 'normal'"
145:                and:
146:                  - condition: state
147:                    entity_id: schedule.notification_quiet_time
148:                    state: "on"
149:                  - condition: template
150:                    value_template: "{{ v_priority != 'normal' }}"
151:        then:
152:          # Process notification
```

**How It Works:**

1. **Lines 117-120:** If quiet hours are OFF, always send
2. **Lines 122-128:** If quiet hours ON but suppress_if_quiet is FALSE (user opted out), send
3. **Lines 130-142:** If quiet hours ON, check if message contains any bypass keyword (case-insensitive)
   - Line 137: Hardcoded keyword list as Jinja2 array
   - Line 138: Loops through each keyword
   - Line 139: Case-insensitive substring match (`in` operator)
   - Line 140: Returns `true` if ANY keyword found
   - Line 142: Empty/no matches returns nothing (falsy)
4. **Lines 144-150:** If quiet hours ON but priority is high/critical, send anyway

**Keyword Matching Algorithm:**

```yaml
136:                    value_template: >
137:                      {%- set keywords = ['emergency', 'fire', 'gas', 'water', 'leak', 'intruder', 'alarm', 'breach', 'danger', 'alert', 'critical', 'urgent'] %}
138:                      {%- for keyword in keywords %}
139:                        {%- if keyword.lower() in message.lower() %}
140:                          true
141:                        {%- endif %}
142:                      {%- endfor %}
```

- Line 137: Hardcoded keyword array with common emergency/safety keywords
- Line 138: Loops through each keyword
- Line 139: Case-insensitive substring match (`in` operator, keyword already lowercase, message converted to lowercase)
- Line 140: Returns `true` on first match (early exit not possible in Jinja2, but last true value persists)
- Line 142: Empty/no matches returns nothing (falsy)

**Behavior Matrix:**

| Quiet Hours | Message Contains Keyword | Priority | Result |
|-------------|--------------------------|----------|--------|
| OFF | N/A | any | ✅ Send |
| ON | YES | any | ✅ Send (keyword bypass) |
| ON | NO | high/critical | ✅ Send (priority override) |
| ON | NO | normal | ❌ Block |
| ON | suppress_if_quiet=false | NO | ✅ Send (user opt-out) |

**Hardcoded Keywords:**
- Safety: `emergency`, `fire`, `gas`, `water`, `leak`
- Security: `intruder`, `alarm`, `breach`, `danger`, `alert`
- Priority: `critical`, `urgent`

**To Change Keywords:**
Edit line 137 in `send_direct_notification` script to add/remove keywords from the array.
Example addition: `'flooding'`, `'intruder_detected'`, `'power_loss'`

**Related Code Patterns:**
- Integration with `schedule.notification_quiet_time` entity
- Used in: `send_direct_notification`, `send_direct_notification_with_url`, `send_home_log_with_local_attachments`

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

**Grep Search Pattern:**
```
Pattern: id: "[candidate_id]"
Output mode: files_with_matches
Example: id: "1234567890123"
```

**Expected Results:**
- **If unique:** No matches found
- **If duplicate:** Returns file path containing ID (e.g., `packages/integrations/messaging/message_callback.yaml`)

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
2. Search for duplicates using Grep
3. If `files_with_matches` returns empty, ID is unique → proceed
4. If matches found, generate new ID and retry (max 3 attempts)
5. Create automation with verified unique ID

**Token Cost:** ~50-100 tokens per Grep search (highly efficient)

### Existing Automation IDs Reference

For verification, here are known automation IDs in the configuration:
- `message_callback.yaml`: `"1625924056779"` (Mobile Notification Action Router)
- `bedroom2.yaml`: Various circadian lighting automations (PR #175)
- `living_room.yaml`: 35+ automations with unique IDs

### Verification Commands

**Check a specific ID:**
```bash
Grep pattern: 'id: "1625924056779"'
Result: Shows file containing ID (or no matches if unique)
```

**Verify ID is unique (example for testing):**
```bash
Grep pattern: 'id: "9999999999999"'
Result: Expected "No matches found" (this ID hasn't been used)
```

### Edge Cases

**Commented IDs:**
- Grep will match IDs in comments (e.g., `# Old ID: "1234567890123"`)
- This is acceptable - prevents accidental reuse of old IDs
- Manual verification recommended if match found

**Multiple Automation Files:**
- Search automatically covers all packages/ subdirectories
- Includes UI-generated automations.yaml
- Grep recursively searches entire working directory

**Rapid Automation Creation:**
- Run uniqueness check before each automation
- Token cost is linear: 50-100 tokens × number of automations
- Still more efficient than alternative approaches

---

## Complete Script Reference Catalog

**Purpose:** Quick lookup to prevent script duplication and find existing implementations

### Core Notification Scripts (637+ calls total)
| Script | Purpose | Call Count | Parameters | Reusable |
|--------|---------|-----------|------------|----------|
| `send_to_home_log` | Log message to home log system | 504 | message, title, log_level | ✅ Core |
| `send_direct_notification` | Send mobile app notification | 637 | message, title, suppress_if_quiet, priority | ✅ Core |
| `send_direct_notification_with_url` | Mobile notification + URL attachment | 25+ | message, title, url | ✅ Core |
| `send_actionable_notification_with_2_buttons` | Mobile notification + 2 action buttons | 45+ | message, title, button1_action, button1_label, button2_action, button2_label | ✅ Core |
| `send_actionable_notification_with_3_buttons` | Mobile notification + 3 action buttons | 30+ | message, title, button1_*, button2_*, button3_* | ✅ Core |
| `send_to_home_assistant_with_url_attachment` | Multi-platform notification with attachment | 25+ | Varies by platform | ✅ Core |

### System Control Scripts
| Script | Purpose | When to Use | Reusable |
|--------|---------|------------|----------|
| `set_alarm_to_armed_away_mode` | Arm alarm (away mode) | Leaving home, guest mode | ✅ Yes |
| `set_alarm_to_armed_home_mode` | Arm alarm (home mode) | Evening, family returning | ✅ Yes |
| `set_alarm_to_disarmed_mode` | Disarm alarm | Arriving home, mobile action | ✅ Yes |
| `lock_front_door` | Lock front door (Nuki) | Leaving home, security | ✅ Yes |
| `unlock_front_door` | Unlock front door (Nuki) | Arriving home, NFC tag | ✅ Yes |
| `turn_everything_off` | Master OFF sequence (lights + devices) | Bedtime, emergency | ✅ Yes |
| `set_central_heating_to_home_mode` | Set heating to home temperature | Arriving home | ✅ Yes |
| `set_central_heating_to_away_mode` | Set heating to away temperature | Leaving home | ✅ Yes |
| `everybody_leave_home` | Execute leave-home sequence | Last person leaves | ✅ Yes |
| `alexa_announce` | Announce via Alexa speakers | Notifications, alerts | ✅ Yes |

### Helper/Utility Scripts
| Script | Purpose | When to Use | Reusable |
|--------|---------|------------|----------|
| `get_clock_emoji` | Return time-based clock emoji (⏰ format) | 28 instances in 9 files | ✅ Pattern |
| `send_actionable_notification_to_home_assistant_with_2_buttons` | Mobile notification (internal version) | Device-specific notifications | ✅ Core |
| `send_actionable_notification_to_home_assistant_with_3_buttons` | Mobile notification (internal version) | Device-specific notifications | ✅ Core |
| `check_conservatory_airer` | Check airer temperature/humidity conditions | Airer scheduling | ❌ Room-specific |
| `turn_off_conservatory_airer` | Turn off conservatory airer | Airer automation | ❌ Room-specific |
| `living_room_flash_lounge_lights_red` | Flash living room lights red | Motion alerts | ❌ Room-specific |
| `flash_lights_yellow` | Flash lights yellow | Motion signals | ✅ Generic |

### Script Decision Tree

**Need to send a notification?**
- Mobile app only → `send_direct_notification`
- Mobile app + URL attachment → `send_direct_notification_with_url`
- Mobile app + action buttons (2) → `send_actionable_notification_with_2_buttons`
- Mobile app + action buttons (3) → `send_actionable_notification_with_3_buttons`
- Internal logging → `send_to_home_log`

**Need to control security/climate?**
- Arm/disarm alarm → `set_alarm_to_*_mode`
- Lock/unlock door → `lock_front_door` / `unlock_front_door`
- Heating control → `set_central_heating_to_*_mode`
- Master OFF → `turn_everything_off`

**Need a utility?**
- Clock emoji → `get_clock_emoji`
- Flash lights → `flash_lights_yellow` (generic) or room-specific version
- Room-specific logic → Check room package first, may already exist

### Creating New Scripts

**Before creating a new script, check:**
1. Does a similar script already exist? (Check this reference)
2. Can you use an existing script with variables?
3. Can you consolidate with existing logic?

**Only create new scripts if:**
- No existing script performs the needed function
- Cannot be achieved with existing scripts + variables
- Function is reusable (not room-specific)

**Example:** Don't create `bedroom_turn_off_lights` - use `turn_everything_off` or `light.turn_off` action directly

---

## Custom Components & Extensions

1. **alexa_media** (v5.9.0) - Alexa Media Player integration (alandtse)
2. **myenergi** (CJNE/ha-myenergi) - Zappi EV charger and Eddi diverter
3. **llmvision** - LLM-based vision/AI integration
4. **retry** - Retry logic for unreliable devices
5. **delete** - File deletion integration

---

## Notable Automation Patterns

### 1. Dynamic Illuminance Thresholds
Living room motion automation changes brightness thresholds based on Terina's work laptop:
- Laptop ON: 81 and 65 lux (need brighter light)
- Laptop OFF: 30 and 25 lux (okay with dimmer light)

### 2. Sophisticated Bed Occupancy
- 4-point pressure sensors (ADS1115)
- BME680 air quality sensor for breathing detection
- Custom IAQ calculation

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
- Excess solar detection and notification

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

## Key Areas of Focus

### 1. Energy/Solar (Primary Focus)
- Sophisticated battery management
- Tariff-aware automation
- Forecast-driven decisions
- Cost optimization across all appliances

### 2. Security (Comprehensive)
- Multi-layer alarm system
- NFC authentication
- Camera monitoring with Ubiquiti Protect
- Window/door sensors
- Motion detection with logging

### 3. Comfort (Advanced)
- Temperature-based automations
- Blind positioning with sun tracking
- Adaptive lighting
- Presence-aware features

### 4. Efficiency
- Power monitoring on 493 switches
- UPS monitoring for critical systems
- Airer cost optimization
- Heating schedule optimization
- Real-time energy tracking

### 5. Family Management
- Children tracking (Leo's Nintendo Switch)
- Different modes for family configurations
- Work detection for adults
- Parental control features (Naughty Step Mode)

---

## Hidden Gems & Clever Solutions

1. **Pressure-based bed sensors** with air quality breathing detection
2. **Work laptop detection** dynamically adjusts lighting thresholds
3. **Naughty Step Mode** - parenting automation that disables motion triggers
4. **3-hour blind safety wait** - checks window closure before proceeding
5. **Music source following** - Spotify switches based on BLE location
6. **Consecutive low-solar tracking** - multi-day weather pattern detection
7. **Interactive notification buttons** - control devices directly from alerts
8. **Fake presence intelligence** - random light patterns mimicking occupancy
9. **Airer cost optimization** - only runs on free/cheap electricity
10. **Inverter mode validation** - alerts if battery not in expected mode

---

## Technical Excellence

### Code Organization
- **Highly modular design** with room and integration packages
- **Clear separation of concerns**
- **Consistent naming conventions**
- **Well-documented automation triggers**

### Monitoring & Observability
- InfluxDB time-series database (30-day retention)
- Grafana external dashboards
- Home log system with debug levels
- UPS battery runtime tracking
- Power consumption monitoring across 493 devices

### Resilience & Reliability
- Fallback mechanisms in automations
- Retry logic for unreliable devices
- Multiple data sources (Solar Assistant vs Growatt)
- External MQTT broker for stability
- Git-tracked configuration with version control

### Performance Optimization
- Smart recorder exclusions (high-frequency entities)
- Parallel automation execution where possible
- External services (EMQX, Grafana) reduce HA load
- Efficient state management

---

## Conclusion

This Home Assistant configuration represents a **mature, professionally-engineered smart home** that successfully balances:
- **Cost savings** through sophisticated energy management
- **Security** with comprehensive monitoring and alerts
- **Comfort** through intelligent automation
- **Family needs** with context-aware modes
- **Maintainability** through excellent code organization

The **energy management system** is world-class, demonstrating deep understanding of solar forecasting, battery optimization, tariff-aware scheduling, and cost minimization. The integration of Predbat, Solar Assistant, myEnergi devices, and Octopus Energy creates an intelligent system that maximizes renewable energy usage while minimizing electricity costs.

The **safety interlocks**, **multi-layer presence detection**, and **context-aware automation** demonstrate exceptional attention to detail and user experience. This isn't just automation for automation's sake - every feature serves a clear purpose in making the home more efficient, secure, or comfortable.

**Overall Assessment:** 10/10 - Professional-grade smart home automation with exceptional energy management.

---

# Technical Implementation Guide

This section provides technical details for implementing new features, modifications, and maintenance in this Home Assistant configuration.

## Directory Structure

```
homeassistant-config/
├── configuration.yaml           # Main config with includes
├── automations.yaml            # UI-generated automations (20 automations)
├── scripts.yaml                # UI-generated scripts
├── scenes.yaml                 # Scene definitions (75 scenes)
├── input_text.yaml             # Text input helpers
├── sensor.yaml                 # Sensor definitions
├── customize.yaml              # Entity customizations
├── device_tracker.yaml         # Device tracker config
├── notify.yaml                 # Notification platform config
├── allowed_external_dirs.yaml  # Filesystem access whitelist
├── allowed_external_urls.yaml  # URL whitelist
├── secrets.yaml                # Secrets (gitignored)
├── packages/                   # Package-based configuration
│   ├── home.yaml              # Home mode automations
│   ├── home_assistant.yaml    # HA system automations
│   ├── time.yaml              # Time-based helpers
│   ├── smoke_alarms.yaml      # Smoke alarm automations
│   ├── tracker.yaml           # Presence tracking
│   ├── rooms/                 # Room-based packages
│   │   ├── living_room.yaml
│   │   ├── kitchen/
│   │   │   ├── kitchen.yaml
│   │   │   └── meater.yaml
│   │   ├── bedroom/
│   │   │   ├── bedroom.yaml
│   │   │   ├── sleep_as_android.yaml
│   │   │   └── awtrix_light.yaml
│   │   ├── conservatory/
│   │   │   ├── conservatory.yaml
│   │   │   ├── octoprint.yaml
│   │   │   └── airer.yaml
│   │   ├── office/
│   │   │   ├── office.yaml
│   │   │   └── steam.yaml
│   │   └── [other rooms]...
│   └── integrations/          # Integration-based packages
│       ├── energy/            # Energy management
│       ├── hvac/              # Climate control
│       ├── messaging/         # Notifications
│       ├── transport/         # Travel/vehicles
│       └── weather/           # Weather integrations
├── esphome/                    # ESPHome device configs
│   ├── common/                # Shared packages
│   ├── bed.yaml               # Bedroom pressure sensors
│   ├── leos-bed.yaml
│   ├── ashlees-bed.yaml
│   ├── office.yaml
│   ├── boiler.yaml
│   ├── central-heating.yaml
│   ├── water-softener.yaml
│   └── [motion sensors]...
└── themes/                     # Frontend themes

Total: 69 package YAML files
```

## Configuration Architecture

### Split Configuration Pattern
The configuration uses `!include` and `!include_dir_named` directives:

```yaml
# configuration.yaml
homeassistant:
  packages: !include_dir_named packages/

automation ui: !include automations.yaml
script ui: !include scripts.yaml
scene: !include scenes.yaml
sensor: !include sensor.yaml
input_text: !include input_text.yaml
notify: !include notify.yaml
```

### Package Structure
Each package file is self-contained and can include:
- `automation:` - Automations for that domain
- `script:` - Scripts for that domain
- `sensor:` - Template sensors
- `binary_sensor:` - Binary sensors
- `input_boolean:` - Toggle helpers
- `input_number:` - Number helpers
- `input_select:` - Dropdown helpers
- `input_datetime:` - Date/time helpers
- `timer:` - Timer helpers
- `group:` - Entity groups

**Example Package Structure:**
```yaml
# packages/rooms/living_room.yaml
automation:
  - id: "1583956425622"
    alias: "Living Room: Motion Detected"
    triggers: [...]
    conditions: [...]
    actions: [...]

script:
  living_room_flash_lounge_lights_red:
    alias: "Living Room: Flash Lights Red"
    sequence: [...]

input_boolean:
  enable_living_room_motion_triggers:
    name: Enable Living Room Motion Triggers
    icon: mdi:motion-sensor

input_number:
  living_room_light_level_2_threshold:
    name: Living Room Light Level 2 Threshold
    min: 0
    max: 200
    step: 1
    unit_of_measurement: lux
```

## Naming Conventions

### Entity IDs

**Automations:**
- Format: `"Room/Domain: Action/Description"`
- Examples:
  - `"Living Room: Motion Detected"`
  - `"Conservatory: Turn On Airer"`
  - `"Home Mode: Changed"`
  - `"Energy: Battery Mode Validation"`

**Scripts:**
- Format: `domain_action_description` (snake_case)
- Room-specific: `room_action`
- System-wide: `action_description`
- Examples:
  - `send_to_home_log`
  - `send_direct_notification`
  - `living_room_flash_lounge_lights_red`
  - `check_conservatory_airer`
  - `arm_alarm_overnight`
  - `set_central_heating_to_home_mode`

**Input Helpers:**
- Booleans: `enable_[feature]` or `[feature]_mode`
- Numbers: `[room]_[metric]_threshold`
- Selects: `[domain]_mode`
- Examples:
  - `input_boolean.enable_living_room_motion_triggers`
  - `input_boolean.enable_conservatory_airer_schedule`
  - `input_boolean.naughty_step_mode`
  - `input_number.living_room_light_level_2_threshold`
  - `input_number.airer_minimum_temperature`
  - `input_select.home_mode`

**Scenes:**
- Format: `room_description` or `room_device_state`
- Examples:
  - `scene.living_room_lights_on`
  - `scene.living_room_lamps_yellow`
  - `scene.living_room_lights_red`
  - `scene.stairs_light_off`

**Sensors:**
- ESPHome: `[location]_[device]_[metric]`
- Template: `[domain]_[calculated_value]`
- Examples:
  - `sensor.living_room_motion_illuminance`
  - `sensor.conservatory_temperature_over_12_hours`
  - `sensor.apollo_r_pro_1_w_ef755c_ltr390_light`
  - `sensor.octopus_energy_electricity_current_rate`

### Automation ID Format
- UI automations: Timestamp-based (e.g., `"1583956425622"`)
- Keep IDs unique and never reuse

### Emoji Usage in Logs
The system uses emojis extensively in log messages for visual identification:
- 🛋️ Living Room
- 🧑‍🍳 Kitchen
- 🔋 Energy/Battery
- 🐾 Motion detected
- 💡 Lights
- 🚷 No motion
- 🔆/🔅 Bright/Dim
- ⏳ Timer
- 🏠 Home
- 🔒 Lock
- 📸 Camera
- :repeat: Mode change
- :detective: Privacy mode

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

### 3. Rate/Cost-Based Automation

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

### 4. Multi-Condition Safety Interlock

```yaml
automation:
  - alias: "Close Blinds with Safety Check"
    sequence:
      - wait_for_trigger:
          - trigger: state
            entity_id: binary_sensor.window_contact
            to: "off"
        timeout: "03:00:00"
        continue_on_timeout: false
      - action: cover.close_cover
        target:
          entity_id: cover.blind
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
              - action: script.send_actionable_notification
                data:
                  message: "Temperature {{ states('sensor.temperature') }}°C. Turn on device?"
```

**Key Principles:**
- First condition in `choose:` wins - order matters!
- Put time/presence conditions first if they should override temperature
- Order temperature checks from highest to lowest after priority conditions
- Use `for:` duration on triggers to prevent rapid cycling

## Common Script Patterns

### Core System Scripts

These scripts are called throughout the configuration:

#### 1. **Logging Script**
```yaml
script:
  send_to_home_log:
    alias: Send to Home Log
    fields:
      message:
        description: Log message
        example: "Motion detected"
      title:
        description: Log title/category
        example: "Living Room"
      log_level:
        description: "Normal or Debug"
        example: "Debug"
    sequence:
      - action: notify.home_log
        data:
          message: "{{ message }}"
          data:
            title: "{{ title }}"
```

**Usage:** Every automation should log significant events using this script.

#### 2. **Direct Notification Script**
```yaml
script:
  send_direct_notification:
    alias: Send Direct Notification
    fields:
      message:
        description: Notification message
      title:
        description: Notification title
    sequence:
      - action: notify.mobile_app_dannys_phone
        data:
          message: "{{ message }}"
          title: "{{ title }}"
```

#### 3. **Actionable Notification Pattern**
```yaml
script:
  send_actionable_notification:
    sequence:
      - action: notify.mobile_app
        data:
          message: "{{ message }}"
          data:
            actions:
              - action: "ACTION_ID"
                title: "Button Label"
```

**Follow-up automation:**
```yaml
automation:
  - alias: "Handle Notification Action"
    triggers:
      - trigger: event
        event_type: mobile_app_notification_action
        event_data:
          action: "ACTION_ID"
    actions:
      - action: [your action here]
```

### Scene Snapshot Pattern

```yaml
script:
  flash_lights_red:
    sequence:
      - action: scene.create
        data:
          scene_id: current_lights_snapshot
          snapshot_entities:
            - light.lamp_left
            - light.lamp_right
      - action: scene.turn_on
        target:
          entity_id: scene.lights_red
        data:
          transition: 0
      - delay:
          milliseconds: 500
      - action: scene.turn_on
        target:
          entity_id: scene.current_lights_snapshot
```

### Clock Emoji Script (Reusable Pattern)

This pattern provides a parameterized script that returns time-based emoji for use in automations:

```yaml
# scripts.yaml
script:
  get_clock_emoji:
    alias: Get Clock Emoji
    fields:
      hour:
        description: Hour in 12-hour format (1-12)
        example: "8"
      minute:
        description: Minute (0-59)
        example: "30"
    sequence:
      - variables:
          minute_suffix: "{% if minute | int > 0 %}30{% endif %}"
      - variables:
          emoji: ":clock{{ hour }}{{ minute_suffix }}:"
      - stop:
          response_variable: clock_result
          value:
            emoji: "{{ emoji }}"
```

**Usage Pattern:** Each automation calling the script should add its own call rather than sharing a result:

```yaml
automation:
  - alias: "Automation 1: Do Something"
    triggers: [...]
    actions:
      - action: script.get_clock_emoji
        data:
          hour: "{{ now().strftime('%I') | int }}"
          minute: "{{ now().minute | int }}"
        response_variable: clock_result
      - action: script.send_to_home_log
        data:
          message: "{{ clock_result.emoji }} Action description"
          title: "Domain"

  - alias: "Automation 2: Do Something Else"
    triggers: [...]
    actions:
      - action: script.get_clock_emoji
        data:
          hour: "{{ now().strftime('%I') | int }}"
          minute: "{{ now().minute | int }}"
        response_variable: clock_result
      - action: script.send_to_home_log
        data:
          message: "{{ clock_result.emoji }} Different action"
          title: "Domain"
```

**Implementation**: Applied to 28 instances across 9 files:
- packages/integrations/alarm.yaml (3)
- packages/integrations/hvac/eddi.yaml (1)
- packages/rooms/bedroom/bedroom.yaml (5)
- packages/rooms/bedroom3.yaml (3)
- packages/rooms/kitchen/kitchen.yaml (3, including 24→12 hour conversion)
- packages/rooms/living_room.yaml (4)
- packages/rooms/office/office.yaml (3)
- packages/rooms/stairs.yaml (1)
- packages/time.yaml (3)

## Template Patterns

### Common Template Sensors

#### Dynamic Rate-Based Decisions
```yaml
value_template: "{{ states('sensor.octopus_energy_electricity_current_rate') | float <= 0 }}"
```

#### Brightness/Attribute Checks
```yaml
value_template: "{{ state_attr('light.lamp', 'brightness') == none }}"
```

#### Multi-Entity State Checks
```yaml
value_template: >
  {{ is_state('binary_sensor.door_1', 'off') and
     is_state('binary_sensor.door_2', 'off') }}
```

#### Time-Based Calculations
```yaml
value_template: >
  {{ (as_timestamp(now()) - as_timestamp(states.sensor.last_update.last_changed)) / 60 > 30 }}
```

### Jinja2 Filters Used
- `| float` - Convert to float
- `| int` - Convert to integer
- `| default(value, true)` - Default value with boolean flag
- `with_unit=True` - Include units in state
- `| random` - Random selection from list
- `| length` - List/string length
- `| list` - Convert to list
- `| map(attribute='entity_id')` - Extract attributes
- `| selectattr('state', 'eq', 'on')` - Filter by state

## Helper Entity Patterns

### Input Boolean Usage
- **Enable/Disable Automations:** `input_boolean.enable_[feature]`
- **Modes:** `input_boolean.[mode]_mode`
- **Feature Flags:** `input_boolean.enable_[specific_condition]`

Example:
```yaml
input_boolean:
  enable_living_room_motion_triggers:
    name: Enable Living Room Motion Triggers
    icon: mdi:motion-sensor
    initial: true
```

### Input Number Usage
- **Thresholds:** Light levels, temperatures, rates
- **Durations:** Timer lengths
- **Limits:** Maximum values

Example:
```yaml
input_number:
  living_room_light_level_2_threshold:
    name: Living Room Light Threshold
    min: 0
    max: 200
    step: 1
    unit_of_measurement: lux
    icon: mdi:brightness-6
```

### Input Select Usage
- **Multi-state modes:** Home modes, heating modes
- **Option selection:** Scenes, presets

Example:
```yaml
input_select:
  home_mode:
    name: Home Mode
    options:
      - Normal
      - Holiday
      - No Children
      - Naughty Step Mode
    icon: mdi:home
```

### Timer Usage
- **Delayed Actions:** Light turn-off, announcements
- **Timeout Protection:** Safety interlocks

Example:
```yaml
timer:
  living_room_lamps_off:
    name: Living Room Lamps Off Timer
    duration: "00:05:00"
    icon: mdi:timer
```

## ESPHome Configuration

### Common Package Pattern
ESPHome devices use shared packages for consistency:

```yaml
# esphome/bed.yaml
substitutions:
  device_name: bed
  friendly_name: Bed

packages:
  esp32: !include common/esp32-base.yaml
  bluetooth: !include common/bluetooth-base.yaml

esphome:
  name: ${device_name}

# Device-specific configuration
sensor:
  - platform: ads1115
    name: "${friendly_name} Top Left"
    id: bed_top_left
    multiplexer: 'A0_GND'
    gain: 4.096
    update_interval: 1s
```

### ESPHome Device Categories

**1. Presence/Occupancy:**
- Pressure sensors (ADS1115)
- mmWave sensors (LD2412)
- Motion sensors (PIR)

**2. Environmental:**
- BME680 (air quality, temperature, humidity)
- LTR390 (light sensor)

**3. Control:**
- Central heating relay
- Boiler monitoring

**4. Utility:**
- Water softener monitoring

### OTA Updates
All ESPHome devices support OTA updates:
```yaml
ota:
  password: !secret esphome_ota_password
```

Update via: ESPHome dashboard or automation trigger

## Integration-Specific Patterns

### Octopus Energy
- Entity: `sensor.octopus_energy_electricity_current_rate`
- Unit: GBP/kWh
- Updates: Every 30 minutes
- Usage: Rate-based automation decisions

### Solar Assistant / Growatt
- Battery SoC: `sensor.growatt_battery_soc`
- Inverter Mode: `select.growatt_mode`
- Grid Import/Export: Real-time monitoring
- Integration: Local polling for faster updates

### Predbat
- Daily summaries via notification
- Battery charge/discharge predictions
- Integration with Octopus Energy tariffs

### Ring Alarm
- States: `armed_away`, `armed_home`, `disarmed`
- Entity: `alarm_control_panel.ring_alarm`
- Check door/window sensors before arming

### Hive Heating
- Entity: `climate.thermostat`
- Modes: `heat`, `off`, `auto`
- Radiator TRVs synchronized via automation

### Alexa Media Player
- Version: v5.9.0 (custom component)
- Announcement script: `script.alexa_announce`
- Multi-device support

### Sun-Based Automations (Circadian/Seasonal Triggers)

Use sun position triggers for automations that should adapt throughout the year:

```yaml
# Trigger at specific solar events
triggers:
  - trigger: sun
    event: sunrise
    id: morning
  - trigger: sun
    event: sunset
    id: evening
  - trigger: sun
    event: sunset
    offset: "-01:00:00"  # 1 hour before sunset
    id: pre_sunset
  - trigger: sun
    event: sunset
    offset: "01:00:00"   # 1 hour after sunset
    id: post_sunset

actions:
  - choose:
      - conditions:
          - condition: trigger
            id: morning
        sequence:
          - action: script.send_to_home_log
            data:
              message: "☀️ Sunrise - Transitioning to daytime settings"

      - conditions:
          - condition: trigger
            id: pre_sunset
        sequence:
          - action: script.send_to_home_log
            data:
              message: "🌆 Pre-sunset - Transitioning to evening settings"
```

**Benefits:**
- Automatically adjusts throughout the year (no seasonal schedule changes)
- Winter: Earlier sunset → earlier warm lighting transitions
- Summer: Later sunset → longer daytime lighting
- More natural alignment with circadian rhythm

**Real-world example:** Circadian lighting implementation for Leo's bedroom uses sun-based triggers at:
- Sunrise: Cool white 4500K for alertness
- Sunset -1h: Warm white 3200K for transition
- Sunset +1h: Very warm 2700K for sleep preparation

## Recorder & Database

### Exclusion Strategy
High-frequency, low-value entities are excluded:

```yaml
recorder:
  exclude:
    domains: [automation, calendar, conversation, image, sun, tts]
    entity_globs:
      - sensor.time*
      - sensor.*_wifi_signal*
      - sensor.*_uptime
      - sensor.*_rssi
      - binary_sensor.*_status
      - media_player.*_volume_level
```

### InfluxDB Integration
- API Version: 2
- Retention: Configured server-side
- External Grafana dashboards
- Use for long-term analytics

## Development Workflow

### 1. Making Changes
- Edit YAML files directly
- Use YAML validator before committing
- Check configuration: Developer Tools → Check Configuration
- Reload specific domains when possible (avoid full restart)

### 2. Testing Automations
- Use "Run Actions" in automation editor
- Check Home Log for debug messages
- Test all conditions and branches
- Verify helper entity states

### 3. Git Workflow

```bash
git status
git add [files]
git commit -m "Description"
git push
```

The Git Pull addon automatically syncs changes.

#### Commit Message Format

Use clear, descriptive commit messages following this structure:

```
<Subject line - imperative mood, ~50 chars>

<Body - what changed and why>
- Bullet points for multiple changes
- Include context and rationale
- Reference line numbers for specific fixes

<Footer>
Related: GitHub issue #XXX (if applicable)
Closes: #XXX (if issue is completed)
```

**Example:**
```
Fix critical issues in office package

- Fixed duplicate automation aliases (lines 587 & 627)
  - Renamed to "Partially Close Office Blinds At Sunset" (closes to 25%)
  - Renamed to "Fully Close Office Blinds At Night" (closes fully 1hr after)
- Fixed timer duration message mismatch
  - Corrected "2 minutes" to "1 minute" for timer duration
  - Updated total to "3 minutes (2 min detection + 1 min timer)"
- Fixed incorrect brightness message operator
  - Changed < to > to match "bright" condition in log message

Related: #172
```

#### GitHub Issue Workflow

**When Issue Complete:** Use `Closes: #XXX` (fully done) or `Related: #XXX` (partial) in commit. Add `testing` label with `gh issue edit <#> --add-label "testing"`. Remains open until user verifies.

**Labels:** `testing` (awaiting verification), `bug` (issue), `enhancement` (feature), `blocked` (external dependency)

**Example Workflow:**
```bash
# After implementing feature
git add packages/integrations/energy/energy.yaml
git commit -m "Add battery depletion notification

Partially completes issue #113

- Implementation details...

Related: #113"

# Tag issue for testing
gh issue edit 113 --add-label "testing"

# User tests and closes issue when verified
```

#### Testing Before Pushing

Always create a testing checklist before pushing changes:
1. Critical functionality affected
2. Automation traces to verify
3. Log messages to check
4. Edge cases to consider

Test locally before pushing to main branch.

### 4. ESPHome Updates
- Edit device YAML in `esphome/` directory
- Validate configuration
- OTA update to device
- Monitor logs for issues

### 5. Rollback Strategy
- Git history for reverting changes
- Snapshot before major changes
- Test in non-critical automations first

### 6. Deferred Work Tracking

**Decision Matrix:**
- **Fix immediately:** Critical bugs (logic/syntax errors), security issues, runtime failures, blocking issues
- **Defer (create GitHub issue):** Low-priority improvements, large refactors, pattern fixes affecting multiple files, optimizations not affecting functionality

**Workflow:**
1. Create issue with `gh issue create --title "..." --body "..." --label enhancement`
2. Document full scope with specific line numbers
3. Reference in claude.md for future work

**Example:** Issue #176 (7 unsafe brightness checks across 3 files) deferred from living room review to maintain focus on 5 critical fixes (#177-181)

## User Preferences & Conventions

### Entity Management

**Helper Entities (input_boolean, input_number, timer):**
- Keep in **UI**, not YAML
- Reason: Easier to adjust values without reloading/restarting
- Exception: May add to YAML for version control if explicitly requested

**Groups:**
- Device_tracker groups defined elsewhere (not in room packages)
- Keeps room packages focused on room-specific logic

### Code Review Approach

**Incremental Fixes Over Large Refactors:**
- Fix critical bugs first, one at a time
- Show changes/diffs before applying edits
- Allow user to provide input before each change
- Commit after each logical group of fixes
- Test before proceeding with more changes

**Defer Complex Refactors:**
- Use GitHub issues to track deferred work
- Document rationale and proposed approach
- Let user review and test critical fixes before major refactors
- Examples: Motion detection consolidation, blind management centralization

### YAML Conventions

**Shorthand Syntax:**
- `- and:` notation is valid (equivalent to `- condition: and`)
- `- or:` notation is valid (equivalent to `- condition: or`)
- Keep code compact where readability isn't impacted

**Emoji Usage:**
- Keep emoji shortcodes like `:hourglass_flowing_sand:`, `:office:`, `:hotsprings:`
- Don't replace with Unicode equivalents in YAML
- Prefer "🏢 Office" format (Unicode + text) for log titles and messages
- Use emojis for visual identification in logs: 🐾 (motion), 💡 (lights), 🚷 (no motion), 🚨 (emergency)

**Home Assistant 2026.1+ Syntax:**
- Use `action:` (not deprecated `service:`)
- Use `triggers:` (not deprecated `trigger:`)
- Use `conditions:` (not deprecated `condition:` at automation level)

**Automation ID Format:**
- Always use 13-digit random numbers for automation IDs
- Example: `id: "1736794523847"`
- Ensures unique IDs and consistency across configuration

**Git Commit Format:**
- Do NOT include `Co-Authored-By: Claude <model> <noreply@anthropic.com>` in commit messages
- Keep commits clean and user-attributed only
- Reason: Maintains clear authorship and responsibility for changes
- **CRITICAL:** This applies to ALL commits without exception

**Edit Approval Process:**
- Show diffs for changes > 20 lines; brief explanation for smaller fixes
- Allow user opportunity to provide context before applying

## Common Gotchas & Best Practices

| Issue | Solution | Example |
|-------|----------|---------|
| **State vs Attributes** | Use `condition: template` for attributes | `{{ state_attr('light.lamp', 'brightness') > 100 }}` |
| **Unavailable Sensors** | Always check for unavailable/unknown | `not in ['unavailable', 'unknown']` |
| **Float Conversion** | Convert sensor values before comparison | `\| float > 0` |
| **Parallel Actions** | Use `parallel:` for independent tasks | Logging + light turn on together |
| **Timer Cancellation** | Cancel timers when condition reverses | `action: timer.cancel` |
| **Mode Selection** | `single` (default), `restart`, `queued`, `parallel` | Use `queued` with `max:` for frequent triggers |
| **Logging** | Always include room/domain title + sensor values | Title: "🛏️ Leo's Bedroom", message with values |
| **Scene Transitions** | `transition: 1` (smooth) or `0` (instant) | Prevent jarring light changes |

### 9. Attribute Access Patterns

**Condition Type Selection:**
- `condition: state` - For entity state only (NOT attributes)
- `condition: numeric_state` with `attribute:` - For numeric attribute comparisons
- `condition: template` - For complex logic or safe null-checking

**Safe Attribute Access:**
- Use `| default(0, true)` filter instead of fragile `== none` checks
- Use `!= 'unavailable'` for state checks
- Example: `{{ state_attr('light.lamp', 'brightness') | default(0, true) > 100 }}`

**Real-world:** Fixed living_room.yaml (lines 1059-1115) where `condition: state` with `attribute:` became `condition: numeric_state`. GitHub Issue #176 tracks 7 remaining unsafe `== none` checks for optimization.

## Entity ID Reference

| Entity | Purpose |
|--------|---------|
| `input_select.home_mode` | Normal/Holiday/No Children/Naughty Step |
| `alarm_control_panel.ring_alarm` | Armed Away/Home/Disarmed |
| `climate.thermostat` | Hive heating |
| `sensor.octopus_energy_electricity_current_rate` | Current electricity rate (GBP/kWh) |
| `sensor.growatt_battery_soc` | Battery state of charge |
| `person.danny`, `.terina`, `.leo`, `.ashlee` | Presence tracking |
| `device_tracker.leos_switch` | Leo's Nintendo Switch |
| `binary_sensor.terinas_work_laptop` | Work laptop status |

**Common Scripts:**
- `send_to_home_log` - Log messages
- `send_direct_notification` - Mobile notifications
- `arm_alarm_overnight`, `set_alarm_to_disarmed_mode`, `set_central_heating_to_home_mode`, `turn_everything_off`, `alexa_announce`

## Testing & Validation

| Phase | Action | Purpose |
|-------|--------|---------|
| **Pre-Deploy** | YAML validate | Catch syntax errors |
| **Pre-Deploy** | Check Configuration | Verify entity refs |
| **Pre-Deploy** | Test automation manually | Verify logic works |
| **Pre-Deploy** | Test edge cases | Handle unavailable sensors |
| **Debugging** | Check automation traces | Verify condition flow |
| **Debugging** | Review Home Log | Check messages |
| **Debugging** | Verify entity states | Monitor changes |
| **Debugging** | Test templates | Check conditions |

## Performance Considerations

### 1. Automation Efficiency
- Use specific entity triggers (not groups of 50+ entities)
- Avoid polling in templates where possible
- Use `update_interval` wisely in sensors
- Consider `mode: queued` with reasonable `max:` values

### 2. Recorder Optimization
- Exclude high-frequency sensors
- Use appropriate `purge_keep_days` (currently 30)
- Monitor database size

### 3. External Services
- MQTT broker (EMQX) - reduces HA load
- Grafana - offloads visualization
- InfluxDB - long-term storage

## Security Considerations

### 1. Secrets Management
All sensitive data in `secrets.yaml`:
```yaml
# Configuration
host: !secret influxdb_host
token: !secret influxdb_token

# secrets.yaml (gitignored)
influxdb_host: "192.168.1.10"
influxdb_token: "your_token_here"
```

### 2. Trusted Proxies
HTTP reverse proxy configuration:
```yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - !secret trusted_proxy1
```

### 3. External Access
- Use allowed URLs/directories
- OpenID authentication configured
- Privacy mode for cameras

## Common Tasks

| Task | Steps |
|------|-------|
| **Add Room** | Create `packages/rooms/[room_name].yaml` → define automations/scripts → check config → reload |
| **Add ESPHome Device** | Create `esphome/[device_name].yaml` → use common packages → compile/upload → auto-discovers |
| **Modify Energy Logic** | Check rate/battery sensors → test threshold logic → log decisions → monitor full cycle |
| **Create Notification** | Use `send_to_home_log` (internal) or `send_direct_notification` (mobile) → add buttons if needed → create action handler |

## File Maintenance

### Regular Updates
- ESPHome firmware updates (automation available)
- Custom component updates (Alexa Media, myEnergi)
- Home Assistant core updates
- Check deprecated features

### Git Maintenance
```bash
# Check current status
git status

# View recent changes
git log --oneline -10

# View specific file history
git log -p packages/rooms/living_room.yaml
```

## Code Review Process

### Review Checklist

When reviewing packages, check for:

**1. Critical Issues (Fix Immediately):**
- Duplicate automation IDs or aliases
- Logic errors (wrong operators, mismatched messages, incorrect conditions)
- Syntax errors or deprecated syntax
- Missing handlers for actionable notifications
- Timer duration mismatches in messages
- Unsafe attribute access patterns (== none instead of default filter)
- Invalid condition syntax (state with attribute: key instead of numeric_state)
- Redundant conditional logic in actions (checking condition that already checked in conditions)
- Missing response variable calls (referencing `clock_result.emoji` without calling `script.get_clock_emoji` first)

**Real-world Examples from Living Room Review (5 critical fixes):**
1. **Undefined response variables:** Lines 435-480, 481-514 - Missing `script.get_clock_emoji` call before using `clock_result.emoji`
2. **Invalid condition syntax:** Lines 1059-1115 - Used `condition: state` with `attribute:` key (6 instances) → Changed to `condition: numeric_state` with `below: 50`
3. **Unquoted YAML values:** Line 969 - `log_level: Debug` (should be `log_level: "Debug"`)
4. **Redundant condition checks:** Lines 1072-1088 - Conditions checked in both automation condition + nested if/then blocks
5. **Motion detection logic clarity:** Lines 21-120 - Yellow flash signal misunderstood; added alias + documentation

**2. Medium Priority (Schedule/Defer):**
- Large refactors that consolidate duplicate logic
- Performance optimizations
- Missing entity definitions (if needed in YAML)
- Automation mode specifications
- File size issues (consider splitting 1000+ line files)

**3. Low Priority (Nice to Have):**
- File organization improvements
- Documentation additions
- Naming consistency
- Comment clarity

### Known Valid Patterns

**Not bugs if they look unusual:**
- Shorthand syntax: `- and:`, `- or:`, `- not:` (equivalent to full condition syntax)
- Emoji shortcodes: `:office:`, `:hourglass_flowing_sand:` (valid in YAML)
- Multiple triggers with different thresholds (temperature cascading)
- Scripts without explicit `mode:` (defaults to `single`)
- Multi-branch motion automations (context-specific responses)
- Blind tilt position checks with `numeric_state` + attributes
- Yellow/red flash signals in motion detection (intentional visual feedback)

### Common Review Findings

| Finding | Solution |
|---------|----------|
| **Large files (1000+ lines)** | Consider splitting by domain (lights, blinds, climate, computer) |
| **Duplicate logic** | Create centralized script or consolidate with better condition ordering |
| **Cascading thresholds** | Order by priority first: Time/presence → highest to lowest threshold |
| **Unsafe attribute access** | Use `numeric_state` or `default()` filter, avoid `== none` |
| **Missing handlers** | Actionable notifications need `mobile_app_notification_action` automation |

**Real-world:** Issue #176 tracks 7 unsafe brightness checks (deferred for optimization pass)

### Review Workflow

| Phase | Focus |
|-------|-------|
| **Initial Scan** | File size, automation count, duplicate IDs/aliases, syntax errors |
| **Logic Review** | `choose:` ordering, operators (>, <, ==), timer messages, cascading logic |
| **Pattern Analysis** | Duplicate logic, consolidation opportunities, complex nesting |
| **Prioritization** | Fix critical bugs first → defer improvements → note enhancements |
| **Implementation** | One issue at time → show diffs → commit per group → test |

### Lessons Learned (2026-01-15)

**Key Fixes Applied:**
- 5 critical bugs (undefined variables, invalid conditions, unquoted values, redundant checks, undocumented logic)
- Circadian lighting automation (PR #175)
- Clock emoji script deployment (28 instances, 9 files)
- Deferred work tracking (Issue #176 for 7 unsafe brightness checks)

**Best Practices:**
- Incremental fixes before refactoring
- Approvals after each fix type
- GitHub issues for deferred work
- Use centralized scripts (DRY code)
- First `choose:` match wins - order matters
- Append log messages, don't replace
- Use `numeric_state` for attribute checks, not `state`
- Document visual signals/intentional behaviors
- Consolidate redundant condition checks

### Session Summary (2026-01-20)

**Comprehensive Room Package Review & Fixes**

**Files Reviewed & Fixed:**
1. **porch.yaml** (644 lines, 4 issues identified)
   - ✅ CRITICAL: Removed impossible condition blocking motion detection automation (lines 12-15)
   - ✅ Fixed malformed emoji `:no_bell:` → 🔕 (2 locations, lines 560, 568)
   - ✅ Added missing space in message "and🧑‍🤝‍🧑" → "and 🧑‍🤝‍🧑" (line 160)
   - ⏸️ Deferred: Duplicate alias "Porch: Front Door Closed" (line 213)
   - Commit: 46bca24b

2. **kitchen/kitchen.yaml** (1,933 lines, 11 issues identified)
   - ✅ CRITICAL: Added `script.get_clock_emoji` calls before using `clock_result.emoji` (3 locations)
     - Line 14-18: "Kitchen: Turn Off Lights At Night"
     - Line 471-475: "Kitchen: Turn Off Lights In The Morning" (weekday)
     - Line 496-500: "Kitchen: Turn Off Lights In The Morning" (weekend)
   - ✅ CRITICAL: Fixed wrong alias "Reset Oven Preheated" → "Reset Dishwasher Cycle In Progress" (line 897)
     - Automation monitors dishwasher but had oven alias (copy-paste error)
   - ✅ CRITICAL: Fixed duplicate alias "Battery has charge left" → "Battery is depleted" (line 1061)
     - Conditions opposite (above vs <=) but had identical alias
   - Commit: 28ae11a2

**Key Findings:**
- Pattern 1: **Undefined response variables** - Using `{{ clock_result.emoji }}` without calling `script.get_clock_emoji` first
  - Solution: Add script call with `response_variable:` before using variable
  - Affected: kitchen.yaml (3 instances)

- Pattern 2: **Duplicate/wrong automation aliases** - Copy-paste errors creating misleading automation names
  - Affected: porch.yaml (1), kitchen.yaml (2)
  - Impact: Difficult debugging, misleading logs

- Pattern 3: **Logic errors with contradictory conditions** - Conditions that can never be true
  - Example: Trigger on sensor="on" but condition requires sensor="off"
  - Affected: porch.yaml (1 CRITICAL)

**Deferred Issues:**
- porch.yaml line 213: Duplicate alias (user chose to defer)
- Remaining 67+ issues across 11 files documented in plan file

**Commits Made:**
- No Claude attribution in any commit messages (enforced per user preference)
- Clear, detailed commit messages with specific line numbers and rationale

**Architecture Insights:**
- `script.get_clock_emoji` is a response-variable script that needs explicit calls
- Each automation should call it independently (not shared response variables)
- Copy-paste errors are common source of logic/alias bugs
- Automation conditions must match trigger logic or they'll never execute

---

This technical guide should enable Claude to assist with implementations, debugging, and enhancements while maintaining consistency with existing patterns and architecture.
