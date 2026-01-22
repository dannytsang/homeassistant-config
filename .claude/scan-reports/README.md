# System Scan Reports

**Directory:** `.claude/scan-reports/`

This directory stores periodic comprehensive scans of the Home Assistant configuration system.

---

## File Naming Convention

```
scan-[YYYY-MM-DD].md
```

Example: `scan-2026-01-15.md`

---

## Report Types

### Quick Scan
- **Duration:** ~15 minutes
- **Token Cost:** ~800 tokens
- **Frequency:** Mid-month checks, after small changes
- **Filename:** `scan-[YYYY-MM-DD]-quick.md`

### Standard Monthly Scan
- **Duration:** ~30 minutes
- **Token Cost:** ~2,000 tokens
- **Frequency:** First Monday of each month
- **Filename:** `scan-[YYYY-MM-DD].md`

### Comprehensive Quarterly Scan
- **Duration:** ~45 minutes
- **Token Cost:** ~2,500 tokens
- **Frequency:** End of each quarter (Jan, Apr, Jul, Oct)
- **Filename:** `scan-[YYYY-MM-DD]-quarterly.md`

---

## Report Structure

Each report includes:

1. **Summary** - High-level overview with key metrics
2. **Scripts Audit** - Script inventory changes
3. **Automation Verification** - Count and distribution checks
4. **Pattern Discovery** - New patterns, deprecated syntax
5. **Dependencies** - Cross-package relationship verification
6. **Deferred Work** - GitHub issues status
7. **Recent Changes** - Commits, PRs, issues since last scan
8. **Consolidation Opportunities** (quarterly only)
9. **Performance Analysis** (quarterly only)
10. **System-index.md Updates** - What needs updating
11. **Action Items** - Follow-up tasks

---

## How to Use

### Running a Scan

1. Copy `.claude/monthly-scan-template.md` to this directory
2. Rename to: `scan-[TODAY-DATE].md`
3. Follow scan-procedures.md for your scan type
4. Fill out template as you go
5. Update system-index.md based on findings
6. Commit report when complete

### Referencing Past Scans

```
# Find all scans from January
ls scan-2026-01-*.md

# View specific report
cat scan-2026-01-15.md

# Compare two scans
diff scan-2025-12-15.md scan-2026-01-15.md
```

### Tracking Trends

Review reports in chronological order to identify:
- Growing automation count (healthy growth or bloat?)
- New patterns emerging
- Unresolved deferred work
- Recurring issues

---

## Archive Strategy

**Keep recent scans:** Current month + 3 months back
**Archive old scans:** Move to `.claude/scan-reports/archive/` after 6 months

---

## Integration Points

**After each scan, update:**
1. `.claude/system-index.md` - Statistics and patterns
2. `.claude/claude.md` - If new patterns discovered
3. GitHub issues - If new issues identified

**Report outputs inform:**
- Monthly system knowledge update
- Code review priorities
- Deferred work scheduling
- Pattern documentation

---

## Quick Reference

- **Scan Procedures:** See `.claude/scan-procedures.md`
- **Report Template:** See `.claude/monthly-scan-template.md`
- **System Index:** See `.claude/system-index.md`
- **Documentation:** See `.claude/claude.md`
