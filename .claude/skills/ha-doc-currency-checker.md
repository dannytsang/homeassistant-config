# Claude Utility: Home Assistant Documentation Currency Checker

**Status:** Production Ready
**Version:** 1.0
**Created:** 2026-01-25
**Purpose:** Validate that reference documentation is current before running validation checks

---

## Purpose

Prevent stale documentation from invalidating validation results. When validators run, they check if the reference docs are within an acceptable age threshold. If docs are too old, the validator alerts the user to refresh them first.

---

## How It Works

### What Gets Checked

Every time a validator runs (ha-yaml-quality-reviewer, ha-entity-reference-validator, ha-package-review), this checker:

1. **Reads metadata** from reference files (`.claude/home-assistant-*.md`)
2. **Calculates age** (current date - Date field from file)
3. **Compares against threshold** (default: 30 days, can vary by validator)
4. **Reports status** at start of validation

### Metadata Locations

Each reference file has a `**Date:**` field in the header:

```markdown
# Home Assistant Automation YAML Reference

**Source:** https://www.home-assistant.io/docs/automation/yaml/
**Date:** 2026-01-22
**Purpose:** Comprehensive guide to writing automations in YAML format
```

The date format is `YYYY-MM-DD`.

---

## Implementation for Validators

### For Each Validator Using Documentation

Add this check section at the **START** of the validation report:

```markdown
## ⚠️ Documentation Currency Check

**Reference Files Status:**
| File | Age | Status |
|------|-----|--------|
| home-assistant-automation-yaml-reference.md | 3 days | ✅ Current |
| home-assistant-templating-reference.md | 3 days | ✅ Current |

**Result:** Documentation is current (0-30 days old). Validation results are based on HA as of 2026-01-25.

---

## Validation Results
[rest of validation report]
```

### If Documentation is Stale

```markdown
## ⚠️ Documentation Currency Check

**Reference Files Status:**
| File | Age | Status |
|------|-----|--------|
| home-assistant-automation-yaml-reference.md | 35 days | ⚠️ STALE |
| home-assistant-templating-reference.md | 35 days | ⚠️ STALE |

**⚠️ WARNING:** Documentation is 35 days old. HA releases monthly (typically 1st Wed/Thu).

**Recommendation:** Before proceeding with this validation, refresh documentation:
```bash
/ha-docs
```

This will check for any new features, syntax changes, or deprecations that might affect validation results.

---

## Validation Results
[rest of validation report]
```

---

## Threshold Guidelines

### Recommended Age Thresholds

| Validator | Threshold | Reason |
|-----------|-----------|--------|
| ha-yaml-quality-reviewer | 30 days | Automation syntax changes frequently |
| ha-entity-reference-validator | 45 days | Entity types less volatile |
| ha-package-review | 30 days | Best practices update with syntax |
| ha-consolidation-analyzer | 30 days | Patterns rely on current features |

**Rationale:** Home Assistant releases monthly (1st Wed/Thu). After 30 days, there's likely a new feature release.

---

## How to Check Documentation Age

### Automated Check (Simple Approach)

When running a validator, include this check:

```python
# Pseudocode for Claude to follow

## Check documentation currency

Get current date: 2026-01-25

Read files:
- .claude/home-assistant-automation-yaml-reference.md → Date: 2026-01-22 → Age: 3 days ✅
- .claude/home-assistant-scripts-reference.md → Date: 2026-01-22 → Age: 3 days ✅
- .claude/home-assistant-templating-reference.md → Date: 2026-01-22 → Age: 3 days ✅
- .claude/home-assistant-splitting-configuration-reference.md → Date: 2026-01-22 → Age: 3 days ✅
- .claude/home-assistant-template-sensors-reference.md → Date: 2026-01-25 → Age: 0 days ✅

Result: All documentation current (max age: 3 days)
Recommendation: Proceed with validation
```

### Manual Check (User Reference)

Users can check documentation age by reading:
- `.claude/documentation-update-log.md` (lists all files with ages)

Or by running:
- `/ha-docs` (will show current cache status)

---

## Integration Points

### Validators That Should Include Doc Currency Check

1. **ha-yaml-quality-reviewer.md**
   - Checks automation/script syntax
   - Needs: automation, scripts, templating docs current
   - Threshold: 30 days

2. **ha-entity-reference-validator.md**
   - Validates entity_id references
   - Needs: automation, template-sensors docs current
   - Threshold: 45 days

3. **ha-package-review.md**
   - Reviews automation structure and patterns
   - Needs: all reference docs current
   - Threshold: 30 days

4. **ha-consolidation-analyzer.md**
   - Recommends consolidation opportunities
   - Needs: automation, scripts, templating docs current
   - Threshold: 30 days

---

## Workflow Example

### User Runs Validator

```
User: "Review the kitchen automations"

Claude:
[Load validator skill]

## ⚠️ Documentation Currency Check

Checking reference file ages...
- home-assistant-automation-yaml-reference.md: 40 days old ⚠️ STALE
- home-assistant-scripts-reference.md: 40 days old ⚠️ STALE
- home-assistant-templating-reference.md: 40 days old ⚠️ STALE

**⚠️ WARNING:** Reference docs are 40 days old. HA may have released new features.

**Recommendation:** Refresh documentation before proceeding:
/ha-docs

Then run review again for most current results.

---

Proceed anyway? [Y/N]
```

### User Refreshes Docs and Retries

```
User: "/ha-docs"

Claude: [Fetches latest documentation, updates cache]

Documentation updated successfully.

User: "Review the kitchen automations"

Claude:
[Load validator skill]

## ⚠️ Documentation Currency Check

Checking reference file ages...
- home-assistant-automation-yaml-reference.md: 0 days old ✅ FRESH
- home-assistant-scripts-reference.md: 0 days old ✅ FRESH
- home-assistant-templating-reference.md: 0 days old ✅ FRESH

All documentation current. Proceeding with validation...

---

## Validation Results

[Validator runs with current docs]
```

---

## FAQ

### Q: What if I ignore the warning and proceed anyway?

**A:** You can proceed, but validation results may miss new features or syntax that was added after your docs were updated. The validator will still work, but may not catch all issues.

### Q: How do I update docs?

**A:** Run `/ha-docs` skill. It will:
1. Check current cache age
2. Fetch latest docs from home-assistant.io
3. Update local reference files
4. Report what changed
5. Update documentation-update-log.md

### Q: How often do I need to update?

**A:**
- **Monthly:** After HA releases (1st Wed/Thu of month)
- **Before major work:** Before validating large automation changes
- **When in doubt:** Run `/ha-docs` to check status

### Q: Can I automate this check?

**A:**
- **Manual reminder:** This utility alerts you when docs are stale
- **Task #2 (Phase 2):** An automated agent could check docs on a schedule
- **For now:** Include doc check in your pre-validation workflow

### Q: What if the reference docs are missing?

**A:** If a reference file is not found:
```
⚠️ WARNING: home-assistant-automation-yaml-reference.md not found

This validator requires current reference documentation.

Action: Run /ha-docs to create reference cache
```

---

## Implementation Status

### Phase 1 (Current)

- ✅ Doc currency checking logic defined
- ✅ Threshold guidelines established
- ✅ Integration points identified
- ⏳ **IN PROGRESS:** Adding checks to each validator

### Phase 2 (Future - Task #2)

- ⏳ Automated scheduled checks
- ⏳ Email/notification alerts for stale docs
- ⏳ Auto-refresh on schedule

---

## Related Documentation

- **Documentation Updater Skill:** `.claude/skills/ha-documentation-updater.md`
- **Update Log:** `.claude/documentation-update-log.md`
- **Validators Using This Utility:**
  - `.claude/skills/ha-yaml-quality-reviewer.md`
  - `.claude/skills/ha-entity-reference-validator.md`
  - `.claude/skills/ha-package-review.md`
  - `.claude/skills/ha-consolidation-analyzer.md`

---

**Utility Created:** 2026-01-25
**Status:** Ready for Integration
**Next Step:** Update each validator to include doc currency checks
