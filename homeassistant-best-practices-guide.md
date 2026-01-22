# Home Assistant Best Practices & Development Guide

**Last Updated:** 2026-01-22
**Scope:** Development Workflow, Code Review, Testing, Maintenance

---

## Development Workflow

### 1. Making Changes

- Edit YAML files directly
- Use YAML validator before committing
- Check configuration: Developer Tools → Check Configuration
- Reload specific domains when possible (avoid full restart)

### 2. Testing Automations

- Use "Run Actions" in automation editor
- Check Home Log for debug messages
- Test all conditions and branches
- Verify helper entity states

### 3. Git Workflow

```bash
git status
git add [files]
git commit -m "Description"
git push
```

The Git Pull addon automatically syncs changes.

#### Commit Message Format

Use clear, descriptive commit messages following this structure:

```
<Subject line - imperative mood, ~50 chars>

<Body - what changed and why>
- Bullet points for multiple changes
- Include context and rationale
- Reference line numbers for specific fixes

<Footer>
Related: GitHub issue #XXX (if applicable)
Closes: #XXX (if issue is completed)
```

**Example:**
```
Fix critical issues in office package

- Fixed duplicate automation aliases (lines 587 & 627)
  - Renamed to "Partially Close Office Blinds At Sunset" (closes to 25%)
  - Renamed to "Fully Close Office Blinds At Night" (closes fully 1hr after)
- Fixed timer duration message mismatch
  - Corrected "2 minutes" to "1 minute" for timer duration
  - Updated total to "3 minutes (2 min detection + 1 min timer)"
- Fixed incorrect brightness message operator
  - Changed < to > to match "bright" condition in log message

Related: #172
```

#### GitHub Issue Workflow

**When Issue Complete:** Use `Closes: #XXX` (fully done) or `Related: #XXX` (partial) in commit. Add `testing` label with `gh issue edit <#> --add-label "testing"`. Remains open until user verifies.

**Labels:** `testing` (awaiting verification), `bug` (issue), `enhancement` (feature), `blocked` (external dependency)

**Example Workflow:**
```bash
# After implementing feature
git add packages/integrations/energy/energy.yaml
git commit -m "Add battery depletion notification

Partially completes issue #113

- Implementation details...

Related: #113"

# Tag issue for testing
gh issue edit 113 --add-label "testing"

# User tests and closes issue when verified
```

#### Testing Before Pushing

Always create a testing checklist before pushing changes:
1. Critical functionality affected
2. Automation traces to verify
3. Log messages to check
4. Edge cases to consider

Test locally before pushing to main branch.

### 4. ESPHome Updates
- Edit device YAML in `esphome/` directory
- Validate configuration
- OTA update to device
- Monitor logs for issues

### 5. Rollback Strategy
- Git history for reverting changes
- Snapshot before major changes
- Test in non-critical automations first

### 6. Deferred Work Tracking

**Decision Matrix:**
- **Fix immediately:** Critical bugs (logic/syntax errors), security issues, runtime failures, blocking issues
- **Defer (create GitHub issue):** Low-priority improvements, large refactors, pattern fixes affecting multiple files, optimizations not affecting functionality

**Workflow:**
1. Create issue with `gh issue create --title "..." --body "..." --label enhancement`
2. Document full scope with specific line numbers
3. Reference in documentation for future work

---

## Code Review Process

### Incremental Fixes Over Large Refactors

- Fix critical bugs first, one at a time
- Show changes/diffs before applying edits
- Allow user to provide input before each change
- Commit after each logical group of fixes
- Test before proceeding with more changes

### Defer Complex Refactors

- Use GitHub issues to track deferred work
- Document rationale and proposed approach
- Let user review and test critical fixes before major refactors
- Examples: Motion detection consolidation, blind management centralization

### Edit Approval Process

- Show diffs for changes > 20 lines; brief explanation for smaller fixes
- Allow user opportunity to provide context before applying

---

## Testing & Validation

| Phase | Action | Purpose |
|-------|--------|---------|
| **Pre-Deploy** | YAML validate | Catch syntax errors |
| **Pre-Deploy** | Check Configuration | Verify entity refs |
| **Pre-Deploy** | Test automation manually | Verify logic works |
| **Pre-Deploy** | Test edge cases | Handle unavailable sensors |
| **Debugging** | Check automation traces | Verify condition flow |
| **Debugging** | Review Home Log | Check messages |
| **Debugging** | Verify entity states | Monitor changes |
| **Debugging** | Test templates | Check conditions |

### Manual Testing Checklist

**Before deploying changes:**
1. ✅ YAML syntax is valid (no parsing errors)
2. ✅ All entity IDs referenced exist and are available
3. ✅ Automation conditions make logical sense
4. ✅ Run Actions works without errors
5. ✅ Home Log shows expected messages
6. ✅ Check Helper entity states are correct
7. ✅ Test edge cases (unavailable sensors, boundary values)
8. ✅ Verify no regressions in related automations

---

## Common Tasks

### Task 1: Add a New Motion-Based Lighting Automation

1. **Create automation ID** (13-digit random)
2. **Validate ID uniqueness** via Grep
3. **Create automation with:**
   - Trigger: `state` on motion sensor to "on"
   - Conditions: `input_boolean.enable_*_motion_triggers` + illuminance check
   - Actions: parallel (logging + light turn on + timer cancel)
4. **Test:** Run Actions → check Home Log → verify lights turn on
5. **Commit:** Reference motion pattern from this guide

**Reference:** See `homeassistant-automation-patterns.md` for Motion-Based Lighting example

### Task 2: Consolidate Multiple Automations Using Trigger IDs

1. **Identify automations** that control same domain/room
2. **Create single automation** with multiple triggers using `id:` field
3. **Use `choose:` block** with `condition: trigger id:` for branching
4. **Add descriptive aliases** for each branch
5. **Verify automation traces** show correct branch execution
6. **Commit:** Include before/after line counts

**Reference:** See `homeassistant-automation-patterns.md` for Trigger ID Branching Pattern

### Task 3: Add Cost-Based Appliance Automation

1. **Get current rate entity:** `sensor.octopus_energy_electricity_current_rate`
2. **Create automation that:**
   - Triggers periodically (time_pattern every 30 minutes)
   - Conditions: rate ≤ 0 (free electricity) + other conditions
   - Actions: turn on appliance + log
3. **Test:** Monitor rates to catch a free window
4. **Commit:** Reference rate-aware pattern

**Reference:** See `homeassistant-energy-management.md` for Rate-Based Patterns

### Task 4: Modify Existing Automation

1. **Locate automation** in appropriate room or integration package
2. **Review current logic** and test current behavior
3. **Make minimal changes** needed for requested modification
4. **Test edge cases** related to change
5. **Check automation traces** for unexpected branches
6. **Commit:** Describe what changed and why

### Task 5: Debug Non-Firing Automation

1. **Check automation enabled** in Automations UI
2. **Verify helper entities** (input_boolean, input_number) exist and correct state
3. **Check automation traces** - what triggered, which conditions failed
4. **Test templates** in Developer Tools → Template
5. **Verify entity IDs** - check for typos or unavailable entities
6. **Check entity states** in Developer Tools → States
7. **Enable Home Log** for additional diagnostic messages

---

## Performance Considerations

### Optimization Guidelines

- **Recorder exclusions** - Exclude high-frequency, low-value entities
- **Parallel automations** - Use `parallel:` for independent actions to save time
- **Template complexity** - Avoid heavy Jinja2 loops in frequently-triggered automations
- **External services** - Use MQTT/Grafana external to reduce HA server load
- **Entity groups** - Use groups for efficient multi-entity operations

### High-Frequency Exclusions

```yaml
recorder:
  exclude:
    entity_globs:
      - sensor.time*
      - sensor.*_wifi_signal*
      - sensor.*_uptime
      - sensor.*_rssi
      - binary_sensor.*_status
      - media_player.*_volume_level
```

---

## Security Considerations

### Safe Template Practices

- Always use `| default()` filter for potentially unavailable entities
- Never assume entities will always be available
- Use `not in ['unavailable', 'unknown']` for state checks
- Validate external input before using in templates

### Script Parameters

- Always define `fields:` with descriptions for script parameters
- Use `selector:` to guide input types
- Validate parameters in script code (especially string inputs)

### Secrets Management

- All sensitive values in `secrets.yaml` (gitignored)
- Use `!secret` syntax in YAML files
- Never commit actual passwords/API keys to git
- Rotate secrets regularly

### Automation Permissions

- Use `input_boolean` gates to enable/disable automations
- Implement "Naughty Step Mode" for parental controls
- Log all security-critical actions (lock, alarm, etc.)

---

## File Maintenance

### Regular Maintenance Tasks

1. **Monthly:**
   - Review Home Log for error patterns
   - Check failed automations in automation editor
   - Verify helper entity values are reasonable

2. **Quarterly:**
   - Review and update threshold values (brightness, temperature)
   - Check for obsolete entities in retired automations
   - Update documentation if major features changed

3. **Annually:**
   - Review energy optimization effectiveness
   - Audit security automations (alarm, locks)
   - Consider refactoring opportunities

### Cleanup of Obsolete Entities

When removing automations or helpers:
1. Comment out in YAML first (test that nothing depends on it)
2. Check Home Log and automation traces for references
3. After confirming no dependencies, delete completely
4. Commit with clear message about what was removed and why

### Documentation Updates

- Update `claude.md` when major features added/removed
- Add comments in YAML for complex logic
- Link to reference documents when adding new patterns
- Keep commit messages detailed for git history documentation

---

## Common Issues & Resolutions

### Issue: Automation Won't Fire
**Check:**
1. Is automation enabled? (Automations UI → toggle)
2. Is trigger entity available? (Developer Tools → States)
3. Do all conditions pass? (Automation → Traces tab)
4. Did you reload automations after YAML edit? (Settings → System → Automations)

### Issue: Wrong Action Executed
**Check:**
1. Are `choose:` branches in correct priority order?
2. Are conditions mutually exclusive or overlapping?
3. Check automation traces to see which branch executed
4. Test individual conditions in template editor

### Issue: Entity Unavailable
**Solution:**
1. Add `| default()` filter to templates
2. Use `condition: template value_template: "{{ entity is defined }}"`
3. Check entity integration status (Settings → Devices & Services)
4. Restart integration or device

### Issue: Automation Too Slow
**Solution:**
1. Move independent actions to `parallel:` block
2. Remove unnecessary logging for frequently-triggered automations
3. Simplify template logic
4. Use timer pattern instead of frequent triggers

---

## Quick Reference: Approved Patterns

### ✅ Preferred Patterns
- **Consolidation:** Use trigger IDs + choose branches instead of multiple automations
- **Logging:** Always parallel (logging + primary action together)
- **Helpers:** Keep helpers in UI for easier adjustment
- **Scene transitions:** Use `transition: 1` for smooth changes
- **Timers:** Cancel when condition reverses

### ❌ Anti-Patterns to Avoid
- Creating room-specific versions of generic scripts (parametrize instead)
- Using `condition: service:` (use `action: domain.service` instead)
- Hardcoding values (use `input_number` for thresholds)
- Complex nested if/then when choose block would be clearer
- Ignoring helper entity enable/disable toggles

---

## Reference Documentation

For detailed information about specific topics:
- **Scripts:** `home-assistant-scripts-reference.md`
- **Templating:** `home-assistant-templating-reference.md`
- **Configuration Splitting:** `home-assistant-splitting-configuration-reference.md`
- **Automation YAML:** `home-assistant-automation-yaml-reference.md`
- **Automation Patterns:** `homeassistant-automation-patterns.md`
- **System Overview:** `homeassistant-system-overview.md`
- **Energy Management:** `homeassistant-energy-management.md`
- **Home Systems:** `homeassistant-home-systems.md`
- **Notifications:** `homeassistant-notification-patterns.md`
- **Technical Implementation:** `homeassistant-technical-implementation.md`

---

## Getting Help

**Step 1:** Check the relevant reference documentation
**Step 2:** Search Home Assistant forums for similar issues
**Step 3:** Check automation traces to understand execution flow
**Step 4:** Test templates in Developer Tools
**Step 5:** Ask in Home Assistant Discord community

**For Configuration Help:**
- Automation patterns → `homeassistant-automation-patterns.md`
- Script creation → `home-assistant-scripts-reference.md`
- Template issues → `home-assistant-templating-reference.md`
- Organization → `home-assistant-splitting-configuration-reference.md`
