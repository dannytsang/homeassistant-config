# Claude Skill: Home Assistant YAML Quality Reviewer

**Status:** Skill Design Document
**Version:** 1.0
**Based On:** Phase 5 Quality Assurance (2026-01-23)

---

## Purpose

Systematically review Home Assistant YAML packages for syntax errors, logic issues, and quality problems using severity-based prioritization.

## When to Use

- After creating or modifying automation packages
- Before committing configuration changes
- Regular quality audits of existing packages
- After major refactoring or consolidation

## Issue Classification Framework

### 🔴 CRITICAL (Blocking)
**Definition:** Errors that prevent automation from working or create logic failures
**Examples:**
- Invalid YAML syntax (missing colons, wrong indentation)
- Undefined script/template/sensor references
- Required parameters missing (title, message, etc.)
- Wrong data types (unquoted strings, mixed formats)
- Invalid emoji or shortcodes

**Action:** Fix immediately, blocking deployment

### 🟡 MEDIUM (Impacts Functionality)
**Definition:** Issues that affect functionality or user experience but don't block execution
**Examples:**
- Missing optional parameters (log_level)
- Inconsistent formatting or spacing
- Copy-paste errors (wrong entity IDs, duplicated aliases)
- Confusing/unclear messages
- Missing spaces in templated messages

**Action:** Fix before deployment, can be deferred temporarily

### 🟢 LOW (Cosmetic)
**Definition:** Code quality issues with no functional impact
**Examples:**
- Inconsistent emoji usage (some rooms use :code: others use Unicode)
- Spelling/grammar in messages
- Inconsistent title formatting
- Redundant comments

**Action:** Fix when convenient, can defer indefinitely

## Review Checklist

### CRITICAL Checks
- [ ] All YAML syntax valid (proper indentation, colons, quotes)
- [ ] **Condition objects use `alias:` ONLY** (never `description:` - unsupported syntax)
- [ ] **`response_variable:` (singular) syntax correct** - template string, NOT mapping
- [ ] **Action domain matches target entity domain** (light.turn_on → light.*, not input_boolean.*)
- [ ] **Strings starting with emoji/special chars are quoted**
- [ ] All script calls have required `title:` field
- [ ] All template sensors/input helpers defined
- [ ] All entity IDs exist in system and match expected domain
- [ ] Emoji codes are valid (not `:invalid_code:`)
- [ ] log_level values quoted ("Debug", "Normal")
- [ ] String values properly quoted when needed
- [ ] No circular dependencies in scripts

### MEDIUM Checks
- [ ] All send_to_home_log calls have title + log_level
- [ ] Scenes referenced in automation actually exist
- [ ] Spacing consistent in multi-line messages
- [ ] Copy-paste errors caught (duplicate titles, wrong IDs)
- [ ] Message formatting clear and helpful

### LOW Checks
- [ ] Consistent emoji usage (Unicode vs :codes:)
- [ ] Consistent title formatting (emoji + text)
- [ ] Grammar/spelling in messages
- [ ] Comments are up-to-date
- [ ] Consistent indentation (2 vs 4 spaces)

## Review Process

### Step 1: Identify Files to Review
```
Scope: All .yaml files in packages/rooms/
Count: 11 remaining room packages
```

### Step 2: Scan for Critical Issues
```
Search for:
- :[a-z_]+: (invalid emoji codes)
- Missing title fields
- Unquoted values (log_level: Debug vs "Debug")
- Missing quotes around titles
- Undefined entity references
```

### Step 3: Document Issues by File
```
For each file:
- List line numbers
- Categorize by severity
- Provide fix examples
```

### Step 4: Create Fix Commits
```
Commit structure:
1. All CRITICAL fixes
2. All MEDIUM fixes
3. All LOW fixes
(Separate commits by severity)
```

## Real-world Example: Phase 5 Results

**Files Reviewed:** 11 room packages
**Issues Found:** 26 total
**Breakdown:**
- 🔴 CRITICAL: 9 (emoji codes, quotes, syntax)
- 🟡 MEDIUM: 11 (missing fields, spacing, formatting)
- 🟢 LOW: 6 (cosmetic inconsistencies)

**Fixes Applied:**
- ✅ Invalid emoji codes replaced (`:ladder:` → 🪜, `:zzz:` → 😴)
- ✅ Missing title fields added
- ✅ Quotes added to unquoted values
- ✅ Spacing fixed in templated messages

## Common Issues Reference

### Syntax Constraint Errors
**Issue:** Invalid `description:` on condition alias
```yaml
# WRONG: Condition objects don't support description parameter
- alias: "Motion detected"
  description: "This condition checks motion"  # INVALID
  conditions:
    - condition: state

# CORRECT: Use alias only
- alias: "Motion detected - bright room"
  conditions:
    - condition: state
```

**Issue:** Wrong `response_variable` syntax in scripts
```yaml
# WRONG: Plural with mapping
response_variables:
  clock_result: "{{ response.emoji }}"

# WRONG: Singular with mapping
response_variable:
  clock_result: "{{ response.emoji }}"

# CORRECT: Singular with template string
response_variable: "{{ response.emoji }}"
```

**Issue:** Entity domain mismatch
```yaml
# WRONG: light.turn_on targeting input_boolean
- action: light.turn_on
  target:
    entity_id: input_boolean.some_bool

# CORRECT: Match action domain with entity domain
- action: light.turn_on
  target:
    entity_id: light.some_light
```

**Issue:** Unquoted string starting with emoji
```yaml
# WRONG: Unquoted emoji string
message: 🚷 Turning off Magic Mirror

# CORRECT: Quoted emoji string
message: "🚷 Turning off Magic Mirror"
```

### Emoji Code Errors
| Invalid | Correct | Reason |
|---------|---------|--------|
| `:ladder:` | 🪜 | Not standard emoji code |
| `:zzz:` | 😴 | Invalid format |
| `:robot_face:` | 🤖 | Incorrect syntax |
| `:sunny:` | ☀️ | Not valid shortcode |
| `:knife_fork_plate:` | 🍽️ | Invalid code |
| `:mirror:` | 🪞 | Not standard code |

**Pattern:** Home Assistant uses Unicode emojis, not :emoji_code: format

### Parameter Issues
```yaml
# WRONG: Missing title
- action: script.send_to_home_log
  data:
    message: "Motion detected"
    log_level: "Debug"

# CORRECT: Title added
- action: script.send_to_home_log
  data:
    message: "Motion detected"
    title: "🛋️ Living Room"
    log_level: "Debug"
```

### Quote Consistency
```yaml
# INCONSISTENT
data:
  log_level: Debug
  title: "Room"
  message: "Text"

# CONSISTENT
data:
  log_level: "Debug"
  title: "Room"
  message: "Text"
```

## Automation & Detection

### Future Enhancement: Automated Scanning
```
Patterns to detect programmatically:
1. :[a-z_]+: (emoji codes)
2. Missing title: in send_to_home_log
3. Unquoted Debug/Normal log levels
4. Undefined entity_id references
5. Duplicate automation aliases
6. description: on condition objects (INVALID - use alias: instead)
7. response_variables: (plural) in scripts (should be response_variable: singular)
8. Entity domain mismatch (light.turn_on → input_boolean.*)
9. Unquoted strings starting with emoji/special chars
10. Entity name inconsistencies (typos, wrong entity names)
```

### Suggested Tools
- Regex patterns for emoji code detection
- AST parsing for YAML structure validation
- Entity reference cross-checking
- Automation alias uniqueness validation
- **NEW:** Condition object parameter validation (alias vs description)
- **NEW:** Script response_variable syntax checker
- **NEW:** Action/entity domain matcher (validates light.turn_on targets light.*)
- **NEW:** Emoji string quote checker

## Output Format

### Review Report Template
```markdown
## filename.yaml
**Lines:** X
**Issues:** N total (C critical, M medium, L low)

### CRITICAL ISSUES
- Line X: Issue description + fix example

### MEDIUM ISSUES
- Line X: Issue description

### LOW ISSUES
- Line X: Issue description

### Summary
Total fixes: N | Estimated time: X min
```

## Quality Gates

**Before Deployment:**
- ✅ 0 CRITICAL issues
- ✅ 0 MEDIUM issues (unless explicitly deferred)
- ✅ YAML validation passes
- ✅ All entity references valid

**Before Merge:**
- ✅ All CRITICAL issues fixed
- ✅ At least 80% of MEDIUM issues fixed
- ✅ Code review approved

## Limitations & Notes

- ⚠️ Cannot detect logic errors (wrong conditions)
- ⚠️ Cannot verify scene definitions completeness
- ⚠️ Cannot check runtime behavior
- ⚠️ Requires manual testing after fixes

## Integration with Workflow

```
Review → Report → Fix (by severity) → Validate → Commit → Test
```

## Next Steps

1. Create automated issue detection script
2. Integrate into pre-commit hooks
3. Build remediation suggestions
4. Document most common issues for team
5. Create style guide based on common patterns

---

**Usage:** Invoke for systematic quality review of Home Assistant packages
**Team:** Danny's Home Assistant optimization
**Last Updated:** 2026-01-23
