# Home Assistant Scripts Reference

**Source:** https://www.home-assistant.io/docs/scripts/
**Date:** 2026-01-22
**Purpose:** Core reference for script syntax, patterns, and best practices

---

## Script Basics

Scripts are **sequences of actions** that execute in order. They're core building blocks for automations and Alexa configurations.

### Basic Structure

```yaml
script:
  script_name:
    alias: "Human-readable name"
    description: "What this script does"
    fields:
      param_name:
        description: "Parameter description"
        example: "example value"
        selector:
          text:
    sequence:
      - action: service.name
        target:
          entity_id: entity.name
        data:
          param: value
    mode: single  # or restart, queued, parallel
```

### Execution Modes

| Mode | Behavior |
|------|----------|
| `single` | Don't start if already running (default) |
| `restart` | Stop existing run and start new one |
| `queued` | Queue up to `max:` invocations |
| `parallel` | Allow unlimited concurrent runs |

**Example with queuing:**
```yaml
mode: queued
max: 10  # Queue up to 10 invocations
```

---

## Variables & Data Flow

### Defining Variables

Variables are set using the `variables` action and can be templated:

```yaml
sequence:
  - variables:
      my_var: "{{ now().hour }}"
      sensor_value: "{{ states('sensor.temperature') }}"
      calculation: "{{ 5 * 2 }}"
  - action: script.some_action
    data:
      param: "{{ my_var }}"
```

### Variable Scope

- Variables defined at top level: accessible throughout script
- Variables in conditional blocks: remain in scope if previously defined
- Variables in nested blocks: scope follows nesting hierarchy

### Response Variables

**⚠️ CRITICAL:** Use `response_variable:` (SINGULAR) with template string syntax to capture script outputs:

```yaml
sequence:
  - action: script.get_clock_emoji
    data:
      hour: "{{ now().strftime('%I') | int }}"
      minute: "{{ now().minute | int }}"
    response_variable: "{{ response.emoji }}"  # Direct template string, NOT mapping
  - action: script.send_to_home_log
    data:
      message: "{{ result }} Log message"  # Use 'result' variable (default name)
```

**CRITICAL SYNTAX RULES:**
1. ✅ `response_variable:` (SINGULAR) - CORRECT
2. ❌ `response_variable:` (PLURAL) - WRONG (will cause script failure)
3. ✅ Direct template string: `response_variable: "{{ response.field }}"`
4. ❌ Mapping syntax: `response_variable: var: "{{ ... }}"` - WRONG

**Default variable name:**
- When using `response_variable:` the result is stored in a variable named based on context
- Check script documentation for exact variable name
- Often accessible directly in template: `"{{ response.field }}"`

**⚠️ WARNING:** Some documentation may incorrectly show `response_variable:` (plural). Always use `response_variable:` (singular) with template string.

### Returning Values from Scripts

Use `stop:` action with optional response variable:

```yaml
sequence:
  - variables:
      emoji: ":clock{{ hour }}{{ minute_suffix }}:"
  - stop:
      response_variable: clock_result
      value:
        emoji: "{{ emoji }}"
```

---

## Control Flow & Conditionals

### If/Then/Else

```yaml
sequence:
  - if:
      - condition: state
        entity_id: light.lamp
        state: "on"
    then:
      - action: light.turn_off
        target:
          entity_id: light.lamp
    else:
      - action: light.turn_on
        target:
          entity_id: light.lamp
```

### Choose (Multiple Branches)

Execute first matching branch (order matters!):

```yaml
sequence:
  - choose:
      # Branch 1: Check this first
      - conditions:
          - condition: state
            entity_id: input_select.home_mode
            state: "Holiday"
        sequence:
          - action: script.fake_presence

      # Branch 2: Check second
      - conditions:
          - condition: time
            after: "22:00:00"
        sequence:
          - action: script.nighttime_mode

      # Default: If no conditions match
      default:
        - action: script.normal_mode
```

**KEY PATTERN:** First matching condition wins - order branches by priority!

---

## Loops

### Repeat Count

```yaml
sequence:
  - repeat:
      count: 5
      sequence:
        - action: script.send_notification
          data:
            message: "Iteration {{ repeat.index }} of {{ repeat.count }}"
```

**Loop variables:**
- `repeat.index` - Current iteration (1-based)
- `repeat.first` - True if first iteration
- `repeat.last` - True if last iteration

### For Each Loop

```yaml
sequence:
  - repeat:
      for_each:
        - light.lamp_1
        - light.lamp_2
        - light.lamp_3
      sequence:
        - action: light.turn_on
          target:
            entity_id: "{{ repeat.item }}"
```

**Loop variables:**
- `repeat.item` - Current list item
- `repeat.index` - Current position (1-based)
- `repeat.first` - True if first item
- `repeat.last` - True if last item

### While Loop

```yaml
sequence:
  - variables:
      attempts: 0
  - repeat:
      while:
        - condition: template
          value_template: "{{ attempts < 3 }}"
      sequence:
        - variables:
            attempts: "{{ attempts + 1 }}"
        - action: script.try_connection
          continue_on_error: true
```

### Until Loop

```yaml
sequence:
  - repeat:
      until:
        - condition: state
          entity_id: switch.device
          state: "on"
      sequence:
        - action: switch.turn_on
          target:
            entity_id: switch.device
        - delay:
            seconds: 2
```

---

## Waiting & Delays

### Delay Syntax

```yaml
# Simple format
- delay: 00:00:30  # 30 seconds
- delay: 00:05:00  # 5 minutes
- delay: 01:00:00  # 1 hour

# Object format
- delay:
    hours: 1
    minutes: 30
    seconds: 15
    milliseconds: 500
```

### Wait for Template

Continue when template evaluates true:

```yaml
sequence:
  - wait_template: "{{ states('light.lamp') == 'on' }}"
    timeout: 00:05:00
    continue_on_timeout: false
  # After timeout, wait.completed contains True/False
```

### Wait for Trigger

Continue when trigger fires:

```yaml
sequence:
  - wait_for_trigger:
      - trigger: state
        entity_id: binary_sensor.motion
        to: "on"
    timeout: 00:10:00
  # After wait: access wait.trigger, wait.completed, wait.remaining
```

**Wait variable contents:**
- `wait.completed` - Boolean: timeout reached?
- `wait.remaining` - Duration remaining
- `wait.trigger` - The trigger data that fired (in wait_for_trigger)

---

## Parallel Execution

Run multiple actions simultaneously:

```yaml
sequence:
  - parallel:
      - action: light.turn_on
        target:
          entity_id: light.lamp
      - action: script.send_to_home_log
        data:
          message: "Lights turned on"
      - action: scene.turn_on
        target:
          entity_id: scene.ambient
```

**Use parallel for:**
- Independent actions (light + logging)
- Non-blocking operations
- Multiple device commands

**Don't use parallel for:**
- Sequential dependencies (e.g., turn on → wait → adjust brightness)
- Conditional logic (use if/then, not parallel + choose)

---

## Events & Custom Responses

### Fire Events

```yaml
sequence:
  - action: events.fire
    event_type: my_custom_event
    event_data:
      device: "kitchen"
      status: "motion_detected"
```

### Conversation Responses

Return text for voice assistant:

```yaml
sequence:
  - action: set_conversation_response
    data:
      response: "The temperature is {{ states('sensor.temperature') }} degrees"
```

---

## Error Handling

### Continue on Error

```yaml
sequence:
  - action: switch.turn_on
    target:
      entity_id: switch.unreliable_device
    continue_on_error: true
  # Script continues even if device fails
  - action: script.send_notification
    data:
      message: "Attempted to turn on device"
```

### Stop Execution

```yaml
sequence:
  - if:
      - condition: state
        entity_id: input_boolean.maintenance_mode
        state: "on"
    then:
      - stop:
          response_variable: result
          value:
            status: "Script skipped - maintenance mode active"
```

---

## Practical Patterns

### Pattern 1: Parameterized Logging

```yaml
script:
  log_with_clock:
    fields:
      title:
        description: Log title
        example: "🧑‍🍳 Kitchen"
      message:
        description: Log message
      log_level:
        description: Debug or Normal
        default: "Debug"
    sequence:
      - action: script.get_clock_emoji
        data:
          hour: "{{ now().strftime('%I') | int }}"
          minute: "{{ now().minute | int }}"
        response_variable:
          clock_result: "{{ response.emoji }}"
      - action: script.send_to_home_log
        data:
          message: "{{ clock_result }} {{ message }}"
          title: "{{ title }}"
          log_level: "{{ log_level }}"
```

### Pattern 2: Device Control with Verification

```yaml
script:
  turn_on_with_verify:
    fields:
      device_id:
        description: Entity to turn on
        example: "switch.device"
      max_attempts:
        description: Number of attempts
        default: 3
    sequence:
      - variables:
          attempts: 0
      - repeat:
          until:
            - condition: state
              entity_id: "{{ device_id }}"
              state: "on"
          sequence:
            - variables:
                attempts: "{{ attempts + 1 }}"
            - if:
                - condition: template
                  value_template: "{{ attempts > max_attempts }}"
              then:
                - action: script.send_direct_notification
                  data:
                    message: "Failed to turn on {{ device_id }} after {{ max_attempts }} attempts"
                - stop:
                    response_variable: result
                    value:
                      success: false
            - action: switch.turn_on
              target:
                entity_id: "{{ device_id }}"
            - delay:
                seconds: 2
      - stop:
          response_variable: result
          value:
            success: true
            attempts: "{{ attempts }}"
```

### Pattern 3: Conditional Multi-Action

```yaml
script:
  handle_motion:
    fields:
      room:
        description: Room name
      brightness:
        description: Light brightness
        default: 100
    sequence:
      - choose:
          # Check 1: Already bright
          - conditions:
              - condition: numeric_state
                entity_id: "light.{{ room }}"
                attribute: brightness
                above: 200
            sequence:
              - action: script.send_to_home_log
                data:
                  message: "Already bright, no action needed"

          # Check 2: Dark - turn on
          - conditions:
              - condition: numeric_state
                entity_id: "light.{{ room }}"
                attribute: brightness
                below: 100
            sequence:
              - parallel:
                  - action: light.turn_on
                    target:
                      entity_id: "light.{{ room }}"
                    data:
                      brightness_pct: "{{ brightness }}"
                  - action: script.send_to_home_log
                    data:
                      message: "🐾 Motion detected - turning on light"

          # Default
          default:
            - action: light.turn_on
              target:
                entity_id: "light.{{ room }}"
              data:
                brightness_pct: 75
```

---

## Common Mistakes to Avoid

| Mistake | Problem | Solution |
|---------|---------|----------|
| `response_variables:` (plural) | Wrong syntax, script fails | Use `response_variable:` (singular) |
| Using mapping syntax | Wrong format | Use `response_variable: "{{ response.field }}"` (direct template) |
| Nested choose in parallel | Invalid structure | Move choose to sequential level |
| Variable scope confusion | Variables inaccessible | Define at appropriate nesting level |
| Accessing undefined entity in template | Runtime error | Use `\| default()` filter for safety |
| Mixing string/object access | Template errors | Understand if value is string or object |
| Too many parallel actions | Performance issues | Keep parallel actions lightweight |
| No timeout on wait_template | Infinite hang | Always set `timeout:` |

---

## Script Integration Examples

### Called from Automation

```yaml
automation:
  - alias: "Motion Detected"
    triggers:
      - trigger: state
        entity_id: binary_sensor.motion
        to: "on"
    actions:
      - action: script.handle_motion
        data:
          room: "kitchen"
          brightness: 100
```

### With Response Variables

```yaml
automation:
  - alias: "Check Temperature"
    triggers:
      - trigger: time_pattern
        minutes: 0
    actions:
      - action: script.check_temperature
        response_variable:
          temp_result: "{{ response.is_high }}"
      - if:
          - condition: template
            value_template: "{{ temp_result }}"
        then:
          - action: script.send_notification
            data:
              message: "Temperature is high!"
```

---

## Best Practices Summary

1. **Use `queued` mode** for scripts called frequently (motion detection, timers)
2. **Use `response_variable:` (SINGULAR)** with template string to return data from scripts
3. **Order choose branches by priority** - first match wins
4. **Test templates before using** - use Developer Tools
5. **Use parallel for independent tasks** - logging + light on together
6. **Always set timeouts on wait actions** - prevent infinite hangs
7. **Use descriptive aliases** - helps with automation traces
8. **Validate entity IDs** - use `| default()` for safety
9. **Keep scripts focused** - single responsibility principle
10. **Document parameters** - include examples and descriptions

---

## Key Differences from Automations

| Feature | Script | Automation |
|---------|--------|-----------|
| Trigger | Called explicitly | Responds to triggers |
| Parameters | Yes, with `fields:` | No, uses state/time |
| Response Variables | Yes, `stop:` action | No direct return |
| Reusability | High - called from many places | Single-use typically |
| Mode | single/restart/queued/parallel | Not applicable |
| Scope | Within script context | System-wide |
