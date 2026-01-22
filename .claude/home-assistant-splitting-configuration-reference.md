# Home Assistant Configuration Splitting Reference

**Source:** https://www.home-assistant.io/docs/configuration/splitting_configuration/
**Date:** 2026-01-22
**Purpose:** Comprehensive guide to organizing and splitting Home Assistant configuration files

---

## Core Principles

Home Assistant supports splitting configuration into multiple files and directories. This enables:
- **Maintainability** - Easier to find and modify specific configurations
- **Scalability** - Large systems become manageable
- **Organization** - Logical grouping of related automations/entities
- **Version Control** - Cleaner git history and less merge conflicts
- **Reusability** - Packages can be shared or duplicated

**CRITICAL:** The main `configuration.yaml` file always remains and acts as the entry point.

---

## Include Methods

### 1. Simple File Include: `!include`

Include a single file's contents at that location:

```yaml
# configuration.yaml
automation: !include automation.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
input_boolean: !include input_boolean.yaml
sensor: !include sensor.yaml
```

**Files referenced:**
- `automation.yaml` - Contains list of automations
- `scripts.yaml` - Contains script definitions
- `sensor.yaml` - Contains sensor configurations

**Rules:**
- File must have `.yaml` extension (`.yml` NOT supported for directory includes)
- File is parsed and inserted at that location
- Indentation matters (typically 2 spaces per level)
- File must contain valid YAML structure

**Example file structure:**

```yaml
# automation.yaml
- id: "1583956425622"
  alias: "Living Room: Motion Detected"
  triggers: [...]

- id: "1583956426000"
  alias: "Kitchen: Turn On Lights"
  triggers: [...]
```

### 2. Directory List Include: `!include_dir_list`

Include all files in a directory as a **list**, ordered alphanumerically:

```yaml
# configuration.yaml
automation: !include_dir_list automations/
```

**Result:** Files are parsed and returned as list items in alphabetical order

**Files in `automations/` directory:**
- `01-morning-routine.yaml` (loaded first)
- `02-evening-routine.yaml` (loaded second)
- `03-night-mode.yaml` (loaded third)

**Each file must contain a single list item:**

```yaml
# automations/01-morning-routine.yaml
- id: "1234567890001"
  alias: "Morning: Wake Up"
  triggers: [...]
```

### 3. Directory Named Include: `!include_dir_named`

Include all files in a directory as a **dictionary**, mapping filenames to content:

```yaml
# configuration.yaml
script: !include_dir_named scripts/
```

**Result:** Returns dictionary where keys are filenames (without .yaml), values are file contents

**Files in `scripts/` directory:**
- `turn_on_lights.yaml`
- `send_notification.yaml`
- `lock_doors.yaml`

**Each file contains a script definition:**

```yaml
# scripts/turn_on_lights.yaml
alias: Turn On Lights
sequence:
  - action: light.turn_on
    target:
      entity_id: light.living_room
```

**Generated structure:**
```yaml
script:
  turn_on_lights:  # Filename becomes key
    alias: Turn On Lights
    sequence: [...]
  send_notification:
    alias: Send Notification
    sequence: [...]
```

### 4. Directory List Merge: `!include_dir_merge_list`

Merge all files in a directory into a **single list**:

```yaml
# configuration.yaml
automation manual: !include_dir_merge_list automations/
```

**Requirements:** Each file must contain a valid list

**Files merged into one list:**

```yaml
# automations/room/bedroom.yaml
- id: "1234567890001"
  alias: "Bedroom: Motion Detected"
  triggers: [...]

- id: "1234567890002"
  alias: "Bedroom: Lights Off"
  triggers: [...]

# automations/room/kitchen.yaml
- id: "1234567890003"
  alias: "Kitchen: Motion Detected"
  triggers: [...]
```

**Result:** Single list with all items combined
```yaml
automation manual:
  - id: "1234567890001"
    alias: "Bedroom: Motion Detected"
  - id: "1234567890002"
    alias: "Bedroom: Lights Off"
  - id: "1234567890003"
    alias: "Kitchen: Motion Detected"
```

### 5. Directory Dict Merge: `!include_dir_merge_named`

Merge all files in a directory into a **single dictionary**:

```yaml
# configuration.yaml
template: !include_dir_merge_named templates/
```

**Requirements:** Each file must contain valid key-value pairs

**Files merged into one dictionary:**

```yaml
# templates/sensors.yaml
- binary_sensor:
    - name: Living Room Motion
      unique_id: living_room_motion_dark
      state: "{{ ... }}"

# templates/calculations.yaml
- binary_sensor:
    - name: Kitchen Motion
      unique_id: kitchen_motion_dark
      state: "{{ ... }}"
```

**Result:** Single merged template structure

---

## Recursion Behavior

Directory includes operate **recursively** across subdirectories:

```
automations/
├── room/
│   ├── bedroom.yaml
│   ├── kitchen.yaml
│   └── living_room.yaml
├── energy/
│   ├── battery.yaml
│   └── solar.yaml
└── time/
    └── daily.yaml
```

With `automation: !include_dir_merge_list automations/`, ALL files are included regardless of nesting depth.

---

## Packages: The Advanced Pattern

**Packages** are the most powerful organizational method. Each package is a self-contained `.yaml` file that can include:
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
- Any other Home Assistant component

### Enable Packages

```yaml
# configuration.yaml
homeassistant:
  packages: !include_dir_named packages/
```

### Package Structure

```
packages/
├── home.yaml                    # Home mode automations
├── time.yaml                    # Time-based automations
├── smoke_alarms.yaml            # Smoke alarm logic
├── tracker.yaml                 # Presence tracking
├── rooms/                       # Room-based packages
│   ├── living_room.yaml
│   ├── bedroom/
│   │   ├── bedroom.yaml
│   │   ├── sleep_as_android.yaml
│   │   └── awtrix_light.yaml
│   ├── kitchen/
│   │   ├── kitchen.yaml
│   │   └── meater.yaml
│   └── conservatory/
│       ├── conservatory.yaml
│       ├── octoprint.yaml
│       └── airer.yaml
└── integrations/                # Integration-based packages
    ├── energy/
    │   ├── energy.yaml
    │   ├── battery.yaml
    │   └── solar.yaml
    ├── hvac/
    │   ├── hvac.yaml
    │   ├── heating.yaml
    │   └── eddi.yaml
    ├── messaging/
    │   ├── notifications.yaml
    │   └── message_callback.yaml
    └── security/
        ├── alarm.yaml
        └── cameras.yaml
```

### Package File Example

```yaml
# packages/rooms/kitchen/kitchen.yaml
# Created by Danny Tsang <danny@tsang.uk>

automation:
  - id: "1583797341647"
    alias: "Kitchen: Turn Off Lights At Night"
    description: "Turn off kitchen lights at 23:30"
    triggers: [...]
    actions: [...]

  - id: "1606158191303"
    alias: "Kitchen: Motion Detected"
    triggers: [...]
    actions: [...]

script:
  kitchen_cancel_all_light_timers:
    alias: "Kitchen: Cancel All Light Timers"
    description: "Stops all kitchen light timers"
    sequence: [...]

sensor:
  - platform: template
    sensors:
      kitchen_motion_illuminance:
        friendly_name: "Kitchen Motion Illuminance"
        unit_of_measurement: lux
        value_template: "{{ state_attr('sensor.apollo_r_pro_1_w_ef755c_ltr390_light', 'illuminance') }}"

input_boolean:
  enable_kitchen_motion_triggers:
    name: Enable Kitchen Motion Triggers
    icon: mdi:motion-sensor
    initial: true

input_number:
  kitchen_light_level_threshold:
    name: Kitchen Light Level Threshold
    min: 0
    max: 200
    step: 1
    unit_of_measurement: lux
    icon: mdi:brightness-6

timer:
  kitchen_cooker_light_dim:
    name: Kitchen Cooker Light Dim
    duration: "00:05:00"
    icon: mdi:timer
```

### Advantages of Packages

1. **Self-contained** - Related automations, scripts, sensors grouped together
2. **Maintainable** - Everything for a room/domain in one file
3. **Reusable** - Can copy entire package to new instance
4. **Namespace** - No conflicts with other packages
5. **Version control** - Easier git management

---

## Multiple Includes for Same Domain

Some integrations allow multiple top-level keys:

```yaml
# configuration.yaml
automation manual: !include_dir_merge_list automations/
automation ui: !include automations.yaml
```

This enables:
- **Manual automations** from `automations/` directory
- **UI automations** from `automations.yaml` (created via UI)

Both are loaded and work together.

**Other domains supporting this:**
- `automation` (manual + ui)
- `script` (manual + ui in newer versions)

---

## Nesting Includes

An included file can itself contain includes:

```yaml
# packages/integrations/energy/energy.yaml
automation: !include_dir_merge_list energy/automations/
script: !include_dir_named energy/scripts/
sensor: !include_dir_merge_list energy/sensors/
input_boolean: !include_dir_named energy/helpers/booleans/
input_number: !include_dir_named energy/helpers/numbers/
```

This creates deep hierarchies while keeping structure logical.

---

## Organization Patterns

### Pattern 1: Room-Based Organization

Organize primarily by room:

```
packages/
├── rooms/
│   ├── living_room.yaml
│   ├── bedroom.yaml
│   ├── kitchen/
│   │   ├── kitchen.yaml
│   │   └── kitchen_meater.yaml
│   └── conservatory/
│       ├── conservatory.yaml
│       ├── octoprint.yaml
│       └── airer.yaml
└── shared/
    ├── helpers.yaml
    └── templates.yaml
```

**Pros:**
- Intuitive - Find room, find all automations
- Natural grouping - Related entities together
- Minimal cross-references

**Cons:**
- Duplicated helper logic across rooms
- Harder to manage system-wide patterns

### Pattern 2: Integration-Based Organization

Organize primarily by integration/function:

```
packages/
├── integrations/
│   ├── lighting/
│   │   ├── motion.yaml
│   │   └── circadian.yaml
│   ├── climate/
│   │   ├── heating.yaml
│   │   └── cooling.yaml
│   ├── security/
│   │   ├── alarm.yaml
│   │   └── cameras.yaml
│   └── energy/
│       ├── battery.yaml
│       └── solar.yaml
└── system/
    ├── home_modes.yaml
    └── presence.yaml
```

**Pros:**
- Clear separation of concerns
- Easy to find logic for specific function
- Shared helper patterns

**Cons:**
- Harder to see all room-specific logic
- More cross-file references

### Pattern 3: Hybrid Organization (Recommended)

Combine room-based + integration-based:

```
packages/
├── rooms/                       # Room-specific automations
│   ├── living_room.yaml
│   ├── bedroom/
│   │   ├── bedroom.yaml
│   │   └── sleep_as_android.yaml
│   └── kitchen/
│       ├── kitchen.yaml
│       └── meater.yaml
├── integrations/               # System-wide integrations
│   ├── energy/
│   ├── messaging/
│   ├── security/
│   └── hvac/
├── shared_helpers.yaml         # Shared scripts & templates
├── home.yaml                   # Home modes & presence
└── time.yaml                   # Time-based automations
```

**Pros:**
- Best of both worlds
- Room logic easy to find
- System logic organized
- Shared helpers centralized

**Cons:**
- Requires discipline in organization

---

## File Naming Conventions

### Room Packages

```
packages/rooms/
├── living_room.yaml            # Simple room
├── bedroom/                     # Complex room with sub-packages
│   ├── bedroom.yaml            # Main room automations
│   ├── sleep_as_android.yaml   # Specific integration
│   └── awtrix_light.yaml       # Device-specific config
├── kitchen/
│   ├── kitchen.yaml
│   └── meater.yaml
└── conservatory/
    ├── conservatory.yaml
    ├── octoprint.yaml
    └── airer.yaml
```

### Integration Packages

```
packages/integrations/
├── energy/
│   ├── energy.yaml             # Main energy config
│   ├── battery.yaml            # Battery-specific
│   └── solar.yaml              # Solar-specific
├── hvac/
│   ├── hvac.yaml
│   ├── heating.yaml
│   └── eddi.yaml
├── messaging/
│   ├── notifications.yaml
│   └── message_callback.yaml
└── security/
    ├── alarm.yaml
    └── cameras.yaml
```

### Naming Rules

1. **Lowercase** - `kitchen.yaml` not `Kitchen.yaml`
2. **Hyphens for multi-word** - `sleep_as_android.yaml` not `sleepAsAndroid.yaml`
3. **Descriptive** - `meater.yaml` describes purpose
4. **Ordered with numbers if sequential** - `01-morning.yaml`, `02-evening.yaml`

---

## YAML Structure Guidelines

### File Indentation

```yaml
# CORRECT - 2 spaces per level
automation:
  - id: "1234567890001"
    alias: "Test Automation"
    triggers:
      - trigger: state
        entity_id: binary_sensor.motion
        to: "on"
    actions:
      - action: light.turn_on

# WRONG - Inconsistent indentation (will fail)
automation:
 - id: "1234567890001"          # 1 space (incorrect)
  alias: "Test Automation"       # 2 spaces
   triggers:                     # 3 spaces
```

### List vs Dictionary Format

```yaml
# LIST FORMAT (for automation, script, etc.)
automation:
  - id: "1234567890001"
    alias: "First Automation"
  - id: "1234567890002"
    alias: "Second Automation"

# DICTIONARY FORMAT (for input_boolean, input_number, etc.)
input_boolean:
  enable_motion_triggers:
    name: Enable Motion Triggers
  night_mode:
    name: Night Mode

# PROPER NESTING
sensor:
  - platform: template
    sensors:
      living_room_temp:
        friendly_name: "Living Room Temperature"
        value_template: "{{ states('sensor.temperature') }}"
```

### Comments and Documentation

```yaml
# packages/rooms/kitchen/kitchen.yaml
# Created by Danny Tsang <danny@tsang.uk>
# Kitchen automation package - handles motion detection and lighting
#
# Automations:
# - Kitchen: Turn Off Lights At Night (23:30)
# - Kitchen: Motion Detected (multi-zone lights)
# - Kitchen: No Motion (timer-based turn off)
#
# Helpers:
# - input_boolean.enable_kitchen_motion_triggers
# - input_number.kitchen_light_level_threshold
# - timer.kitchen_cooker_light_dim

automation:
  # region Motion Detection
  - id: "1606158191303"
    alias: "Kitchen: Motion Detected Table Lights Off"
    # ... automation definition ...
  # endregion

  # region Timer-Based Actions
  - id: "1606652871369"
    alias: "Kitchen: No Motion Short Time"
    # ... automation definition ...
  # endregion
```

---

## Configuration Validation

### Pre-Deployment Checks

```bash
# Check YAML syntax
# Use Home Assistant's built-in validator:
# Settings → System → Restart → Check Configuration
```

### Common YAML Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "mapping values are not allowed here" | Indentation issue | Check spaces (use 2-space indent) |
| "expected <block end>" | Unmatched list/dict | Verify all colons and dashes aligned |
| "line X: expected a key, but got '?'" | Invalid YAML syntax | Check for special characters, quotes |
| "while scanning a flow mapping" | Unclosed bracket | Verify `{}` or `[]` are matched |
| "expected ':':" | Missing colon after key | Add `:` after all key names |

---

## Performance Considerations

### Include Method Overhead

| Method | Performance | Use Case |
|--------|-------------|----------|
| `!include` | Fastest | Single file includes |
| `!include_dir_list` | Fast | Small number of files (<50) |
| `!include_dir_named` | Fast | Moderate files (50-200) |
| `!include_dir_merge_list` | Moderate | Large automation lists (200+) |
| `!include_dir_merge_named` | Moderate | Many named entities |
| `packages:` | Optimal | 10-100 packages (recommended) |

### Optimization Tips

1. **Don't over-split** - 5 files with 100 lines each is better than 50 files with 10 lines
2. **Group related items** - Keep motion detection together even across rooms
3. **Limit directory depth** - 3-4 levels maximum
4. **Use packages for logical grouping** - Not arbitrary split
5. **Avoid circular includes** - Package A shouldn't include Package B which includes A

---

## Common Patterns

### Pattern 1: Shared Helpers Package

```yaml
# packages/shared_helpers.yaml
script:
  send_to_home_log:
    alias: "Send to Home Log"
    fields:
      message:
        description: "Log message"
      title:
        description: "Log title"
    sequence: [...]

  get_clock_emoji:
    alias: "Get Clock Emoji"
    fields:
      hour:
        description: "Hour (1-12)"
    sequence: [...]

template:
  - binary_sensor:
      - name: "Kitchen Motion Dark"
        unique_id: kitchen_motion_dark
        state: "{{ ... }}"

input_boolean:
  debug_mode:
    name: "Debug Mode"
    initial: false
```

**Usage:** Referenced by all other packages

### Pattern 2: Room Package with Sub-Packages

```yaml
# packages/rooms/kitchen/kitchen.yaml
automation:
  - id: "1583797341647"
    alias: "Kitchen: Turn Off Lights At Night"
    triggers: [...]

script:
  kitchen_cancel_all_light_timers:
    alias: "Cancel Kitchen Timers"
    sequence: [...]

input_boolean:
  enable_kitchen_motion_triggers:
    name: Enable Kitchen Motion Triggers

timer:
  kitchen_cooker_light_dim:
    name: Kitchen Cooker Light Dim
```

```yaml
# packages/rooms/kitchen/meater.yaml
automation:
  - id: "1234567890001"
    alias: "Meat Thermometer: Temperature Alert"
    triggers: [...]

input_number:
  meater_target_temperature:
    name: Meater Target Temperature
    min: 0
    max: 100
```

### Pattern 3: Integration Package

```yaml
# packages/integrations/energy/energy.yaml
automation: !include_dir_merge_list energy/automations/
script: !include_dir_named energy/scripts/
sensor: !include_dir_merge_list energy/sensors/
input_boolean: !include_dir_named energy/helpers/booleans/

# packages/integrations/energy/automations/battery.yaml
- id: "1234567890001"
  alias: "Energy: Battery Mode Validation"
  triggers: [...]

- id: "1234567890002"
  alias: "Energy: Low Battery Alert"
  triggers: [...]
```

---

## Best Practices

### DO:
✅ **Use packages** for logical grouping of related automations/scripts
✅ **Name files descriptively** - Easy to understand purpose
✅ **Keep related logic together** - Motion detection in same file
✅ **Use comments** - Document complex automations
✅ **Validate before deploying** - Use HA's config checker
✅ **Keep directory structure logical** - 3-4 levels max
✅ **Use consistent naming** - Lowercase with hyphens
✅ **Document package purpose** - Top-level comment with overview

### DON'T:
❌ **Over-split files** - 10 files with 50 lines each instead of 1 file with 500 lines
❌ **Create circular includes** - Package A including B which includes A
❌ **Mix organizational schemes** - Sometimes by room, sometimes by function
❌ **Nest too deeply** - More than 4 levels of directories
❌ **Use inconsistent indentation** - Always 2 spaces
❌ **Leave files without comments** - Future you won't remember why
❌ **Include unrelated items** - Keep motion detection separate from timers (unless related)
❌ **Ignore YAML syntax** - Test in Developer Tools first

---

## Real-World Example: Your Configuration

```
packages/
├── shared_helpers.yaml                    # Global scripts & templates
├── home.yaml                              # Home modes & presence
├── time.yaml                              # Time-based automations
├── smoke_alarms.yaml                      # Smoke detector logic
├── tracker.yaml                           # Device tracking
├── rooms/
│   ├── living_room.yaml
│   ├── bedroom/
│   │   ├── bedroom.yaml
│   │   ├── sleep_as_android.yaml
│   │   └── awtrix_light.yaml
│   ├── kitchen/
│   │   ├── kitchen.yaml                   # Main kitchen logic
│   │   └── meater.yaml                    # Meat thermometer
│   ├── conservatory/
│   │   ├── conservatory.yaml
│   │   ├── octoprint.yaml
│   │   └── airer.yaml
│   ├── office/
│   │   ├── office.yaml
│   │   └── steam.yaml
│   ├── stairs.yaml
│   ├── porch.yaml
│   ├── back_garden.yaml
│   └── front_garden.yaml
└── integrations/
    ├── alarm.yaml
    ├── energy/
    │   ├── energy.yaml
    │   ├── battery.yaml
    │   └── solar.yaml
    ├── hvac/
    │   ├── hvac.yaml
    │   ├── heating.yaml
    │   └── eddi.yaml
    ├── messaging/
    │   ├── notifications.yaml
    │   └── message_callback.yaml
    ├── weather/
    │   └── weather.yaml
    └── transport/
        └── transport.yaml
```

**Why this structure works:**
1. **Room packages** - Find all kitchen logic in one place
2. **Integration packages** - Find all energy logic together
3. **Shared helpers** - Reusable across entire system
4. **System automations** - Home modes and presence separate
5. **3-level max depth** - Easy to navigate

---

## Migration Strategy

### From Monolithic to Split Configuration

**Before:**
```yaml
# configuration.yaml - 2000+ lines
automation: [...]   # 500 lines
script: [...]       # 300 lines
sensor: [...]       # 800 lines
```

**After:**
```yaml
# configuration.yaml - 50 lines
homeassistant:
  packages: !include_dir_named packages/

automation ui: !include automations.yaml
script ui: !include scripts.yaml
```

**Migration steps:**
1. Create `packages/` directory
2. Create sub-packages for each room/integration
3. Move automation blocks to room packages
4. Move scripts to shared or room packages
5. Move sensors to appropriate packages
6. Test configuration incrementally
7. Restart Home Assistant
8. Verify all automations load

---

## Troubleshooting

### Configuration Won't Load

1. **Check logs** - Home Assistant logs will show which file has error
2. **Validate YAML** - Use online YAML validator or `yamllint` tool
3. **Check indentation** - Verify 2-space indent consistency
4. **Verify file exists** - Confirm path and filename correct
5. **Test syntax** - Load file in text editor with YAML highlight

### Automations Not Triggering

1. **Verify package loaded** - Check Home Assistant startup log
2. **Check automation ID** - Ensure unique IDs across all files
3. **Test in UI** - Manual run automation through UI
4. **Check conditions** - Verify conditions actually met
5. **Review traces** - Use automation traces to debug

### Performance Issues

1. **Check file count** - Too many tiny files vs few large files
2. **Verify include type** - Using most efficient method?
3. **Monitor logs** - Look for repeated parse errors
4. **Profile reload time** - Time to reload automations
5. **Consider caching** - For frequently accessed packages

---

## Key Takeaways

1. **Packages are the primary organization method** - Not individual includes
2. **Logical grouping beats arbitrary splitting** - Room or integration basis
3. **Consistency matters** - Naming, indentation, structure
4. **Documentation helps** - Comments explain why, not what
5. **Validate before deploying** - YAML errors will crash config reload
6. **Nest carefully** - 3-4 levels max
7. **Keep related items together** - Same file for related automations
8. **Test incrementally** - Don't split everything at once
9. **Use version control** - Makes splitting easier with git
10. **Reference community examples** - Learn from other configs
