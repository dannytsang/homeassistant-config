# Archiving Strategy for .claude Directory

**Version:** 1.0
**Created:** 2026-01-25
**Purpose:** Keep .claude directory focused on current work while preserving historical context

---

## Archive Structure

```
.claude/
├── skills/              ← NEVER ARCHIVE (Living documentation)
├── agents/              ← NEVER ARCHIVE (Agent specifications)
├── home-assistant-*     ← NEVER ARCHIVE (Reference cache)
├── REFLECTION-METRICS.md ← NEVER ARCHIVE (Running tracker)
├── README.md            ← NEVER ARCHIVE (Master guide)
├── README.md            ← NEVER ARCHIVE (Master guide)
│
├── archive/
│   ├── reflections/
│   │   ├── 2025-10/     (Reflection files from Oct 2025)
│   │   ├── 2025-11/     (Reflection files from Nov 2025)
│   │   ├── 2025-12/     (Reflection files from Dec 2025)
│   │   ├── 2026-01/     (Reflection files from Jan 2026)
│   │   └── [YYYY-MM]/   (New months created as needed)
│   │
│   ├── scans/
│   │   ├── 2025/        (Scan reports from 2025)
│   │   ├── 2026/        (Scan reports from 2026)
│   │   └── [YYYY]/      (New years created as needed)
│   │
│   └── projects/
│       ├── room-documentation-phase-1/
│       ├── consolidation-2025-q4/
│       └── [project-name]/
```

---

## Monthly Archiving Schedule

### First of Every Month: Run Archiving

**Time to run:** Start of each month (e.g., 2026-02-01)

**Files to move:**

#### 1. Reflection Files >3 Months Old
Move from `.claude/` to `.claude/archive/reflections/[YYYY-MM]/`

Example: Moving 2025-10 reflections on 2026-01-01
```
2025-10-15 reflection → archive/reflections/2025-10/
2025-10-22 reflection → archive/reflections/2025-10/
```

**File pattern:** `REFLECTION-*.md` or `*REFLECTION*.md`

**Keep in main:** Current and previous 3 months of reflections

#### 2. Scan Reports >6 Months Old
Move from `.claude/` to `.claude/archive/scans/[YYYY]/`

Example: Moving 2025-07 scans on 2026-01-01
```
scan-2025-07-15.md → archive/scans/2025/
scan-2025-07-22.md → archive/scans/2025/
```

**File pattern:** `scan-*.md`

**Keep in main:** Current and previous 6 months of scans

#### 3. Completed Project Status Files
Move from `.claude/` to `.claude/archive/projects/[project-name]/`

When project is complete (e.g., all rooms documented):
```
ROOM-DOCUMENTATION-PROGRESS.md → archive/projects/room-documentation-phase-1/
```

**Keep in main:** Active projects only

---

## What NEVER Gets Archived

### Skills (Living Documentation)
- `skills/README.md`
- `skills/ha-*.md` (all 13 skills)
- Reason: Updated monthly with new patterns and validations
- Size impact: ~145KB - manageable
- Access: Core to every session's refresh

### Agents Directory
- `agents/*.md` (all agent specifications)
- Reason: Define system behavior, referenced regularly
- Size impact: ~10KB - minimal
- Access: Used when invoking specialized agents

### Home Assistant Reference Docs
- `home-assistant-automation-yaml-reference.md`
- `home-assistant-templating-reference.md`
- `home-assistant-scripts-reference.md`
- `home-assistant-splitting-configuration-reference.md`
- `home-assistant-template-sensors-reference.md`
- Reason: Syntax reference needed during automation work
- Size impact: ~120KB - worth keeping
- Access: Frequently checked during development
- Update: Manually refreshed via ha-documentation-updater skill

### Project Tracking
- `REFLECTION-METRICS.md` - Running metrics across all months
- `documentation-update-log.md` - Audit trail of doc changes
- Active project files (e.g., `ROOM-DOCUMENTATION-PROGRESS.md`)

### Configuration
- `settings.local.json` - Security permissions
- `SKILLS-ROADMAP.md` - Future development plan
- `monthly-scan-template.md` - Template for monthly scans
- `scan-procedures.md` - Comprehensive scan procedures
- `README.md` - Master guide (this file)

---

## Archiving Criteria by File Type

### Reflection Files
**Pattern:** `REFLECTION-*.md`, `*-REFLECTION.md`, `*-REFLECTION-*.md`

**Archive if:**
- Older than 3 months from today
- Example: If today is 2026-01-25, archive files dated before 2025-10-25

**Why 3 months:**
- Recent patterns still relevant for current work
- Long enough history for trend analysis
- Keep errors fresh in Claude's knowledge
- 3 months of reflections = ~50KB in main directory

**Keep examples:**
- 2025-11-15 reflection (2+ months old) ✓ Keep
- 2025-10-20 reflection (3+ months old) ✗ Archive
- 2026-01-24 reflection (current) ✓ Keep

### Scan Reports
**Pattern:** `scan-*.md`

**Archive if:**
- Older than 6 months from today
- Example: If today is 2026-01-25, archive files dated before 2025-07-25

**Why 6 months:**
- Longer history useful for audit trail
- Scans are discrete snapshots (not ongoing)
- Can be referenced for historical comparisons
- 6 months of scans = ~30KB in main directory

**Keep examples:**
- 2025-08-15 scan (5+ months old) ✓ Keep
- 2025-07-20 scan (6+ months old) ✗ Archive
- 2026-01-20 scan (current) ✓ Keep

### Project Files
**Pattern:** `PROJECT-*`, `*-PROGRESS.md`, `*-PROJECT-*.md`

**Archive if:**
- Project is complete/closed
- File is inactive/historical
- Note: Ongoing projects like room documentation stay in main

**Examples to archive:**
- `ROOM-DOCUMENTATION-PROGRESS.md` → When all rooms documented
- `CONSOLIDATION-Q4-2025.md` → When Q4 consolidation complete
- `PHASE1-COMPLETION-*.md` → After Phase 1 is done and Phase 2+ active

**Examples to keep:**
- `ROOM-DOCUMENTATION-PROGRESS.md` → While rooms still being added
- `HA-DOCUMENTATION-PROJECT-STATUS.md` → While doc system being built

---

## Archiving Process (Monthly)

### Step 1: List Candidates
```bash
# Find reflection files >3 months old
ls -la .claude/REFLECTION-*.md | grep 2025-10
ls -la .claude/*-REFLECTION*.md | grep 2025-10

# Find scan files >6 months old
ls -la .claude/scan-*.md | grep 2025-07
```

### Step 2: Verify File Type
- Confirm it matches archiving criteria
- Check it's not an active project file
- Verify it's not in "Never Archive" list

### Step 3: Move to Archive
```bash
mv .claude/REFLECTION-FILE.md .claude/archive/reflections/[YYYY-MM]/
mv .claude/scan-FILE.md .claude/archive/scans/[YYYY]/
```

### Step 4: Update documentation-update-log.md
Add entry to log what was archived and when

### Step 5: Verify Archive
```bash
# Confirm file moved
ls .claude/archive/reflections/2025-10/ | grep FILE

# Confirm not in main directory
! ls .claude/REFLECTION-FILE.md 2>/dev/null
```

---

## Space Impact Analysis

### Current State (2026-01-25)
- Main `.claude/` directory: ~290KB
- Breakdown:
  - Skills: 145KB (never archived)
  - References: 120KB (never archived)
  - Reflections: 35KB (will start archiving Feb 1)
  - Projects: 40KB (ongoing)
  - Config: 15KB (never archived)

### After Monthly Archiving (Feb 1)
- Main directory: ~255KB
  - Remove: ~35KB of Oct/Nov/Dec 2025 reflections
- Archive directory: ~35KB
  - Add: Oct/Nov/Dec 2025 reflections

**Impact:** Faster directory scans, clearer "current" context

### After First Quarterly Archiving (Apr 1)
- Main directory: ~225KB
  - Remove: Jan/Feb/Mar scan reports
  - Keep: Apr scan, reflections
- Archive directory: ~65KB
  - Add: All 2025 scan reports

---

## How Claude Uses This Strategy

### When Finding Files
1. **Need current skill?** → Search `skills/` (never archived)
2. **Need error patterns?** → Load `ha-known-error-detector.md` (never archived)
3. **Need recent reflection?** → Check main `.claude/` (current 3 months)
4. **Need old reflection?** → Check `archive/reflections/[YYYY-MM]/`
5. **Need scan?** → Check main if recent, archive if historical

### When Suggesting Context Load
```
"I notice your project is 6+ months old. The relevant documentation
is in archive/projects/[name]. Load from there to refresh that context."
```

### When Performing Cleanup
```
"Time for monthly archiving. Let me move files >3 months old to
archive/reflections/[month] and update the log."
```

---

## Integration with Refresh Strategy

**See:** `.claude/README.md` for complete context refresh strategy

**How they work together:**
1. **Minimal refresh** loads from main `skills/` (always available)
2. **Project refresh** loads from main `.claude/` (active projects)
3. **Historical lookup** loads from `archive/` (if needed)
4. **Clean directory** improves search speed and clarity

---

## Archiving vs Deleting

**Why we archive instead of delete:**
- ✅ Preserves historical context if needed
- ✅ Maintains audit trail of all work
- ✅ Allows research of old patterns
- ✅ Supports quarterly/yearly reviews
- ✅ Small storage cost (400KB total is minimal)

**When to delete (rarely):**
- Duplicate files (keep most recent)
- Incorrect/corrupted files (keep good versions)
- Test files (if truly not needed)

**Default:** Archive, don't delete

---

## Archive Cleanup Strategy (Quarterly)

**Every 3 months (Q1, Q2, Q3, Q4):**
1. Review archive directories
2. Consolidate if needed (e.g., merge monthly subdirs)
3. Check for duplicates
4. Verify space usage
5. Document any patterns discovered

**Annual cleanup (Q4 → Q1):**
1. Review year-old archives
2. Move very old scans to cold storage if needed
3. Update archiving strategy based on learnings
4. Plan next year's retention

---

## Implementation Checklist

- [x] Create `.claude/archive/` directory
- [x] Create `.claude/archive/reflections/` subdirectory
- [x] Create `.claude/archive/scans/` subdirectory
- [x] Create `.claude/archive/projects/` subdirectory
- [x] Create pre-filled month/year directories (2025-10 onwards)
- [x] Document in `.claude/README.md`
- [x] Create this archiving strategy guide
- [ ] Execute first monthly archiving (2026-02-01)
- [ ] Update monthly-scan-template.md to reference archiving
- [ ] Add to scan procedures: "Remember to archive old files"

---

## Questions & Answers

**Q: What if I need an archived file?**
A: It's still in `archive/[type]/[date]/`, just not in the main directory. Ask Claude to load it from there.

**Q: Should I manually archive or wait for Claude?**
A: Either works. If you manually archive, update the log. If you ask Claude, it will do both.

**Q: What if I need to keep something longer?**
A: Edit this file to extend the archiving criteria. Note: Keep in `.claude/README.md` what gets archived.

**Q: How does archiving affect context refresh?**
A: Minimal refresh loads from main (unaffected). If you need archived context, ask Claude to load from archive.

**Q: What about git?**
A: Archive directories are in `.claude/` which is in `.gitignore`. Archive files don't go to git.

---

**Last Updated:** 2026-01-25
**Next Review:** 2026-02-01 (first archiving)
**Next Quarterly:** 2026-04-01 (Q1 review)
