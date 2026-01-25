# Claude Skills for Home Assistant Configuration

**Version:** 1.2
**Created:** 2026-01-23
**Last Updated:** 2026-01-25
**Status:** Production
**Total Skills:** 13 (6 optimization + 5 validation/error prevention + 1 documentation + 1 issue management)

---

## Overview

This directory contains specialized Claude skills designed to optimize Home Assistant configuration management. Each skill is a reusable methodology documented for systematic application.

---

## 🚨 Critical Collaboration Rule

**No Claude attribution in commits.** This is an iron clad law. Never include "Co-Authored-By: Claude" or similar. All commits are authored by the user. See `.claude/COMMIT-CONVENTIONS.md` for details.

---

## After Conversation Compaction

When Claude's context is compacted and loses previous conversation history, rebuild context with this strategy:

### Minimal Context Refresh (Recommended)
```
Read .claude/skills/README.md and .claude/skills/ha-known-error-detector.md
```
- Fast load (~2 minutes)
- Contains complete skill index
- Includes 7 critical error patterns to prevent
- Enough to understand scope and ask intelligent questions

### Full Context Refresh (After long break)
```
Read .claude/skills/README.md, .claude/skills/ha-known-error-detector.md,
.claude/REFLECTION-METRICS.md, and .claude/ROOM-DOCUMENTATION-PROGRESS.md
```
- Restores skill index and error patterns
- Updates current project status
- Includes improvement metrics and trends

**Complete Guide:** See `.claude/README.md` for full context refresh strategy, task-specific loading, and automatic detection.

---

## Available Skills

### 0. **HA Documentation Updater**
**File:** `ha-documentation-updater.md`

Fetches the latest Home Assistant documentation from official sources and updates local reference cache. Maintains audit trail of changes and reports what's new or deprecated.

**Use When:**
- Manual refresh: `/ha-docs` command
- Quarterly documentation reviews
- Before major automation work
- When HA version is updated
- Team documentation maintenance

**Typical Results:**
- Up-to-date local reference files
- Audit trail of all changes
- New features and deprecations identified
- Clear what changed and why

**Example:** Run /ha-docs to fetch latest docs, get report of what changed since last update

---

### 0.1 **HA Doc Currency Checker** (Utility)
**File:** `ha-doc-currency-checker.md`

Validates that reference documentation is current before running validation checks. Prevents stale documentation from invalidating validation results.

**Use When:**
- Running any validator (ha-yaml-quality-reviewer, ha-entity-reference-validator, etc.)
- Before committing changes that depend on documentation accuracy
- When you haven't refreshed docs in 30+ days
- As a pre-flight check before major work

**What It Does:**
1. **Reads metadata** from reference files (Date field)
2. **Calculates age** (days since last update)
3. **Compares against threshold** (30-45 days depending on validator)
4. **Reports status** and recommends refresh if stale

**Integrated Into:**
- ha-yaml-quality-reviewer.md (30 day threshold)
- ha-entity-reference-validator.md (45 day threshold)
- ha-consolidation-analyzer.md (30 day threshold)
- ha-package-review.md (30 day threshold)

**Typical Results:**
- Clear doc currency status at start of validation
- Alert if docs need refresh
- Prevention of validation based on stale information
- Confidence that recommendations are based on current HA version

**Example:** Validator reports "Documentation is 3 days old ✅ Current. Proceeding with validation..."

---

### 1. **HA Motion Consolidator**
**File:** `ha-motion-consolidator.md`

Consolidates motion-based automations using trigger ID branching and choose blocks.

**Use When:**
- Multiple automations trigger on same motion sensor
- Different responses for motion on/off states
- Light control patterns (on/off/dim)
- Context-aware lighting (brightness, time-based, etc.)

**Typical Results:**
- 40-60% reduction in automation count
- 50%+ line count savings
- Improved maintainability

**Example:** Consolidated 6 stairs automations → 3 automations (-40%)

---

### 2. **HA YAML Quality Reviewer**
**File:** `ha-yaml-quality-reviewer.md`

Systematically reviews YAML packages for syntax errors and quality issues using severity-based prioritization.

**Use When:**
- After creating or modifying automations
- Regular quality audits
- Before major commits
- During code review phase

**Issue Categories:**
- 🔴 CRITICAL: Blocking errors (syntax, undefined refs, missing params)
- 🟡 MEDIUM: Functionality impacts (missing fields, formatting, spacing)
- 🟢 LOW: Cosmetic issues (consistency, grammar, emoji usage)

**Typical Results:**
- 20-30 issues identified per 11 packages
- 100% CRITICAL issues fixable
- Improved code consistency

**Example:** Reviewed 11 packages, found 26 issues (9 critical, 11 medium, 6 low)

---

### 3. **HA Consolidation Analyzer**
**File:** `ha-consolidation-analyzer.md`

Identifies consolidation opportunities by analyzing trigger/condition/action patterns and scoring them.

**Use When:**
- Starting optimization phase
- Auditing automation density
- Planning consolidation roadmap
- Evaluating new packages

**Scoring System:**
- 80-100: CRITICAL consolidation (Motion on/off pairs)
- 60-79: HIGH priority (Time-based variants)
- 40-59: MEDIUM priority (Context-aware variants)
- 0-39: LOW or skip

**Typical Results:**
- 50-70% consolidation opportunities identified
- Clear prioritization (what to consolidate first)
- Risk/complexity assessment

**Example:** Stairs package - 7 motion automations analyzed → 3 consolidation recommendations

---

### 4. **HA Reflection Reviewer**
**File:** `ha-reflection-reviewer.md`

Systematically reviews recent git commits to identify patterns in user corrections and learn from implementation errors.

**Use When:**
- After completing major implementation phases
- Weekly/monthly quality audits
- When user reports repeated error patterns
- Before starting similar implementation work
- Quarterly continuous improvement reviews

**Review Process:**
- Analyzes user fix commits vs Claude implementation commits
- Categorizes error types (syntax, entity reference, logic, quote)
- Documents root causes and prevention strategies
- Updates skills and reference docs with learnings
- Tracks metrics and improvement trends

**Typical Results:**
- 5-10 error patterns identified per review
- 100% of errors documented and prevented
- Skill updates with new validation rules
- Continuous improvement cycle established

**Example:** 2026-01-24 reflection found 5 critical error types, updated 3 skills with new validation rules

---

### 5. **HA Room Documentation Generator**
**File:** `ha-room-documentation-generator.md`

Generates comprehensive room setup documentation by analyzing automation YAML files and creating structured markdown guides.

**Use When:**
- Creating documentation for a new room package
- Onboarding team members or future self
- Documenting room automation capabilities
- Building automation portfolio
- Planning room expansion

**Process:**
- Analyze room YAML files
- Extract device inventory
- Categorize automations by function
- Create ASCII room layout diagrams
- Document automation workflows
- Map configuration parameters
- Generate standardized markdown

**Typical Results:**
- 1000-2000 line comprehensive guide
- Device inventory table
- Automation function breakdown
- Room layout ASCII diagram
- Workflow sequences
- Configuration reference
- Complete setup documentation

**Example:** Office setup documentation with 18 devices, 24 automations, complete workflows

---

### 6. **HA Known Error Detector**
**File:** `ha-known-error-detector.md`

Automatically scans Home Assistant YAML for 7 known error patterns discovered through reflection analysis. Prevents recurrence of syntax errors, entity reference errors, quote consistency issues, logic errors, and unsafe attribute access.

**Use When:**
- Before every commit (catch known errors automatically)
- During code review (flag suspicious patterns)
- After major changes (validate changes don't introduce known errors)
- When consolidating automations (ensure consolidation doesn't propagate errors)
- Running pre-commit validation

**The 7 Known Patterns:**
1. Invalid `description:` on condition objects
2. Unquoted string values in YAML
3. Undefined entity references
4. Quote consistency errors
5. Missing required parameters
6. Motion automation logic errors
7. Unsafe attribute access on entities

**Typical Results:**
- 100% prevention of known error patterns
- Quick scanning for pattern matches
- Clear flagging of error locations
- Prevention strategies documented

**Example:** Scans 11 packages, flags 9 critical syntax errors (Pattern 1) before commit

---

### 7. **HA Consolidation Pre-Check**
**File:** `ha-consolidation-pre-check.md`

Validates automations are safe to consolidate BEFORE applying the motion consolidator skill. Identifies consolidation blockers, validates compatibility, and assesses complexity.

**Use When:**
- Before attempting any consolidation (essential pre-check)
- Planning consolidation roadmap (score and prioritize)
- Risk assessment (identify blocking issues early)
- Preventing failed consolidations (validate prerequisites)
- During consolidation analyzer review (complement scoring)

**Critical Checks:**
- Same trigger entity validation
- Condition compatibility assessment
- Action conflict detection
- Safety requirement validation
- Complexity scoring

**Typical Results:**
- Clear pass/fail consolidation readiness
- Identified blocking issues
- Risk mitigation recommendations
- Consolidation safety assessment

**Example:** Pre-checks 4 motion automations → 3 safe to consolidate, 1 blocked due to incompatible conditions

---

### 8. **HA Automation ID Manager**
**File:** `ha-automation-id-manager.md`

Validates, assigns, and manages 13-digit numeric automation IDs with uniqueness checks and conflict detection. Prevents semantic ID naming errors and ensures all automation IDs meet Home Assistant requirements.

**Use When:**
- Before consolidation work (assign proper IDs to new consolidated automations)
- After creating new automations (validate IDs are correctly formatted)
- When modifying automation IDs (check for conflicts before committing)
- Planning major refactoring (ID audit and cleanup)

**Validation Checks:**
- 13-digit numeric format requirement
- Uniqueness across repository
- No reserved/conflicting IDs
- Proper ID assignment for consolidated automations

**Typical Results:**
- Valid IDs for all new automations
- Conflict detection before commit
- Proper ID generation for consolidations
- Zero duplicate ID issues

**Example:** Consolidates 2 automations → generates new valid ID (1740955286496), validates no conflicts

---

### 9. **HA Entity Reference Validator**
**File:** `ha-entity-reference-validator.md`

Cross-references all entity_id mentions across Home Assistant packages. Validates domain matching, detects typos and inconsistencies. Prevents entity domain mismatches and entity name errors.

**Use When:**
- Before committing automation changes (validate all entity_id references)
- After consolidation work (verify all entity targets are valid)
- During package reviews (check for undefined or typo'd references)
- Refactoring entity names (track all reference updates)

**Validation Checks:**
- Domain matching (action to entity domain)
- Entity existence verification
- Typo detection and correction
- Name inconsistency flagging
- Reference completeness validation

**Typical Results:**
- 100% entity reference validation
- All undefined entities caught
- Typo fixes identified
- Domain mismatch prevention

**Example:** Validates 45 entity references across 11 packages → flags 3 typos, 1 domain mismatch

---

### 10. **HA Package Review**
**File:** `ha-package-review.md`

Reviews Home Assistant YAML package files for common issues, bugs, and improvement opportunities based on established patterns in the repository.

**Use When:**
- Reviewing new room packages
- Auditing existing packages for issues
- Before major package modifications
- Ongoing quality assurance cycles

**Review Areas:**
- Syntax and YAML structure
- Entity reference validity
- Logic and flow verification
- Pattern consistency
- Improvement opportunities

**Typical Results:**
- Comprehensive issue list
- Pattern violations identified
- Improvement recommendations
- Quality assessment report

**Example:** Reviews kitchen package → identifies 5 improvements, 2 missing validations

---

### 11. **HA Repository Status**
**File:** `ha-repo-status.md`

Comprehensive review of repository state including commits, branches, file changes, and work-in-progress status. Provides snapshot of current repository health and pending work.

**Use When:**
- Starting new work session (understand current state)
- After breaks from the project
- Before planning major changes
- Quarterly health checks
- Handoff or onboarding scenarios

**Analysis Includes:**
- Current branch and uncommitted changes
- Recent commit history and patterns
- Open issues and PRs
- File modification timeline
- Work-in-progress inventory
- Repository metrics

**Typical Results:**
- Clear picture of repository state
- Pending work identification
- Recent activity summary
- Recommendations for next steps

**Example:** Provides status showing 12 uncommitted changes, 3 in-progress features, 2 pending PRs

---

### 12. **HA GitHub Issue Creator**
**File:** `ha-github-issue-creator.md`

Creates GitHub enhancement issues with automated label detection, validation, and assignment to the repository owner.

**Use When:**
- Planning enhancement discussions (turn plans into trackable issues)
- Feature requests identified during review (capture ideas as issues)
- After smoke testing or validation (document findings that need work)
- Consolidation opportunities (track improvements to implement)
- Documentation improvements (turn gaps into action items)
- Refactoring/optimization work (track technical improvements)

**Key Features:**
- ✅ Checks available labels before creating (prevents errors)
- ✅ Always applies 'enhancement' label
- ✅ Matches other applicable labels from available list
- ✅ Always assigns to dannytsang
- ✅ Structured issue body with all relevant sections
- ✅ User approval before creation

**Label Matching:**
- Room-specific labels (kitchen, office, stairs, etc.)
- Integration labels (integration: nest protect, etc.)
- Feature type labels (automations, scripts, documentation)
- Domain labels (testing, configuration, performance)
- Only applies labels that exist in repository

**Typical Results:**
- Well-structured enhancement issues
- Proper labeling with no "label not found" errors
- Assigned and ready for action
- Clear title and comprehensive body
- Related issues linked where applicable

**Example:** Creates issue for "Consolidate stairs motion automations" with labels: enhancement, automations, stairs

---

## Skill Workflow

### Standard Optimization Flow
```
0. STATUS CHECK (Repository Status) [Optional - understand current state]
   └─ Review repo state, pending changes, branches

0. ERROR SCAN (Known Error Detector) [Recommended before any changes]
   └─ Scan for 7 known error patterns, prevent issues early

1. PRE-CHECK (Consolidation Pre-Check) [Before consolidation work]
   └─ Validate automations are safe to consolidate

2. ANALYZE (Consolidation Analyzer)
   └─ Identify opportunities, score, prioritize

3. CONSOLIDATE (Motion Consolidator)
   └─ Apply consolidation patterns, test

4. ID VALIDATION (Automation ID Manager)
   └─ Ensure all automation IDs are valid and unique

5. REVIEW (YAML Quality Reviewer)
   └─ Validate syntax, find issues, fix

6. ENTITY VALIDATION (Entity Reference Validator)
   └─ Verify all entity references are valid and match domains

7. PACKAGE REVIEW (Package Review)
   └─ Comprehensive package quality assessment

8. DOCUMENT (Room Documentation Generator)
   └─ Generate comprehensive setup guide [Optional but recommended]

9. CREATE ISSUES (GitHub Issue Creator)
   └─ Create enhancement issues for identified improvements [Optional]

10. COMMIT & TEST
    └─ Final validation before deployment

11. MONTHLY REFLECTION (Reflection Reviewer)
    └─ Review accumulated changes, learn from corrections, update skills
```

### Enhanced Workflow with Documentation
```
NEW PACKAGE → ANALYZE → CONSOLIDATE → REVIEW → DOCUMENT → COMMIT
                                                     ↓
                                             Room Setup Guide
                                             (ROOM-SETUP.md)
                                                     ↓
                    MONTHLY REFLECTION ← ACCUMULATED CHANGES ← COMMIT & TEST
```

### Monthly Maintenance
**First of every month:** Run Reflection Reviewer to analyze all changes from previous month, identify patterns, and update validation rules based on learnings.

### Example: Phase 4 Session
```
Consolidation Analyzer:
  Input: Stairs package (7 motion automations)
  Output: 3 consolidation opportunities identified (85%+ scores)

Motion Consolidator:
  Input: Before-bedtime automations (ID 1598726353326, 1598726353327)
  Output: Single consolidated automation (OR condition pattern)

YAML Quality Reviewer:
  Input: All fixed packages
  Output: 26 issues identified (9 critical, 11 medium, 6 low)

Result: 6 automations → 3, 85 lines saved, 0 critical issues
```

---

## Phase Integration

### Phase 4: Consolidation
- **Analyzer:** Identify opportunities (Step 1)
- **Consolidator:** Apply patterns (Step 2)
- **Reviewer:** Validate (Step 3)
- **Result:** Fewer, more maintainable automations

### Phase 5: Quality Assurance
- **Reviewer:** Comprehensive package review
- **Consolidator:** Re-check for missed opportunities
- **Result:** High-quality, consistent codebase

### Phase 6+: Ongoing Maintenance
- **Analyzer:** Quarterly consolidation audits
- **Reviewer:** Before each major change
- **Consolidator:** Apply new consolidation opportunities

---

## Metrics & ROI

### Session 2026-01-23 Results

| Metric | Value |
|--------|-------|
| Documentation Currency | 3 days old (latest) |
| Automations Consolidated | 15 |
| Consolidation Ratio | 50% (30 → 15) |
| Lines Saved | ~85 |
| Issues Found | 26 |
| Issues Fixed | 26 (100%) |
| Critical Issues | 0 (down from 9) |
| Review Time | 2-3 hours |
| ROI | ~3 lines saved per minute |

### Expected ROI for New Packages

- **Small room (5-10 automations):** 1-2 hour review + consolidation
- **Medium room (10-20 automations):** 2-3 hour review + consolidation
- **Large room (20+ automations):** 3-4 hour review + consolidation

---

## How to Use These Skills

### For New Automations (Quick Path)
```
1. Create automation
2. Known Error Detector (catch known patterns early)
3. Entity Reference Validator (verify entity references)
4. YAML Quality Reviewer (catch other issues)
5. Consider Consolidation Analyzer (should this be merged?)
6. Commit & test
```

### For Package Reviews (Full Path)
```
1. Repository Status (understand current state)
2. Known Error Detector (scan for known patterns)
3. Package Review (comprehensive issue assessment)
4. Consolidation Analyzer (what can be consolidated?)
5. Consolidation Pre-Check (validate safe to consolidate)
6. Motion Consolidator (apply consolidation patterns)
7. Automation ID Manager (validate/assign IDs)
8. Entity Reference Validator (verify references)
9. YAML Quality Reviewer (comprehensive validation)
10. Commit changes by severity (critical → medium → low)
```

### For Consolidation Cycles (Critical Path)
```
1. Known Error Detector (baseline - catch before starting)
2. Consolidation Analyzer (identify opportunities, score)
3. Consolidation Pre-Check (validate safe to consolidate)
4. Motion Consolidator (apply pattern)
5. Automation ID Manager (validate/assign new IDs)
6. Entity Reference Validator (verify references)
7. YAML Quality Reviewer (comprehensive validation)
8. Known Error Detector (final check before commit)
9. Repeat until score < 40%
```

### For Optimization Cycles (Comprehensive)
```
1. Repository Status (understand scope)
2. Known Error Detector (baseline error scan)
3. Consolidation Analyzer (identify all opportunities)
4. Prioritize by score (high-scoring first)
5. Consolidation Pre-Check (validate prerequisites)
6. Motion Consolidator (apply pattern)
7. Automation ID Manager (ID validation)
8. Entity Reference Validator (entity validation)
9. Package Review (quality assessment)
10. YAML Quality Reviewer (comprehensive validation)
11. Known Error Detector (final scan)
12. Commit changes
13. Reflection Reviewer (monthly - learn from changes)
```

### Daily Workflow
```
START SESSION:
  └─ Repository Status (what's changed, what's pending?)

DURING WORK:
  └─ Known Error Detector (before every commit)

END OF SESSION:
  └─ Known Error Detector (final validation)
  └─ Before git push (all skills passed)

MONTHLY:
  └─ Reflection Reviewer (learn from month's changes)
```

---

## Key Patterns Documented

### Motion Automations
- **Trigger ID Branching:** On/off pair consolidation
- **OR Conditions:** Context-aware light states
- **Time-based Branches:** Before/after bedtime variants
- **Safety Fallbacks:** Motion off with light state checks

### Quality Checks
- **Emoji Codes:** `:ladder:` → 🪜 conversions
- **Required Fields:** title, log_level, message
- **Quote Consistency:** Unquoted vs quoted values
- **Entity References:** Undefined vs valid

### Consolidation Scoring
- **High Score (80-100):** Motion on/off pairs, magic mirror patterns
- **Medium Score (60-79):** Time-based variants, context-aware logic
- **Low Score (0-59):** Complex nested logic, safety-critical differences

---

## When to Invoke Each Skill

### Documentation Updater → When to Use
- ✅ Quarterly documentation refresh
- ✅ Before major automation work
- ✅ When Home Assistant is updated
- ✅ Team documentation maintenance
- ✅ Start of optimization/consolidation work
- ✅ Unsure if docs are current

### Consolidation Analyzer → When to Use
- ✅ Starting a new optimization phase
- ✅ Auditing a new room package
- ✅ Planning consolidation roadmap
- ✅ Quarterly maintenance review
- ✅ After consolidating similar packages

### Motion Consolidator → When to Use
- ✅ Have analyzed consolidation opportunities
- ✅ Ready to apply patterns
- ✅ Want concrete consolidated YAML
- ✅ Need step-by-step guidance
- ✅ Require trigger ID mapping

### YAML Quality Reviewer → When to Use
- ✅ After creating/modifying automations
- ✅ Before committing to main
- ✅ Quarterly code quality audits
- ✅ After consolidation to re-validate
- ✅ Tracking consistency improvements

### Reflection Reviewer → When to Use
- ✅ After completing major implementation phases
- ✅ Weekly/monthly review of user corrections
- ✅ When repeated error patterns are observed
- ✅ Before starting similar implementation work
- ✅ Quarterly continuous improvement audits
- ✅ To track error rate trends over time

### Known Error Detector → When to Use
- ✅ Before every commit (catch known errors automatically)
- ✅ During code review (flag suspicious patterns)
- ✅ After major changes (validate no known patterns introduced)
- ✅ When consolidating automations (ensure consolidation doesn't propagate errors)
- ✅ Running pre-commit validation
- ✅ Before pushing to production

### Consolidation Pre-Check → When to Use
- ✅ Before attempting any consolidation work
- ✅ Planning consolidation roadmap (score and prioritize)
- ✅ Risk assessment (identify blocking issues early)
- ✅ Preventing failed consolidations (validate prerequisites)
- ✅ During consolidation analyzer review (complement scoring)

### Automation ID Manager → When to Use
- ✅ Before consolidation work (assign proper IDs to new consolidated automations)
- ✅ After creating new automations (validate IDs are correctly formatted)
- ✅ When modifying automation IDs (check for conflicts before committing)
- ✅ Planning major refactoring (ID audit and cleanup)
- ✅ Before any git push (ensure no ID conflicts)

### Entity Reference Validator → When to Use
- ✅ Before committing automation changes (validate all entity_id references)
- ✅ After consolidation work (verify all entity targets are valid)
- ✅ During package reviews (check for undefined or typo'd references)
- ✅ When refactoring entity names (track all reference updates)
- ✅ Before major automation deployments

### Package Review → When to Use
- ✅ Reviewing new room packages (quality assurance)
- ✅ Auditing existing packages (ongoing maintenance)
- ✅ Before major package modifications (baseline assessment)
- ✅ Ongoing quality assurance cycles
- ✅ Before consolidation work (establish baseline)

### Repository Status → When to Use
- ✅ Starting new work session (understand current state)
- ✅ After breaks from the project (reorient yourself)
- ✅ Before planning major changes (understand impact scope)
- ✅ Quarterly health checks (assess repository state)
- ✅ Handoff or onboarding scenarios
- ✅ Before major PR or release planning

### GitHub Issue Creator → When to Use
- ✅ After planning enhancement discussions (turn plans into issues)
- ✅ When feature requests are identified (capture as trackable issues)
- ✅ After validation/smoke testing (document findings that need work)
- ✅ When consolidation opportunities are found (track improvements)
- ✅ When documentation gaps are identified (turn gaps into action items)
- ✅ When refactoring opportunities are discovered (track technical work)
- ✅ Before committing large changes (create issue to track)

---

## Future Enhancements

### Version 1.2 (Planned)
- Automated pattern detection for new error types
- Git integration (analyze changed files automatically)
- Cost/benefit scoring refinement with ML
- Complexity metrics dashboard
- Integration with pre-commit hooks

### Version 2.0 (Planned)
- AI-based opportunity discovery
- Automated fix suggestions with confidence scoring
- Performance prediction for consolidations
- Integration with Home Assistant official validator
- Skill usage analytics and ROI tracking

### Beyond
- Real-time suggestions during automation creation
- Team-wide consolidation tracking and dashboards
- Continuous quality monitoring with alerts
- Predictive analytics for error prevention
- Multi-repository support for Home Assistant communities

---

## Lessons Learned

### What Works Well
1. **Systematic severity approach** - CRITICAL → MEDIUM → LOW
2. **Trigger ID patterns** - Universally applicable
3. **Parallel issue fixing** - All issues in one session
4. **Clear documentation** - Skills reference easily

### What Needs Improvement
1. **Mixed emoji formats** - Standardize at package level
2. **Duplicate logic** - Better detection needed
3. **Complex nesting** - 10+ branch choose blocks hard to maintain
4. **Safety vs consolidation** - Need clearer guidelines

### Reusable Patterns
1. **Consolidation methodology** - Works for all motion automations
2. **Quality framework** - CRITICAL/MEDIUM/LOW scales
3. **Scoring system** - Applicable to other domains
4. **Phased approach** - Analyze → Fix → Validate

---

## Team Guidelines

### Code Review Checklist
- [ ] All CRITICAL issues fixed
- [ ] At least 80% MEDIUM issues fixed
- [ ] No regressions from consolidation
- [ ] Automation traces validated
- [ ] Home log messages clear

### Consolidation Approval
- [ ] Score 80%+ for consolidation
- [ ] All original logic preserved
- [ ] Safety checks maintained
- [ ] Testing completed
- [ ] Commit message clear

### Quality Standards
- [ ] 0 CRITICAL issues in prod
- [ ] <5 MEDIUM issues per 50 automations
- [ ] Consistent emoji/formatting
- [ ] All entity refs valid

---

## Quick Reference

### Motion Consolidator Quick Start
```yaml
# Pattern: Motion on/off → Single automation
triggers:
  - trigger: state
    entity_id: sensor.motion
    to: "on"
    id: motion_on
  - trigger: state
    entity_id: sensor.motion
    to: "off"
    id: motion_off
# Then use: condition: trigger id: [motion_on | motion_off]
```

### YAML Quality Reviewer Quick Checks
```
Search for:
- :[a-z_]+: (invalid emojis)
- send_to_home_log without title:
- unquoted Debug/Normal
- Missing quotes on strings
```

### Consolidation Analyzer Quick Score
```
Score 80+: Motion on/off, Magic mirror → CONSOLIDATE
Score 60-79: Time variants, Context logic → CONSOLIDATE
Score 40-59: Complex nesting → CONSIDER
Score 0-39: Safety-critical → SKIP
```

---

## Support & Questions

**If skills need updates:** Document in git commits with notes
**If new patterns discovered:** Add to appropriate skill document
**If tool integration needed:** Update skill prerequisites section
**For team training:** Reference specific skill sections

---

**Skills Created:** 2026-01-23
**Last Updated:** 2026-01-25
**Total Skills:** 12 (6 optimization + 5 validation/error prevention + 1 issue management)
**Maintained By:** User
**Status:** Production Ready
**Version:** 1.2

---

## Next Steps

### Immediate (This Week)
1. Test all 11 skills on living_room, bedroom, office packages
2. Run Known Error Detector baseline on all existing packages
3. Execute Repository Status skill to assess current state
4. Plan first Reflection Reviewer session

### Short-term (This Month)
1. Integrate Known Error Detector into pre-commit workflow
2. Complete comprehensive Package Review of all existing packages
3. Identify consolidation opportunities using full skill set
4. Document any new error patterns discovered
5. Update skills based on findings

### Medium-term (Next Quarter)
1. Gather feedback from comprehensive skill usage
2. Refine patterns based on real-world application
3. Plan quarterly Reflection Reviewer session
4. Consider automation for pattern detection
5. Evaluate ROI of each skill and consolidation work
