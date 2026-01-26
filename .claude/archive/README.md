# .claude Archive

**Purpose:** Store historical documentation, completed projects, and old reflection files to keep the main `.claude/` directory focused on current work.

**Archiving Policy:** Files are moved here based on age and relevance, keeping the active `.claude/` directory lean and organized.

---

## Directory Structure

### `/archive/reflections/YYYY-MM/`

**Contents:** Monthly reflection files documenting error patterns, improvements, and lessons learned.

**Files Archived Here:**
- `REFLECTION-*.md` - Detailed reflection analyses
- `REFLECTION-KITCHEN-2026-01-24.md` - Kitchen-specific reflection
- `REFLECTION-REPORT-*.md` - Monthly summary reports

**Archiving Schedule:** After 3 months
- Example: Reflections from January 2026 archive in April 2026
- Used for historical context and trend analysis

**Access:** Reference for understanding past patterns and learning trends over time.

---

### `/archive/scans/YYYY/`

**Contents:** Historical system scan reports from audits and reviews.

**Files Archived Here:**
- `scan-reports/` directory moved here annually
- `scan-2026-01-19.md` - Historical scan from January 2026
- `scan-YYYY-MM-DD.md` - Dated scan reports

**Archiving Schedule:** After 6 months
- Example: Scans from January 2026 archive in July 2026
- Kept for audit trail and historical review

**Access:** Reference for understanding repository state changes over time.

---

### `/archive/projects/`

**Contents:** Completed project tracking files and phase documentation.

**Files Archived Here:**
- `PHASE1-COMPLETION-2026-01-24.md` - Completed phase report
- `PHASE2-PROGRESS-2026-01-24.md` - Phase progress tracking
- `ROOM-DOCUMENTATION-PROGRESS.md` (when complete) - When all 11 rooms documented

**Archiving Trigger:** Immediately upon project completion
- PHASE files moved when phase complete and learnings integrated into skills
- Project files moved when all deliverables done

**Access:** Reference for understanding completed work and project history.

---

## What Stays in Main `.claude/` Directory

### Always Current (Never Archive)

**Skills System:**
- `skills/` directory (all 13 skill files)
- `agents/` directory (agent specifications)
- `skills/README.md` (master skill index)

**Reference Documentation:**
- `home-assistant-*-reference.md` (5 reference docs)
- `settings.local.json` (security permissions)

**Ongoing Tracking:**
- `REFLECTION-METRICS.md` (continuous improvement metrics)
- `documentation-update-log.md` (audit trail of doc updates)
- `ROOM-DOCUMENTATION-PROGRESS.md` (current project status)

**Current Work:**
- Planning files for active projects
- Status documents for in-progress work
- Active project tracking files

---

## Monthly Archiving Checklist

**Every First Friday of Month (or first working day):**

```
□ Check for reflection files >3 months old
  └─ Move REFLECTION-*.md files from 3+ months ago to archive/reflections/YYYY-MM/

□ Check for scan reports >6 months old
  └─ Move scan-reports older than 6 months to archive/scans/YYYY/

□ Check for completed projects
  └─ Move PHASE completion files to archive/projects/
  └─ Move ROOM-DOCUMENTATION-PROGRESS when all 11 rooms complete

□ Update this README with monthly summary
  └─ Note what was archived
  └─ Update dates if new archive periods needed
```

---

## Archive Summary

| Period | Category | Files | Status |
|--------|----------|-------|--------|
| 2026-01 | Reflections | 3 files | Archived on 2026-01-25 |
| 2026 | Scans | 2 files (+ README) | Archived on 2026-01-25 |
| — | Projects | 2 files (PHASE1, PHASE2) | Archived on 2026-01-25 |

---

## How to Find Archived Files

**To search archived reflections:**
```bash
find .claude/archive/reflections -name "*KITCHEN*" -type f
```

**To list scans by year:**
```bash
ls -la .claude/archive/scans/2026/
```

**To access completed projects:**
```bash
ls -la .claude/archive/projects/
```

---

## When to Restore from Archive

Files in archive can be brought back to main `.claude/` if:

1. **Reference needed for learning** - Bring back specific reflection file to review patterns
2. **Project restarted** - Restore project tracking file if similar work resuming
3. **Error recurrence** - Restore old reflection to analyze if pattern returns

**Example:** If consolidation errors happen again, restore `archive/reflections/2026-01/REFLECTION-KITCHEN-TIMER-2026-01-24.md` to compare root causes.

---

## Related Documentation

- **Archiving Strategy Details:** `.claude/ARCHIVING-STRATEGY.md`
- **Context Refresh Guide:** `.claude/README.md` (when created)
- **Skills Index:** `.claude/skills/README.md`

---

**Archive Created:** 2026-01-25
**Last Updated:** 2026-01-25
**Status:** Operational
**Next Review:** 2026-02-01 (or first day of month)
