# Home Assistant Templating Reference

**Source:** https://www.home-assistant.io/docs/configuration/templating/
**Engine:** Jinja2 (Python templating)
**Date:** 2026-01-22
**Purpose:** Comprehensive reference for template syntax, functions, filters, and best practices

---

## Template Fundamentals

### Basic Syntax

All templates use **Jinja2** syntax wrapped in `{{ }}`:

```yaml
# Single-line templates MUST use quotes
value_template: "{{ states('sensor.temperature') }}"

# Multi-line templates can use quotes or block syntax
value_template: >
  {% set temp = states('sensor.temperature') | float(0) %}
  The temperature is {{ temp }}°C
```

### Template Contexts

Templates can be used in:
- **Automation conditions** - `condition: template`
- **Sensor templates** - `value_template:`, `attribute_templates:`
- **Binary sensor templates** - `value_template:`
- **Trigger variables** - `trigger_variables:`
- **MQTT topics** - Message processing
- **Notifications** - Dynamic message content
- **Script data** - Parameterized calls

---

## State Access Functions

### states() Function

Get entity state as a **string**:

```jinja
{{ states('light.kitchen') }}          # Returns: "on" or "off"
{{ states('sensor.temperature') }}     # Returns: "23.5" (as string!)
{{ states('switch.device') }}          # Returns: "unavailable" if offline
```

**CRITICAL:** Returns strings, not typed values!

### state_attr() Function

Get entity **attributes**:

```jinja
{{ state_attr('light.kitchen', 'brightness') }}        # Returns: 128
{{ state_attr('weather.home', 'temperature') }}        # Returns: 18.5
{{ state_attr('cover.blind', 'current_position') }}    # Returns: 75
```

### is_state() Function

Test entity state **safely**:

```jinja
{% if is_state('light.kitchen', 'on') %}
  Light is on
{% endif %}

{{ 'On' if is_state('light.kitchen', 'on') else 'Off' }}
```

### is_state_attr() Function

Test entity attribute value:

```jinja
{% if is_state_attr('light.kitchen', 'brightness', 255) %}
  Light is full brightness
{% endif %}
```

---

## Type Conversion & Validation

### String to Number

```jinja
# Convert to float (with default)
{{ states('sensor.temperature') | float(0) }}          # Default to 0 if unavailable
{{ states('sensor.temperature') | float }}             # Error if unavailable

# Convert to integer
{{ states('sensor.count') | int(0) }}
{{ states('sensor.count') | int }}
```

**CRITICAL:** Always use `| float(default_value)` to prevent errors!

### Type Checking

```jinja
# Is this a number?
{{ is_number(some_value) }}              # True/False

# Is this available?
{{ states('sensor.temp') not in ['unavailable', 'unknown'] }}

# Safe comparison with type check
{{ value | float(0) > 20 if is_number(value) else False }}
```

---

## String Filters

### Common String Operations

```jinja
# Case conversion
{{ "hello" | upper }}                    # HELLO
{{ "HELLO" | lower }}                    # hello
{{ "hello world" | capitalize }}         # Hello world
{{ "hello world" | title }}              # Hello World

# String replacement
{{ "hello world" | replace("world", "HA") }}   # hello HA
{{ "hello123world" | regex_replace("\\d+", "") }}  # helloworld

# String length
{{ "hello" | length }}                   # 5

# String slicing
{{ "hello"[0:3] }}                       # hel

# Remove whitespace
{{ "  hello  " | trim }}                 # hello
{{ "hello  world" | wordwrap(5) }}       # hello world (wrapped)

# Slug/URL-safe format
{{ "Hello World!" | slugify }}           # hello-world

# Base64 encoding/decoding
{{ "hello" | b64encode }}                # aGVsbG8=
{{ "aGVsbG8=" | b64decode }}             # hello

# Encoding to JSON
{{ my_dict | to_json }}
{{ my_dict | tojson }}
```

---

## Numeric Filters & Functions

### Math Operations

```jinja
# Rounding
{{ 18.7 | round }}                       # 19
{{ 18.7 | round(1) }}                    # 18.7
{{ 18.7 | round(0) }}                    # 19
{{ 18.3 | round(0, 'floor') }}          # 18 (round down)
{{ 18.7 | round(0, 'ceil') }}           # 19 (round up)

# Absolute value
{{ -5 | abs }}                           # 5

# Min/Max
{{ [5, 2, 8, 1] | min }}                 # 1
{{ [5, 2, 8, 1] | max }}                 # 8

# Sum
{{ [1, 2, 3, 4] | sum }}                 # 10

# Average
{{ [10, 20, 30] | average }}             # 20
```

### Math Functions

```jinja
# Basic math
{{ 16 | sqrt }}                          # 4.0
{{ 2 | pow(3) }}                         # 8
{{ 0.5 | sin }}                          # 0.479...
{{ 0.5 | cos }}                          # 0.877...
{{ 10 | log }}                           # 2.302...
{{ 100 | log(10) }}                      # 2.0
```

---

## Time & Date Functions

### now() Function

```jinja
# Current datetime in local timezone
{{ now() }}                              # 2026-01-22 14:30:45.123456+00:00

# Extract components
{{ now().hour }}                         # 14
{{ now().minute }}                       # 30
{{ now().second }}                       # 45
{{ now().day }}                          # 22
{{ now().month }}                        # 1
{{ now().year }}                         # 2026
{{ now().weekday() }}                    # 2 (0=Monday, 6=Sunday)

# Format as string
{{ now().strftime('%Y-%m-%d') }}         # 2026-01-22
{{ now().strftime('%H:%M:%S') }}         # 14:30:45
{{ now().strftime('%I') }}               # 02 (12-hour format)
{{ now().strftime('%p') }}               # PM

# Unix timestamp
{{ now().timestamp() }}                  # 1737548445.123456

# Date arithmetic
{{ now() - timedelta(days=7) }}          # 7 days ago
{{ now() + timedelta(hours=2) }}         # In 2 hours
{{ (now() - as_timestamp(states.sensor.last_update.last_changed)) / 3600 }}  # Hours since
```

### as_timestamp() Function

Convert datetime to Unix timestamp:

```jinja
{{ as_timestamp(now()) }}                # 1737548445.123456
{{ as_timestamp('2026-01-22 14:30:45') }}  # Parse and convert
{{ as_timestamp(state_attr('automation.test', 'last_triggered')) }}
```

### relative_time() Function

Human-readable time difference:

```jinja
{{ relative_time(now()) }}               # just now
{{ relative_time(now() - timedelta(hours=2)) }}  # 2 hours ago
{{ relative_time(now() - timedelta(days=1)) }}   # a day ago
{{ relative_time(states.sensor.last_update.last_changed) }}
```

---

## List & Dict Operations

### List Filters

```jinja
# Join list items
{{ ['a', 'b', 'c'] | join(', ') }}       # a, b, c

# Get unique items
{{ [1, 2, 2, 3, 3, 3] | unique }}        # [1, 2, 3]

# Sort list
{{ [3, 1, 2] | sort }}                   # [1, 2, 3]
{{ [3, 1, 2] | sort(reverse=true) }}     # [3, 2, 1]

# Reverse list
{{ [1, 2, 3] | reverse }}                # [3, 2, 1]

# Get first/last items
{{ [1, 2, 3] | first }}                  # 1
{{ [1, 2, 3] | last }}                   # 3

# Flatten nested lists
{{ [[1, 2], [3, 4]] | flatten }}         # [1, 2, 3, 4]
{{ [[1, 2], [3, [4, 5]]] | flatten(1) }} # [1, 2, 3, [4, 5]] (1 level deep)

# Length of list
{{ [1, 2, 3] | length }}                 # 3
```

### Set Operations

```jinja
# Union (combine)
{{ [1, 2, 3] | union([3, 4, 5]) }}       # [1, 2, 3, 4, 5]

# Intersection (common items)
{{ [1, 2, 3] | intersect([2, 3, 4]) }}   # [2, 3]

# Difference (in first, not in second)
{{ [1, 2, 3] | difference([2, 4]) }}     # [1, 3]

# Symmetric difference (in either, not both)
{{ [1, 2, 3] | symmetric_difference([2, 3, 4]) }}  # [1, 4]
```

### List Comprehension

```jinja
# Filter list by condition
{{ [x for x in [1, 2, 3, 4] if x > 2] }}        # [3, 4]

# Map/transform list
{{ [x * 2 for x in [1, 2, 3]] }}                 # [2, 4, 6]

# Nested comprehension
{{ [[y * 2 for y in row] for row in [[1, 2], [3, 4]]] }}  # [[2, 4], [6, 8]]
```

### Dict Access

```jinja
# Direct access
{{ my_dict['key'] }}
{{ my_dict.key }}                # Both work for keys without special chars

# Safe access with default
{{ my_dict.get('missing', 'default_value') }}

# Dictionary keys/values/items
{{ my_dict | dictsort }}         # Sort by keys
{{ my_dict | dictsort(by='value') }}  # Sort by values

# JSON data from MQTT/REST
{{ value_json['temperature'] }}
{{ value_json.sensors[0].temp }}
```

---

## Conditional Logic

### If/Else

```jinja
{% if is_state('light.kitchen', 'on') %}
  Light is on
{% elif is_state('light.kitchen', 'off') %}
  Light is off
{% else %}
  Light is unavailable
{% endif %}
```

### Ternary Operator (Inline If)

```jinja
{{ 'On' if is_state('light.kitchen', 'on') else 'Off' }}

{{ states('sensor.temp') | float(0) | round(1)
   if is_number(states('sensor.temp'))
   else 'N/A' }}
```

### Logical Operators

```jinja
# AND
{% if is_state('light.kitchen', 'on') and states('sensor.temp') | float(0) > 20 %}
  Lights on and warm
{% endif %}

# OR
{% if is_state('light.kitchen', 'on') or is_state('light.bedroom', 'on') %}
  Some lights are on
{% endif %}

# NOT
{% if is_state('light.kitchen', 'off') %}  # Same as: not is_state(..., 'on')
  Light is off
{% endif %}

# Complex conditions
{% if (is_state('light.kitchen', 'on') or is_state('light.lounge', 'on'))
      and states('sensor.temp') | float(0) > 25 %}
  Lights on and very warm
{% endif %}
```

---

## Loops

### For Loop

```jinja
# Simple iteration
{% for entity in expand('group.lights') %}
  {{ entity.entity_id }}: {{ entity.state }}
{% endfor %}

# Loop over dictionary
{% for key, value in my_dict.items() %}
  {{ key }}: {{ value }}
{% endfor %}

# Loop variables
{% for item in [1, 2, 3] %}
  {{ loop.index }}: {{ item }}      # 1: 1, 2: 2, 3: 3
  {% if loop.first %}First item{% endif %}
  {% if loop.last %}Last item{% endif %}
{% endfor %}

# Break and continue (enabled extensions)
{% for item in items %}
  {% if item == 'skip_me' %}
    {% continue %}
  {% endif %}
  {% if item == 'stop_here' %}
    {% break %}
  {% endif %}
  {{ item }}
{% endfor %}
```

### Loop Variables

```jinja
{% for item in items %}
  loop.index      # 1-based index
  loop.index0     # 0-based index
  loop.revindex   # Reverse index (length - loop.index)
  loop.revindex0  # Reverse 0-based
  loop.first      # True on first iteration
  loop.last       # True on last iteration
  loop.length     # Total number of items
  loop.cycle()    # Cycle through values: loop.cycle('odd', 'even')
{% endfor %}
```

---

## Default Filter (Safety Critical!)

The `default` filter prevents errors when accessing undefined values:

```jinja
# Without default - ERRORS if undefined
{{ states('sensor.missing').state }}           # KeyError!

# With default - SAFE
{{ states('sensor.missing') | default('N/A') }}     # N/A

# With default(true) - Returns empty string instead of failing
{{ undefined_var | default }}                  # (empty string)
{{ undefined_var | default('fallback') }}      # fallback

# Safe attribute access
{{ state_attr('light.lamp', 'brightness') | default(0, true) }}
```

**CRITICAL PATTERN:** Always use `| default()` when accessing potentially undefined values!

---

## Advanced Patterns

### Pattern 1: Safe Number Comparison

```jinja
# WRONG - Can fail if sensor is unavailable
{% if states('sensor.temperature') > 20 %}
  Too warm
{% endif %}

# CORRECT - Handles unavailable/unknown states
{% if states('sensor.temperature') | float(-999) > 20 %}
  Too warm
{% endif %}

# MOST CORRECT - Type checking first
{% if is_number(states('sensor.temperature')) and states('sensor.temperature') | float(0) > 20 %}
  Too warm
{% endif %}
```

### Pattern 2: Entity Group Processing

```jinja
# Expand group into individual entities
{% for light in expand('group.all_lights') %}
  {{ light.name }}: {{ light.state }}
{% endfor %}

# Count lights that are on
{{ expand('group.all_lights') | selectattr('state', 'eq', 'on') | list | length }}

# Get list of on lights
{% set lights_on = expand('group.all_lights') | selectattr('state', 'eq', 'on') | map(attribute='entity_id') | list %}
{{ lights_on | join(', ') }}
```

### Pattern 3: Conditional Formatting with Units

```jinja
{% set temp = states('sensor.temperature') | float(0) %}
{% set temp_unit = state_attr('sensor.temperature', 'unit_of_measurement') %}

The temperature is {{ temp | round(1) }}{{ temp_unit if temp_unit else '°C' }}
```

### Pattern 4: JSON Processing from MQTT

```jinja
# Parse JSON from MQTT message
{{ value_json['sensor']['temperature'] | float(0) | round(1) }}

# Nested access with safety
{{ value_json.get('data', {}).get('reading', 'N/A') }}

# Array processing
{% for item in value_json['readings'] %}
  Reading {{ loop.index }}: {{ item['value'] }}
{% endfor %}
```

### Pattern 5: Attribute Fallback Chain

```jinja
# Try primary attribute, fall back to secondary
{% set brightness = state_attr('light.kitchen', 'brightness') or 0 %}
{% set color = state_attr('light.kitchen', 'color') or state_attr('light.kitchen', 'hs_color') or [] %}
Brightness: {{ brightness }}, Color: {{ color }}
```

### Pattern 6: Time-Based Logic

```jinja
# Turn on lights if sun down and motion
{% if (now().hour >= 18 or now().hour < 6) and is_state('binary_sensor.motion', 'on') %}
  Turn on lights - dark and motion detected
{% endif %}

# Seasonal adjustment
{% set is_winter = now().month in [11, 12, 1, 2] %}
Heating boost: {{ 'on' if is_winter else 'off' }}
```

### Pattern 7: Sensor Thresholding

```jinja
# Multi-level thresholding
{% set temp = states('sensor.temperature') | float(0) %}
{% if temp < 10 %}
  Too cold - boost heating
{% elif temp < 18 %}
  Cold
{% elif temp > 26 %}
  Too hot - open windows
{% elif temp > 22 %}
  Warm
{% else %}
  Comfortable
{% endif %}
```

---

## Common Filters Reference

| Filter | Purpose | Example |
|--------|---------|---------|
| `default(value)` | Fallback for undefined | `\| default('N/A')` |
| `float(default)` | Convert to float | `\| float(0)` |
| `int(default)` | Convert to integer | `\| int(0)` |
| `round(decimals)` | Round number | `\| round(1)` |
| `abs` | Absolute value | `\| abs` |
| `upper` | Uppercase string | `\| upper` |
| `lower` | Lowercase string | `\| lower` |
| `capitalize` | Capitalize first letter | `\| capitalize` |
| `replace(old, new)` | Replace substring | `\| replace('old', 'new')` |
| `regex_replace(pattern, replacement)` | Regex substitution | `\| regex_replace('[0-9]+', '')` |
| `trim` | Remove whitespace | `\| trim` |
| `join(sep)` | Join list with separator | `\| join(', ')` |
| `length` | Length of string/list | `\| length` |
| `sort` | Sort list | `\| sort` |
| `reverse` | Reverse list | `\| reverse` |
| `unique` | Remove duplicates | `\| unique` |
| `min` | Minimum value | `\| min` |
| `max` | Maximum value | `\| max` |
| `sum` | Sum list items | `\| sum` |
| `average` | Average of list | `\| average` |
| `b64encode` | Base64 encode | `\| b64encode` |
| `b64decode` | Base64 decode | `\| b64decode` |
| `to_json` | Convert to JSON | `\| to_json` |
| `tojson` | Convert to JSON | `\| tojson` |

---

## Common Functions Reference

| Function | Purpose | Example |
|----------|---------|---------|
| `states(entity_id)` | Get entity state | `states('light.kitchen')` |
| `state_attr(entity_id, attr)` | Get entity attribute | `state_attr('light.kitchen', 'brightness')` |
| `is_state(entity_id, state)` | Test entity state | `is_state('light.kitchen', 'on')` |
| `is_state_attr(entity_id, attr, value)` | Test attribute | `is_state_attr('light.kitchen', 'brightness', 255)` |
| `is_number(value)` | Check if value is numeric | `is_number(states('sensor.temp'))` |
| `expand(group_id)` | Expand group to entities | `expand('group.lights')` |
| `range(end)` | Generate number sequence | `range(5)` produces 0-4 |
| `range(start, end)` | Number range | `range(1, 5)` produces 1-4 |
| `range(start, end, step)` | Stepped range | `range(0, 10, 2)` produces 0,2,4,6,8 |
| `now()` | Current datetime | `now()` |
| `as_timestamp(dt)` | Convert to Unix timestamp | `as_timestamp(now())` |
| `relative_time(dt)` | Human-readable time diff | `relative_time(now())` |
| `distance(loc1, loc2)` | Distance between coordinates | `distance('zone.home', 'zone.work')` |
| `regex_match(pattern, string)` | Regex match | `regex_match('[0-9]+', '123')` |
| `regex_findall(pattern, string)` | Find all regex matches | `regex_findall('[0-9]+', 'a1b2c3')` |
| `regex_findall_index(pattern, string, index)` | Get indexed match | `regex_findall_index('([0-9]+)', '123abc', 0)` |
| `regex_replace(pattern, replacement, string)` | Regex substitution | `regex_replace('[0-9]+', 'X', 'a1b2')` |
| `slugify(string)` | URL-safe slug | `slugify('Hello World!')` |
| `sqrt(number)` | Square root | `sqrt(16)` |
| `pow(number, exponent)` | Power function | `pow(2, 3)` |
| `sin(number)` | Sine function | `sin(0.5)` |
| `cos(number)` | Cosine function | `cos(0.5)` |
| `tan(number)` | Tangent function | `tan(0.5)` |
| `asin(number)` | Arcsine function | `asin(0.5)` |
| `acos(number)` | Arccosine function | `acos(0.5)` |
| `atan(number)` | Arctangent function | `atan(0.5)` |
| `log(number)` | Natural logarithm | `log(10)` |
| `log(number, base)` | Logarithm with base | `log(100, 10)` |
| `e` | Euler's number | `e` |
| `pi` | Pi constant | `pi` |
| `tau` | Tau constant | `tau` |

---

## Limited Templates

Some contexts use a **restricted template subset** with fewer functions available:

**Not available in limited templates:**
- `distance()`
- `expand()`
- Time functions (partial restrictions)
- Some state access functions

**Contexts that are limited:**
- Trigger conditions in some automations
- `trigger_variables:` in automations
- Some integration-specific templates

**Workaround:** Use full templates in automation conditions instead of trigger conditions when complex logic needed.

---

## Common Mistakes to Avoid

| Mistake | Problem | Solution |
|---------|---------|----------|
| No quotes on single-line template | YAML parsing error | Always use `"{{ ... }}"` |
| Direct state comparison | String vs number mismatch | Use `\| float()` before math |
| Accessing undefined states | Error/exception | Use `\| default()` or `is_state()` |
| String concatenation wrong | Type mismatch | Use filter: `\| round(1)` or format: `{{ value }}.5` |
| Missing parentheses on function calls | Function not called | Use `now()` not `now` |
| Accessing unavailable entity | Error | Check with `not in ['unavailable', 'unknown']` |
| Attribute doesn't exist | KeyError | Use `state_attr(...) \| default()` |
| Loop variable scope | Variable undefined after loop | Define before loop if needed after |
| Wrong filter order | Unexpected results | Order matters: `\| float(0) \| round(1)` |
| Case sensitivity | No match found | Use `\| lower` or `\| upper` for comparison |

---

## Safe Attribute Access Pattern

Attributes don't always exist on entities. They may be missing when:
- Entity is in `off`, `unavailable`, or `unknown` state
- Attribute requires entity to be in specific state (e.g., `brightness` only when light is `on`)
- Device doesn't report that attribute
- Integration hasn't provided the attribute yet

### ❌ WRONG: Direct Attribute Access

```yaml
# WRONG: Fails when light is off (brightness doesn't exist)
- condition: numeric_state
  entity_id: light.kitchen
  attribute: brightness
  below: 100

# WRONG: Same issue, crashes when processing
- condition: template
  value_template: "{{ state_attr('light.kitchen', 'brightness') < 100 }}"
```

**Problem:** `KeyError` at runtime when attribute doesn't exist.

### ✅ CORRECT: Variables with Defaults

```yaml
# CORRECT: Extract with safe default in variables
actions:
  - variables:
      # Extract attribute, default to 0 if missing
      brightness: "{{ state_attr('light.kitchen', 'brightness')|int(0) }}"
      color_temp: "{{ state_attr('light.kitchen', 'color_temp')|int(370) }}"
      rgb_color: "{{ state_attr('light.kitchen', 'rgb_color')|default([255,255,255]) }}"

  # Now use safely in conditions/templates
  - condition: template
    value_template: "{{ brightness < 100 }}"

  - if:
      - condition: template
        value_template: "{{ color_temp > 300 }}"
    then:
      - action: light.turn_on
        target:
          entity_id: light.kitchen
```

### ✅ ALSO CORRECT: State Check Before Attribute

```yaml
# Check state first, THEN attribute
- condition: state
  entity_id: light.kitchen
  state: "on"

- condition: numeric_state
  entity_id: light.kitchen
  attribute: brightness
  below: 100
```

**Why this works:** If light is `on`, brightness attribute definitely exists.

### Common Safe Defaults

```jinja
# Numeric attributes
brightness: "{{ state_attr('light.kitchen', 'brightness')|int(0) }}"
temperature: "{{ state_attr('climate.room', 'current_temperature')|float(20) }}"
battery: "{{ state_attr('sensor.motion', 'battery')|int(100) }}"

# List attributes
rgb_color: "{{ state_attr('light.kitchen', 'rgb_color')|default([255,255,255]) }}"
color_xy: "{{ state_attr('light.kitchen', 'xy_color')|default([0.3, 0.3]) }}"

# String attributes
friendly_name: "{{ state_attr('entity', 'friendly_name')|default('Unknown') }}"
icon: "{{ state_attr('entity', 'icon')|default('mdi:help') }}"
```

### Real-world Example: Light Brightness Check

```yaml
# ❌ BAD: Fails when light is off
actions:
  - if:
      - condition: numeric_state
        entity_id: light.kitchen
        attribute: brightness
        below: 100
    then:
      - action: light.turn_on
        target:
          entity_id: light.kitchen

# ✅ GOOD: Safe attribute access
actions:
  - variables:
      brightness: "{{ state_attr('light.kitchen', 'brightness')|int(0) }}"
  - if:
      - condition: state
        entity_id: light.kitchen
        state: "off"
      - or:
          - condition: template
            value_template: "{{ brightness < 100 }}"
    then:
      - action: light.turn_on
        target:
          entity_id: light.kitchen
```

---

## Best Practices Summary

1. **Always use `| default()` for safety** - Prevents undefined variable errors
2. **Convert strings to numbers before math** - Use `| float(0)` or `| int(0)`
3. **Use `is_state()` for safety** - Safer than direct state access
4. **Quote single-line templates** - Required by YAML parser
5. **Check if number before comparing** - Use `is_number()` first
6. **Use state_attr() not direct access** - More reliable
7. **Handle unavailable/unknown states** - Not all entities always available
8. **Use loops for group expansion** - `expand()` returns individual entities
9. **Test templates in Developer Tools** - Catch errors before deployment
10. **Document complex templates** - Comment tricky conditionals
11. **Use filters in order** - `type conversion → math → formatting`
12. **Leverage template testing** - Developer Tools → Template tab

---

## Template Testing (Developer Tools)

Use **Developer Tools → Template** to test templates before deployment:

```jinja
# Test state access
{{ states('sensor.temperature') }}

# Test math with conversion
{{ states('sensor.temperature') | float(0) + 5 }}

# Test conditionals
{% if is_state('light.kitchen', 'on') %}
  Light is on
{% endif %}

# Test loops
{% for entity in expand('group.lights') %}
  {{ entity.name }}: {{ entity.state }}
{% endfor %}

# See results immediately - catch errors before production
```

---

## Real-World Examples from Config

### Example 1: Kitchen Motion Log Message
```jinja
🐾 Motion detected and it's dark
({{ states('sensor.kitchen_motion_ltr390_light') }} &
{{ states('sensor.kitchen_motion_2_illuminance') }}
< {{ states('input_number.kitchen_light_level_threshold') }} &
{{ states('input_number.kitchen_light_level_2_threshold', with_unit=True) }})
Turning cooker 💡 🔆 lights on.
```

### Example 2: Conditional Light Response
```jinja
{% if state_attr('light.lamp', 'brightness') | default(0, true) > 100 %}
  Lights already bright ({{ state_attr('light.lamp', 'brightness') }} brightness)
{% else %}
  Lights dim or off - adjusting...
{% endif %}
```

### Example 3: Time-Based Automation
```jinja
{% if now().hour >= 22 or now().hour < 6 %}
  It's nighttime - use dim lights
{% elif now().hour >= 6 and now().hour < 9 %}
  Morning - boost brightness
{% else %}
  Daytime - standard settings
{% endif %}
```

### Example 4: List Processing
```jinja
{% set lights_on = expand('group.living_room_lights') | selectattr('state', 'eq', 'on') | map(attribute='name') | list %}
Currently on: {{ lights_on | join(', ') if lights_on else 'No lights on' }}
```

### Example 5: Device Availability Check
```jinja
{{ 'Device online' if states('sensor.device_status') not in ['unavailable', 'unknown'] else 'Device offline' }}
```
