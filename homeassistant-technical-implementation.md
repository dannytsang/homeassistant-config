# Home Assistant Technical Implementation Guide

**Last Updated:** 2026-01-22
**Scope:** Directory Structure, Architecture, Naming Conventions, Patterns, Best Practices

---

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
│   ├── shared_helpers.yaml    # Global scripts & templates
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

---

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

---

## Naming Conventions

### Automations
- Format: `"Room/Domain: Action/Description"`
- Examples:
  - `"Living Room: Motion Detected"`
  - `"Conservatory: Turn On Airer"`
  - `"Home Mode: Changed"`
  - `"Energy: Battery Mode Validation"`

### Scripts
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

### Input Helpers
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

### Scenes
- Format: `room_description` or `room_device_state`
- Examples:
  - `scene.living_room_lights_on`
  - `scene.living_room_lamps_yellow`
  - `scene.living_room_lights_red`
  - `scene.stairs_light_off`

### Sensors
- ESPHome: `[location]_[device]_[metric]`
- Template: `[domain]_[calculated_value]`
- Examples:
  - `sensor.living_room_motion_illuminance`
  - `sensor.conservatory_temperature_over_12_hours`
  - `sensor.apollo_r_pro_1_w_ef755c_ltr390_light`
  - `sensor.octopus_energy_electricity_current_rate`

### Automation IDs
- UI automations: Timestamp-based (e.g., `"1583956425622"`)
- Always 13-digit random numbers
- Keep unique and never reuse

### Emoji Usage in Logs
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

---

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

---

## Recorder & Database Configuration

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

---

## User Preferences & Conventions

### Entity Management

**Helper Entities (input_boolean, input_number, timer):**
- Keep in **UI**, not YAML
- Reason: Easier to adjust values without reloading/restarting
- Exception: May add to YAML for version control if explicitly requested

**Groups:**
- Device_tracker groups defined elsewhere (not in room packages)
- Keeps room packages focused on room-specific logic

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

**Condition Aliases & Descriptions:**
- Condition objects support `alias:` parameter for documentation
- Condition objects do NOT support `description:` parameter (invalid syntax)
- Use `alias:` for brevity, descriptive labels on complex conditions
- Example:
  ```yaml
  - alias: "Quiet time is OFF"
    condition: state
    entity_id: schedule.notification_quiet_time
    state: "off"
  ```

**Git Commit Format:**
- Do NOT include `Co-Authored-By: Claude <model> <noreply@anthropic.com>` in commit messages
- Keep commits clean and user-attributed only
- Reason: Maintains clear authorship and responsibility for changes
- **CRITICAL:** This applies to ALL commits without exception

---

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

### Attribute Access Patterns

**Condition Type Selection:**
- `condition: state` - For entity state only (NOT attributes)
- `condition: numeric_state` with `attribute:` - For numeric attribute comparisons
- `condition: template` - For complex logic or safe null-checking

**Safe Attribute Access:**
- Use `| default(0, true)` filter instead of fragile `== none` checks
- Use `!= 'unavailable'` for state checks
- Example: `{{ state_attr('light.lamp', 'brightness') | default(0, true) > 100 }}`

---

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
