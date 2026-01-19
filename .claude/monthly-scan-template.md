# Monthly Scan Template

**Copy this file and fill it out during monthly scans**
**Rename to: `scan-reports/scan-[YYYY-MM-DD].md`**

---

# System Scan Report
**Date:** [YYYY-MM-DD]
**Scan Type:** Standard
**Duration:** [X] minutes
**Token Cost:** ~2,000 tokens
**Performed By:** Claude

---

## Summary

| Metric | Previous | Current | Delta | Status |
|--------|----------|---------|-------|--------|
| Total Automations | 434 | [COUNT] | [+/-X] | ✅ OK |
| Total Scripts | 43+ | [COUNT] | [+/-X] | ✅ OK |
| Total Scenes | 75+ | [COUNT] | [+/-X] | ✅ OK |
| Helper Entities | 20+ | [COUNT] | [+/-X] | ✅ OK |
| Issues Opened | [COUNT] | [COUNT] | [+/-X] | ✅ OK |
| Issues Closed | [COUNT] | [COUNT] | [+/-X] | ✅ OK |

**Overall Assessment:** [GREEN/YELLOW/RED]

---

## Phase 1: Scripts Audit

### Scripts Found
- Total count: [NUMBER]
- New scripts added:
  - [ ] `script_name` - Description
  - [ ] `script_name` - Description
- Removed scripts:
  - [ ] (none) or list here
- Renamed scripts:
  - [ ] (none) or list here

### Status
- [ ] ✅ Verified - counts match claude.md
- [ ] ⚠️ Discrepancies - [DESCRIBE]
- [ ] ❌ Issues - [DESCRIBE]

---

## Phase 2: Automation Verification

### Count Verification
- Total automations found: [NUMBER]
- Expected (from system-index.md): 434+
- Status:
  - [ ] ✅ Within range
  - [ ] ⚠️ Slightly different (+/- 5)
  - [ ] ❌ Significant change (>5)

### Distribution by Package
| Package | Count | Change | Notes |
|---------|-------|--------|-------|
| Living Room | 35 | [+/-] | |
| Bedroom | 20 | [+/-] | |
| Kitchen | 15 | [+/-] | |
| Office | 22 | [+/-] | |
| Alarm | 20 | [+/-] | |
| Other | 322 | [+/-] | |

### Large Files Check
- Files >1000 lines:
  - [ ] office.yaml (1,629 lines)
  - [ ] living_room.yaml (3,326 lines)
  - [ ] [other?]

---

## Phase 3: Pattern Discovery

### New Trigger Types Found
- [ ] No new types
- [ ] New types:
  - `[trigger_type]` - Used in: [PACKAGES]
  - `[trigger_type]` - Used in: [PACKAGES]

### Condition Type Distribution (Top 5)
1. `state` - ~[NUMBER] uses
2. `numeric_state` - ~[NUMBER] uses
3. `template` - ~[NUMBER] uses
4. `time` - ~[NUMBER] uses
5. `sun` - ~[NUMBER] uses

### Deprecated Syntax Check
- [ ] ✅ No `service:` found (good - should be `action:`)
- [ ] ✅ No deprecated `trigger:` (good - should be `triggers:`)
- [ ] ✅ No deprecated `condition:` at automation level
- [ ] ⚠️ Deprecated syntax found:
  - [DESCRIBE LOCATION]

### New Patterns Discovered
- [ ] None
- [ ] New patterns:
  - Pattern name: [DESCRIBE]
  - Files: [LIST]
  - Applicability: [High/Medium/Low reuse potential]

---

## Phase 4: Cross-Package Dependencies

### Messaging Package Calls
- Total calls to `send_to_home_log`: [COUNT] (expect: 500+)
- Total calls to `send_direct_notification`: [COUNT] (expect: 637+)
- Trend: [Increasing/Stable/Decreasing]
- Status:
  - [ ] ✅ Healthy
  - [ ] ⚠️ Unexpectedly low
  - [ ] ❌ Issue detected

### Energy Package Dependencies
- Packages importing energy sensors: [NUMBER]
- Files using `octopus_energy`: [COUNT]
- Files using `growatt`: [COUNT]
- Status:
  - [ ] ✅ Normal
  - [ ] ⚠️ Changes detected
  - [ ] ❌ Issues

### Circular Dependencies
- [ ] ✅ None detected (good)
- [ ] ⚠️ Potential issue: [DESCRIBE]
- [ ] ❌ Circular dependency found: [DESCRIBE]

### Inter-Package Calls
- New calls detected:
  - [ ] None
  - [ ] From [PACKAGE] to [PACKAGE]: [COUNT] calls
  - [ ] From [PACKAGE] to [PACKAGE]: [COUNT] calls

---

## Phase 5: Deferred Work Status

### Open GitHub Issues

| Issue # | Title | Status | Priority | Notes |
|---------|-------|--------|----------|-------|
| #176 | Unsafe brightness checks | Open | Low | 7 instances, deferred |
| #177 | Smart quiet hours | Testing | High | PR ready, awaiting approval |
| #178 | Notification acknowledgment | Planning | Medium | Implementation plan ready |
| #179 | Device-aware routing | Planning | Medium | 3 approaches documented |
| [#NEW] | [Title] | [Status] | [Priority] | [Notes] |

### Issues to Create
- [ ] None
- [ ] New issues identified:
  - [ ] [Issue description] - Priority: High/Medium/Low
  - [ ] [Issue description] - Priority: High/Medium/Low

### Recommendations
- Issue #176: [Should continue deferring/Ready to implement] because [REASON]
- Issue #178: [Should implement/Defer further] because [REASON]
- Issue #179: [Should implement/Defer further] because [REASON]

---

## Phase 6: Recent Changes

### Commits Since Last Scan
```
Total commits: [NUMBER]
Date range: [YYYY-MM-DD] to [YYYY-MM-DD]

Key changes:
- [Commit message/theme]
- [Commit message/theme]
- [Commit message/theme]
```

### PRs Merged
- [ ] None
- [ ] PR #[NUMBER]: [Title] - Merged [DATE]
- [ ] PR #[NUMBER]: [Title] - Merged [DATE]

### Issues Closed
- [ ] None
- [ ] Issue #[NUMBER]: [Title] - Closed [DATE]
- [ ] Issue #[NUMBER]: [Title] - Closed [DATE]

### Patterns Introduced
- [ ] None
- [ ] New patterns:
  - Pattern: [Name] - Files: [LIST]
  - Pattern: [Name] - Files: [LIST]

---

## Consolidation Opportunities (If Quarterly Scan)

### Single-Use Scripts Found
- [ ] None identified
- [ ] Scripts used in only one location:
  - `script_name` (location: packages/...yaml)
  - Recommendation: Consider consolidating into automation directly

### Duplicate Logic Patterns
- [ ] None
- [ ] Patterns found in multiple files:
  - Pattern: [DESCRIBE]
  - Files: [LIST]
  - Recommendation: [Centralize/Create shared script/No action]

### Recommended Consolidations
1. [HIGH PRIORITY] [DESCRIPTION] - Affects [#] files
2. [MEDIUM PRIORITY] [DESCRIPTION] - Affects [#] files
3. [LOW PRIORITY] [DESCRIPTION] - Affects [#] files

---

## Performance Analysis (If Quarterly Scan)

### Automation File Sizes
- office.yaml: 1,629 lines (consider splitting)
- living_room.yaml: 3,326 lines (consider splitting)
- [Other large files?]

### Complexity Check
- Automations with 10+ branches: [COUNT]
- Automations with 5-9 branches: [COUNT]
- Simple automations: [COUNT]

### Trigger Frequency
- `trigger: state` automations: [COUNT]
- `trigger: numeric_state` automations: [COUNT]
- `trigger: time` automations: [COUNT]

### Recommendations
- [ ] No action needed
- [ ] Consider:
  - [RECOMMENDATION]
  - [RECOMMENDATION]

---

## System-index.md Updates Needed

**Files/sections to update:**
- [ ] Scripts Inventory - Add: [LIST]
- [ ] Automation Patterns - Update: [PATTERN_NAME]
- [ ] Cross-Package Dependencies - Update: [SECTION]
- [ ] Known Issues & Deferred Work - Update: [SECTION]
- [ ] Recent Changes & Commits - Add: [CHANGES]
- [ ] Statistics - Update total counts

---

## Changes Summary

### What Changed Since Last Scan
- [BULLET POINT]
- [BULLET POINT]
- [BULLET POINT]

### What Stayed the Same
- [BULLET POINT]
- [BULLET POINT]

### Overall Health
- [ ] 🟢 Green: System healthy, no concerns
- [ ] 🟡 Yellow: Minor issues, non-blocking
- [ ] 🔴 Red: Issues requiring attention

---

## Action Items

| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| Update system-index.md | Claude | Today | [ ] |
| Create GitHub issue #[N] | Claude | Today | [ ] |
| Review PR #[N] | Danny | [DATE] | [ ] |
| Implement [FEATURE] | Claude | [DATE] | [ ] |

---

## Next Scan

**Date:** [YYYY-MM-DD]
**Type:** [Quick/Standard/Quarterly]
**Trigger:** [Regular schedule/After PR/After issue close]

**Focus areas for next scan:**
- [ITEM]
- [ITEM]
- [ITEM]

---

## Notes

- Scan completed successfully
- No critical issues found
- System knowledge updated
- Ready for next month

[ADD ANY ADDITIONAL OBSERVATIONS HERE]
