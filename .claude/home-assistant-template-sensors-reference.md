# Home Assistant Template Integration Reference

**Source:** https://www.home-assistant.io/integrations/template/
**Date:** 2026-01-25
**Purpose:** Complete reference for creating template-based entities (sensors, switches, lights, etc.) derived from other data using Jinja2 templates

---

## Overview

The Template integration enables creation of entities whose values derive from other data through template specifications. It supports 15 entity types including sensors, binary sensors, switches, lights, locks, covers, fans, weather, and more.

Key benefit: Create virtual entities that calculate values from existing data without needing separate hardware or integrations.

---

## Configuration Methods

### UI Setup
Access via: **Settings > Devices & services > Helpers > Create helper > Template**

Requirements:
- `default_config:` in `configuration.yaml`
- Can be mixed with YAML-based templates

### YAML Configuration

Entities defined under the `template:` key. Multiple configuration blocks supported:

```yaml
template:
  - sensor:
      - name: "Average temperature"
        state: >
          {% set bedroom = states('sensor.bedroom_temperature') | float %}
          {% set kitchen = states('sensor.kitchen_temperature') | float %}
          {{ ((bedroom + kitchen) / 2) | round(1, default=0) }}
```

---

## Two Entity Update Modes

### 1. State-Based Entities
- Update automatically when referenced entities change
- No triggers required
- Lower overhead
- Best for: Simple calculations, derivations from other entities

**Example:**
```yaml
template:
  - sensor:
      - name: "Sum of temperatures"
        state: "{{ states('sensor.room1_temp') | float(0) + states('sensor.room2_temp') | float(0) }}"
```

### 2. Trigger-Based Entities
- Update only when defined triggers fire
- Format mirrors automation triggers
- Greater control over update timing
- Best for: Expensive calculations, external data, webhooks

**Example:**
```yaml
template:
  - triggers:
      - trigger: time_pattern
        hours: 0
        minutes: 0
    sensor:
      - name: "Days since event"
        state: '{{ ((as_timestamp(now()) - as_timestamp(strptime("06.07.2018", "%d.%m.%Y"))) / 86400) | round() }}'
        unit_of_measurement: "Days"
```

---

## Common Configuration Options (All Entity Types)

| Option | Type | Description |
|--------|------|-------------|
| `availability` | template | Boolean determining if entity is available |
| `icon` | template | Dynamic icon definition |
| `name` | template | Entity name (supports templates) |
| `unique_id` | string | Unique identifier for UI customization and persistence |
| `variables` | map | Key-value pairs available in all templates |
| `default_entity_id` | string | Override automatic entity ID generation |

### Variables Example

```yaml
template:
  - triggers:
      - trigger: state
        entity_id: sensor.temperature
    variables:
      temp: "{{ states('sensor.temperature') | float(0) }}"
    sensor:
      - name: "Temperature Status"
        state: "{{ temp }}"
      - name: "Too Hot"
        state: "{{ temp > 25 }}"
```

---

## Supported Entity Types

### Template Sensor

State-based entity for numeric or string values.

```yaml
template:
  - sensor:
      - name: "Sun Angle"
        unit_of_measurement: "°"
        state: "{{ '%+.1f'|format(state_attr('sun.sun', 'elevation')) }}"
        icon: "mdi:sun"
        device_class: "illuminance"
```

**Configuration Options:**
- `state` (required): Template evaluating to numeric or string
- `unit_of_measurement`: Measurement units
- `state_class`: `measurement`, `total`, `total_increasing`
- `device_class`: Sets sensor type
- `attributes`: Custom attribute templates

**Device Classes:**
- `aqi`, `apparent_power`, `battery`, `co`, `co2`, `current`, `data_rate`, `data_size`, `date`, `distance`, `duration`, `energy`, `energy_storage`, `enum`, `frequency`, `gas`, `humidity`, `illuminance`, `irradiance`, `monetary`, `nitrogen_dioxide`, `nitrogen_monoxide`, `nitrous_oxide`, `ozone`, `pm1`, `pm10`, `pm25`, `power`, `power_factor`, `pressure`, `reactive_power`, `smoke`, `sound_pressure`, `speed`, `sulphur_dioxide`, `temperature`, `time`, `timestamp`, `volatile_organic_compounds`, `volatile_organic_compounds_parts`, `voltage`, `volume`, `volume_flow_rate`, `water`

---

### Template Binary Sensor

Boolean sensor with on/off states.

```yaml
template:
  - binary_sensor:
      - name: "Washing Machine"
        delay_off:
          minutes: 5
        state: "{{ states('sensor.washing_machine_power') | float(0) > 50 }}"
        device_class: "power"
        icon: "mdi:washing-machine"
```

**Configuration Options:**
- `state` (required): Template evaluating to True/False
- `device_class`: Sets sensor type (motion, presence, problem, etc.)
- `delay_on`: Time before transition to on (filters rapid toggles)
- `delay_off`: Time before transition to off
- `auto_off`: Duration to automatically turn off (trigger-based only)

**Device Classes:**
- `apparent_power`, `aqi`, `battery`, `battery_charging`, `co`, `co2`, `cold`, `connectivity`, `door`, `damp`, `dust`, `energy_storage`, `equipment_problem`, `exceptional`, `external_power`, `failure`, `fire`, `fog`, `frost`, `gas`, `generic_boolean`, `geofence`, `heat`, `heat_exchanger_valve`, `high_vibration`, `hinge`, `hot`, `humidity`, `light`, `lock`, `low_battery`, `low_memory`, `mailbox`, `moisture`, `motion`, `moving`, `mains_voltage`, `occupancy`, `opening`, `plug`, `power`, `presence`, `problem`, `radon`, `rain`, `recent_motion`, `running`, `safety`, `smoke`, `sound`, `speed`, `spoil`, `stability`, `stalk`, `sunny`, `temperature`, `tamper`, `tilt`, `tilt_open`, `update`, `uv_index`, `valve`, `vibration`, `visibility`, `voltage`, `water`, `wet`, `wetness`, `wind_movement`, `wind_speed`, `window`, `workplace_safety`

---

### Template Switch

Control a switch state.

```yaml
template:
  - switch:
      - name: "Skylight"
        state: "{{ is_state('binary_sensor.skylight', 'on') }}"
        turn_on:
          action: switch.turn_on
          target:
            entity_id: switch.skylight_open
        turn_off:
          action: switch.turn_off
          target:
            entity_id: switch.skylight_close
        icon: "mdi:window-closed"
```

**Configuration Options:**
- `state` (optional): Template for current state
- `turn_on` (required): Action definition
- `turn_off` (required): Action definition
- `optimistic`: Update state immediately without waiting for template

**Optimistic Mode Example:**
```yaml
template:
  - switch:
      - name: "Fast Toggle"
        optimistic: true
        turn_on:
          action: script.toggle_device
        turn_off:
          action: script.toggle_device
```

---

### Template Light

Create virtual light with optional brightness and color.

```yaml
template:
  - light:
      - name: "Theater Lights"
        state: "{{ state_attr('sensor.theater', 'power') | bool }}"
        level: "{{ state_attr('sensor.theater', 'brightness') | int(0) }}"
        turn_on:
          action: script.theater_on
        turn_off:
          action: script.theater_off
        set_level:
          action: script.set_brightness
          data:
            brightness: "{{ brightness }}"
```

**Configuration Options:**
- `level`: Brightness template (0-255)
- `temperature`: Color temperature (in Kelvin)
- `hs`: Hue/saturation (0-360, 0-100)
- `rgb`: Red/green/blue (0-255)
- `rgbw`: Red/green/blue/white (0-255)
- `rgbww`: Red/green/blue/warm white/cool white (0-255)
- `effect`: Current effect
- `effect_list`: Available effects
- `supports_transition`: Boolean for transition capability
- `turn_on/turn_off/set_level/set_temperature/set_hs/set_rgb`: Action definitions

---

### Template Lock

Control lock state.

```yaml
template:
  - lock:
      - name: "Front Door"
        state: "{{ is_state('sensor.door_lock', 'locked') }}"
        lock:
          action: switch.turn_on
          target:
            entity_id: switch.door_lock
        unlock:
          action: switch.turn_off
          target:
            entity_id: switch.door_lock
        code_format: "^[0-9]{4}$"
```

**Configuration Options:**
- `state`: Optional state template
- `lock` (required): Lock action
- `unlock` (required): Unlock action
- `open`: Open action (optional)
- `code_format`: Python regex for code validation
- `code_arm_required`: Boolean

---

### Template Cover

Control cover (blind, garage door, shade).

```yaml
template:
  - cover:
      - name: "Garage Door"
        device_class: garage
        state: "{{ states('sensor.garage_state') }}"
        position: "{{ states('sensor.garage_position') | int(0) }}"
        open_cover:
          action: script.open_garage
        close_cover:
          action: script.close_garage
        stop_cover:
          action: script.stop_garage
        set_cover_position:
          action: script.set_position
          data:
            position: "{{ position }}"
```

**Configuration Options:**
- `state`: open/opening/closing/closed/unknown
- `position`: 0-100 percentage (0=closed, 100=open)
- `tilt`: Tilt position
- `optimistic`: Maintain state internally
- `device_class`: awning, blind, curtain, damper, door, garage, gate, shade, shutter, window
- `open_cover`, `close_cover`, `stop_cover`: Action definitions
- `set_cover_position`, `set_cover_tilt`: Actions with parameters

---

### Template Select

Choose from predefined options.

```yaml
template:
  - select:
      - name: "Camera Mode"
        state: "{{ state_attr('camera.porch', 'mode') }}"
        options: "{{ ['off', 'on', 'auto'] }}"
        select_option:
          action: script.set_camera_mode
          data:
            mode: "{{ option }}"
```

**Configuration Options:**
- `options` (required): Available selections (list or template)
- `state`: Current selection template
- `select_option` (required): Action for selection

---

### Template Number

Control numeric value.

```yaml
template:
  - number:
      - name: "Desk Height"
        unit_of_measurement: "in"
        state: "{{ states('sensor.desk_height') | float(0) }}"
        min: 1
        max: 24
        step: 0.5
        mode: slider
        set_value:
          action: script.set_desk_height
          data:
            value: "{{ value }}"
```

**Configuration Options:**
- `min`: Minimum value
- `max`: Maximum value
- `step`: Increment size
- `mode`: slider or box
- `state`: Current value template
- `unit_of_measurement`: Units
- `set_value` (required): Action for value change

---

### Template Fan

Control fan speed and mode.

```yaml
template:
  - fan:
      - name: "Bedroom Fan"
        state: "{{ is_state('input_boolean.fan', 'on') }}"
        percentage: "{{ states('input_number.speed') | int(0) }}"
        preset_mode: "{{ states('input_select.mode') }}"
        turn_on:
          action: script.fan_on
        turn_off:
          action: script.fan_off
        set_percentage:
          action: script.set_speed
          data:
            percentage: "{{ percentage }}"
        set_preset_mode:
          action: script.set_mode
          data:
            mode: "{{ preset_mode }}"
        preset_modes:
          - auto
          - smart
          - low
          - medium
          - high
```

**Configuration Options:**
- `percentage`: Speed 0-100
- `preset_mode/preset_modes`: Named speed modes
- `oscillating`: Oscillation toggle template
- `direction`: forward/reverse
- `turn_on/turn_off`: Actions
- `set_percentage/set_preset_mode`: Actions with parameters

---

### Template Weather

Virtual weather entity from other data.

```yaml
template:
  - weather:
      - name: "Composite Weather"
        condition_template: "{{ states('weather.home') }}"
        temperature_template: "{{ states('sensor.indoor_temp') | float }}"
        temperature_unit: "°C"
        humidity_template: "{{ states('sensor.humidity') | float }}"
        pressure_template: "{{ states('sensor.pressure') | float }}"
        pressure_unit: "hPa"
        wind_speed_template: "{{ states('sensor.wind_speed') | float }}"
        wind_speed_unit: "m/s"
        forecast_daily_template: "{{ state_attr('weather.forecast', 'forecast') }}"
```

**Configuration Options:**
- `condition_template` (required): sunny, cloudy, rainy, snowy, windy, etc.
- `temperature_template` (required): Current temperature
- `humidity_template` (required): Humidity percentage
- `pressure_template`: Pressure value
- `wind_speed_template`: Wind speed
- `wind_bearing_template`: Wind direction (0-360°)
- `visibility_template`: Visibility distance
- `uv_index_template`: UV index
- `forecast_daily_template`: Daily forecast data
- `forecast_hourly_template`: Hourly forecast
- `forecast_twice_daily_template`: Twice-daily forecast
- `temperature_unit`: °C, °F, K
- `pressure_unit`: Pa, hPa, inHg, bar, mbar, mmHg
- `wind_speed_unit`: m/s, km/h, mph, knots

---

### Template Alarm Control Panel

Virtual alarm system.

```yaml
template:
  - alarm_control_panel:
      - name: "Home Alarm"
        state: "{{ states('input_select.alarm') }}"
        code_format: number
        arm_away:
          action: script.arm_away
        arm_home:
          action: script.arm_home
        arm_night:
          action: script.arm_night
        disarm:
          action: script.disarm
```

**Configuration Options:**
- `state`: armed_away, armed_home, armed_night, disarmed, triggered
- `code_format`: number, text, or no_code
- `code_arm_required`: Require code for arming
- `arm_away/arm_home/arm_night/disarm`: Action definitions

---

### Template Button

Simple button (no state).

```yaml
template:
  - button:
      - name: "Fast Forward"
        press:
          action: remote.send_command
          target:
            entity_id: remote.living_room
          data:
            command: fast_forward
```

**Note:** Buttons don't support state or trigger-based updates. Only press action.

---

### Template Image

Display image from URL.

```yaml
template:
  - image:
      - name: "Camera Snapshot"
        url: "http://192.168.1.100:8000/snapshot.jpg"
        verify_ssl: true
```

**Configuration Options:**
- `url`: Image URL (supports templates)
- `verify_ssl`: SSL verification

---

### Template Event

Fire events from templates.

```yaml
template:
  - event:
      - name: "Scene Controller"
        device_class: button
        event_type: "{{ states('input_select.button') }}"
        event_types:
          - single_press
          - double_press
          - hold
```

---

### Template Update

Monitor update availability.

```yaml
template:
  - update:
      - name: "Frigate Update"
        installed_version: "{{ states('sensor.frigate_version') }}"
        latest_version: "{{ states('sensor.frigate_latest') }}"
        install:
          action: script.update_frigate
```

---

### Template Vacuum

Control vacuum cleaner.

```yaml
template:
  - vacuum:
      - name: "Cleaning Robot"
        state: "{{ states('sensor.vacuum_state') }}"
        battery_level: "{{ states('sensor.vacuum_battery') | int(0) }}"
        start:
          action: script.start_vacuum
        return_to_base:
          action: script.vacuum_home
        stop:
          action: script.stop_vacuum
```

---

## Advanced Features

### Trigger-Based with Conditions & Actions

```yaml
template:
  - triggers:
      - trigger: state
        entity_id: sensor.temperature
    conditions:
      - condition: template
        value_template: "{{ is_number(states('sensor.temperature')) }}"
    actions:
      - action: script.process_temperature
        data:
          temp: "{{ states('sensor.temperature') }}"
    sensor:
      - name: "Valid Temperature"
        state: "{{ states('sensor.temperature') }}"
        unit_of_measurement: "°C"
```

### Self-Referencing (Trigger-based)

```yaml
template:
  - triggers:
      - trigger: event
        event_type: button_press
    binary_sensor:
      - name: "Recent Button Press"
        state: "{{ trigger.platform == 'event' }}"
        auto_off:
          seconds: 5
```

The `auto_off` property automatically transitions to off after specified duration.

### Webhook Trigger with Response Data

```yaml
template:
  - triggers:
      - trigger: webhook
        webhook_id: my_webhook_123
    actions:
      - action: script.process_webhook
        data:
          payload: "{{ trigger.json }}"
    sensor:
      - name: "Webhook Data"
        state: "{{ trigger.json.status }}"
        attributes:
          full_data: "{{ trigger.json }}"
```

Webhook response data available in templates through `trigger.json`.

---

## Template Functions & Filters

### State Access
- `states('entity_id')`: Get current state
- `state_attr('entity_id', 'attribute')`: Get attribute value
- `is_state('entity_id', 'value')`: Boolean check
- `is_number()`: Validate numeric value

### Filters
- `float(default)`: Convert to float with fallback
- `int(default)`: Convert to integer with fallback
- `round(digits, default)`: Round to decimal places
- `timestamp_custom()`: Format timestamp
- `timestamp_local()`: Local timestamp
- `as_timestamp()`: Convert to timestamp

### String Formatting
```
{{ '%+.1f'|format(value) }}  # Format with sign and decimals
{{ '{:.0f}%'.format(value) }}  # Format percentage
```

### Conditionals
```
{{ 'on' if is_state('light.kitchen', 'on') else 'off' }}
{% if value > 25 %}hot{% elif value > 15 %}warm{% else %}cool{% endif %}
```

### Math
```
{{ (value1 + value2) / 2 }}  # Average
{{ (value * 100) | round(1) }}  # Percentage
```

---

## Startup & Persistence

### Trigger-Based Entities
- Retain state across restarts
- Values preserved between HA sessions
- Recalculate on next trigger

### State-Based Entities
- Recalculate immediately upon startup
- No persistence (always derived)

---

## Legacy Migration

Old template sensor format (deprecated):

```yaml
# Old format (no longer recommended)
sensor:
  - platform: template
    sensors:
      my_sensor:
        value_template: "{{ states('sensor.source') }}"

# New format (current standard)
template:
  - sensor:
      - name: "My Sensor"
        state: "{{ states('sensor.source') }}"
```

---

## Common Use Cases

### 1. Average Multiple Sensors
```yaml
template:
  - sensor:
      - name: "Average Temperature"
        unit_of_measurement: "°C"
        state: >
          {%- set temps = [
            states('sensor.temp1') | float(0),
            states('sensor.temp2') | float(0),
            states('sensor.temp3') | float(0)
          ] %}
          {{ (temps | sum / temps | length) | round(1) }}
```

### 2. Conditional Light State
```yaml
template:
  - binary_sensor:
      - name: "Lights On"
        state: >
          {{ states('light.kitchen') == 'on' or
             states('light.bedroom') == 'on' }}
```

### 3. Weather-Responsive Automation
```yaml
template:
  - sensor:
      - name: "Recommended Action"
        state: >
          {% if states('weather.home') == 'rainy' %}
            Close shutters
          {% elif state_attr('weather.home', 'temperature') | float < 5 %}
            Close blinds for insulation
          {% else %}
            Open blinds for natural light
          {% endif %}
```

### 4. Device Status Summary
```yaml
template:
  - sensor:
      - name: "House Status"
        state: >
          {%- if is_state('binary_sensor.motion', 'on') %}
            Home - Activity detected
          {%- elif is_state('binary_sensor.door', 'on') %}
            Home - Door open
          {%- else %}
            Away - All clear
          {%- endif %}
```

---

## Troubleshooting

### Template Not Updating
- **State-based**: Check if referenced entities exist and change
- **Trigger-based**: Verify triggers are defined and firing
- Use `Developer Tools > States` to check entity presence

### Invalid Values
- Use `float(0)` or `int(0)` to provide fallback defaults
- Check `default_entity_id` doesn't conflict with other entities

### Slow Performance
- Complex templates on frequently-updating entities
- Use trigger-based instead of state-based if possible
- Reduce calculation complexity

---

## Related Documentation
- **Jinja2 Templating:** Home Assistant templating guide
- **Automations:** Trigger and condition syntax
- **Scripts:** Action execution patterns
- **Development Tools:** Testing templates

---

**Reference Created:** 2026-01-25
**HA Integration:** Template
**Status:** Current & Complete
**Last Updated:** 2026-01-25
