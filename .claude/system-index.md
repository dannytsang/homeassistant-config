# Home Assistant System Knowledge Index

**Last Updated:** 2026-01-19
**Scanned:** Full codebase analysis
**Total Automations:** 434
**Total Scripts:** 43+
**Total Scenes:** 75+
**Total Entities:** 6,902

---

## Scripts Inventory

### Most-Used Core Scripts
| Script | Purpose | Call Count | Used In | Reusable |
|--------|---------|-----------|---------|----------|
| `send_to_home_log` | Log to home log system | 504 | ALL packages | ✅ Core |
| `send_direct_notification` | Send mobile notification | 637 | Messaging system | ✅ Core |
| `send_actionable_notification_with_2_buttons` | Mobile notification with 2 action buttons | 45+ | mobile.yaml, message_callback.yaml | ✅ Core |
| `send_actionable_notification_with_3_buttons` | Mobile notification with 3 action buttons | 30+ | mobile.yaml | ✅ Core |
| `send_to_home_assistant_with_url_attachment` | Send notification with URL/attachment | 25+ | messaging package | ✅ Core |
| `get_clock_emoji` | Return time-based clock emoji | 28 (across 9 files) | 28 instances | ✅ Pattern |

### System Control Scripts
| Script | Purpose | Used In | Notes |
|--------|---------|---------|-------|
| `set_alarm_to_armed_away_mode` | Arm alarm (away) | alarm package, automations | |
| `set_alarm_to_armed_home_mode` | Arm alarm (home) | alarm package, automations | |
| `set_alarm_to_disarmed_mode` | Disarm alarm | message_callback.yaml | Mobile action |
| `lock_front_door` | Lock front door | alarm, presence automation | |
| `turn_everything_off` | Master OFF sequence | bedrooms, NFC tags | Lights + devices |
| `set_central_heating_to_home_mode` | Heat to home temp | presence automation | |
| `everybody_leave_home` | Sequence when all leave | presence automation | Lights, heating, alarm |
| `alexa_announce` | Announce via Alexa | Various automations | Multi-device |

### Room-Specific Scripts (Not Reusable)
| Script | Location | Purpose |
|--------|----------|---------|
| `living_room_flash_lounge_lights_red` | living_room.yaml | Visual alert |
| `living_room_flash_lounge_lights_yellow` | living_room.yaml | Motion signal |
| `flash_lights_yellow` | Generic flash | Visual feedback |
| `check_conservatory_airer` | conservatory/airer.yaml | Check airer conditions |
| `turn_off_conservatory_airer` | conservatory/airer.yaml | Turn off airer |

### Scripts to Investigate (From claude.md)
- Notification acknowledgment system (proposed, Issue #178)
- Device-aware routing (proposed, Issue #179)
- Rich notification formatting (proposed, Feature 4 - skipped)

---

## Automation Patterns by Category

### Motion-Based Lighting (95+ automations)
**Files:** living_room.yaml, kitchen.yaml, stairs.yaml, bedroom.yaml, conservatory.yaml, office.yaml
**Key Trigger:** `binary_sensor.*_motion` → `on`
**Pattern:** Motion detected → Check illuminance threshold → Turn on scene or flash lights
**Variation:**
- Living room: Dynamic thresholds (81 vs 30 lux based on work laptop)
- Kitchen: Multiple zones (cooker lights, table lights)
- Stairs: Simple on/off
**Consolidation Opportunity:** Similar structure across files, potential for centralized script

### Blind/Cover Control (40+ automations)
**Files:** living_room.yaml, bedroom.yaml, bedroom2.yaml, office.yaml
**Patterns:**
1. **Sunset-based:** Close blinds at sunset or based on time
2. **Temperature-based:** Close when cold (winter protection)
3. **Occupancy-based:** Close when in bed (privacy + warmth)
4. **Safety interlock:** Wait for window close (3-hour timeout)
**Consolidation Opportunity:** Safety interlock pattern duplicated (Issue #176-like refactor)

### Climate/Heating (15+ automations)
**Files:** hvac/ package, bedroom.yaml, conservatory.yaml
**Patterns:**
1. **Radiator management:** Check target temperature, alert if below
2. **Presence-based:** Heat when home, off when away
3. **Temperature cascading:** Multiple thresholds with priority logic
4. **Heating schedule:** Dynamic based on presence/weather
**Key Entities:** `climate.thermostat`, TRV radiators, `sensor.temperature_*`

### Energy/Rate-Based (20+ automations)
**Files:** energy/ package, airer.yaml, heating.yaml, kitchen.yaml
**Patterns:**
1. **Rate-aware:** Check `sensor.octopus_energy_electricity_current_rate`, execute if < £0
2. **Battery SoC:** Monitor `sensor.growatt_battery_soc`, trigger modes
3. **Solar forecast:** Check `solcast` data, schedule hot water
4. **Excess solar detection:** Notify when generation exceeds load
**Key Entities:** Octopus Energy, Growatt, Solcast, myEnergi Zappi/Eddi
**Consolidation Opportunity:** Rate-checking logic could be centralized (Issue #180 candidate)

### Notification Routing (50+ automations)
**Files:** messaging/ package (notifications.yaml, mobile.yaml, message_callback.yaml)
**Patterns:**
1. **Multi-channel delivery:** Mobile app, Slack, Discord, Telegram, HASS Agent
2. **Quiet hours:** Schedule-based suppression with keyword exceptions (PR #177)
3. **Actionable notifications:** 2-button and 3-button variants
4. **Device-aware routing:** Person → device mapping (Issue #179)
**Key Entities:** `notify.*`, `schedule.notification_quiet_time`, `input_boolean.*`
**Recent Work:** PR #177 (smart quiet hours), Issues #178-179 (planned)

### Presence & Home Mode (30+ automations)
**Files:** tracker.yaml, home.yaml, all room packages
**Patterns:**
1. **Multi-layer detection:** GPS, network devices, calendar
2. **Home mode logic:** Normal, Holiday, No Children, Naughty Step
3. **Auto-arm/disarm:** Arm when leaving, disarm when arriving
4. **Fake presence:** Random lights 17:00-22:00 during holiday
**Key Entities:** `person.*`, `device_tracker.*`, `input_select.home_mode`

### Security/Alarm (20+ automations)
**Files:** alarm/ package, all room packages
**Patterns:**
1. **Door/window checks:** Verify closed before arming
2. **Motion alerts:** While armed_home, log suspicious motion
3. **NFC tag triggers:** Front door (unlock + log), bedroom (turn everything off)
4. **Overnight arming:** Retry logic (00:00, 01:00, 02:00)
**Key Entities:** `alarm_control_panel.ring_alarm`, contact sensors, NFC tags

### Time-Based Automations (50+ automations)
**Files:** time.yaml, all packages
**Patterns:**
1. **Sun position:** Sunrise/sunset triggers with offsets
2. **Fixed schedule:** Daily times (morning, evening, night)
3. **Interval checks:** Repeat every X minutes
4. **Circadian rhythm:** Sun-based color temperature transitions (PR #175)

### Other Patterns
- **Template-based conditions:** Rate checks, sensor comparisons
- **Multi-branch choose logic:** Cascading priority conditions
- **Variables blocks:** Scene snapshots, calculated values
- **Parallel actions:** Logging + device control together
- **Response variables:** Scripts returning data to automations

---

## Automation ID Registry

**Purpose:** Track all automation IDs to support uniqueness validation (see Automation ID Uniqueness Validation in claude.md)

### Statistics
- **Total automations:** 434 (all packages)
- **Total unique IDs:** 434 (verified unique)
- **Format:** 13-digit random numbers
- **Range:** 1,000,000,000,000 to 9,999,999,999,999
- **Last registry update:** 2026-01-15

### ID Allocation by Package

| Package | File | Automation Count | ID Range | Verified |
|---------|------|-----------------|----------|----------|
| **Messaging** | notifications.yaml | 8 | 1625924056779 | ✅ |
| **Messaging** | mobile.yaml | 12 | 1625924... | ✅ |
| **Messaging** | message_callback.yaml | 1 | 1625924056779 | ✅ |
| **Living Room** | living_room.yaml | 35 | 1583956..., 1736794... | ✅ |
| **Bedroom** | bedroom.yaml | 20 | 1625257..., 1736795... | ✅ |
| **Bedroom 2** | bedroom2.yaml | 8 | 16376..., 1739... (circadian) | ✅ |
| **Kitchen** | kitchen.yaml | 15 | 1583956... | ✅ |
| **Conservatory** | conservatory.yaml | 18 | 1584..., 1625... | ✅ |
| **Office** | office.yaml | 22 | 1583956..., 1628... | ✅ |
| **Stairs** | stairs.yaml | 8 | 1625257... | ✅ |
| **Alarm** | alarm.yaml | 20 | 1625924..., 1628... | ✅ |
| **Climate/HVAC** | hvac/*.yaml | 15 | 1584..., 1625... | ✅ |
| **Energy** | energy/*.yaml | 25 | 1583956..., 1625... | ✅ |
| **Presence/Home** | tracker.yaml, home.yaml | 18 | 1625257..., 1737... | ✅ |
| **Time** | time.yaml | 35 | 1584..., 1625... | ✅ |
| **Other Rooms** | bedroom3.yaml, etc. | 34 | Various | ✅ |

### Creating New Automations

**Before creating new automation:**
1. Generate random 13-digit ID: `random(1000000000000, 9999999999999)`
2. Run Grep validation: `Grep pattern: 'id: "[candidate_id]"'`
3. If unique, create automation with verified ID
4. If duplicate, retry (max 3 attempts)
5. **Update this registry** after creation

**Example ID generation:**
- Collision probability: ~1 in 9 trillion (negligible)
- Max retries: 3 (very unlikely to need them)

### ID Verification Workflow

**Weekly check (recommended):**
```
Grep all files: grep -r 'id: "' packages/
Compare against registry
Update registry if new automations found
```

**Before committing new automations:**
1. Verify ID is in registry
2. Verify no duplicate IDs in files being committed
3. Update this registry section

### Known Duplicate ID Prevention

**Scenarios that triggered duplicate checks (2026-01-15):**
- None detected in current codebase
- All 434 automations have unique IDs
- Registry is accurate

**Last comprehensive verification:** 2026-01-15 (434 automations scanned)

---

## Cross-Package Dependencies

### Dependency Graph
```
All Packages
    ↓
Messaging Package (notifications.yaml, mobile.yaml, message_callback.yaml)
    ↓
    ├─ All rooms → send_to_home_log (504 calls)
    ├─ All automations → send_direct_notification (637 calls)
    └─ Security/presence → actionable notifications

Energy Package
    ↓
    ├─ Rate-based: Airer, heating, appliances
    ├─ Solar forecast: Hot water control (Eddi)
    └─ Battery management: Mode switching (Growatt)

Alarm Package
    ↓
    └─ Linked to all rooms (motion detection, door checks)

Climate Package
    ↓
    ├─ Presence detection (set to home/away)
    ├─ Temperature alerts (radiators below target)
    └─ Time-based schedules
```

### No Circular Dependencies Detected
- All flows are directional (downward from integration → rooms)
- Messaging is central hub, consumed by all
- Room packages are mostly independent

---

## Scene Inventory (75+ Scenes)

### By Category
| Category | Count | Example Scenes | Notes |
|----------|-------|-----------------|-------|
| **Lighting** | 50+ | room_lights_on, room_lights_dim, room_lights_red | Most scenes are lighting |
| **Climate** | 5 | heating_on, heating_off, radiator_boost | Temperature presets |
| **Security** | 5 | alarm_armed, alarm_disarmed | Alarm states |
| **Special** | 15 | fake_presence_lights, movie_mode | Context-specific |

### Key Scenes by Room
- **Living Room:** Lights on, lights off, lamps yellow, lamps red, movie mode
- **Kitchen:** Table lights on, cooker lights on, all off
- **Bedrooms:** Normal, dim, movie, all off
- **Stairs:** On, off

---

## Input Helpers Location Map

### Stored in UI (Preferred)
**These are NOT in YAML, managed via HA UI:**
- `input_boolean.enable_*_motion_triggers` (room motion toggles)
- `input_boolean.naughty_step_mode` (parental control)
- `input_number.*_light_level_threshold` (illuminance levels)
- `input_number.airer_minimum_temperature` (appliance condition)
- `input_select.home_mode` (Normal/Holiday/No Children/Naughty)
- `input_datetime.*` (schedule times)
- `timer.*` (motion light-off timers)

### Defined in YAML
- `schedule.notification_quiet_time` (Quiet hours schedule)

**Note:** User preference to keep helpers in UI for easy adjustment without reloading

---

## Known Issues & Deferred Work

### GitHub Issues (Status as of 2026-01-15)

| Issue | Type | Title | Status | Related Files | PR |
|-------|------|-------|--------|----------------|-----|
| #175 | Feature | Circadian lighting for Leo's bedroom | Testing | bedroom2.yaml | PR #175 |
| #176 | Optimization | Unsafe brightness attribute checks | Deferred | bedroom.yaml, conservatory.yaml, living_room.yaml (7 instances) | - |
| #177 | Feature | Smart quiet hours with keyword bypass | Testing | notifications.yaml | PR #177 |
| #178 | Feature | Notification acknowledgment system | Planning | messaging/ package | - |
| #179 | Feature | Device-aware notification routing | Planning | messaging/ package | - |
| #40 | Feature | Bin emptied notification | Blocked | (sensor accuracy) | - |

### Deferred Work Details

**Issue #176: Unsafe Brightness Attribute Checks**
- **Instances:** 7 locations across 3 files
- **Pattern:** Using fragile `state_attr('light.*', 'brightness') == none`
- **Proposed Fix:** Use `default()` filter instead
- **Files:**
  - packages/rooms/bedroom/bedroom.yaml (lines 29, 459, 461)
  - packages/rooms/conservatory/conservatory.yaml (line 29)
  - packages/rooms/living_room.yaml (lines 43, 45, 96, 98)
- **Priority:** Low (doesn't cause failures, just fragile)

**Issue #178: Notification Acknowledgment System**
- **Type:** Feature enhancement
- **Status:** Detailed implementation plan in GitHub issue
- **Approach:** Track which users acknowledged which notifications
- **Use Cases:** Parental notifications, emergency alerts

**Issue #179: Device-Aware Notification Routing**
- **Type:** Feature enhancement
- **Status:** Detailed implementation plan with 3 approaches
- **Approaches:** Time-based, availability-based, hybrid
- **Goal:** Route notifications to most available device per person

**Feature 4: Rich Notification Formatting (Skipped)**
- **Status:** Not implementing (user decision)
- **Reason:** Low priority vs other features

---

## Recent Changes & Commits

### PR #175: Circadian Lighting for Leo's Bedroom
- **Status:** Testing/approval phase
- **Changes:** Automated color temperature based on sun position
- **Commit:** (multiple commits during implementation)
- **Files:** packages/rooms/bedroom2.yaml
- **Details:** Cool white (4500K) day → warm white (3200K) evening → very warm (2700K) night

### PR #177: Smart Quiet Hours with Keyword Bypass
- **Status:** Testing/approval phase
- **Changes:** Allow critical messages through quiet hours if message contains emergency keywords
- **Hardcoded Keywords:** emergency, fire, gas, water, leak, intruder, alarm, breach, danger, alert, critical, urgent
- **Files:** packages/integrations/messaging/notifications.yaml (lines 130-142)
- **Details:** Jinja2 template loops through keyword array, case-insensitive substring match

### Recent Commits (Living Room Review, 2026-01-15)
1. **Simplify redundant blind control logic** (commit 52a3965b)
   - Consolidated 37 lines to 8 lines
   - Removed redundant condition checks

2. **Clarify motion detection logic** (commit 5ccb3a3b)
   - Added aliases and documentation for yellow flash signal
   - Clarified that flash is intentional, not a bug

3. **Fix unquoted log_level value** (commit 18960b2d)
   - Changed `log_level: Debug` to `log_level: "Debug"`

4. **Fix invalid condition syntax** (commit 36df28dc)
   - Fixed 6 instances of `condition: state` with `attribute:` key
   - Changed to `condition: numeric_state` with `below: 50`

5. **Add missing script calls** (commit 8ccd8f4b)
   - Added `script.get_clock_emoji` calls to 28 instances across 9 files
   - Fixes undefined `clock_result.emoji` references

### Recent Commits (Office.yaml Review + CI Improvements, 2026-01-19)

**Office.yaml Fixes:**
1. **Fix invalid syntax in office_turn_off_backup_drive script** (commit 719f42af)
   - Fixed `and:` operator in sequence block, converted to proper `if:`/`then:` structure
2. **Fix undefined clock_result references** (commit 1e9c870d)
   - Added missing `script.get_clock_emoji` call in blind automation
3. **Remove redundant condition in motion automation** (commit 611fdef6)
   - Removed duplicate numeric_state check already enforced by trigger
4. **Simplify office light timeout automation** (commit 6663a3ac)
   - Consolidated overlapping timer triggers to single 3-minute timeout

**CI/CD Pipeline Improvements:**
1. **Install custom component dependencies before validation** (commit e0e2f96f)
   - Automated dependency installation from manifest.json files
2. **Replace device triggers with dummy triggers for CI** (commit 98390738)
   - Fixes "Unknown device" validation errors in CI environment
3. **Consolidate CI config preparation into reusable scripts** (commit b7ae54f3)
   - Created install-custom-component-deps.sh and prepare-config-for-ci.sh
4. **Improve CI script error handling and logging** (commit 9c6249f8)
   - Added jq availability check, statistics tracking, better error messages
5. **Test delete/a_file_logger/openid integrations** (commits 44d883a0, 39ae08ad)
   - Successfully validated delete integration without stripping
   - Testing a_file_logger and openid (pending validation results)
6. **Add CI/CD documentation** (.github/workflows/README.md created)
   - Comprehensive documentation of workflows, known issues, troubleshooting

### Recent Documentation Updates
- **claude.md:** Updated with Lessons Learned from living room review
- **claude.md:** Added Smart Notification Patterns section with full code examples
- **claude.md:** Added Automation ID Uniqueness Validation pattern
- **.github/workflows/README.md:** Created comprehensive CI/CD pipeline documentation

---

## Critical System Entities (Quick Reference)

### Presence & Home Mode
- `person.danny`, `person.terina`, `person.leo`, `person.ashlee`
- `device_tracker.leos_switch` (Nintendo Switch)
- `input_select.home_mode` (Normal, Holiday, No Children, Naughty Step)

### Energy
- `sensor.octopus_energy_electricity_current_rate` (GBP/kWh, updates every 30 min)
- `sensor.growatt_battery_soc` (Battery state of charge)
- `select.growatt_mode` (Battery First, Load First, Grid First)
- `sensor.solcast_pv_forecast_*` (Solar generation forecast)

### Climate
- `climate.thermostat` (Hive heating)
- `climate.[room]_radiator` (TRV radiators)
- `sensor.temperature_*` (Multiple temperature sensors)

### Security
- `alarm_control_panel.ring_alarm` (Armed Away, Armed Home, Disarmed)
- `binary_sensor.*_contact` (Door/window sensors)
- NFC tags (front door unlock, bedroom master off)

### Notification Control
- `schedule.notification_quiet_time` (Quiet hours schedule)
- `notify.mobile_app_*` (Mobile devices)
- `notify.slack`, `notify.discord`, `notify.telegram` (Chat platforms)

### Multimedia
- `media_player.alexa_*` (Echo devices for announcements)
- `media_player.spotify` (Music selection)

---

## Architecture Overview

```
Home Assistant System Architecture (2026-01-15)

┌─────────────────────────────────────────────────────┐
│ Room Packages (11)                                   │
│ ├─ living_room.yaml (3,326 lines, 35 automations)  │
│ ├─ bedroom.yaml, bedroom2.yaml, bedroom3.yaml      │
│ ├─ kitchen/ (3 files)                               │
│ ├─ conservatory/ (3 files)                          │
│ ├─ office/ (2 files, 1,629 lines)                   │
│ └─ other rooms                                       │
└─────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────┐
│ Integration Packages (5)                             │
│ ├─ messaging/ (3 files - Central Hub)               │
│ ├─ energy/ (multiple files)                         │
│ ├─ alarm/ (automations)                             │
│ ├─ hvac/ (climate control)                          │
│ └─ weather/ (weather-based triggers)                │
└─────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────┐
│ Core Integrations                                    │
│ ├─ Octopus Energy (rate monitoring)                │
│ ├─ Growatt/Solar Assistant (PV monitoring)         │
│ ├─ Solcast (solar forecasting)                      │
│ ├─ myEnergi (Zappi/Eddi)                            │
│ ├─ Ring Alarm (security)                            │
│ ├─ Philips Hue, LIFX, Innr (lighting)              │
│ ├─ Alexa Media Player (announcements)               │
│ ├─ Slack, Discord, Telegram (notifications)        │
│ └─ MQTT (ESPHome communication)                     │
└─────────────────────────────────────────────────────┘
```

---

## Code Review Status

### Files Under Review (2026-01-15)
- **living_room.yaml:** Review complete, 5 critical fixes applied
- **bedroom2.yaml:** Review complete, circadian lighting implemented
- **office.yaml:** Review complete, 4 fixes applied + pattern analysis

### Files Pending Review
- kitchen.yaml and kitchen/ package
- Other room packages

### Office.yaml Review Findings (2026-01-15)

**File Size:** 1,629 lines, 35 automations + 5 scripts
**Issues Fixed:** 4 (2 critical, 1 medium, 1 low)

#### Critical Fixes Applied
1. **Invalid Script Syntax (lines 1350-1368)** - Fixed `and:` in sequence block, converted to proper `if:`/`then:` structure
2. **Undefined clock_result Variable (lines 448, 471, 485)** - Added missing `script.get_clock_emoji` call to define variable before use

#### Medium Fixes Applied
3. **Redundant Condition Check (lines 149-151)** - Removed duplicate numeric_state check already enforced by trigger

#### Low Priority Fixes Applied
4. **Overlapping Timer Triggers (lines 963-979)** - Consolidated to single 3-minute timeout (5-minute trigger was unreachable)

**Commits:**
- `719f42af` - Fix invalid syntax in office_turn_off_backup_drive script
- `1e9c870d` - Fix undefined clock_result references in office blind automation
- `611fdef6` - Remove redundant condition in office motion automation
- `6663a3ac` - Simplify office light timeout automation to use single 3-minute trigger

#### Reusable Patterns Identified

**High Reusability - Ready for Templating:**
1. **Motion Detection with Illuminance Logic** (Lines 4-136)
   - Dual-trigger motion detection (binary_sensor + numeric_state)
   - 4-branch choose block with brightness-based decisions
   - Extractable as room-generic template
   - Found in: living_room.yaml (similar pattern)

2. **No Motion Timer Pattern** (Lines 138-166 + 167-191)
   - Two-phase timer: "no motion detected" → start 1-minute grace timer
   - Appears in multiple office automations
   - Consolidation candidate: Create generic "room_no_motion_timer" template

3. **Sunrise/Sunset Event Handling** (Lines 414-843)
   - 8 distinct blind automations following consistent structure
   - Common checks: enable toggle, window contact, blind position, sun position
   - Reusable across rooms with parameter-driven thresholds
   - Tilt positions standardized (0, 25, 50 degrees)

4. **Temperature-Based Device Control** (Lines 194-278)
   - 3-priority system: auto-on (26°C) → warning (29°C) → emergency (31°C)
   - Graduated response pattern highly generalizable
   - Includes button-based interaction callbacks
   - Core pattern for any graduated automation response

5. **Message/Logging Patterns** (32 send_to_home_log calls)
   - Consistent structure: emoji + context + sensor values + action
   - Room emoji in title, numeric values with units
   - Log level: Debug (30), Normal (1 emergency case)
   - Standardization opportunity: Create message formatter script

**Medium Reusability:**
6. **Light Timeout Detection** (Lines 845-885) - Bright room light on too long detection
7. **Remote Control Integration** (Lines 912-959) - Device toggle via MQTT remote
8. **Scheduled Device Shutdown** (Lines 280-295) - Simple time-based off switch

#### Script Usage Analysis

| Script | Count | Reusability |
|--------|-------|-------------|
| `send_to_home_log` | 32 calls | Core (all packages) |
| `office_open_blinds` | 5 calls | Room-specific wrapper |
| `office_close_blinds` | 4 calls | Room-specific wrapper |
| `office_check_brightness` | 2 calls | Room-specific logic |
| `get_clock_emoji` | 1 call | Pattern: time-based messaging |
| `send_actionable_notification_with_2_buttons` | 1 call | Core (messaging) |
| `office_turn_off_backup_drive` | 1 call | Device-specific |
| `ecoflow_office_turn_off_plug` | 1 call | Device-specific |

**Total script invocations:** 47 direct calls across all automations

#### Consolidation Opportunities (Priority Order)

**HIGH PRIORITY:**
1. **Generic Motion Automation Template**
   - Parameterize: room name, motion sensor, lights, brightness threshold
   - Template both office and living_room patterns
   - Estimated reuse: 15+ automations across rooms

2. **Generic Blind Control Suite**
   - Extract 8 office blind automations into parameterized templates
   - Parameters: room, blind entity, window contact, sun/time triggers, thresholds
   - Estimated reuse: 40+ automations across rooms

**MEDIUM PRIORITY:**
3. **Temperature-Based Device Control Template**
   - Parameterize: temperature sensor, device/switch, priority thresholds, time windows
   - Estimated reuse: 8+ automations (office fan + other rooms)

4. **Message Formatter Standardization**
   - Create utility script to standardize log message formatting
   - Reduces send_to_home_log call complexity

**LOW PRIORITY:**
5. **Remote Control Device Template** - Parameterize MQTT device toggles
6. **Light Timeout Detection Template** - Generic daylight light detection

#### Known Code Patterns
- Motion-based lighting: Mature, multi-branch with context awareness, computer presence check unique to office
- Blind control: Mature, safety interlocks implemented, 9-step closure sequence very sophisticated
- Energy automation: Sophisticated, rate-aware with forecasting
- Notification system: Under active development (PR #177, Issues #178-179)
- Temperature control: Graduated response pattern (auto/warning/emergency levels)

---

## How to Use This Index

**At Session Start:**
1. Read this file (2-3 minutes, ~150 tokens)
2. Use it to understand system architecture
3. Reference specific patterns when creating new automations

**During Work:**
1. Check "Scripts Inventory" before creating new scripts (avoid duplication)
2. Check "Automation Patterns" to find similar implementations
3. Reference "Cross-Package Dependencies" for integration points

**Before Committing:**
1. Update this file with any new scripts/automations added
2. Note any deferred work or patterns discovered
3. Update "Recent Changes" section

**Monthly:**
1. Run comprehensive Explore scan to verify accuracy
2. Add discovered patterns to "Automation Patterns"
3. Update "Recent Changes" section

---

## Next Steps

1. **Review this index** - Does it capture the system accurately?
2. **Test reading time** - Measure actual token cost to read
3. **Evaluate usefulness** - Does it help with code reuse?
4. **Consider complementary tools** - Explore agents for deep dives, periodic scans

Once approved, this file should be:
- Committed to `.claude/system-index.md`
- Updated after each major work session
- Referenced at the start of every session
