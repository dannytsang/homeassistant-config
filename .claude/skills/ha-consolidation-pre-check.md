# Claude Skill: Home Assistant Consolidation Pre-Check

**Status:** Production Ready
**Version:** 1.0
**Created:** 2026-01-24
**Purpose:** De-risk consolidation work by validating automations meet consolidation criteria before attempting

---

## Purpose

Validate automations are safe to consolidate BEFORE applying the motion consolidator skill. Identifies consolidation blockers, validates compatibility, and assesses complexity.

---

## When to Use

- **Before attempting any consolidation** - Essential pre-check
- **Planning consolidation roadmap** - Score and prioritize
- **Risk assessment** - Identify blocking issues early
- **Preventing failed consolidations** - Validate prerequisites
- **During consolidation analyzer review** - Complement scoring process

---

## Critical Pre-Consolidation Checks

### Check 1: Same Trigger Entity

**Purpose:** Validate all automations share the same trigger source

**Rule:** Cannot consolidate automations that trigger on different entities

**Check Process:**
```yaml
# Group of automations to consolidate:
- id: "1606428361967"
  triggers:
    - trigger: state
      entity_id: binary_sensor.kitchen_motion    ← Entity A

- id: "1587044886896"
  triggers:
    - trigger: state
      entity_id: binary_sensor.kitchen_motion    ← Entity A (SAME ✅)

- id: "1587044886897"
  triggers:
    - trigger: state
      entity_id: binary_sensor.office_motion     ← Entity B (DIFFERENT ❌)
```

**Detection:**
```bash
# Extract trigger entities from potential consolidation group
for id in "1606428361967" "1587044886896" "1587044886897"; do
  echo "Automation $id:"
  grep -A 5 "id: \"$id\"" packages/rooms/*/*.yaml | \
    grep "entity_id:" | head -1
done

# Expected output:
# Automation 1606428361967: entity_id: binary_sensor.kitchen_motion
# Automation 1587044886896: entity_id: binary_sensor.kitchen_motion ✅ SAME
# Automation 1587044886897: entity_id: binary_sensor.office_motion ❌ DIFFERENT
```

**Blocker:** ❌ If triggers differ → Cannot consolidate without refactoring

---

### Check 2: Same Trigger State

**Purpose:** Validate automations trigger on same state change

**Rule:** Cannot consolidate if triggers on different states (one on "on", another on "off")

**Check Process:**
```yaml
# Automations to consolidate:
- id: "1606428361967"
  triggers:
    - trigger: state
      entity_id: binary_sensor.kitchen_motion
      to: "on"    ← Triggers when motion detected

- id: "1587044886896"
  triggers:
    - trigger: state
      entity_id: binary_sensor.kitchen_motion
      to: "on"    ← Triggers when motion detected (SAME ✅)

- id: "1606428361968"
  triggers:
    - trigger: state
      entity_id: binary_sensor.kitchen_motion
      to: "off"   ← Triggers when motion stops (DIFFERENT ❌)
```

**Exception:** Motion on/off pair CAN be consolidated with trigger ID branching

**Detection:**
```bash
# Extract trigger state from each automation
for id in "1606428361967" "1587044886896" "1606428361968"; do
  echo "Automation $id:"
  grep -A 7 "id: \"$id\"" packages/rooms/*/*.yaml | \
    grep "to:" | head -1
done

# Expected output:
# Automation 1606428361967: to: "on"
# Automation 1587044886896: to: "on" ✅ SAME
# Automation 1606428361968: to: "off" ⚠️ DIFFERENT (but can use trigger ID)
```

**Blocker:** ❌ If states differ and no trigger ID branching → Flag as complexity

---

### Check 3: No Conflicting Conditions

**Purpose:** Validate consolidated conditions won't create logical impossibilities

**Rule:** Conditions must not be mutually exclusive

**Check Process:**
```yaml
# Automation 1: Trigger on motion IF brightness < 50
- id: "1606428361967"
  triggers: [...]
  conditions:
    - condition: numeric_state
      entity_id: sensor.brightness
      below: 50

# Automation 2: Trigger on motion IF brightness > 100
- id: "1587044886896"
  triggers: [...]
  conditions:
    - condition: numeric_state
      entity_id: sensor.brightness
      above: 100
```

**Analysis:**
- Automation 1 runs when brightness < 50 (dark)
- Automation 2 runs when brightness > 100 (bright)
- These are NOT mutually exclusive ✅ CAN consolidate

**Bad Example (Conflicting):**
```yaml
# Automation 1: Only if kitchen is occupied
- condition: state
  entity_id: binary_sensor.kitchen_occupied
  state: "on"

# Automation 2: Only if kitchen is NOT occupied
- condition: state
  entity_id: binary_sensor.kitchen_occupied
  state: "off"
```

**Analysis:**
- Cannot be both occupied AND not occupied at same time
- Mutually exclusive ❌ Cannot consolidate

**Detection Algorithm:**
```python
def has_conflicting_conditions(automations):
    """Check if conditions are mutually exclusive"""

    conditions = [auto.conditions for auto in automations]

    for i, cond1 in enumerate(conditions):
        for j, cond2 in enumerate(conditions[i+1:]):
            # Check for same entity with opposite states
            if cond1.entity == cond2.entity:
                if is_opposite_state(cond1.state, cond2.state):
                    return True  # ❌ Conflicting

    return False  # ✅ Safe to consolidate
```

**Blocker:** ❌ If conflicting conditions → Cannot consolidate

---

### Check 4: Trigger Order Doesn't Affect Logic

**Purpose:** Validate consolidation order won't break logic

**Rule:** If consolidating motion on/off pair, on must execute before off

**Check Process:**

For motion detection consolidation:
```yaml
# Motion detectors - order matters!
- trigger: state
  entity_id: sensor.motion
  to: "on"
  id: motion_on    # Must execute FIRST

- trigger: state
  entity_id: sensor.motion
  to: "off"
  id: motion_off   # Can execute after motion_on
```

**Logic:** When motion starts:
1. Execute motion_on branch (turn lights on)
2. Start timer
3. When motion ends, execute motion_off branch (turn lights off)

If reversed, logic breaks → Timer never starts

**Detection:**
```bash
# Check motion pairs exist for same entity
grep -rn "to: \"on\"" packages/rooms/ | grep "motion"
grep -rn "to: \"off\"" packages/rooms/ | grep "motion"

# Count: If both exist for same entity, motion pair consolidation is valid
```

**Blocker:** ⚠️ If time-based or complex ordering → Flag as high complexity

---

### Check 5: Nesting Depth Won't Exceed Complexity Limit

**Purpose:** Validate consolidated automation won't be too deeply nested

**Rule:** Maximum nesting depth should be < 6 levels

**Why:** Deep nesting becomes hard to maintain and debug

**Current Nesting Analysis:**
```yaml
# Motion consolidation typically creates this structure:
automation:
  - id: "consolidated_motion"
    triggers: [...]
    conditions: [...]
    actions:
      - choose:                           # Level 1
          - alias: "Table lights"
            conditions: [...]
            sequence:
              - parallel:                 # Level 2
                  - action: scene.turn_on
                  - action: script.send_log
          - alias: "Cooker lights"
            conditions: [...]
            sequence:
              - parallel:                 # Level 2
                  - action: scene.turn_on
      - choose:                           # Level 1
          - alias: "Ambient lights"
            conditions: [...]
            sequence:
              - if:                       # Level 2
                  conditions: [...]
                  then:
                    - action: scene.turn_on
```

**Nesting Depth:** 2-3 levels ✅ Acceptable

**Detection:**
```bash
# Count indentation levels in consolidated automation
grep -A 100 "id: \"consolidated_motion\"" packages/rooms/*/kitchen.yaml | \
  sed 's/^\([ \t]*\).*/\1/' | \
  sed 's/\t/    /g' | \
  awk '{print length($0)/4}' | sort -rn | head -1

# Result: Should be < 6
```

**Blocker:** ❌ If nesting > 6 levels → Split into multiple automations

---

### Check 6: No Cross-Package Dependencies

**Purpose:** Ensure consolidated automation doesn't depend on other packages

**Rule:** Cannot consolidate automations with dependencies on external automations

**Check Process:**
```yaml
# Automation in kitchen.yaml
- id: "kitchen_motion"
  triggers: [motion]
  actions:
    - action: scene.turn_on
      target:
        entity_id: scene.kitchen_table_lights_on
    # References kitchen scenes ✅ Same package

# Automation in office.yaml
- id: "office_motion"
  triggers: [motion]
  actions:
    - action: automation.trigger
      target:
        entity_id: automation.lighting_scene_change  # ❌ Cross-package dependency
```

**Detection:**
```bash
# Find automations calling other automations
grep -rn "automation.trigger\|automation.turn_on" packages/rooms/*/

# Find automations calling scripts from other packages
grep -rn "action: script\." packages/rooms/*/ | \
  grep -v "packages/rooms/CURRENT_PACKAGE"

# These are blocking issues
```

**Blocker:** ❌ If cross-package dependencies → Cannot consolidate without refactoring

---

## Safety Scoring System

### Score Consolidation Safety

```
Total Score: 0-100 points

Safe Consolidation Criteria:
✅ Same trigger entity: +25 points
✅ Same trigger state: +25 points
✅ No conflicting conditions: +20 points
✅ No trigger order dependencies: +15 points
✅ Nesting depth < 6: +10 points
✅ No cross-package dependencies: +5 points

Result:
90-100: SAFE TO CONSOLIDATE - Proceed immediately
70-89:  SAFE WITH CAUTION - Review nesting depth
50-69:  BLOCKERS EXIST - Requires refactoring first
0-49:   NOT SAFE - Do not consolidate
```

### Scoring Examples

**Example 1: Simple Motion Light Consolidation**
```yaml
Automations: 3 (Table on, Cooker on, Ambient on)
Same trigger: ✅ All binary_sensor.kitchen_motion (+25)
Same state: ✅ All to: "on" (+25)
Conditions: ✅ No conflicts (brightness checks) (+20)
Trigger order: ✅ No dependencies (+15)
Nesting: ✅ < 6 levels (+10)
Dependencies: ✅ None (+5)
---
TOTAL: 100/100 ✅ SAFE - Consolidate immediately
```

**Example 2: Time-Based with Dependencies**
```yaml
Automations: 2 (Sunset close, Night close)
Same trigger: ⚠️ Different times (-15)
Same state: ✅ Both set cover position (+25)
Conditions: ❌ Complex ordering issues (-10)
Trigger order: ⚠️ Sunset must run before Night (+5)
Nesting: ✅ Simple sequence (+10)
Dependencies: ❌ Calls automation.lighting (+0)
---
TOTAL: 15/100 ❌ NOT SAFE - Major blockers
```

**Example 3: Motion with Room Mode**
```yaml
Automations: 4 (Day lights, Evening lights, Night lights, Movie mode)
Same trigger: ✅ All binary_sensor.office_motion (+25)
Same state: ❌ Different to states (-10)
Conditions: ✅ No conflicts (+20)
Trigger order: ❌ Complex decision tree (-10)
Nesting: ⚠️ 4 levels (+8)
Dependencies: ✅ Local scenes only (+5)
---
TOTAL: 38/100 ⚠️ MODERATE RISK - Reconsider or refactor
```

---

## Pre-Consolidation Checklist

### Before Consolidation Starts

- [ ] **Check 1:** All automations trigger same entity (✅ or ❌ blocker)
- [ ] **Check 2:** All trigger same state OR can use trigger ID branching (✅ or ⚠️)
- [ ] **Check 3:** No mutually exclusive conditions (✅ or ❌ blocker)
- [ ] **Check 4:** Trigger order validated (✅ or ⚠️ high complexity)
- [ ] **Check 5:** Resulting nesting depth < 6 levels (✅ or ❌ blocker)
- [ ] **Check 6:** No cross-package dependencies (✅ or ❌ blocker)
- [ ] **Score:** Consolidation safety score > 70
- [ ] **Plan:** Document consolidation approach before starting

### If Any Blocker Found

❌ Stop consolidation attempt
- [ ] List all blockers
- [ ] Plan refactoring needed
- [ ] Reschedule consolidation after refactoring
- [ ] Update consolidation roadmap

---

## Usage Examples

### Example 1: Pre-Check Motion Consolidation (PASS)

**Task:** Pre-check kitchen motion automations for consolidation

```bash
# Step 1: Identify automations to consolidate
grep -rn "Kitchen: Motion Detected" packages/rooms/kitchen/kitchen.yaml
# Result: IDs: 1606428361967, 1587044886896, 1587044886897

# Step 2: Extract and validate triggers
for ID in "1606428361967" "1587044886896" "1587044886897"; do
  echo "Checking $ID..."
  grep -A 5 "id: \"$ID\"" packages/rooms/kitchen/kitchen.yaml | \
    grep -E "entity_id:|to:"
done

# Result:
# 1606428361967: entity_id: binary_sensor.kitchen_motion, to: "on"
# 1587044886896: entity_id: binary_sensor.kitchen_motion, to: "on" ✅
# 1587044886897: entity_id: binary_sensor.kitchen_motion, to: "on" ✅

# Step 3: Check conditions
grep -A 8 "id: \"1606428361967\"" packages/rooms/kitchen/kitchen.yaml | grep "condition:"
# All use brightness threshold - no conflicts ✅

# Step 4: Check for dependencies
grep -A 30 "id: \"1606428361967\"" packages/rooms/kitchen/kitchen.yaml | \
  grep "action: automation\|action: script"
# No dependencies found ✅

# Step 5: Estimate nesting
# Expected: 2 levels (choose + parallel) ✅

# Verdict: ✅ SAFE - Score 95/100
# Action: PROCEED WITH CONSOLIDATION
```

### Example 2: Pre-Check Time-Based Consolidation (FAIL)

**Task:** Pre-check blind automations for consolidation

```bash
# Step 1: Identify automations
grep -rn "Blind.*\(Sunset\|Morning\|Night\)" packages/rooms/office/office.yaml
# Result: IDs: 1622374444832, 1622374233312, 1622374233310

# Step 2: Extract triggers
for ID in "1622374444832" "1622374233312" "1622374233310"; do
  echo "Checking $ID..."
  grep -A 5 "id: \"$ID\"" packages/rooms/office/office.yaml | \
    grep "trigger:"
done

# Result:
# 1622374444832: trigger: sun (sunrise)
# 1622374233312: trigger: sun (sunset)
# 1622374233310: trigger: time (23:00) ❌ DIFFERENT TRIGGER TYPES

# Blocker Found: ❌ Different trigger entities/types

# Step 3: Check conditions for logic
grep -A 15 "id: \"1622374233312\"" packages/rooms/office/office.yaml | \
  grep "condition:"
# Condition: if sun elevation < 15 (specific angle requirement)

# Step 4: Check order dependencies
# Morning (sunrise): Open blinds at 8:00 AM
# Sunset (sunset): Close blinds at sunset
# Night (time): Force close at 23:00
# These are time-sequenced - ORDER CRITICAL ❌

# Verdict: ❌ NOT SAFE - Score 35/100
# Blockers:
#   1. Different trigger types (sun vs time)
#   2. Order-dependent logic
#   3. Complex nesting likely needed
# Action: DO NOT CONSOLIDATE - Keep separate automations
```

---

## Integration with Other Skills

### With ha-motion-consolidator.md
- **Prerequisite:** Run pre-check before consolidation
- **Gate:** Only proceed if score > 70
- **Validation:** Verify all checks passed

### With ha-consolidation-analyzer.md
- **Pre-scoring:** Run checks before assigning consolidation score
- **Risk factor:** Incorporate safety score into overall score
- **Blocking:** Flag low-score automations as not ready

### With ha-yaml-quality-reviewer.md
- **Pre-review:** Run checks before quality review
- **Dependency mapping:** Identify cross-package dependencies
- **Complexity validation:** Flag overly nested structures

---

## Troubleshooting

### Problem: "Found different trigger entities"

**Situation:**
```yaml
- id: "auto1"
  triggers:
    - entity_id: binary_sensor.kitchen_motion

- id: "auto2"
  triggers:
    - entity_id: binary_sensor.office_motion  # ❌ DIFFERENT
```

**Solution:**
- ❌ Cannot consolidate these together
- ✅ Consolidate kitchen motions separately from office motions
- ✅ Or: Consolidate at room level (one automation per room)

### Problem: "Conditions are mutually exclusive"

**Situation:**
```yaml
- id: "auto1"
  conditions:
    - condition: state
      entity_id: mode
      state: "day"  # Only runs in day mode

- id: "auto2"
  conditions:
    - condition: state
      entity_id: mode
      state: "night"  # Only runs in night mode ❌ CONFLICTS
```

**Solution:**
- ❌ Cannot consolidate - different modes
- ✅ Use choose branches with mode conditions
- ✅ Or: Keep separate (they run at different times anyway)

### Problem: "Nesting too deep (> 6 levels)"

**Situation:** Trying to consolidate 8+ automations with complex conditions

**Solution:**
- ❌ Would create overly complex automation
- ✅ Split into two automations (e.g., "Lights On" + "Lights Off")
- ✅ Or: Keep some separate based on function
- ✅ Result: Simpler, more maintainable automations

---

## Success Criteria

✅ All automations checked for consolidation safety
✅ No consolidation attempted without pre-check
✅ All blockers identified before consolidation starts
✅ All consolidations score > 70 safety
✅ No overly nested automations created (depth < 6)
✅ No cross-package dependencies created
✅ Consolidation roadmap updated with scores

---

## Key Learnings

**From consolidation experience:**
- Not all automations SHOULD be consolidated
- Simple consolidations (same trigger, same state): Safe ✅
- Complex consolidations (different conditions, time-based): Risky ❌
- Pre-check prevents wasted effort and broken logic
- Nesting depth matters for maintainability

---

## Next Steps

1. **Run pre-check on all consolidation candidates**
   - Score each group
   - Document blockers
   - Prioritize by score

2. **Update consolidation roadmap**
   - Mark high-score items (safe to consolidate)
   - Mark low-score items (refactor first)
   - Plan refactoring for blockers

3. **Integrate into workflow**
   - Always run pre-check before consolidation
   - Use safety score to determine approach
   - Document decisions for each consolidation

---

**Usage:** Run before every consolidation attempt to validate safety and identify blockers
**Team:** Danny's Home Assistant optimization
**Created:** 2026-01-24
**Status:** Production Ready
