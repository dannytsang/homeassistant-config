# Home Assistant Package Review Skill

## Description
Reviews Home Assistant YAML package files for common issues, bugs, and improvement opportunities based on established patterns in this repository.

## Usage
```
/ha-package-review <package-file-path>
```

or

```
review the <room> package
```

---

## ⚠️ Documentation Currency Check

**Before running this review, confirm reference documentation is current:**

**Required Reference Files:**
- `home-assistant-automation-yaml-reference.md` - Automation syntax
- `home-assistant-scripts-reference.md` - Script patterns
- `home-assistant-templating-reference.md` - Template syntax
- `home-assistant-splitting-configuration-reference.md` - Package organization

**Threshold:** 30 days

**How to Check:**
1. Read `.claude/documentation-update-log.md` for current ages
2. If any file is >30 days old, run `/ha-docs` to refresh
3. Then proceed with this package review

**If Documentation is Stale:**
```
⚠️ WARNING: Reference documentation is X days old
→ Recommendation: Run /ha-docs before proceeding
→ Reason: New syntax, features, or patterns may have been introduced
```

**Why This Matters:**
- Package reviews depend on knowledge of current HA syntax
- New features may enable better package organization
- Deprecated patterns need to be caught and updated
- Best practices evolve with each HA release

---

## Instructions

You are a Home Assistant configuration expert reviewing YAML packages for issues and improvements.

### Phase 1: Initial Scan

1. **Read the package file** specified by the user
2. **Gather statistics:**
   - Total lines
   - Number of automations
   - Number of scripts
   - Number of scenes
   - Number of helper entities defined
3. **Quick scan for critical issues:**
   - Duplicate automation IDs or aliases (search for repeated `id:` or `alias:` values)
   - Obvious syntax errors
   - Deprecated syntax (`service:` instead of `action:`, `trigger:` instead of `triggers:`)

### Phase 2: Deep Logic Review

Review each automation for:

**Critical Issues:**
- [ ] **Duplicate automation IDs/aliases** - Search for repeated values
- [ ] **Logic errors:**
  - Wrong operators (< vs >, == vs !=)
  - Mismatched messages (e.g., message says "2 minutes" but timer is "00:01:00")
  - Incorrect condition logic
- [ ] **Missing notification handlers:**
  - If automation sends actionable notification (action: `script.send_actionable_notification_*`)
  - Verify handler automation exists for the action name
- [ ] **Cascading logic order:**
  - In `choose:` blocks with multiple temperature/brightness thresholds
  - Verify highest priority conditions come first (first match wins)
  - Check: Time/presence → Highest threshold → Medium threshold → Lowest threshold
- [ ] **Unsafe attribute access:**
  - Check for brightness/attribute checks without handling `unavailable` state
  - Look for missing `| int(0)` or `| float(0)` defaults

**Medium Priority Issues:**
- [ ] **Duplicate logic** across multiple automations
- [ ] **Complex nested conditions** that could use variables
- [ ] **Large file size** (1000+ lines - consider splitting)
- [ ] **Missing entity definitions** (referenced but not defined)
- [ ] **Repeated patterns** that could be centralized in scripts

**Low Priority:**
- [ ] File organization
- [ ] Naming consistency
- [ ] Missing comments
- [ ] Documentation

### Phase 3: Known Valid Patterns Check

Before flagging as bugs, verify these are NOT issues:
- `- and:` / `- or:` / `- not:` shorthand (valid syntax)
- Emoji shortcodes like `:office:`, `:hourglass_flowing_sand:` (intentional)
- Multiple triggers with different thresholds (temperature cascading pattern)
- Scripts without explicit `mode:` (defaults to `single`)

### Phase 4: Generate Report

Create a structured report with:

1. **Executive Summary:**
   - Overall assessment (X/10)
   - File statistics
   - Quick wins identified

2. **Critical Issues (Fix Immediately):**
   - List each with line number and description
   - Show current code snippet
   - Provide fix recommendation

3. **Medium Priority Issues:**
   - Consolidation opportunities with estimated line savings
   - Refactoring suggestions

4. **Low Priority Issues:**
   - Nice-to-have improvements

5. **Action Items:**
   - Prioritized list (High/Medium/Low)
   - Estimated effort for each

### Phase 5: Implementation Approach

After presenting the report, ask user preference:
- **Fix critical issues immediately** (one at a time, with commits)
- **Create GitHub issues** for deferred work
- **Skip and move on**

**When fixing issues:**
1. Fix **one issue at a time**
2. Show proposed change before applying
3. Allow user to provide additional context
4. Commit after each logical fix with clear message
5. Create GitHub issues for deferred refactors

## Commit Message Template

When committing fixes, use this format:

```
Fix <category> in <package> package

- Fixed <issue 1> (line X)
  - Context/rationale
- Fixed <issue 2> (lines Y-Z)
  - Context/rationale

Related: GitHub issue #XXX (if applicable)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Example Workflow

```markdown
User: review the office package
Claude: I'll review the office package for issues.

[Reads packages/rooms/office/office.yaml]

**Office Package Review Report**

File: packages/rooms/office/office.yaml
Lines: 1629
Automations: 42
Scripts: 3
Assessment: 6/10 - Functional but needs refactoring

**Critical Issues Found:**
1. Duplicate automation aliases (lines 587, 627)
2. Timer message mismatch (line 257 says "2 min", actually 1 min)
3. Wrong operator in log message (line 117: < should be >)

**Medium Priority:**
1. Motion detection split into 2 automations (~230 lines duplicate logic)
2. Blind management (10 automations, repeated sun logic)
3. Temperature cascading logic needs reordering

Would you like me to:
A) Fix critical issues immediately
B) Create GitHub issues for deferred work
C) Skip and move on

User: fix them one by one

Claude: I'll fix the issues one by one, starting with the duplicate aliases...

[Proceeds with Phase 5 implementation approach]
```

## User Preferences

**Entity Management:**
- Keep helper entities (input_boolean, input_number, timer) in UI, NOT YAML
- Only add to YAML if explicitly requested for version control

**Code Changes:**
- Show proposed changes before applying
- Give user chance to provide additional context
- Keep emoji shortcodes (don't replace with Unicode)
- Use `- and:` shorthand (valid syntax)

**Commit Strategy:**
- One logical fix per commit
- Test after critical fixes before continuing
- Defer large refactors to GitHub issues

## Reference Patterns

### Temperature Cascading (Correct Order)
```yaml
choose:
  # Priority 1: Time/presence (if specified)
  - conditions: [time + people conditions]
    sequence: [auto action]
  # Priority 2: Highest threshold (emergency)
  - conditions: [temp > 31]
    sequence: [force on]
  # Priority 3: Medium threshold (notify)
  - conditions: [temp > 29]
    sequence: [notification]
```

### Safe Attribute Check
```yaml
light_brightness: "{{ state_attr('light.office', 'brightness') | int(0) }}"
sensor_available: "{{ states('sensor.temp') not in ['unavailable', 'unknown'] }}"
```

### Actionable Notification Handler Pattern
```yaml
# Sending notification
- action: script.send_actionable_notification
  data:
    action1_name: some_action_name

# Required handler automation
- alias: "Handle: Some Action Name"
  triggers:
    - trigger: event
      event_type: mobile_app_notification_action
      event_data:
        action: "some_action_name"
  actions:
    - [handle the action]
```

## Success Criteria

**Good Review:**
- Identifies all critical bugs
- Prioritizes issues correctly
- Provides specific line numbers
- Shows code snippets
- Offers actionable fixes
- Follows user preferences
- One fix at a time with commits

**Great Review:**
- Additionally identifies consolidation opportunities
- Estimates line savings from refactors
- Provides before/after examples
- Creates GitHub issues for deferred work
- Maintains test-first approach

