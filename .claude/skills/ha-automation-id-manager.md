# Claude Skill: Home Assistant Automation ID Manager

**Status:** Production Ready
**Version:** 1.0
**Created:** 2026-01-24
**Based On:** Kitchen consolidation correction (commit 71982199)

---

## Purpose

Validate, assign, and manage 13-digit numeric automation IDs with uniqueness checks and conflict detection. Prevents semantic ID naming errors and ensures all automation IDs meet Home Assistant requirements.

---

## When to Use

- **Before consolidation work** - Assign proper IDs to newly created consolidated automations
- **After creating new automations** - Validate IDs are correctly formatted
- **When modifying automation IDs** - Check for conflicts before committing
- **In pre-commit validation** - Catch ID errors before they block automations
- **During package merges** - Detect ID conflicts from different branches

---

## Critical Rules

### Home Assistant Automation ID Requirements

✅ **MUST:** 13-digit numeric string
```yaml
# CORRECT
- id: "1606158191303"
  alias: "Kitchen: Motion Detected - Lights"
```

❌ **MUST NOT:** Semantic/alphabetic names
```yaml
# WRONG
- id: "kitchen_motion_lights_on"
  alias: "Kitchen: Motion Detected - Lights"

# WRONG
- id: "motion_lights"

# WRONG
- id: "1606158191303_kitchen"
```

❌ **MUST NOT:** Duplicate IDs across packages
❌ **MUST NOT:** Non-numeric characters (dashes, underscores, letters)

---

## Validation Process

### Step 1: Extract All Automation IDs

**Search for:** All `id:` fields in automation blocks

```bash
# Find all automation IDs in packages
grep -r "id: \"" packages/rooms/ | grep -v "#" | sort
```

**What to Extract:**
- File path
- Line number
- Current ID value
- Automation alias (for context)

**Example:**
```
packages/rooms/kitchen/kitchen.yaml:25: id: "1606158191303"
packages/rooms/stairs/stairs.yaml:15: id: "kitchen_motion_lights_on"  ⚠️
```

---

### Step 2: Validate ID Format

**For Each ID Found:**

1. **Check if 13-digit numeric string**
   ```bash
   # Valid pattern: exactly 13 digits, no other characters
   grep -E 'id: "[0-9]{13}"$'
   ```

2. **Flag violations:**
   - ❌ Contains letters: `id: "kitchen_motion_lights_on"`
   - ❌ Contains dashes/underscores: `id: "1606158191303_v2"`
   - ❌ Too short/long: `id: "160615819"` or `id: "16061581913031"`
   - ❌ Not quoted: `id: 1606158191303`
   - ❌ Contains special chars: `id: "160615-819-1303"`

**Mark as:** 🔴 **CRITICAL ERROR** - Will block automation loading

---

### Step 3: Check for Duplicates

**Process:**
1. Extract all IDs from all packages
2. Check for duplicates: `sort | uniq -d`
3. For each duplicate found:
   - List all files using that ID
   - Flag as CRITICAL error
   - Require manual resolution

**Example:**
```
DUPLICATE ID: 1606428361967
  Used in: packages/rooms/office/office.yaml:47
  Used in: packages/rooms/living_room/living_room.yaml:152
  ⚠️ CONFLICT - Must use different ID
```

---

### Step 4: Validate Uniqueness Across System

**Check Against:**
- All room packages (packages/rooms/*/*)
- Shared automations (if any)
- Template automations
- Any other automation files

**Output:** Full inventory of all automation IDs with uniqueness verification

---

## ID Assignment Process

### For NEW Consolidated Automations:

**Step 1: Determine New ID Needed**
```
Count current automations in file
Identify consolidation count (how many being merged)
Determine: Need N new IDs
```

**Step 2: Generate Candidate IDs**

Use these strategies (in order of preference):

**Strategy 1: Use Existing ID from Original**
```yaml
# If consolidating these automations:
- id: "1606428361967"  ← Use this for consolidated version
  alias: "Motion Detected - Lights On"

- id: "1587044886896"  ← Being consolidated (remove)
  alias: "Table Lights On"

- id: "1587044886897"  ← Being consolidated (remove)
  alias: "Cooker Lights On"
```

**Strategy 2: Generate New 13-Digit ID**
- Use current timestamp: `date +%s%3N` = 13 digits
- Example: `1606158191303` (seconds + milliseconds)

**Strategy 3: Use ID from Deleted Automation**
- When consolidating 5 automations → 1
- Use ID from first/main automation
- Assign new IDs to any new automations created

**Step 3: Verify Generated ID**
```bash
# Check if ID already exists
grep -r "id: \"NEWID\"" packages/rooms/
# Should return: (no matches)
```

**Step 4: Document ID Assignment**
```yaml
# CONSOLIDATED FROM (Phase 4.2):
# Original automations with their old IDs:
# - id: "1606428361967" - Motion Detected Table Lights
# - id: "1587044886896" - Motion Detected Cooker Lights
# - id: "1587044886897" - Motion Detected Ambient Lights
#
# New consolidated automation:
- id: "1606158191303"
  alias: "Kitchen: Motion Detected - Lights"
```

---

## Quality Checklist

### Before Consolidation
- [ ] All original automation IDs are 13-digit numeric
- [ ] No duplicate IDs across packages
- [ ] Current ID inventory documented

### During Consolidation
- [ ] New consolidated automation assigned 13-digit numeric ID
- [ ] ID does not conflict with existing IDs
- [ ] ID verified with `grep -r "id: \"XXXX\"" packages/`
- [ ] Original automation IDs being removed are documented

### After Consolidation
- [ ] New ID exists and is correctly formatted
- [ ] No duplicate IDs created
- [ ] All original IDs removed (if consolidating into single automation)
- [ ] Commit message documents ID changes
- [ ] YAML validation passes (HA config check)

---

## Common Mistakes & How to Avoid

### Mistake 1: Using Semantic Names
```yaml
# WRONG - Semantic name instead of numeric
- id: "kitchen_motion_lights_on"

# CORRECT - Use numeric ID
- id: "1606158191303"

# Prevention: Check that ID contains ONLY digits
```

### Mistake 2: Duplicate IDs
```yaml
# File 1
- id: "1606158191303"
  alias: "Kitchen Motion"

# File 2 (copy-paste error)
- id: "1606158191303"  ⚠️ DUPLICATE
  alias: "Office Motion"

# Prevention: Run `grep -r "id: \"1606158191303\""` before committing
```

### Mistake 3: Non-13-Digit IDs
```yaml
# WRONG - Too short
- id: "160615819"

# WRONG - Too long
- id: "16061581913031"

# WRONG - Contains non-digits
- id: "1606158191303_v2"

# Prevention: Validate format with regex: `^[0-9]{13}$`
```

### Mistake 4: Not Quoted
```yaml
# WRONG - Unquoted number
- id: 1606158191303

# CORRECT - Quoted string
- id: "1606158191303"

# Prevention: Always use quotes in YAML
```

### Mistake 5: Using Deleted ID
```yaml
# If consolidating and deleting original automation:
- id: "1606428361967"  # Being deleted
  alias: "Old Motion On"

# New consolidated automation - MUST use NEW ID:
- id: "1606158191303"  # NEW - not the old one
  alias: "Motion Detected - All Lights"

# Prevention: Generate new ID, don't reuse deleted ones
```

---

## Usage Examples

### Example 1: Validate Existing Package

**Task:** Check kitchen.yaml for ID issues

```bash
# Step 1: Extract IDs
grep "id: \"" packages/rooms/kitchen/kitchen.yaml

# Expected output:
# id: "1583797341647"
# id: "1606158191303"
# id: "1606158191304"
# id: "1606428361967"

# Step 2: Validate format (all 13 digits, numeric)
# ✅ All valid

# Step 3: Check for duplicates across system
grep -r "id: \"1583797341647\"" packages/rooms/

# Expected output: Only in kitchen.yaml
# ✅ No duplicates

# Status: ✅ PASS - All IDs valid
```

### Example 2: Consolidation with ID Assignment

**Task:** Consolidate 5 motion automations into 1, assign proper ID

```yaml
# Original automations (being consolidated):
- id: "1606428361967"
  alias: "Motion Detected Table Lights On"

- id: "1587044886896"
  alias: "Motion Detected Table Lights Off"

- id: "1587044886897"
  alias: "Motion Detected Cooker Lights On"

- id: "1606428361968"
  alias: "Motion Detected Cooker Lights Off"

- id: "1606428361969"
  alias: "Motion Detected Ambient Lights"

# New consolidated automation:
# ID chosen: Use first automation's ID (1606428361967)
- id: "1606428361967"
  alias: "Kitchen: Motion Detected - Lights"
  triggers: [...]
  conditions: [...]
  actions: [...]

# Deleted automations:
# - id: "1587044886896"
# - id: "1587044886897"
# - id: "1606428361968"
# - id: "1606428361969"

# Validation:
# ✅ New ID: 1606428361967 (13 digits, numeric)
# ✅ No conflicts: grep -r "id: \"1606428361967\"" → only in kitchen.yaml
# ✅ Old IDs removed: All 4 deleted
# ✅ Ready to commit
```

### Example 3: Detect & Fix ID Conflicts

**Task:** Found duplicate ID when merging branches

```
Branch A created:
  - id: "1606158191303"
    alias: "Kitchen Motion"

Branch B created:
  - id: "1606158191303"  ⚠️ Same ID!
    alias: "Office Motion"

Resolution:

Step 1: Identify conflict
✅ Found duplicate: "1606158191303" in both kitchen.yaml and office.yaml

Step 2: Assign new ID to one automation
  Option A: Keep kitchen.yaml as is, assign new ID to office.yaml
  Option B: Keep office.yaml as is, assign new ID to kitchen.yaml

Step 3: Generate new ID for office.yaml
  Current timestamp: 1706079600123 = "1706079600123" (13 digits)

Step 4: Update office.yaml
  - id: "1706079600123"  # NEW - no longer duplicates
    alias: "Office Motion"

Step 5: Verify
  ✅ grep -r "id: \"1606158191303\"" → only kitchen.yaml
  ✅ grep -r "id: \"1706079600123\"" → only office.yaml

Status: ✅ Conflict resolved
```

---

## Pre-Commit Validation Script

**Add to git pre-commit hook:**

```bash
#!/bin/bash
# Validate automation IDs before commit

echo "Validating automation IDs..."

# Find all automation IDs
IDS=$(grep -rh "id: \"" packages/rooms/ | grep -oE '"[0-9a-z_-]+"' | sort)

# Check for non-numeric IDs
INVALID=$(echo "$IDS" | grep -v '^"[0-9]\{13\}"$')
if [ -n "$INVALID" ]; then
    echo "❌ CRITICAL: Found invalid automation ID format:"
    echo "$INVALID"
    exit 1
fi

# Check for duplicates
DUPES=$(echo "$IDS" | uniq -d)
if [ -n "$DUPES" ]; then
    echo "❌ CRITICAL: Found duplicate automation IDs:"
    echo "$DUPES"
    exit 1
fi

echo "✅ All automation IDs valid"
exit 0
```

---

## Integration with Other Skills

### With ha-motion-consolidator.md
- **Step 6:** "Assign Automation ID"
- Use this skill to validate new ID
- Verify no conflicts with existing IDs

### With ha-consolidation-analyzer.md
- **Scoring update:** Include ID format as part of readiness check
- Flag automations with invalid IDs as blocking consolidation

### With ha-yaml-quality-reviewer.md
- **CRITICAL check:** All automation IDs are 13-digit numeric
- Flag any non-numeric IDs
- Check for duplicates across files being reviewed

### With pre-commit validation
- Run ID format check before every commit
- Block commits with invalid IDs
- Generate ID conflict warnings

---

## Troubleshooting

### Problem: "Duplicate ID found across packages"

**Solution:**
```bash
# 1. Find which files have the duplicate
grep -rn "id: \"1606158191303\"" packages/rooms/

# 2. Decide which automation keeps the ID
# 3. Generate new ID for the other automation
# 4. Update one of the files

# 5. Verify fix
grep -rn "id: \"1606158191303\"" packages/rooms/
# Should now show only 1 file
```

### Problem: "Automation uses semantic name instead of numeric ID"

**Solution:**
```bash
# Current (WRONG)
- id: "kitchen_motion_lights_on"

# Fix 1: Use timestamp-based ID
- id: "1706079600123"

# Fix 2: Use existing automation ID from consolidation
- id: "1606428361967"

# Verify
grep -E 'id: "kitchen_motion' packages/rooms/
# Should return: (no matches)
```

### Problem: "ID is not 13 digits"

**Solution:**
```bash
# Current (WRONG - 10 digits)
- id: "1606158191"

# Current (WRONG - 15 digits)
- id: "160615819131303"

# Fix: Use 13-digit format
- id: "1606158191303"

# Verify with wc
echo "1606158191303" | wc -c
# Should show: 14 (13 digits + newline)
```

---

## Success Criteria

✅ All automation IDs are 13-digit numeric strings
✅ No semantic names (no letters, dashes, underscores)
✅ No duplicate IDs across any packages
✅ All IDs properly quoted in YAML
✅ Pre-commit validation passes
✅ All consolidations use new numeric IDs

---

## Key Learnings

**From kitchen correction (2026-01-24):**
- Consolidation process creates new automations that need IDs
- Semantic names are intuitive but violate Home Assistant requirements
- Missing post-consolidation ID validation step
- Single ID error can block entire automation loading

**Prevention:**
- Always assign 13-digit numeric ID to consolidated automations
- Validate ID format before committing
- Check for conflicts with existing IDs
- Document ID changes in commit message

---

## Next Steps

1. **Update ha-motion-consolidator.md:**
   - Add Step 6: "Assign Automation ID with validation"
   - Reference this skill
   - Require 13-digit numeric ID

2. **Add to pre-commit hooks:**
   - Validate ID format before any commit
   - Check for duplicate IDs across packages
   - Block commits with invalid IDs

3. **Audit existing automations:**
   - Find any semantic IDs (should be zero)
   - Fix before consolidation work begins

---

**Usage:** Invoke when assigning IDs to new automations or consolidations
**Team:** Danny's Home Assistant optimization
**Created:** 2026-01-24
**Status:** Production Ready

---

## Quick Reference

**13-Digit Numeric ID Format:**
```
1606158191303  ✅ CORRECT
```

**Common Mistakes:**
- `kitchen_motion_lights_on` ❌ (semantic name)
- `160615819` ❌ (too short)
- `16061581913031` ❌ (too long)
- `1606158191303_v2` ❌ (contains non-digits)
- `1606158191303` (unquoted) ❌ Must be `"1606158191303"`

**Validation Command:**
```bash
grep -rh "id: \"" packages/rooms/ | \
  grep -v "id: \"[0-9]\{13\}\"" | \
  head -20
# Should return: (empty - no invalid IDs)
```
