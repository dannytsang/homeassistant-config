# Claude Skill: Home Assistant Documentation Updater

**Status:** Production Ready
**Version:** 1.0
**Created:** 2026-01-25
**Purpose:** Fetch latest Home Assistant documentation and keep local reference cache current

---

## Purpose

Fetch the latest Home Assistant documentation from official sources, update local reference files, maintain an audit trail of changes, and report what's new or deprecated. Ensures the team always works with current HA features and syntax.

---

## When to Use

- **Manual documentation refresh** - Run `/ha-docs` to update reference cache
- **Quarterly reviews** - Keep documentation aligned with HA releases
- **Before major automation work** - Refresh docs to catch new features
- **When HA version is updated** - Ensure docs match installed version
- **Team documentation maintenance** - Centralized source of truth
- **Pre-planning automation design** - Understand latest HA capabilities

---

## How This Skill Works

### Three Core Responsibilities

**1. Check Current Cache Status**
- Examine each reference document's `Date:` field
- Calculate age (days since last update)
- Identify which docs are stale (>30 days recommended)
- Report overall cache health

**2. Fetch Latest Documentation**
- Web fetch from https://www.home-assistant.io/docs/
- Extract relevant content sections
- Convert HTML → Markdown if needed
- Preserve structure (headings, code blocks, tables)

**3. Update & Report**
- Update `.claude/` reference files with new content
- Update metadata headers (Date, Fetched timestamp)
- Create audit trail entry
- Report what changed (new features, deprecations, syntax changes)

---

## Process Overview

### Step 1: Status Check

Read current reference files and report cache status:

```
Checking local documentation cache...

home-assistant-automation-yaml-reference.md
  └─ Last updated: 2026-01-22 (3 days old)
  └─ Status: ✅ Recent (no update needed yet)

home-assistant-scripts-reference.md
  └─ Last updated: 2026-01-22 (3 days old)
  └─ Status: ✅ Recent

home-assistant-templating-reference.md
  └─ Last updated: 2026-01-22 (3 days old)
  └─ Status: ✅ Recent

home-assistant-splitting-configuration-reference.md
  └─ Last updated: 2026-01-22 (3 days old)
  └─ Status: ✅ Recent

Overall Cache Age: 3 days
Recommendation: Optional - docs are recent. Run /ha-docs if you want latest content.
```

### Step 2: Fetch Latest

If user confirms or cache is >30 days old:

```
Fetching latest documentation from home-assistant.io...

✅ Fetching: https://www.home-assistant.io/docs/automation/
   └─ Retrieved 8,247 lines of content
   └─ Found 14 major sections
   └─ New: "Await automations" (v2024.12+)

✅ Fetching: https://www.home-assistant.io/docs/scripts/
   └─ Retrieved 4,156 lines of content
   └─ Found 9 major sections
   └─ Deprecated: Old service format (replaced with action)

✅ Fetching: https://www.home-assistant.io/docs/configuration/templating/
   └─ Retrieved 6,892 lines of content
   └─ Found 12 major sections
   └─ New: "Template functions" section expanded

✅ Fetching: https://www.home-assistant.io/docs/configuration/splitting_configuration/
   └─ Retrieved 2,145 lines of content
   └─ Found 7 major sections
   └─ No changes detected
```

### Step 3: Update & Report

```
Updating local reference files...

✅ Updated: home-assistant-automation-yaml-reference.md
   └─ Previous: 36,497 bytes (2026-01-22)
   └─ Current: 38,291 bytes (2026-01-25)
   └─ Change: +1,794 bytes

✅ Updated: home-assistant-scripts-reference.md
   └─ Previous: 14,525 bytes (2026-01-22)
   └─ Current: 14,628 bytes (2026-01-25)
   └─ Change: +103 bytes

✅ Updated: home-assistant-templating-reference.md
   └─ Previous: 24,570 bytes (2026-01-22)
   └─ Current: 25,847 bytes (2026-01-25)
   └─ Change: +1,277 bytes

✅ Unchanged: home-assistant-splitting-configuration-reference.md
   └─ No changes detected

Documentation cache updated successfully!
```

### Step 4: Create Audit Trail

Log entry added to `.claude/documentation-update-log.md`:

```markdown
## 2026-01-25 13:45 UTC

**Updated by:** /ha-docs skill
**Docs Version:** Latest (HA 2024.12.x)

### Files Updated
- home-assistant-automation-yaml-reference.md (+1,794 bytes)
- home-assistant-scripts-reference.md (+103 bytes)
- home-assistant-templating-reference.md (+1,277 bytes)

### Changes Detected
- New "Await automations" section in Automation reference
- Scripts reference: Updated with action format (service deprecated)
- Templating: Expanded "Template functions" section
- Splitting: No changes

### New Features Found
1. **Await Automations** (v2024.12+)
   - Docs: https://www.home-assistant.io/docs/automation/await/
   - Use case: Complex async automation flows

### Deprecations Noted
1. **Old Service Format** (service: → action:)
   - Migration guide: https://www.home-assistant.io/docs/automation/service-calls/

### Action Items
- Team should review "Await automations" if using HA 2024.12+
- Update any legacy `service:` calls to `action:` format
```

---

## Reference Documentation Sources

### Official HA Documentation URLs

These are the authoritative sources for this skill:

1. **Automation YAML**
   - URL: https://www.home-assistant.io/docs/automation/
   - Section: Full automation syntax and patterns
   - File: `home-assistant-automation-yaml-reference.md`

2. **Scripts**
   - URL: https://www.home-assistant.io/docs/scripts/
   - Section: Script syntax, triggers, conditions, actions
   - File: `home-assistant-scripts-reference.md`

3. **Templating**
   - URL: https://www.home-assistant.io/docs/configuration/templating/
   - Section: Template syntax, filters, functions
   - File: `home-assistant-templating-reference.md`

4. **Configuration Splitting**
   - URL: https://www.home-assistant.io/docs/configuration/splitting_configuration/
   - Section: YAML splitting and organization patterns
   - File: `home-assistant-splitting-configuration-reference.md`

---

## Cache File Format

### Header Metadata

Each reference file includes a metadata header that tracks versioning:

```markdown
# Home Assistant Automation YAML Reference

**Source:** https://www.home-assistant.io/docs/automation/
**Date:** 2026-01-25
**Fetched:** 2026-01-25 13:45 UTC
**Last Verified:** 2026-01-25
**Purpose:** Comprehensive guide to writing automations in YAML format

---
```

**Fields Explained:**
- `Source:` URL of authoritative documentation
- `Date:` When this file was last updated (for age calculation)
- `Fetched:` Timestamp of last fetch (ISO 8601 format)
- `Last Verified:` Last time accuracy was confirmed
- `Purpose:` What this reference is used for

---

## Integration with Existing Skills

### When to Use Before Other Skills

**Recommended Workflow:**

```
1. /ha-docs (refresh documentation)
   └─ Ensures all reference files are current

2. ha-package-validator (validate YAML)
   └─ Validates against latest HA syntax

3. ha-code-optimizer (find improvements)
   └─ Suggests using latest HA features

4. ha-yaml-quality-reviewer (quality audit)
   └─ Checks against current standards

5. Commit changes
   └─ Reference updated docs in commit message
```

### Documentation Currency Check

Before running validators or optimization skills, check if docs need refresh:

```bash
# Check doc age
grep "^**Date:**" .claude/home-assistant-*.md

# If any are >30 days old:
/ha-docs

# Then proceed with validation/optimization
```

---

## Common Use Cases

### Use Case 1: Team Onboarding
```
New team member joining? Run /ha-docs first.
↓
Ensures everyone is learning from latest HA docs
↓
Reduces "feature doesn't exist" confusion
```

### Use Case 2: HA Version Update
```
Just updated Home Assistant to new version?
↓
/ha-docs
↓
See what changed, what's new, what's deprecated
↓
Audit existing automations for compatibility
```

### Use Case 3: Major Automation Work
```
Planning complex automation consolidation?
↓
/ha-docs (refresh docs)
↓
Review new features that might simplify logic
↓
Redesign using latest patterns
↓
Save lines of code, improve maintainability
```

### Use Case 4: Quarterly Maintenance
```
Every quarter: Mandatory documentation review
↓
/ha-docs
↓
ha-reflection-reviewer (analyze recent changes)
↓
Update skills based on latest HA capabilities
```

---

## Expected Outputs

### Report Format

```
Home Assistant Documentation Updater - Report
===============================================

RUN TIME: 2026-01-25 13:45 UTC
TRIGGER: Manual (/ha-docs command)
CACHE AGE: 3 days

CACHE STATUS
─────────────────────────────────────────────
automation.md:          3 days (2026-01-22)  ✅
scripts.md:             3 days (2026-01-22)  ✅
templating.md:          3 days (2026-01-22)  ✅
splitting.md:           3 days (2026-01-22)  ✅

FETCH RESULTS
─────────────────────────────────────────────
✅ Automation docs:      Updated (+1,794 bytes)
✅ Scripts docs:         Updated (+103 bytes)
✅ Templating docs:      Updated (+1,277 bytes)
✅ Splitting docs:       Unchanged

CHANGES DETECTED
─────────────────────────────────────────────
NEW FEATURES:
  • Await automations (v2024.12+)
  • Template function expansion

DEPRECATIONS:
  • Old service: format → use action: instead

AUDIT TRAIL
─────────────────────────────────────────────
✅ Logged to: .claude/documentation-update-log.md
✅ Audit entry created with timestamp
✅ Change summary recorded

NEXT STEPS
─────────────────────────────────────────────
1. Review "Await automations" if using HA 2024.12+
2. Update any legacy service: → action: calls
3. Consider using new features in future automations
4. Reference docs are ready for validation work

STATUS: ✅ Complete
```

---

## Audit Trail Log

The skill maintains `.claude/documentation-update-log.md` to track all updates:

```markdown
# Documentation Update Log

## 2026-01-25 13:45 UTC
- Triggered: Manual (/ha-docs command)
- Files updated: 3
- Bytes changed: +3,174
- New features found: 2
- Deprecations noted: 1

## 2026-01-22 (Initial)
- Created reference files
- Initial population from HA docs
- Baseline: 99,860 bytes total

---
```

---

## Tips & Best Practices

### Tip 1: Regular Refresh Cycle
```
Recommended Schedule:
- Monthly: Check age, refresh if >30 days
- Quarterly: Full refresh + team review
- On HA updates: Immediate refresh
```

### Tip 2: Integration with Commits
```
When updating docs and using them in changes:

git commit -m "Add motion consolidation automation

- Consolidated 3 motion automations using trigger ID branching
- Latest HA syntax validated against docs (2026-01-25)
- New await patterns reviewed for future use
- Ref: .claude/documentation-update-log.md (2026-01-25)
"
```

### Tip 3: Checking Specific Topics
```
After /ha-docs, grep for topics you care about:

# Check automation features
grep -A 5 "trigger:" .claude/home-assistant-automation-yaml-reference.md

# Check template functions
grep -A 2 "filter:" .claude/home-assistant-templating-reference.md

# Check script syntax
grep -A 3 "sequence:" .claude/home-assistant-scripts-reference.md
```

### Tip 4: Before Validation Work
```
Always check docs first:
1. /ha-docs (refresh if needed)
2. Review "New Features" section in audit log
3. Consider using latest features in validations
4. Reference updated docs in validation reports
```

---

## Technical Details

### Web Fetch Strategy

The skill uses WebFetch to:
1. Retrieve HTML from HA documentation pages
2. Extract main content area
3. Convert to markdown format
4. Preserve code blocks, tables, and structure
5. Clean up HTML artifacts

### Storage Location

All reference files stored in: `.claude/`

```
.claude/
├── home-assistant-automation-yaml-reference.md
├── home-assistant-scripts-reference.md
├── home-assistant-templating-reference.md
├── home-assistant-splitting-configuration-reference.md
├── documentation-update-log.md
└── skills/
    └── ha-documentation-updater.md (this file)
```

### Performance Characteristics

- **Fetch Time:** ~30-60 seconds (depends on page size)
- **Update Time:** ~5-10 seconds (file writes)
- **Report Time:** ~2-3 seconds (analysis)
- **Total:** ~45-75 seconds per run
- **Frequency:** No limit - can run as often as needed

---

## Prerequisites

- Write access to `.claude/` directory
- WebFetch capability
- ~5 MB free disk space (for documentation cache)
- Internet connection to fetch from home-assistant.io

---

## Error Handling

### If Fetch Fails

```
❌ Failed to fetch automation documentation
   └─ Error: Connection timeout
   └─ Action: Retry in 5 minutes or check internet connection
   └─ Fallback: Current docs remain unchanged
   └─ Impact: No update made this session
```

### If File Write Fails

```
❌ Failed to update home-assistant-automation-yaml-reference.md
   └─ Error: Permission denied
   └─ Action: Check file permissions, try again
   └─ Fallback: Fetch succeeded, write failed - no changes applied
   └─ Impact: Old docs remain current
```

### If Parse Fails

```
⚠️  Partial update: automation docs
   └─ Error: Could not parse section "Advanced patterns"
   └─ Action: Manual review recommended
   └─ Status: Core content updated, 1 section may be incomplete
```

---

## Rollout & Adoption

### Phase 1 (This Session)
- ✅ Create skill file
- ✅ Document methodology
- ✅ Add to skills/README.md
- ✅ Create audit trail file

### Phase 2 (Next Session)
- [ ] Test `/ha-docs` command
- [ ] Verify docs update correctly
- [ ] Check audit trail creation
- [ ] Gather team feedback

### Phase 3 (Optional)
- [ ] Add automatic daily check agent
- [ ] Integration with validators
- [ ] Slack/Discord notifications
- [ ] Weekly digest reports

---

## Maintenance & Support

### How to Request Updates

If reference docs feel incomplete or outdated:

```
1. Run /ha-docs to refresh
2. Check .claude/documentation-update-log.md for recent changes
3. Review what changed (new features, deprecated syntax)
4. Report any gaps in the updated docs
```

### How to Report Issues

If you find:
- Missing content in reference files
- Outdated information
- Syntax that's no longer valid
- New features not yet documented

→ Note it in your commit message and the team will review in next reflection session

---

## Success Metrics

✅ **When this skill is working well:**
- Team always has docs <7 days old
- /ha-docs command runs successfully
- Audit trail shows regular updates
- Validation errors decrease (using latest syntax)
- New HA features are discovered quickly
- Zero "feature doesn't exist" surprises

---

## Related Skills

- **ha-package-validator.md** - Validates against latest HA syntax
- **ha-code-optimizer.md** - Uses latest features for optimization
- **ha-yaml-quality-reviewer.md** - Quality checks with latest rules
- **ha-reflection-reviewer.md** - Analyzes change patterns

---

**Skill Created:** 2026-01-25
**Last Updated:** 2026-01-25
**Status:** Production Ready
**Model:** Haiku (for speed)
**Complexity:** Low (documentation fetch and update)
**Maintenance:** Low (automated via /ha-docs)

---

## Next Steps

1. Test `/ha-docs` command
2. Verify reference files update
3. Check audit trail creation
4. Add to team documentation
5. Consider Phase 2 (automatic agent checks)
