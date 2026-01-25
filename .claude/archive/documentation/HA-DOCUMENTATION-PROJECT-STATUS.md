# HA Documentation Lookup System - Project Status

**Status:** IMPLEMENTATION IN PROGRESS
**Created:** 2026-01-25
**Decision:** Implementing as Skill + Agent (modular architecture)

---

## Project Overview

Create a system to look up, cache, and verify Home Assistant documentation currency to ensure latest information is available for automations, scripts, and templating work.

---

## Current State Analysis

### ✅ What Already Exists

**Documentation Cache (4 files):**
- `home-assistant-automation-yaml-reference.md` (36,497 bytes, dated 2026-01-22)
- `home-assistant-scripts-reference.md` (14,525 bytes)
- `home-assistant-templating-reference.md` (24,570 bytes)
- `home-assistant-splitting-configuration-reference.md` (24,292 bytes)

**Pattern:** Each has metadata header with `Date:` field
- Example: `**Date:** 2026-01-22` (3 days old, slightly stale)

**Skills System (11 production skills):**
- ha-motion-consolidator.md
- ha-yaml-quality-reviewer.md
- ha-consolidation-analyzer.md
- ha-reflection-reviewer.md
- ha-room-documentation-generator.md
- ha-entity-reference-validator.md
- ha-known-error-detector.md
- ha-automation-id-manager.md
- ha-consolidation-pre-check.md
- ha-package-review.md
- ha-repo-status.md

**Agents System (2 production agents):**
- ha-package-validator.md (model: haiku)
- ha-code-optimizer.md (model: sonnet)

### ❌ What's Missing

1. **No automatic currency checking** - Docs could be weeks old
2. **No web fetch integration** - Can't update docs automatically
3. **No manual refresh skill** - Users can't request /ha-docs update
4. **No audit trail** - No record of which doc versions were used
5. **No currency warnings** - No alerts when docs are stale
6. **No agent integration** - Validators don't check doc dates

---

## Implementation Plan

### Two-Component Architecture (Recommended)

**Component 1: Documentation Updater Skill**
- **File:** `ha-documentation-updater.md`
- **Trigger:** Manual via `/ha-docs` command
- **Purpose:** Fetch latest HA docs and update local cache
- **Scope:** Skill (user-requested manual operation)

**Component 2: Documentation Reference Agent** (OPTIONAL)
- **File:** `agents/ha-documentation-reference.md`
- **Trigger:** Automatic when working on HA files
- **Purpose:** Verify docs are current, warn if stale
- **Scope:** Agent (automatic background checking)

### Why Skill vs Agent vs Both?

**Skill (ha-documentation-updater):**
- ✅ User explicitly triggers `/ha-docs`
- ✅ Clear manual control
- ✅ Quick implementation
- ✅ Doesn't require agent infrastructure
- ✅ Easy to integrate with existing workflow

**Agent (ha-documentation-reference):**
- ✅ Automatic background checking
- ✅ Can warn before validation runs
- ✅ Follows existing agent patterns
- ❌ More complex setup
- ❌ Slower (agent overhead)
- ❌ May be overkill for simple currency check

**Recommended Approach:**
1. **Phase 1 (TODAY):** Implement Skill only - straightforward, user-controlled
2. **Phase 2 (OPTIONAL):** Add Agent if needed for automatic warnings

---

## Implementation Detail: Documentation Updater Skill

### Skill Responsibilities

1. **Check Current Cache Status**
   - Read each reference doc's `Date:` field
   - Calculate age (today - date)
   - Report which docs are stale (>30 days)

2. **Fetch Latest Documentation**
   - Web fetch from https://www.home-assistant.io/docs/
   - Convert HTML → Markdown (using WebFetch + processing)
   - Extract key content sections

3. **Update Local References**
   - Overwrite old reference files with new content
   - Update `Date:` metadata header
   - Add `fetched:` timestamp
   - Preserve structure (heading levels, code blocks, etc.)

4. **Report Changes**
   - What was updated
   - How old the previous version was
   - Any new features/deprecations found
   - Links to source pages

5. **Create Audit Trail**
   - Log in `.claude/documentation-update-log.md`
   - Record what was fetched and when
   - Document what changed

### Documentation Sources

```
https://www.home-assistant.io/docs/automation/
https://www.home-assistant.io/docs/automation/yaml/
https://www.home-assistant.io/docs/scripts/
https://www.home-assistant.io/docs/configuration/templating/
https://www.home-assistant.io/docs/configuration/splitting_configuration/
```

### Cache File Format

**Current (Manual):**
```markdown
# Home Assistant Automation YAML Reference

**Source:** https://www.home-assistant.io/docs/automation/yaml/
**Date:** 2026-01-22
**Purpose:** Comprehensive guide to writing automations in YAML format

---

[Content...]
```

**Proposed Update (Auto-Updated):**
```markdown
# Home Assistant Automation YAML Reference

**Source:** https://www.home-assistant.io/docs/automation/yaml/
**Date:** 2026-01-25
**Fetched:** 2026-01-25 13:45 UTC
**Last Verified:** 2026-01-25
**HA Version:** Latest (2024.12.x)

---

[Content...]
```

### Skill Workflow

```
/ha-docs
  ↓
Check cache status
  ├─ automation.md: 3 days old (OK)
  ├─ scripts.md: 5 days old (OK)
  ├─ templating.md: 3 days old (OK)
  └─ splitting.md: 3 days old (OK)
  ↓
Fetch fresh docs from web
  ├─ automation: ✅ Updated
  ├─ scripts: ✅ Updated
  ├─ templating: ✅ Updated
  └─ splitting: ✅ Updated
  ↓
Report Changes
  ├─ What changed
  ├─ New features
  ├─ Deprecated syntax
  └─ Links to official docs
  ↓
Log Update Event
  └─ .claude/documentation-update-log.md
```

---

## Implementation Steps (Skill Only - Phase 1)

### Step 1: Create Skill File
- Create `skills/ha-documentation-updater.md`
- Define skill structure (Purpose, Methodology, Examples)
- Document web fetch strategy and markdown conversion

### Step 2: Implement Check Logic
- Read and parse `Date:` fields from existing reference files
- Calculate age in days
- Report currency status

### Step 3: Implement Fetch Logic
- Use WebFetch to pull latest HA docs
- Convert HTML to markdown format
- Preserve structure and content

### Step 4: Implement Update Logic
- Update reference files with new content
- Update metadata headers (`Date:`, `Fetched:`, etc.)
- Validate files are valid markdown

### Step 5: Implement Reporting
- Generate summary of what changed
- Highlight new/deprecated features
- Create audit trail

### Step 6: Integration
- Test with `/ha-docs` command
- Verify files update correctly
- Document usage in README

---

## Decision: Skill vs Agent vs Both?

**RECOMMENDATION: Implement Skill First**

**Rationale:**
1. Simpler implementation (Skill is just a procedure)
2. User has explicit control (`/ha-docs`)
3. No automatic complexity
4. Easier testing and validation
5. Can be called ad-hoc when needed
6. Can add Agent layer later if needed

**Phase 1 (Today):** Skill only
- User can manually run `/ha-docs` anytime
- Clean, simple implementation
- Quick to build and test

**Phase 2 (Future - Optional):** Add Agent
- If team wants automatic currency checks
- Skill handles manual updates
- Agent handles automatic warnings
- Both work together

---

## Critical Files

**To Create:**
- `.claude/skills/ha-documentation-updater.md` (Skill definition)
- `.claude/documentation-update-log.md` (Audit trail)

**To Update:**
- `.claude/home-assistant-automation-yaml-reference.md` (Via skill)
- `.claude/home-assistant-scripts-reference.md` (Via skill)
- `.claude/home-assistant-templating-reference.md` (Via skill)
- `.claude/home-assistant-splitting-configuration-reference.md` (Via skill)
- `.claude/skills/README.md` (Add skill documentation)

**Optional Future:**
- `.claude/agents/ha-documentation-reference.md` (Agent - Phase 2)

---

## Success Criteria

### Phase 1 (Skill Implementation):
- ✅ Skill file created and documented
- ✅ `/ha-docs` command works
- ✅ Fetches latest documentation
- ✅ Updates reference files
- ✅ Creates audit trail
- ✅ Reports what changed
- ✅ Users can refresh documentation on-demand

### Phase 2 (Optional Agent):
- ✅ Agent created
- ✅ Checks doc currency automatically
- ✅ Warns before validation if docs >30 days old
- ✅ Suggests running `/ha-docs`
- ✅ Integrates with validators

### Overall:
- ✅ No more stale documentation
- ✅ Team always has latest HA features
- ✅ Clear audit trail of doc versions used
- ✅ Easy manual refresh workflow
- ✅ Optional automatic currency alerts

---

## Next Action

**Proceed with Phase 1:** Create `ha-documentation-updater.md` skill

This will:
1. Fetch latest HA docs from official sources
2. Update local cache files
3. Create audit trail
4. Report changes to user
5. Be triggered manually via `/ha-docs` command

---

**Project Owner:** Danny Tsang
**Status:** Ready to implement
**Target:** Complete Phase 1 today
**Phase 2:** Optional, can defer to future session
