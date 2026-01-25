# Claude Skill: Home Assistant Entity Reference Validator

**Status:** Production Ready
**Version:** 1.0
**Created:** 2026-01-24
**Based On:** Reflection analysis (40% of recent errors - entity domain mismatches and name inconsistencies)

---

## Purpose

Cross-reference all entity_id mentions across Home Assistant packages, validate domain matching, detect typos and inconsistencies. Prevents entity domain mismatches (light.turn_on targeting input_boolean) and entity name errors.

---

## When to Use

- **Before committing automation changes** - Validate all entity_id references
- **After consolidation work** - Verify all entity targets are valid
- **During package reviews** - Check for undefined or typo'd entity references
- **When renaming entities** - Find all references to update
- **In pre-commit validation** - Catch entity errors before deployment

---

## ⚠️ Documentation Currency Check

**Before running this validator, confirm reference documentation is current:**

**Required Reference Files:**
- `home-assistant-automation-yaml-reference.md` - Service actions and domains
- `home-assistant-template-sensors-reference.md` - Entity types and device classes
- `home-assistant-splitting-configuration-reference.md` - Package entity organization

**Threshold:** 45 days (Entity types are more stable than automation syntax)

**How to Check:**
1. Read `.claude/documentation-update-log.md` for current ages
2. If any file is >45 days old, run `/ha-docs` to refresh
3. Then proceed with this validation

**If Documentation is Stale:**
```
⚠️ WARNING: Reference documentation is X days old
→ Recommendation: Run /ha-docs before proceeding
→ Reason: New entity types, integrations, or domain changes may be missing
```

**Why This Matters:**
- Entity domains can change between HA versions
- New integrations introduce new entity types
- Action domains may be updated or deprecated
- Service parameters may change

**Note:** This validator ensures entity_id references match valid domains. Outdated docs means missing new entity types and services.

---

## Critical Rules

### Rule 1: Action Domain Must Match Entity Domain

✅ **CORRECT EXAMPLES:**
```yaml
# light.turn_on requires light.* entity
- action: light.turn_on
  target:
    entity_id: light.kitchen_main

# switch.turn_on requires switch.* entity
- action: switch.turn_on
  target:
    entity_id: switch.office_fan

# input_boolean.turn_on requires input_boolean.* entity
- action: input_boolean.turn_on
  target:
    entity_id: input_boolean.enable_motion_triggers
```

❌ **WRONG EXAMPLES:**
```yaml
# light.turn_on targeting wrong domain
- action: light.turn_on
  target:
    entity_id: input_boolean.enable_kitchen_lights  # ❌ WRONG

# switch.turn_on targeting wrong domain
- action: switch.turn_on
  target:
    entity_id: light.office_fan  # ❌ WRONG

# input_boolean.turn_on targeting wrong domain
- action: input_boolean.turn_on
  target:
    entity_id: switch.motion_enabled  # ❌ WRONG
```

### Rule 2: Entity Names Must Match Exactly

✅ **CORRECT:**
```yaml
entity_id: light.leo_s_bedroom_lights  # Exact match
entity_id: input_number.motion_threshold  # Exact match
```

❌ **WRONG:**
```yaml
entity_id: light.leo_s_bedroom_light    # Missing 's' at end
entity_id: light.leos_bedroom_lights    # Wrong apostrophe format
entity_id: input_number.motion_threshhold  # Typo: "threshhold" vs "threshold"
```

### Rule 3: All Referenced Entities Must Exist

❌ **UNDEFINED ENTITY:**
```yaml
entity_id: light.bedroom_lights_that_dont_exist  # ❌ Not in system
```

---

## Validation Process

### Step 1: Extract All Entity References

**Search for:** All `entity_id:` mentions in automations

```bash
# Find all entity_id references
grep -rn "entity_id:" packages/rooms/ | \
  grep -oE "[a-z_]+\.[a-z_0-9_]+" | \
  sort | uniq
```

**What to Extract:**
- Entity domain (light, switch, input_boolean, sensor, etc.)
- Entity name
- File path and line number
- Context (action/condition/trigger)

**Example:**
```
File: packages/rooms/kitchen/kitchen.yaml:52
  action: light.turn_on
  target:
    entity_id: light.kitchen_table_white

File: packages/rooms/kitchen/kitchen.yaml:68
  condition: numeric_state
  entity_id: light.kitchen_cooker_white
```

---

### Step 2: Extract Home Assistant Entity Registry

**Get list of valid entities:**

```bash
# From Home Assistant (via Developer Tools → States)
# Or from automations, scripts, and helper definitions

# Example entities in system:
light.kitchen_table_white
light.kitchen_cooker_white
light.kitchen_ambient
input_boolean.enable_kitchen_motion_triggers
input_number.kitchen_light_level_threshold
sensor.kitchen_motion_illuminance
```

**Document all entities by domain:**
- light.* (lighting devices)
- switch.* (switches)
- input_boolean.* (boolean helpers)
- input_number.* (numeric helpers)
- input_datetime.* (datetime helpers)
- input_select.* (select helpers)
- sensor.* (sensors)
- binary_sensor.* (binary sensors)
- cover.* (covers/blinds)
- group.* (device groups)

---

### Step 3: Validate Domain Matching

**For Each Action in YAML:**

Check if action domain matches target entity domain:

```python
# Pseudo-code for validation

for action in automations:
    action_service = action.service  # e.g., "light.turn_on"
    action_domain = action_service.split('.')[0]  # e.g., "light"

    for target in action.targets:
        entity_id = target.entity_id  # e.g., "light.kitchen_table"
        entity_domain = entity_id.split('.')[0]  # e.g., "light"

        if action_domain != entity_domain:
            print(f"❌ DOMAIN MISMATCH: {action_service} → {entity_id}")
            # Flag as CRITICAL error
```

**Example Error Detection:**
```yaml
# Line 52 in kitchen.yaml
- action: light.turn_on
  target:
    entity_id: input_boolean.enable_kitchen_lights

# ❌ CRITICAL ERROR:
# Action domain: light
# Entity domain: input_boolean
# Mismatch: light.turn_on cannot control input_boolean entities
```

---

### Step 4: Validate Entity Existence

**For Each Entity Reference:**

1. **Extract entity_id:** `light.kitchen_table_white`
2. **Check if exists in registry:** `grep "light.kitchen_table_white"`
3. **Flag if not found:** 🔴 CRITICAL - Undefined entity

**Example:**
```bash
# Entity referenced: light.bedroom_lights_that_dont_exist
grep -r "light.bedroom_lights_that_dont_exist" /home/homeassistant/.homeassistant/

# Output: (no matches)
# ❌ CRITICAL ERROR - Entity does not exist
```

---

### Step 5: Detect Name Typos & Inconsistencies

**Common Typo Patterns:**

1. **Wrong spelling:**
   ```
   Expected: light.leo_s_bedroom_lights
   Found:    light.leo_s_bedroom_light    ❌ Missing 's'
   ```

2. **Apostrophe format:**
   ```
   Expected: input_boolean.enable_leo_s_circadian_lighting
   Found:    input_boolean.enable_leos_circadian_lighting    ❌ Missing underscore+s
   ```

3. **Common misspellings:**
   ```
   threshold vs threshhold
   motion vs motin
   brightness vs brightnes
   ```

**Detection Method:**
```bash
# Find similar names (Levenshtein distance)
# Use fuzzy matching to find likely typos

# Example: Search for variations of entity name
grep -r "brightness\|brightnes" packages/rooms/
# Find any variations (even typo'd ones)
```

---

### Step 6: Generate Validation Report

**Output Format:**

```markdown
# Entity Reference Validation Report

## Summary
- Total entities referenced: 245
- Valid references: 240
- Domain mismatches: 3
- Undefined entities: 2
- Typos detected: 2

## Critical Issues (Must Fix)

### Domain Mismatch Errors (3)
1. File: kitchen/kitchen.yaml:52
   ❌ light.turn_on targeting input_boolean.enable_kitchen_lights

2. File: bedroom2/sleep_as_android.yaml:33
   ❌ light.turn_on targeting input_boolean.enable_leo_s_circadian_lighting

3. File: bedroom2/sleep_as_android.yaml:37
   ❌ light.turn_on targeting input_boolean.enable_leos_circadian_lighting

### Undefined Entities (2)
1. File: kitchen/kitchen.yaml:102
   ❌ sensor.kitchen_motion_ltr390_brightness (should be: light.kitchen_motion_illuminance)

2. File: office/office.yaml:45
   ❌ switch.office_fan_that_does_not_exist

### Typos Detected (2)
1. File: bedroom2/sleep_as_android.yaml:33
   ⚠️ input_boolean.enable_leo_s_circadian_lighting (missing apostrophe?)
   Similar entities:
     - input_boolean.enable_leos_circadian_lighting (close match)

2. File: kitchen/kitchen.yaml:88
   ⚠️ input_number.motion_threshhold (likely typo)
   Similar entities:
     - input_number.motion_threshold (close match)

## Validation Complete
Status: ❌ 7 issues found (3 CRITICAL, 2 MEDIUM, 2 LOW)
```

---

## Quality Checklist

### Before Committing
- [ ] All `light.turn_on` actions target only `light.*` entities
- [ ] All `switch.turn_on` actions target only `switch.*` entities
- [ ] All `input_boolean.turn_on` actions target only `input_boolean.*` entities
- [ ] All `sensor.*` conditions target only `sensor.*` entities
- [ ] All entity names match expected format (underscores, apostrophes)
- [ ] No undefined entity references
- [ ] No typos in entity names

### During Consolidation
- [ ] All entity references in consolidated automation are valid
- [ ] No domain mismatches introduced by consolidation
- [ ] Entity names unchanged (unless intentional)

### After Consolidation
- [ ] All consolidated automation entity references validated
- [ ] No new undefined entities introduced
- [ ] Validation report shows zero critical issues

---

## Common Errors & How to Detect

### Error 1: Action Domain Mismatch

**Pattern:**
```yaml
- action: light.turn_on
  target:
    entity_id: input_boolean.*  # ❌ Wrong domain
```

**Detection:**
```bash
# Find all light.turn_on actions targeting non-light entities
grep -A 2 "action: light.turn_on" packages/rooms/ | \
  grep "entity_id:" | \
  grep -v "light\."
```

**Example in codebase (from reflection):**
- kitchen.yaml: `light.turn_on` targeting `input_boolean.enable_kitchen_lights`
- bedroom2.yaml: 6 occurrences of same error

---

### Error 2: Undefined Entities

**Pattern:**
```yaml
entity_id: light.entity_that_does_not_exist
```

**Detection:**
```bash
# Extract entity_id
ENTITY="light.bedroom_lights_that_dont_exist"

# Check if exists anywhere in system
grep -r "$ENTITY" packages/
# If no matches: ❌ UNDEFINED

# Check in automation traces
# If automation runs but no action on entity: ❌ UNDEFINED
```

---

### Error 3: Entity Name Typos

**Pattern:**
```yaml
# Expected name
entity_id: input_boolean.enable_leo_s_circadian_lighting

# Actual typo
entity_id: input_boolean.enable_leos_circadian_lighting  # Missing underscore before 's'
```

**Detection:**
```bash
# Find similar entity names (Levenshtein distance < 3)
# Use fuzzy string matching

FOUND="enable_leos_circadian_lighting"
EXPECTED="enable_leo_s_circadian_lighting"

# These are 1 character different (missing underscore)
# Flag for manual review
```

**Example from reflection:**
- bedroom2.yaml line 37: `enable_leos_circadian_lighting` (should be `enable_leo_s_circadian_lighting`)

---

## Usage Examples

### Example 1: Validate Kitchen Package

**Task:** Check kitchen.yaml for entity reference errors

```bash
# Step 1: Extract all entity references
grep -rn "entity_id:" packages/rooms/kitchen/kitchen.yaml

# Step 2: For each entity, check:
# A) Domain matches action domain
# B) Entity exists in registry
# C) Name spelled correctly

# Step 3: Report findings
# ✅ All light.turn_on actions target light.* entities
# ✅ All input_boolean.turn_on actions target input_boolean.* entities
# ❌ CRITICAL: Found 2 domain mismatches (light.turn_on targeting input_boolean)
```

### Example 2: Detect Domain Mismatch

**Task:** Find `light.turn_on` actions targeting wrong entity domains

```bash
# Step 1: Find all light.turn_on actions
grep -B 1 "entity_id:" packages/rooms/kitchen/kitchen.yaml | \
  grep -B 1 "light\." | head -20

# Step 2: Extract entity targets
# light.kitchen_table_white ✅ (light.* - correct)
# light.kitchen_cooker_white ✅ (light.* - correct)
# input_boolean.enable_kitchen_lights ❌ (input_boolean.* - WRONG!)

# Step 3: Flag mismatch
# ❌ CRITICAL: kitchen.yaml:68
#    light.turn_on targeting input_boolean.enable_kitchen_lights
```

### Example 3: Find Typos in Entity Names

**Task:** Detect misspelled entity names

```bash
# Step 1: Find similar entity names
# Looking for: input_boolean.enable_leo_s_circadian_lighting
# Found in code: input_boolean.enable_leos_circadian_lighting

# Step 2: Fuzzy match comparison
# Difference: 1 character (missing underscore before 's')
# Likelihood: 99% typo

# Step 3: Check if correct name exists
grep -r "enable_leo_s_circadian_lighting" packages/
# Result: Found 5 other uses with correct spelling

# Step 4: Flag as error
# ⚠️ MEDIUM: bedroom2.yaml:37
#    Entity name typo: enable_leos_circadian_lighting
#    Should be: enable_leo_s_circadian_lighting
```

---

## Pre-Commit Validation Script

**Add to git pre-commit hook:**

```bash
#!/bin/bash
# Validate entity references before commit

echo "Validating entity references..."

# Array of valid entity domains
VALID_DOMAINS=("light" "switch" "input_boolean" "input_number" "sensor" "binary_sensor" "cover" "group")

# Check for domain mismatches
MISMATCHES=$(grep -rn "action: light\.turn_on\|action: light\.turn_off" packages/rooms/ | \
  grep -v "light\." | wc -l)

if [ $MISMATCHES -gt 0 ]; then
    echo "❌ CRITICAL: Found $MISMATCHES domain mismatch errors"
    grep -rn "action: light\.turn_on" packages/rooms/ | \
      grep -v "light\." | head -5
    exit 1
fi

# Check for undefined entities
UNDEFINED=$(grep -rn "entity_id:" packages/rooms/ | \
  grep -oE "[a-z_]+\.[a-z_0-9_]+" | \
  while read entity; do
    if ! grep -q "$entity" packages/ 2>/dev/null; then
      echo "$entity"
    fi
  done | wc -l)

if [ $UNDEFINED -gt 0 ]; then
    echo "⚠️ WARNING: Found $UNDEFINED potentially undefined entities"
fi

echo "✅ Entity reference validation complete"
exit 0
```

---

## Integration with Other Skills

### With ha-yaml-quality-reviewer.md
- Add CRITICAL check: Entity domain matches action domain
- Add CRITICAL check: Entity exists in registry
- Flag undefined entities

### With ha-motion-consolidator.md
- Validate all entity references in consolidated automation
- Check domain matching for all new actions
- Verify entity names unchanged in consolidation

### With ha-consolidation-analyzer.md
- Check entity references before scoring consolidation
- Flag consolidations with undefined entities as blockers

### With ha-automation-id-manager.md
- Cross-check with automation validator
- Ensure entity references don't cause circular dependencies

---

## Troubleshooting

### Problem: "Found domain mismatch - light.turn_on targeting input_boolean"

**Solution:**
```bash
# Step 1: Find the wrong reference
grep -rn "light\.turn_on" packages/rooms/ | \
  grep -A 2 "entity_id:" | \
  grep "input_boolean"

# Step 2: Identify the correct entity
# Find correct light entity that should be targeted
grep -r "light\." packages/rooms/ | grep "table"
# Result: light.kitchen_table_white

# Step 3: Update the reference
# Change: entity_id: input_boolean.enable_kitchen_lights
# To: entity_id: light.kitchen_table_white

# Step 4: Verify fix
grep -n "light\.turn_on" packages/rooms/kitchen/kitchen.yaml
```

### Problem: "Entity name has typo - enable_leos vs enable_leo_s"

**Solution:**
```bash
# Step 1: Confirm correct spelling
grep -r "enable_leo_s_circadian" packages/
# Result: Found 5 uses with underscore before 's'

# Step 2: Find typo'd version
grep -r "enable_leos_circadian" packages/
# Result: Found 1 use without underscore

# Step 3: Fix typo
# Change: input_boolean.enable_leos_circadian_lighting
# To: input_boolean.enable_leo_s_circadian_lighting

# Step 4: Verify
grep -r "enable_leos_circadian" packages/
# Result: (no matches - fixed)
```

### Problem: "Undefined entity reference"

**Solution:**
```bash
# Step 1: Identify undefined entity
# Entity not found: light.bedroom_lights_that_dont_exist

# Step 2: Find similar valid entities
grep -r "bedroom.*lights" packages/ | grep "entity_id:"
# Results:
# - light.leo_s_bedroom_lights
# - light.leo_s_bedroom_lights_rgb

# Step 3: Determine correct entity
# Choose appropriate entity based on context

# Step 4: Update reference
# Change: entity_id: light.bedroom_lights_that_dont_exist
# To: entity_id: light.leo_s_bedroom_lights

# Step 5: Verify
grep -n "leo_s_bedroom_lights" packages/rooms/bedroom/
```

---

## Success Criteria

✅ All action domains match target entity domains
✅ No light.turn_on targeting non-light entities
✅ No switch.turn_on targeting non-switch entities
✅ All entity_id references exist in system
✅ No typos in entity names (exact matches)
✅ All references use correct apostrophe/underscore format
✅ Pre-commit validation passes

---

## Key Learnings

**From reflection analysis (2026-01-24):**
- Entity domain mismatch is 40% of recent errors
- 6 occurrences of light.turn_on targeting input_boolean
- Entity name typos like missing apostrophes are common
- Copy-paste errors propagate domain mismatches

**Prevention:**
- Always validate domain matching before consolidation
- Check entity existence before using in actions
- Verify entity names match registry exactly
- Use fuzzy matching to catch typos

---

## Next Steps

1. **Apply to current codebase:**
   - Run validation on all 11 room packages
   - Fix all domain mismatches (6+ expected)
   - Fix all typos and inconsistencies

2. **Integrate into workflow:**
   - Add to pre-commit hooks
   - Run before every commit
   - Flag issues before deployment

3. **Generate baseline report:**
   - Document all entity references
   - Current state before fixes
   - Track improvements

---

**Usage:** Invoke when validating entity references or before committing automation changes
**Team:** Danny's Home Assistant optimization
**Created:** 2026-01-24
**Status:** Production Ready

---

## Quick Reference

**Domain Matching Rules:**
```
light.turn_on → light.* ONLY
light.turn_off → light.* ONLY
switch.turn_on → switch.* ONLY
switch.turn_off → switch.* ONLY
input_boolean.turn_on → input_boolean.* ONLY
sensor.* → sensor.* ONLY
```

**Common Mistakes:**
- `light.turn_on` targeting `input_boolean.*` ❌
- `switch.turn_on` targeting `light.*` ❌
- `light.bedroom_lights_that_dont_exist` ❌ (undefined)
- `enable_leos_circadian` ❌ (should be `enable_leo_s_circadian`)

**Validation Command:**
```bash
# Find all domain mismatches
grep -rn "action: light.turn_on" packages/rooms/ | \
  grep -A 2 "entity_id:" | \
  grep -v "entity_id: light\." | head -20
# Should return: (empty - no mismatches)
```
