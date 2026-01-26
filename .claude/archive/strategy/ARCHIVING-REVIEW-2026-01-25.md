# .claude Directory Archiving Review - 2026-01-25

**Purpose:** Analyze .claude files to determine what can be archived vs kept active

---

## File Categorization

### TIER 1: CORE SYSTEM (Keep in main .claude/)

These files are essential for ongoing operations and should never be archived.

**Navigation & Context:**
- `README.md` (13K) - Post-compaction context refresh guide - **KEEP**
- `COMMIT-CONVENTIONS.md` (5.3K) - Commit rules and policies - **KEEP**
- `REFLECTION-METRICS.md` (8.7K) - Monthly improvement tracking - **KEEP**
- `ROOM-DOCUMENTATION-PROGRESS.md` (16K) - Current room status (6/11 done) - **KEEP**
- `documentation-update-log.md` (3.5K) - Reference doc cache tracking - **KEEP**

**Subdirectories:**
- `skills/` - All 13 skills (never archive)
- `agents/` - Agent specs (never archive)

**Total TIER 1:** 46.5K (active system)

---

### TIER 2: REFERENCE DOCUMENTATION (Keep in main .claude/)

These are the cached HA documentation files actively used by validators and skills.

- `home-assistant-automation-yaml-reference.md` (36K) - **KEEP - Active**
- `home-assistant-scripts-reference.md` (15K) - **KEEP - Active**
- `home-assistant-templating-reference.md` (24K) - **KEEP - Active**
- `home-assistant-splitting-configuration-reference.md` (24K) - **KEEP - Active**
- `home-assistant-template-sensors-reference.md` (20K) - **KEEP - Active**

**Total TIER 2:** 119K (reference library)

---

### TIER 3: CURRENT ROOM DOCUMENTATION (Keep in main .claude/)

Completed room setup guides - actively used reference material.

- `BEDROOM-SETUP.md` (21K) - **KEEP - Completed room documentation**

**Total TIER 3:** 21K (completed work)

---

### TIER 4: PROJECT DELIVERABLES (Archive to archive/ directory)

These are completed project reports, analyses, and documentation that should be archived after extracting key knowledge.

**Documentation Projects:**
- `MISSING-DOCUMENTATION-TOPICS.md` (27K)
  - Task #6 analysis: Identified 14 topics for documentation
  - Priority matrix: Phase 1 (6 docs) vs Phase 2 (8 docs)
  - Frequency analysis: 1500+ automations analyzed
  - **Archive Path:** `archive/documentation/`

- `DOC-CURRENCY-INTEGRATION-SUMMARY.md` (9.6K)
  - Task #5 implementation: Integrated doc checks into 4 validators
  - Threshold guidelines: 30-45 days by validator type
  - **Archive Path:** `archive/completed-tasks/`

- `DOCUMENTATION-UPDATER-IMPLEMENTATION.md` (13K)
  - Implementation summary for ha-documentation-updater skill
  - Phase 1 findings and approach
  - **Archive Path:** `archive/completed-tasks/`

- `HA-DOCUMENTATION-PROJECT-STATUS.md` (8.6K)
  - Phase 1 exploration and design
  - Gap analysis: No automatic sync existed before
  - **Archive Path:** `archive/documentation/`

**Verification/Testing:**
- `CONTEXT-REFRESH-TEST-REPORT.md` (19K)
  - Task #8: Comprehensive test of post-compaction workflows
  - 8 test categories, all passing (100% pass rate)
  - Token budget verification
  - **Archive Path:** `archive/completed-tasks/`

- `CONTEXT-REFRESH-VERIFICATION.md` (11K)
  - Verification of context refresh strategy
  - Supports testing report
  - **Archive Path:** `archive/completed-tasks/`

**Room Reviews/Reflections:**
- `KITCHEN-RECENT-CHANGES-REFLECTION.md` (14K)
  - Analysis of kitchen commits (Pattern 7: Unsafe Attribute Access)
  - Architecture improvements identified
  - **Archive Path:** `archive/reflections/2026-01/`

- `LIVING-ROOM-REVIEW-2026-01-24.md` (8.1K)
  - Room review from 2026-01-24
  - **Archive Path:** `archive/reflections/2026-01/`

**Procedural Documentation:**
- `scan-procedures.md` (11K)
  - Scanning procedures for automations
  - Reference for future scans
  - **Archive Path:** `archive/procedures/`

- `monthly-scan-template.md` (7.4K)
  - Template for monthly scans
  - Reusable procedure
  - **Archive Path:** `archive/procedures/`

**Strategic Documents:**
- `ARCHIVING-STRATEGY.md` (11K)
  - Archiving policy and procedures
  - Monthly checklist
  - **Archive Path:** `archive/strategy/`

- `SKILLS-ROADMAP.md` (2.3K)
  - Original roadmap
  - Superseded by current task list
  - **Archive Path:** `archive/strategy/`

**Exploratory Work:**
- `HYBRID-TODO-SYNC.md` (12K)
  - Exploration of todo sync implementation
  - Analysis of options
  - **Archive Path:** `archive/explorations/`

- `AGENT-HA-ROOM-DOCUMENTATION.md` (8.6K)
  - Agent spec for room documentation
  - Now in skills/ directory
  - **Archive Path:** `archive/explorations/`

**Utilities/Tools:**
- `QUICK-REFRESH-COMMANDS.md` (6K)
  - Quick command reference
  - Useful but can be consolidated into README.md
  - **Archive Path:** `archive/utilities/`

- `UNSAFE-ATTRIBUTE-ACCESS-SCAN-2026-01-25.md` (5K)
  - Scan results from date
  - Point-in-time report
  - **Archive Path:** `archive/scans/2026-01/`

**Total TIER 4:** 181K (archivable project deliverables)

---

## Archive Plan

### Files to Archive (181K total)

Move to `.claude/archive/` with structure:

```
archive/
├── completed-tasks/
│   ├── DOC-CURRENCY-INTEGRATION-SUMMARY.md
│   ├── DOCUMENTATION-UPDATER-IMPLEMENTATION.md
│   ├── CONTEXT-REFRESH-TEST-REPORT.md
│   └── CONTEXT-REFRESH-VERIFICATION.md
├── documentation/
│   ├── MISSING-DOCUMENTATION-TOPICS.md
│   └── HA-DOCUMENTATION-PROJECT-STATUS.md
├── reflections/2026-01/
│   ├── KITCHEN-RECENT-CHANGES-REFLECTION.md
│   └── LIVING-ROOM-REVIEW-2026-01-24.md
├── procedures/
│   ├── scan-procedures.md
│   └── monthly-scan-template.md
├── strategy/
│   ├── ARCHIVING-STRATEGY.md
│   └── SKILLS-ROADMAP.md
├── explorations/
│   ├── HYBRID-TODO-SYNC.md
│   └── AGENT-HA-ROOM-DOCUMENTATION.md
├── utilities/
│   └── QUICK-REFRESH-COMMANDS.md
└── scans/2026-01/
    └── UNSAFE-ATTRIBUTE-ACCESS-SCAN-2026-01-25.md
```

### Files to Keep in Main .claude/ (186.5K)

- Core system: 46.5K
- Reference docs: 119K
- Room docs: 21K

---

## Knowledge Extraction Before Archiving

### Key Learnings to Preserve

**From MISSING-DOCUMENTATION-TOPICS.md:**
- 14 topics identified for Phase 1+2 documentation
- Phase 1: 6 priority docs covering 90% of automation patterns (110KB)
  - Conditions Reference (1,200+ uses)
  - Service Calls Reference (1,000+ uses)
  - Advanced Jinja2 Patterns (240+ uses)
  - For-Each Loops & Repeat (30+ uses)
  - Parallel Execution & Events (80+ uses)
  - Timers, Scenes & Notifications (150+ uses)
- 1,500+ automation triggers/conditions analyzed
- Frequency-based prioritization methodology established

**→ Add to:** `ROOM-DOCUMENTATION-PROGRESS.md` as "Next Documentation Phase" subsection

---

**From DOC-CURRENCY-INTEGRATION-SUMMARY.md:**
- Doc currency checks integrated into 4 validators
- Threshold: 30 days for active validators, 45 days for reference
- Validators now alert if docs are stale before proceeding
- Integration improves reliability of validation results

**→ Add to:** `skills/README.md` as note under doc-currency-checker utility

---

**From CONTEXT-REFRESH-TEST-REPORT.md:**
- Minimal context (56KB): Sufficient for 90% of tasks
- Full context (84KB): Provides comprehensive project status
- Token budgets verified: Minimal 12K, Full 30K (conservative)
- 6 automatic detection patterns identified for detection rules
- All 26 files in .claude verified and accessible
- Real-world scenarios: 5/5 passing

**→ Add to:** `.claude/README.md` under success metrics

---

**From KITCHEN-RECENT-CHANGES-REFLECTION.md:**
- Pattern 7 identified: Unsafe Attribute Access on conditional lights
- Root cause: numeric_state on `attribute:` without state check
- Solution: Use `state_attr()` with `|int(0)` default or check state first
- Architecture improvement: Unconditional timer cancellation (before conditionals)

**→ Add to:** `skills/ha-known-error-detector.md` as Pattern 7 details (already there - verify coverage)

---

**From ARCHIVING-STRATEGY.md:**
- Monthly archiving policy established
- Reflections >3 months old → archive
- Scans >6 months old → archive
- Completed projects → archive immediately
- Archive structure: reflections/YYYY-MM/, scans/YYYY/, projects/

**→ Already in place:** Policy is active

---

**From scan-procedures.md & monthly-scan-template.md:**
- Standardized scanning procedures documented
- Monthly template available for reuse
- Procedure for automations analysis established

**→ Already referenced in:** Monthly reflection process

---

### Integration Summary

Most key knowledge is already in active files or skills. Archive doesn't mean loss - it means:
- Keeps main .claude/ focused on current work
- Preserves complete history in archive/
- Knowledge in project deliverables is findable if needed
- Core operations stay clean and fast

---

## Final Recommendation

✅ **Archive 181K of project deliverables** to `.claude/archive/`

**Keeps main .claude/ focused on:**
- 46.5K core system files (active operations)
- 119K reference documentation (validator tools)
- 21K room documentation (completed work)
- **Total: 186.5K** (down from 367.5K - 49% reduction)

**Benefits:**
- Faster to navigate .claude directory
- Clear separation of active vs archived work
- Complete history preserved in archive/
- Context refresh loads only what's needed
- Archive structure enables future retrieval

**Time to Archive:** 10-15 minutes to move files and verify links
**Risk:** Low - archive is just organization, no functionality changes
**Reversibility:** 100% - can restore from git if needed

---

**Ready to proceed with archiving? Confirm and I'll:**
1. Create archive directory structure
2. Move files with preserved directory tree
3. Update any internal links
4. Commit with clear message
5. Verify .claude/ is cleaner and faster
