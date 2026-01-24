# Leo's Bedroom (Bedroom 2) - Automation Review

**File:** `packages/rooms/bedroom2.yaml`
**Automations:** 20
**Scenes:** 2
**Scripts:** 1 (disabled - weather-based)
**Review Date:** 2026-01-14

---

## Summary

Leo's bedroom has **20 automations** focused heavily on blind control (9 automations), with basic light controls and scene management. The setup is generally solid but shows signs of accumulated complexity that could be optimized.

**Current Strengths:**
- Calendar-aware blind opening logic
- Remote control support
- Window integration for blind safety
- Bed occupancy detection

**Areas for Improvement:**
- Conflicting/overlapping blind automation times
- Missing motion-based lighting automations
- No temperature/comfort automations
- Lack of routine automations (bedtime, morning)
- Missing notification alerts for events
- Disabled weather automation (incomplete)

---

## Critical Issues Found

### 🔴 Issue 1: Contradictory Logic in Line 158
**File:** bedroom2.yaml, line 158
```yaml
- condition: state
  entity_id: input_boolean.enable_leos_blind_automations
  state: "off"
```
**Problem:** This automation (ID: 1627285063814) opens blinds at 9am ONLY when blind automations are DISABLED.
**Expected:** Should probably be `state: "on"` to open blinds when automations are enabled.
**Impact:** High - This automation likely never runs as intended.
**Status:** ⚠️ NEEDS FIX

### 🔴 Issue 2: Wrong Condition Check in Line 168
**File:** bedroom2.yaml, line 168
```yaml
- condition: state
  entity_id: binary_sensor.workday_sensor
  state: "on"
```
**Problem:** Same automation checks "No Children" mode on a "working day" - contradictory logic.
**Expected:** Should check `state: "off"` (non-working day).
**Impact:** High - Logic is backwards.
**Status:** ⚠️ NEEDS FIX

### 🔴 Issue 3: Message/Action Mismatch in Lines 334-339
**File:** bedroom2.yaml, lines 305-340
```yaml
alias: "Leo's Room: Open Blinds In The Morning When No One Is In Bed"
...
from: "on"
to: "off"  # Triggered when LEAVING bed
...
message: "🪟 🛏️ Someone is in Leo's bed. Closing blinds."
...
action: cover.open_cover  # OPENS blinds
```
**Problem:**
- Trigger: Fires when Leo LEAVES bed
- Message: Says "Someone IS in bed" (contradicts trigger)
- Action: Opens blinds (but should close them when leaving bed?)

**Expected:** Logic should either:
- CLOSE blinds when leaving bed, OR
- Change trigger to when bed becomes occupied

**Impact:** High - The automation does the opposite of its message.
**Status:** ⚠️ NEEDS FIX

---

## Optimization Opportunities

### 1. Conflicting/Redundant Blind Opening Times
**Lines:** 32-42, 154, 284, 309

You have **5 different automations** that open blinds in the morning:

| Time | Trigger | Conditions |
|------|---------|-----------|
| 07:45 | Time | School day + workday |
| 08:00 | Time | School day + workday |
| 09:00 | Time | School day + workday OR no children mode |
| 10:00 | Time | Fallback if still closed |
| 09:30 | Time | Always (no conditions) |
| Variable | Bed occupied -> unoccupied | Morning hours 7am-12pm |

**Problem:** These can conflict and cause duplicate executions.
**Recommendation:** Consolidate into single automation with smart logic:
```yaml
- Single trigger at 07:45
- Check calendars/mode
- Set appropriate open time based on conditions
- Use mode: single to prevent duplicates
```

### 2. Blind Closing Logic Duplication
**Lines:** 199-248

Three identical closing branches with duplicated logic:
```yaml
choose:
  - conditions: [window open]
    sequence: [log message]
  - conditions: [no children mode]
    sequence: [log + close]
  - conditions: [window closed]
    sequence: [log + close]  # Duplicate of last branch
```

**Recommendation:** Simplify to:
```yaml
choose:
  - conditions: [window open]
    sequence: [log skip]
default:
  - log message
  - close cover
```

### 3. Repeated Log Message Template
**Lines:** 209, 224, 240

All three use the same clock emoji template:
```
:clock{{ now().strftime('%I') | int }}{% if now().minute | int > 25 and now().minute | int < 35 %}30{% else %}{% endif %}:
```

**Recommendation:** Create helper template sensor for `sensor.current_clock_emoji` to reuse everywhere.

### 4. Window Condition Checked Multiple Times
**Lines:** 203, 234, 266, 347, 508

Window sensor state checked in 5 different automations.
**Recommendation:** Could create template binary_sensor for "leo's bedroom safe to close blinds" that combines window + time logic.

---

## Missing Automations / New Features

### 🚀 High Priority Features

#### 1. Motion-Based Lighting (Nighttime)
**Concept:** Turn on lights dimly when motion detected at night
```yaml
- Trigger: Motion detected (binary_sensor.leos_bedroom_motion)
- Conditions:
  - Time between 22:00 - 07:00
  - Light currently off
  - Brightness below 50 lux
- Action: Turn on lights at 10% brightness, warm color
```
**Benefit:** Safe navigation at night without full brightness

#### 2. Bedtime Routine Automation
**Concept:** Turn off lights + close blinds at bedtime
```yaml
- Trigger: Time at input_datetime.childrens_bed_time
- Action:
  - Dim lights to 5%
  - Close blinds
  - Play notification: "Time for bed"
  - Set temperature to 18°C
```
**Benefit:** Consistent bedtime routine, sleep preparation

#### 3. Morning Routine Automation
**Concept:** Gradual wake-up lighting + open blinds
```yaml
- Trigger: Time at 07:00 on school days
- Conditions: Leo's bed occupied OR motion detected
- Action:
  - Gradually brighten lights over 15 minutes
  - Open blinds
  - Play morning notification
  - Set temperature to 20°C
```
**Benefit:** Healthy wake-up, natural light exposure

#### 4. Room Temperature Control
**Concept:** Monitor and adjust heating based on occupancy/time
```yaml
- Trigger: Leo's bed occupied/unoccupied
- Conditions: Time outside school hours
- Action: Adjust thermostat to comfort range
```
**Benefit:** Energy efficiency + comfort

#### 5. Door Opening Notification
**Concept:** Alert when Leo's bedroom door opens/closes
```yaml
- Trigger: Door contact changes
- Action: Log to home log + notify parents (if late night)
```
**Benefit:** Safety awareness, bedtime monitoring

---

### 🎯 Medium Priority Features

#### 6. Humidity/Moisture Alert
**Using:** Existing mold_indicator sensor (line 692)
```yaml
- Trigger: Humidity above 70% for 30 minutes
- Action:
  - Log warning
  - Suggest opening window if temperature safe
```
**Benefit:** Prevent mold, improve air quality

#### 7. Light Color Temperature Automation
**Concept:** Warm lights before bed, cool lights in morning
```yaml
- Trigger: Time patterns
- Action: Set light color temp to 2700K (warm) after 19:00
- Action: Set light color temp to 5000K (cool) after 07:00
```
**Benefit:** Supports natural sleep rhythm

#### 8. Occupancy-Based Light Off
**Concept:** Turn lights off when room unoccupied for 10+ minutes
```yaml
- Trigger: No motion for 10 minutes
- Conditions:
  - Lights currently on
  - Time between 08:00-22:00 (daytime)
- Action: Turn lights off
```
**Benefit:** Energy saving, automatic management

#### 9. Excessive Screen Time Alert
**Concept:** Notify if lights on continuously for 3+ hours
```yaml
- Trigger: Lights on for 3 hours
- Action: Send notification to parents
```
**Benefit:** Encourage breaks, homework balance

---

### 💡 Low Priority Features

#### 10. Window Open Alert (Evening)
**Concept:** Remind if window left open after sunset
```yaml
- Trigger: Sunset + window still open
- Conditions: Time after 20:00
- Action: Notification to close window
```
**Benefit:** Security, heating efficiency

#### 11. Remote Battery Level Check
**Concept:** Monitor remote control battery
```yaml
- Trigger: Daily at 09:00
- Action: Check battery level, notify if low
```
**Benefit:** Proactive maintenance

#### 12. Lights Left On Reminder
**Concept:** Remind if lights on when Leo leaves house
```yaml
- Trigger: Leo leaves home + lights on
- Action: Send notification
```
**Benefit:** Energy saving, prevents accidental drain

#### 13. Homework Mode Scene
**Concept:** Dedicated lighting scene for studying
```yaml
- Scene: "Leo's Bedroom Homework"
  - Brightness: 90%
  - Color temp: 5500K (bright cool white)
  - Optional: Disable motion-off automation
```
**Benefit:** Better lighting for focus

---

## Code Quality Issues

### 1. Inconsistent Descriptions
- Many automations have empty descriptions (lines 6, 31, 151, etc.)
- **Recommendation:** Add meaningful descriptions for web UI visibility

### 2. Unused/Disabled Features
- Weather script (lines 462-530) has TODO comments and appears disabled
- **Recommendation:** Either complete the feature or document why it's disabled

### 3. Magic Numbers
- Bed occupancy thresholds: 0.06, 0.07 (lines 704-707)
- **Recommendation:** Document these calibration values

### 4. No Help Text
- No explanation of why certain times were chosen
- Example: Why 07:45 vs 08:00 vs 09:00 for blind opening?
- **Recommendation:** Add comments explaining logic

---

## Summary of Recommendations

### 🔴 Must Fix (Critical Bugs)
1. Line 158: Fix `enable_leos_blind_automations` condition (currently backwards)
2. Line 168: Fix `workday_sensor` check for "No Children" mode
3. Lines 305-340: Fix message/action mismatch for bed leaving trigger

### 🟡 Should Optimize (Medium Effort, High Value)
1. Consolidate 5 blind opening times into 1-2 automations
2. Simplify blind closing logic (remove duplication)
3. Create reusable clock emoji template sensor
4. Document design decisions for timing choices

### 🟢 Nice to Have (Low Effort, Good Value)
1. Add motion-based nighttime lighting
2. Add bedtime routine automation
3. Add morning routine automation
4. Add occupancy-based light off
5. Enable/complete weather script or remove it

---

## Complexity Metrics

| Metric | Count | Status |
|--------|-------|--------|
| Automations | 20 | High |
| Blind-focused automations | 9 | Could reduce to 4-5 |
| Trigger types | State, Time, Device | Balanced |
| Condition complexity | Medium | Some redundancy |
| Mode usage | Single, Queued | Appropriate |

---

## Files Affected by Recommendations

- `packages/rooms/bedroom2.yaml` - Main changes
- Potentially: Helper templates/sensors for shared logic
- Potentially: New routines package for bedtime/morning

**Estimated Effort:**
- Critical fixes: 30 minutes
- Optimization: 1-2 hours
- New features: 2-4 hours (depending on scope)

---

**Status:** Ready for implementation
**Priority:** Fix critical bugs first, then optimize, then add new features
