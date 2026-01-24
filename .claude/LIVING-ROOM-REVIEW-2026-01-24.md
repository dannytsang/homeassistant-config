# Living Room Review - Based on Kitchen Timer Reflection

**Date:** 2026-01-24
**Review Type:** Pattern validation against newly discovered kitchen timer errors
**Reviewer:** Claude (Self-review based on kitchen reflection learnings)

---

## Executive Summary

Living Room automation has **1 CRITICAL pattern** that should be refactored based on kitchen reflection findings:

**Finding:** Unsafe brightness attribute access without safe defaults
- **Location:** Motion detection automation (ID: 1583956425622)
- **Lines:** 34-45
- **Severity:** 🔴 CRITICAL
- **Risk:** Template evaluation errors when lights are off

---

## Pattern Analysis

### Issue 1: Unsafe Brightness Attribute Access

**Location:** Motion Detected automation (lines 34-45)

**Current Code (UNSAFE):**
```yaml
conditions:
  - or:
      - condition: numeric_state
        entity_id: light.living_room_lamp_left
        attribute: brightness
        below: 190  # ❌ FAILS when light is off (attribute doesn't exist)
      - condition: numeric_state
        entity_id: light.living_room_lamp_right
        attribute: brightness
        below: 190
      - condition: template
        value_template: "{{ state_attr('light.living_room_lamp_left', 'brightness') == none }}"  # ❌ UNSAFE
      - condition: template
        value_template: "{{ state_attr('light.living_room_lamp_right', 'brightness') == none }}"  # ❌ UNSAFE
```

**Problem:**
1. `numeric_state` on `attribute: brightness` fails when light is off (attribute doesn't exist)
2. Checking `state_attr(...) == none` is dangerous - accessing undefined attributes
3. Redundant logic: checking if attribute is none AND checking if < 190

**Root Cause:**
Brightness attribute only exists when light is `on`. When light is `off` or `unavailable`, the attribute doesn't exist, causing:
- Template evaluation errors
- Condition logic failures
- Unexpected behavior

---

## Recommended Fixes

### Fix 1: Safe Attribute Access with Variables

**Replace lines 34-45 with:**

```yaml
conditions:
  - variables:
      lamp_left_brightness: "{{ state_attr('light.living_room_lamp_left', 'brightness')|int(0) }}"
      lamp_right_brightness: "{{ state_attr('light.living_room_lamp_right', 'brightness')|int(0) }}"

  - or:
      # Sensor 1: Dark room (motion sensor light levels low)
      - condition: numeric_state
        entity_id: sensor.apollo_r_pro_1_w_ef755c_ltr390_light
        below: input_number.living_room_light_level_2_threshold
      - condition: numeric_state
        entity_id: sensor.living_room_motion_illuminance
        below: input_number.living_room_light_level_4_threshold
      - condition: state
        entity_id: sensor.living_room_motion_illuminance
        state: "unavailable"

  # Lamps are off or dim (brightness < 190)
  - or:
      - condition: state
        entity_id: light.living_room_lamp_left
        state: "off"
      - condition: state
        entity_id: light.living_room_lamp_right
        state: "off"
      - condition: template
        value_template: "{{ lamp_left_brightness < 190 }}"
      - condition: template
        value_template: "{{ lamp_right_brightness < 190 }}"
```

**Why This Works:**
1. Extract brightness with safe default (`|int(0)`) at top level
2. Use state checks first (light is off)
3. Then use template conditions with variables
4. No more unsafe attribute access

---

## Other Observations

### ✅ Good Patterns Found

**1. Timer-based shutdown sequence** (lines 132-275)
- Motion off → Start dim timer (2 min)
- Dim timer expires → Start off timer (5 min)
- Off timer expires → Turn off lights
- **Advantage:** Gives user time to re-trigger before shutdown
- **Advantage:** Timers are NOT in conditional branches (correct)

**2. Illuminance threshold checks** (lines 24-29)
- Using numeric_state on SENSOR values (safe - sensors are always available)
- Using input_number for thresholds (parameterized, good)
- Good fallback for unavailable sensor

**3. Parallel actions for logging + control** (lines 47-77)
- Logging and light control in parallel (correct)
- No blocking operations

---

## Comparison to Kitchen Pattern

### Kitchen Error Pattern (Commit 458ac9dd)
```yaml
# WRONG: Timer cancellation only if conditions met
- if:
    - condition: numeric_state
      entity_id: light.kitchen
      attribute: brightness
      below: 100
  then:
    - action: script.cancel_all_timers
```

### Living Room (Similar Issue - Different Manifestation)
```yaml
# UNSAFE: Brightness check fails when light is off
- condition: numeric_state
  entity_id: light.living_room_lamp_left
  attribute: brightness
  below: 190
```

**Pattern:** Both use unsafe brightness attribute access
**Symptom:** Kitchen had lights dimming despite motion; Living Room could have condition logic failures
**Solution:** Both need safe attribute access with defaults

---

## Implementation Guide

### Step 1: Extract Attribute to Variable

```yaml
actions:
  - variables:
      lamp_left_brightness: "{{ state_attr('light.living_room_lamp_left', 'brightness')|int(0) }}"
      lamp_right_brightness: "{{ state_attr('light.living_room_lamp_right', 'brightness')|int(0) }}"

  # Rest of automation continues with these safe variables
```

### Step 2: Update Condition Logic

Replace direct `numeric_state` on `attribute: brightness` with:
- State check: `state: "off"` (safe, doesn't need attribute)
- Template check: `{{ variable < threshold }}` (safe, variable has default)

### Step 3: Verify Logic

Test with:
- [ ] Lights OFF → Motion detected → Should turn on
- [ ] Lights ON (bright) → Motion detected → Should NOT trigger
- [ ] Lights ON (dim) → Motion detected → Should turn on
- [ ] Lights UNAVAILABLE → Motion detected → Should handle gracefully

---

## Code Quality Impact

**Before Fix:**
- ⚠️ Potential runtime errors when lights are off
- ⚠️ Unsafe attribute access (anti-pattern)
- ⚠️ Inconsistent condition logic (numeric_state + template checks)

**After Fix:**
- ✅ Safe attribute access with defaults
- ✅ Clearer logic structure (state checks + template conditions)
- ✅ Consistent with new validation standards
- ✅ No runtime errors from missing attributes

---

## Files to Update

**Primary File:**
- `packages/rooms/living_room.yaml` (lines 34-45 in motion detection automation)

**Documentation:**
- `packages/rooms/LIVING-ROOM-SETUP.md` (reflects current code, will need review after fix)

---

## Cross-Reference

**Related Patterns:**
- Kitchen Timer Error: `.claude/REFLECTION-KITCHEN-TIMER-2026-01-24.md`
- Safe Attribute Access: `.claude/home-assistant-templating-reference.md` (Safe Attribute Access Pattern section)
- Quality Checker: `.claude/skills/ha-yaml-quality-reviewer.md` (Pattern 7: Unsafe attribute access)

---

## Risk Assessment

**Fix Complexity:** Medium
- Requires modifying condition logic
- Requires testing multiple light states
- Low risk of breaking existing functionality (improves robustness)

**Testing Required:**
- Motion detection with various light states
- Verify dim/bright conditions work correctly
- Verify lamps turn on when they should

**Rollback Plan:**
- Keep original YAML for reference
- Easy to revert if issues found
- Patterns are well-established (tested in kitchen fix)

---

## Summary & Recommendations

### Immediate Action
- [ ] Apply safe attribute access pattern to motion detection automation
- [ ] Add variables for lamp_left_brightness, lamp_right_brightness
- [ ] Replace unsafe numeric_state conditions with safe template conditions
- [ ] Test motion detection with lights in various states

### Medium-term
- [ ] Review all other rooms for similar patterns
- [ ] Run error detector script (Pattern 7) across all packages
- [ ] Apply consistency across all motion automations

### Long-term
- [ ] Add this pattern to pre-commit validation
- [ ] Document as standard for attribute access
- [ ] Consider broader refactoring of attribute-based conditions

---

**Status:** Ready for implementation
**Priority:** 🔴 CRITICAL (potential runtime errors)
**Estimated Fix Time:** 15-20 minutes
**Estimated Test Time:** 10-15 minutes

---

**Review Completed:** 2026-01-24
**Next Steps:** User decision on implementation
