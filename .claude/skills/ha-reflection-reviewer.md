# Claude Skill: Home Assistant Reflection Reviewer

**Status:** Production Ready
**Version:** 1.0
**Created:** 2026-01-24
**Based On:** Reflection Report 2026-01-24 Analysis

---

## Purpose

Systematically review recent git commits to identify patterns in user corrections and learn from implementation errors. This skill ensures continuous improvement by analyzing what went wrong, codifying learnings, and updating validation rules.

## When to Use

- **Monthly Recurring** - Scheduled review of accumulated changes (1st of every month)
- After completing a major implementation phase
- Weekly when actively developing/fixing issues
- When user reports repeated error patterns
- Before starting similar implementation work
- As part of quarterly quality audits

## Monthly Review Schedule

**Trigger:** First day of every month or after significant implementation work

**Scope:** Review all commits from previous month (or since last reflection)

**Time Estimate:** 15-30 minutes depending on commit volume

**Expected Cadence:**
- January: Phase completion reviews + quarterly audit
- Monthly: Regular pattern tracking + skill updates
- Quarterly: Deep dive analysis + comprehensive metrics

**Reminder:** Schedule monthly reflection reviews to maintain continuous improvement

## Reflection Process

### Step 1: Identify Recent User Fixes
```bash
# Find commits containing "fix", "error", "bug" keywords
git log --all --oneline --since="7 days ago" | grep -i "fix\|error\|bug"

# Look for user commits after Claude implementations
git log --all --oneline --author="<user-name>" --since="7 days ago"

# Compare Claude commits vs user fix commits
git log --all --oneline --since="7 days ago" | head -30
```

### Step 2: Analyze Fix Patterns
For each user fix commit:
1. Read the commit diff (`git show <commit-hash>`)
2. Identify what Claude did wrong
3. Identify what user had to fix
4. Categorize error type (syntax, logic, entity reference, etc.)
5. Determine root cause
6. Document prevention strategy

### Step 3: Categorize Error Types
```
Error Categories:
- Syntax Errors: Invalid YAML structure, unsupported parameters
- Entity Reference Errors: Wrong entity_id, domain mismatches
- Logic Errors: Wrong conditions, incorrect sequences
- Quote Consistency Errors: Missing quotes on special chars
- Validation Errors: Skipped validation steps
```

### Step 4: Create Reflection Report
Generate comprehensive report with:
- Executive summary of errors found
- Detailed analysis of each error
- Root cause analysis
- Prevention recommendations
- Metrics and trends
- Action items for skill updates

---

## Reflection Report Template

```markdown
# Claude Implementation Reflection Report
**Date:** YYYY-MM-DD
**Period Analyzed:** X days / commits
**Files Reviewed:** N files

## Executive Summary
- Total errors found: X
- Critical errors: Y
- Error categories: Z
- User fix time: ~N minutes

## Critical Errors Identified

### Error 1: [Brief Description]
**Commit:** [hash] - [message]
**File:** [path:line]
**Severity:** 🔴 CRITICAL

**What Claude Did Wrong:**
[Code snippet showing error]

**What User Had to Fix:**
[Code snippet showing correction]

**Root Cause:**
[Analysis of why this happened]

**Prevention:**
[Specific validation rule or skill update]

---

## Error Patterns & Trends
[Analysis of common patterns]

## Impact Assessment
- Automation execution impact
- Development workflow impact
- Trust & reliability impact

## Recommended Improvements
1. [Specific actionable improvement]
2. [Another improvement]

## Action Items
### Immediate
- [ ] Update skill X with validation Y
- [ ] Add rule Z to reference doc

### Short-term
- [ ] Create automated check for pattern P

### Long-term
- [ ] Implement continuous reflection process

## Metrics
- Error distribution by category
- Error distribution by severity
- Fixes required by file

## Lessons Learned
### What Went Wrong
[Key failures]

### What Should Change
[Required process changes]

### What Worked
[Successful elements to preserve]
```

---

## Common Error Patterns

### Pattern 1: Syntax Assumption Errors
**Indicators:**
- Added unsupported YAML parameters
- Used wrong syntax for Home Assistant features
- Assumed general YAML rules apply to HA-specific constraints

**Examples:**
- `description:` on condition objects (only `alias:` supported)
- `response_variables:` (plural) instead of `response_variable:` (singular)

**Prevention:**
- Always consult Home Assistant docs before using syntax
- Validate against HA YAML schema, not general YAML
- Add syntax constraint checks to quality reviewer

### Pattern 2: Entity Reference Errors
**Indicators:**
- Wrong entity_id used in actions
- Entity domain doesn't match action domain
- Entity names inconsistent (typos, wrong names)

**Examples:**
- `light.turn_on` targeting `input_boolean.*` entity
- `light.leo_s_bedroom_main_light` vs `light.leo_s_bedroom_lights`

**Prevention:**
- Grep/verify all entity_id references before committing
- Validate action domain matches target entity domain
- Cross-check entity names against Home Assistant registry

### Pattern 3: Quote Consistency Errors
**Indicators:**
- Unquoted strings starting with special characters
- Inconsistent quoting across similar parameters

**Examples:**
- `message: 🚷 Turning off` (unquoted emoji)
- `log_level: Debug` vs `log_level: "Debug"`

**Prevention:**
- Always quote strings starting with emoji/special chars
- Maintain consistent quoting for same parameter types
- Add quote validation to pre-commit checks

### Pattern 4: Copy-Paste Propagation
**Indicators:**
- Same error repeated across multiple locations
- Systematic wrong entity_id in multiple actions

**Examples:**
- 6 occurrences of `input_boolean.*` as light target

**Prevention:**
- Validate first occurrence before copy-paste
- Review all instances of copied code
- Use find/replace with verification step

### Pattern 5: False Positive Parameter Validation
**Indicators:**
- Flagging script parameters as unsupported without checking script definition
- Assuming parameters are invalid based on parameter name alone
- Not verifying against actual script field definitions

**Examples:**
- 2026-01-25: Incorrectly flagged `log_level` parameter in `send_to_home_log` calls as "invalid"
- Actual status: `log_level` is a VALID optional parameter with options ["Normal", "Debug"]
- Caused scan to report 16+ false positive issues across 8 files

**Script Reference - send_to_home_log Supported Parameters:**
```yaml
script.send_to_home_log:
  fields:
    message:          # required, string
    title:            # optional, string
    log_level:        # optional, default: "Debug"
                      # values: ["Normal", "Debug"]
                      # Controls log platform routing based on input_select.home_log_level
```

**Prevention:**
- Always verify script definition before flagging parameters as invalid
- Reference: `/packages/integrations/messaging/notifications.yaml`
- Check Home Assistant script fields BEFORE running validation
- Build parameter whitelist from actual script definitions, not assumptions
- Document all verified parameters in validation rules

**Lesson Learned:**
- Parameter validation requires actual script inspection
- Don't assume parameter names indicate support/lack thereof
- Maintain updated reference docs of all custom scripts and their fields
- False positives in scans reduce reliability of validation rules

---

## Integration with Existing Skills

### With ha-yaml-quality-reviewer.md
- Reflection findings → New CRITICAL checks
- Error patterns → Common issues reference
- Detection patterns → Automated scanning rules

### With ha-motion-consolidator.md
- Logic errors → Consolidation warnings
- Entity reference errors → Validation checklist

### With ha-consolidation-analyzer.md
- Complexity errors → Risk assessment updates

## Integration into Regular Workflow

**Monthly Maintenance Cycle:**
1. First of month: Run reflection review
2. Analyze all commits from previous month
3. Update skills with learnings
4. Document metrics for trending
5. Schedule next monthly review

**Quarterly Audit:**
1. Run comprehensive reflection on full quarter
2. Analyze error trends across months
3. Identify systemic improvements needed
4. Plan skill enhancements for next quarter

**Before New Phases:**
1. Run reflection on previous phase
2. Identify lessons learned
3. Update validation rules based on findings
4. Apply learnings to next phase planning

---

## Automation Opportunities

### Automated Reflection Triggers
```bash
# Weekly reflection on user fixes
git log --since="7 days ago" --author="Danny" | grep -i "fix\|error"

# Compare Claude vs User commit ratio
CLAUDE_COMMITS=$(git log --since="7 days ago" --grep="Phase\|Fix:" | wc -l)
USER_FIX_COMMITS=$(git log --since="7 days ago" --author="Danny" --grep="Fix\|fix" | wc -l)
ERROR_RATE=$(echo "scale=2; $USER_FIX_COMMITS / $CLAUDE_COMMITS" | bc)
```

### Automated Pattern Detection
- Track frequency of each error type over time
- Identify high-risk files or automation types
- Measure time-to-fix for different error categories
- Generate trend reports (improving vs degrading)

---

## Reflection Checklist

### Pre-Reflection
- [ ] Identify time range for analysis (7 days, 30 days, etc.)
- [ ] Collect list of user fix commits
- [ ] Collect list of Claude implementation commits
- [ ] Prepare reflection report template

### During Reflection
- [ ] Read each user fix commit diff
- [ ] Identify what Claude did wrong
- [ ] Categorize error type
- [ ] Determine root cause
- [ ] Document prevention strategy
- [ ] Count and trend errors

### Post-Reflection
- [ ] Generate reflection report
- [ ] Update affected skills with new rules
- [ ] Update reference docs with constraints
- [ ] Create action items for improvements
- [ ] Track metrics over time

---

## Metrics to Track

### Error Metrics
- Total errors found per reflection period
- Errors by category (syntax, entity, logic, quote)
- Errors by severity (critical, medium, low)
- Error rate (user fixes / Claude commits)

### Impact Metrics
- Time user spent fixing errors
- Number of commits required for fixes
- Files affected by errors
- Automations broken by errors

### Improvement Metrics
- Error rate trend over time
- Reduction in specific error categories
- Time-to-detection of errors
- Effectiveness of validation rules

---

## Success Criteria

### Short-term Success
- ✅ Reflection report generated within 15 minutes
- ✅ All error patterns identified and categorized
- ✅ Root causes documented for each error
- ✅ Prevention strategies defined

### Medium-term Success
- ✅ Error rate decreases by 50% within 1 month
- ✅ Specific error types eliminated (e.g., condition description errors)
- ✅ Validation rules prevent recurrence
- ✅ Skills updated with learnings

### Long-term Success
- ✅ Error rate < 10% (user fixes / Claude commits)
- ✅ Zero critical syntax errors
- ✅ Automated reflection process established
- ✅ Continuous improvement cycle operational

---

## Output Format

### Reflection Report
- Markdown file: `.claude/REFLECTION-REPORT-YYYY-MM-DD.md`
- Stored in project for historical reference
- Includes metrics, trends, and action items

### Skill Updates
- Update affected skill files with new validation rules
- Add examples to common issues reference
- Update detection patterns for automation

### Reference Doc Updates
- Add syntax constraints to automation reference
- Document unsupported parameters
- Provide correct examples

---

## Real-world Example: 2026-01-24 Reflection

**Input:**
- 10 commits analyzed on kitchen.yaml and related files
- 5 unique error types found
- 11 total fixes required by user

**Process:**
1. Analyzed commits `4dae3d94`, `8d5b7e7b`, `aa78e01d`
2. Identified error patterns:
   - Condition `description:` errors
   - `response_variable` syntax errors
   - Entity domain mismatches
   - Unquoted emoji strings
   - Entity name inconsistencies
3. Categorized and documented each error
4. Created prevention strategies

**Output:**
- Reflection report generated: `.claude/REFLECTION-REPORT-2026-01-24.md`
- Updated `ha-yaml-quality-reviewer.md` with 4 new CRITICAL checks
- Updated reference docs with syntax constraints
- Created this reflection skill for future use

**Impact:**
- Prevented recurrence of all 5 error types
- Added automated detection patterns
- Established continuous improvement process

---

## Limitations & Notes

- ⚠️ Requires manual analysis of git commits
- ⚠️ Cannot automatically fix all errors
- ⚠️ Requires human judgment for root cause analysis
- ⚠️ Effectiveness depends on consistent application

---

## Monthly Review Checklist

**[ ] Pre-Review (5 min)**
- [ ] Note current date and time period to review
- [ ] Identify date range (1st of last month → today)
- [ ] Prepare reflection report template
- [ ] Gather git commit history

**[ ] Analysis Phase (15-20 min)**
- [ ] Identify all user fix commits
- [ ] Read each fix commit diff in detail
- [ ] Categorize error types found
- [ ] Document root causes
- [ ] Create prevention strategies

**[ ] Documentation Phase (5-10 min)**
- [ ] Generate reflection report
- [ ] Update affected skill files
- [ ] Update reference documentation
- [ ] Create action items

**[ ] Post-Review (5 min)**
- [ ] Commit all changes
- [ ] Log metrics in tracking file
- [ ] Schedule next monthly review
- [ ] Note any patterns for quarterly deep dive

---

## Monthly Review Template

```markdown
# Monthly Reflection Review
**Date:** YYYY-MM-01
**Period:** YYYY-MM-01 to YYYY-MM-30
**Reviewed By:** Claude

## Quick Summary
- Commits analyzed: X
- User fix commits: Y
- Errors found: Z
- New validation rules: N

## Error Categories This Month
| Category | Count | Examples |
|----------|-------|----------|
| Syntax | X | ... |
| Entity Reference | X | ... |
| Logic | X | ... |
| Quote/Format | X | ... |

## Top Patterns
1. [Most common error this month]
2. [Second most common]
3. [Trending issue]

## Skills Updated
- [Skill 1] - Added X checks
- [Skill 2] - Fixed Y documentation

## Metrics Tracking
- Error rate: X% (was Y% last month)
- Most affected file: [filename]
- Improvement areas: [list]

## Next Month Focus
- [ ] Priority 1
- [ ] Priority 2
- [ ] Priority 3
```

---

## Best Practices

1. **Schedule Regular Reflections** - Monthly on 1st of month, weekly during active development
2. **Be Thorough** - Analyze ALL user fixes, not just obvious ones
3. **Document Root Causes** - Don't just fix symptoms, understand why
4. **Update Skills Immediately** - Don't defer skill updates
5. **Track Metrics** - Measure improvement over time
6. **Share Learnings** - Document for future reference
7. **Set Monthly Reminders** - Block calendar time for first of month reviews
8. **Build on Previous Months** - Track trends, don't just address individual issues

---

## Next Steps

1. Run first reflection after each major phase completion
2. Track error rates over 30 days
3. Identify top 3 error categories to eliminate
4. Automate reflection triggers (git hooks, scheduled tasks)
5. Build error pattern database

---

**Usage:** Invoke after implementation phases or periodically to review user corrections
**Team:** Danny's Home Assistant optimization
**Created:** 2026-01-24
**Status:** Production Ready
