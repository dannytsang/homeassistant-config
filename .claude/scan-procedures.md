# Periodic Comprehensive Scan Procedures

**Purpose:** Systematically verify and update system-index.md and claude.md with current codebase state

**Frequency:** Monthly (or after major feature additions)
**Estimated Token Cost:** ~2,500 tokens per comprehensive scan
**Time Investment:** ~30 minutes per scan
**Output:** Updated system files + scan report

---

## Scan Types

### Type A: Quick Scan (15 min, ~800 tokens)
**When to use:** Mid-month verification, after small changes
**Checks:**
- New scripts created
- New automations added
- Recent commits reviewed
- Quick pattern check

**Output:** Brief delta report (what changed)

### Type B: Standard Monthly Scan (30 min, ~2,000 tokens)
**When to use:** Regular monthly maintenance
**Checks:**
- All scripts (verify count, new additions)
- Automation categories (verify distribution)
- New patterns discovered
- Deferred work status
- Recent changes

**Output:** Full monthly scan report

### Type C: Comprehensive Quarterly Scan (45 min, ~2,500 tokens)
**When to use:** Every 3 months, or before major releases
**Checks:**
- Everything in Type B, plus:
- Cross-package dependency analysis
- Scene inventory update
- Helper entity locations
- Code review findings
- Potential consolidation opportunities
- Performance bottleneck identification

**Output:** Quarterly comprehensive report + recommendations

---

## Procedure: Standard Monthly Scan (Type B)

### Phase 1: Prepare (~2 minutes)
1. Create new scan report file: `.claude/scan-reports/scan-[YYYY-MM-DD].md`
2. Note: Date of scan, type (Quick/Standard/Quarterly)
3. Record baseline from system-index.md (current counts)

### Phase 2: Script Inventory Check (~8 minutes)

**Task:** Verify all scripts exist and nothing new was added

**Steps:**
1. Grep all script definitions:
   ```bash
   grep -r "^  [a-z_]*:$" packages/*/scripts.yaml scripts.yaml
   ```
2. Compare against complete script reference in claude.md
3. Note:
   - New scripts added (if any)
   - Scripts removed (if any)
   - Scripts renamed (if any)

**Output to report:**
```markdown
## Scripts Audit
- Total scripts found: [COUNT]
- New scripts: [LIST] or "None"
- Removed scripts: [LIST] or "None"
- Status: ✅ Verified OR ❌ Discrepancies found
```

### Phase 3: Automation Count Verification (~5 minutes)

**Task:** Verify total automation count and distribution

**Steps:**
1. Grep all automation IDs:
   ```bash
   grep -r "^  - id:" packages/ automations.yaml | wc -l
   ```
2. Compare total count against system-index.md (should be 434+)
3. Spot-check a few packages:
   ```bash
   grep -c "^  - id:" packages/rooms/living_room.yaml
   grep -c "^  - id:" packages/rooms/kitchen/kitchen.yaml
   ```

**Output to report:**
```markdown
## Automation Verification
- Total automations: [COUNT] (expected: 434+)
- Growth since last scan: +[NUMBER] or "No change"
- Large files (1000+ lines): [LIST]
- Status: ✅ Verified OR ❌ Changes needed
```

### Phase 4: Pattern Discovery (~10 minutes)

**Task:** Identify new patterns or changes in existing patterns

**Steps:**
1. Search for new trigger types:
   ```bash
   grep -r "trigger: " packages/ | grep -v "state\|time\|numeric_state" | sort | uniq
   ```
2. Check for new condition types:
   ```bash
   grep -r "condition: " packages/ | sort | uniq -c | sort -rn | head -10
   ```
3. Look for new helper entity patterns:
   ```bash
   grep -r "input_boolean\|input_number\|input_select" packages/ | wc -l
   ```
4. Verify no deprecated syntax used:
   ```bash
   grep -r "service:" packages/ automations.yaml (should return nothing)
   grep -r "trigger:" packages/ (should be "triggers:")
   ```

**Output to report:**
```markdown
## Pattern Analysis
- New trigger types discovered: [LIST] or "None"
- Condition distribution: [TOP 5]
- Helper entities: [COUNT]
- Deprecated syntax found: [LIST] or "None - ✅ Good"
- New patterns: [LIST] or "None"
```

### Phase 5: Cross-Package Dependencies Check (~4 minutes)

**Task:** Verify no new circular dependencies introduced

**Steps:**
1. Identify which packages import from messaging:
   ```bash
   grep -r "send_to_home_log\|send_direct_notification" packages/ | wc -l
   ```
   (Should be 500+, verify it's growing, not shrinking)

2. Check for new inter-package calls:
   ```bash
   grep -r "script\." packages/ | grep -v "send_\|set_alarm\|lock\|unlock\|turn_everything" | head -20
   ```

3. Verify energy package dependencies:
   ```bash
   grep -r "octopus_energy\|growatt" packages/ | grep -v "energy/" | head -10
   ```

**Output to report:**
```markdown
## Dependency Verification
- Messaging calls: [COUNT] (expected: 500+)
- Energy dependencies: [COUNT] packages depend on energy
- New inter-package calls: [LIST] or "None"
- Circular dependencies: ✅ None detected OR ❌ [ISSUES]
```

### Phase 6: Deferred Work Status (~3 minutes)

**Task:** Check status of open GitHub issues

**Steps:**
1. List all open GitHub issues:
   ```bash
   gh issue list --state open
   ```

2. For each issue, verify:
   - Still relevant? (Y/N)
   - Implementation started? (Y/N)
   - Blocking other work? (Y/N)

3. Check if new issues should be created for patterns found

**Output to report:**
```markdown
## Deferred Work Status
| Issue | Title | Status | Notes |
|-------|-------|--------|-------|
| #176 | Unsafe brightness checks | Open | 7 instances, not started |
| #178 | Notification acknowledgment | Open | Implementation plan ready |
| #179 | Device-aware routing | Open | 3 approaches documented |

New issues to create: [LIST] or "None"
```

### Phase 7: Recent Changes Review (~2 minutes)

**Task:** Log what changed since last scan

**Steps:**
1. Check git log since last scan date:
   ```bash
   git log --oneline --since="2026-01-01" --until="2026-01-31"
   ```

2. Summarize changes (features, fixes, refactors)

3. Note any patterns or anti-patterns introduced

**Output to report:**
```markdown
## Recent Changes Summary
- Commits since last scan: [COUNT]
- Key changes: [BULLET LIST]
- PRs merged: [LIST]
- Issues closed: [LIST]
- Patterns introduced: [LIST] or "None"
```

---

## Comprehensive Quarterly Scan (Type C)

**Run all Type B procedures, plus:**

### Additional Phase 1: Scene Inventory Deep Dive

**Steps:**
1. Count all scenes:
   ```bash
   grep -r "^  [a-z_]*_[a-z_]*:" scenes.yaml | wc -l
   ```

2. Categorize by type (lighting, climate, security, special)

3. Check for unused scenes:
   ```bash
   for scene in $(grep "^  [a-z_]*:" scenes.yaml); do
     grep -r "$scene" packages/ || echo "UNUSED: $scene"
   done
   ```

**Output:**
```markdown
## Scene Inventory
- Total scenes: [COUNT] (expected: 75+)
- By category: Lighting [#], Climate [#], Security [#], Special [#]
- Unused scenes: [LIST] or "None"
```

### Additional Phase 2: Input Helpers Audit

**Steps:**
1. Find all input helpers:
   ```bash
   grep -r "input_boolean\|input_number\|input_select\|input_datetime" packages/
   ```

2. Verify all are in UI (not YAML) except schedule entities

3. Check for naming consistency

**Output:**
```markdown
## Helper Entities Audit
- Booleans: [COUNT] (all in UI except: [LIST])
- Numbers: [COUNT] (all in UI except: [LIST])
- Selects: [COUNT] (all in UI except: [LIST])
- Naming consistency: ✅ Good OR ⚠️ [ISSUES]
```

### Additional Phase 3: Consolidation Opportunities

**Steps:**
1. Identify duplicate logic patterns:
   ```bash
   # Look for similar automation structures
   grep -r "condition: numeric_state" packages/ | wc -l
   grep -r "mode: queued" packages/ | wc -l
   grep -r "parallel:" packages/ | wc -l
   ```

2. Check for scripts called from single location only:
   ```bash
   # These could be consolidated
   for script in $(grep "^  [a-z_]*:" scripts.yaml); do
     count=$(grep -r "action: script\.$script" packages/ | wc -l)
     if [ $count -eq 1 ]; then echo "SINGLE_USE: $script"; fi
   done
   ```

3. Note opportunities for centralization

**Output:**
```markdown
## Consolidation Opportunities
- Single-use scripts: [LIST with locations]
- Duplicate patterns: [DESCRIPTION with file refs]
- Recommended consolidations: [LIST]
- Priority: High/Medium/Low
```

### Additional Phase 4: Performance Analysis

**Steps:**
1. Identify large automations:
   ```bash
   wc -l packages/rooms/*.yaml | sort -rn | head -5
   ```

2. Count complex automations (many branches):
   ```bash
   grep -r "^      - conditions:" packages/ | wc -l
   ```

3. Check for high-frequency triggers:
   ```bash
   grep -r "trigger: state" packages/ | wc -l
   grep -r "trigger: numeric_state" packages/ | wc -l
   ```

**Output:**
```markdown
## Performance Considerations
- Largest files: [LIST with line counts]
- Complex automations (10+ branches): [COUNT]
- High-frequency triggers: [SUMMARY]
- Recommendations: [LIST]
```

---

## Report Template

Create file: `.claude/scan-reports/scan-[YYYY-MM-DD].md`

```markdown
# System Scan Report
**Date:** [YYYY-MM-DD]
**Scan Type:** [Quick/Standard/Quarterly]
**Duration:** [X minutes]
**Token Cost:** ~[X] tokens

---

## Summary
- Baseline automations: 434 → Current: [COUNT]
- Baseline scripts: 43+ → Current: [COUNT]
- Issues found: [NUMBER]
- Actions required: [YES/NO]

---

## Findings

[Include all phases from procedures above]

---

## Changes Since Last Scan
- [BULLET LIST]

---

## Deferred Work Impact
- No new blockers detected
- Issue #176: Still applicable, 7 instances
- Issue #178: Ready for implementation
- Issue #179: Ready for implementation

---

## Recommendations
1. [PRIORITY ACTION]
2. [FOLLOW-UP ACTION]
3. [MONITORING ACTION]

---

## Next Scan
**Scheduled:** [DATE]
**Type:** [Quick/Standard/Quarterly]
```

---

## Quick Reference: When to Run Each Scan Type

| Trigger | Scan Type | When |
|---------|-----------|------|
| Regular schedule | Standard | First Monday of each month |
| Small change | Quick | After adding 1-2 automations |
| Major feature | Standard | After PR merge |
| Quarterly review | Comprehensive | End of quarter (Jan, Apr, Jul, Oct) |
| Pre-release | Comprehensive | Before pushing to production |
| Investigation | Type-specific | When debugging or analyzing |

---

## Integration with system-index.md

**After each scan:**
1. Update system-index.md statistics if counts changed
2. Add new scripts to "Scripts Inventory"
3. Update "Recent Changes" section
4. Update "Known Issues & Deferred Work"
5. Note scan date and findings

**Monthly rhythm:**
- Run scan: 30 min
- Update system-index.md: 10 min
- Commit findings: 5 min
- **Total: ~45 min per month**

---

## Cost-Benefit Analysis

**Monthly scan cost:**
- Tokens: ~2,000 per standard scan
- Time: ~30 minutes
- Monthly cost: ~2,000 tokens + 30 min

**Value delivered:**
- Prevents pattern duplication
- Catches emerging issues early
- Maintains system knowledge accuracy
- Enables strategic planning
- Improves code reuse effectiveness

**ROI:** 2,000 tokens prevents 10,000+ tokens of wasted duplication work

---

## Automation Ideas (Future)

Once scanning becomes routine, consider:
1. Creating a Github Action to validate automation IDs
2. Automating duplicate pattern detection
3. Generating monthly reports automatically
4. Setting up Slack notifications for findings

For now: Manual scans provide human insight and flexibility.
