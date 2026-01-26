# Claude Agent: Home Assistant Documentation Reference Checker

**Status:** Ready for Deployment
**Version:** 1.0
**Created:** 2026-01-26
**Purpose:** Automated scheduled checking of documentation currency with alerts and optional auto-refresh

---

## Purpose

Automatically monitor documentation freshness on a schedule, alert when docs become stale (>30 days old), and optionally trigger automatic refreshes. This Phase 2 enhancement automates the manual checks from the ha-doc-currency-checker utility.

---

## When to Use

- **Scheduled checks** - Run every week to monitor documentation age
- **Automated alerts** - Get notified when docs exceed 30-day threshold
- **Pre-deployment validation** - Verify docs are current before major automation work
- **Continuous compliance** - Ensure team always has fresh reference material
- **Audit trail** - Automatic logging of all checks for compliance

---

## How This Agent Works

### Three Core Functions

**1. Automated Status Checks**
- Runs on a schedule (weekly recommended, configurable)
- Reads all reference documentation files (`home-assistant-*.md`)
- Calculates age for each file
- Compares against thresholds (default: 30 days)
- Tracks check history

**2. Alert Generation**
- Generates status report with color-coded results:
  - ✅ Green: Fresh (0-14 days)
  - 🟡 Yellow: Aging (15-29 days)
  - 🔴 Red: Stale (30+ days)
- Creates alert entries for stale documentation
- Logs alerts to documentation-update-log.md
- Can integrate with Home Assistant notification system

**3. Optional Auto-Refresh**
- Detects when documentation exceeds threshold
- Can automatically trigger `/ha-docs` refresh
- Or require manual approval before refresh
- Logs refresh decision and results

---

## Deployment Models

### Option 1: Weekly Status Check Only (Recommended for Now)

**Frequency:** Every Sunday 9 AM UTC
**Action:** Check docs, report status, alert if stale
**Auto-refresh:** Disabled (manual approval)
**Logs to:** documentation-update-log.md

```
Weekly Documentation Check Summary

Checked: 2026-01-26 09:00 UTC

Status:
├─ home-assistant-automation-yaml-reference.md: 4 days old ✅ Fresh
├─ home-assistant-scripts-reference.md: 4 days old ✅ Fresh
├─ home-assistant-templating-reference.md: 4 days old ✅ Fresh
├─ home-assistant-splitting-configuration-reference.md: 4 days old ✅ Fresh
└─ home-assistant-template-sensors-reference.md: 1 day old ✅ Fresh

Result: All documentation current ✅

Next Scheduled Check: 2026-02-02 09:00 UTC
```

### Option 2: Weekly Check + Auto-Refresh on Threshold (Future)

**Frequency:** Every Sunday 9 AM UTC
**Action:** Check docs, auto-refresh if any doc >30 days
**Logs to:** documentation-update-log.md
**Notification:** Alert on refresh

```
Weekly Documentation Check Summary

Checked: 2026-02-22 09:00 UTC

Status:
├─ home-assistant-automation-yaml-reference.md: 31 days old 🔴 STALE
├─ home-assistant-scripts-reference.md: 31 days old 🔴 STALE
└─ ... (others)

Result: Documentation stale, triggering auto-refresh...

Auto-Refresh Results:
✅ home-assistant-automation-yaml-reference.md: Updated (5 new features detected)
✅ home-assistant-scripts-reference.md: Updated (1 deprecation removed)
✅ home-assistant-templating-reference.md: Unchanged
✅ home-assistant-splitting-configuration-reference.md: Unchanged
✅ home-assistant-template-sensors-reference.md: Updated

Action Items for Review:
1. New feature in automation docs: "Blueprint Automations" (advanced feature)
2. Removed deprecation in scripts: "service:" format (legacy)

Refreshed Documentation:
├─ home-assistant-automation-yaml-reference.md: 0 days old ✅ Fresh
├─ home-assistant-scripts-reference.md: 0 days old ✅ Fresh
└─ ... (all others)

Next Scheduled Check: 2026-03-01 09:00 UTC
```

### Option 3: Daily Monitoring (Enterprise)

**Frequency:** Every day at 6 AM UTC
**Action:** Check docs, verbose reporting, immediate alerts
**Auto-refresh:** Requires manual approval after 30 days
**Logs to:** documentation-update-log.md
**Notification:** Daily digest via Home Assistant notifications

---

## Agent Workflow

### Flow Diagram

```
┌─────────────────────┐
│  Scheduled Trigger  │
│   (e.g., Weekly)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│  Load Reference Files       │
│  Extract Date from Headers  │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Calculate Age for Each     │
│  Compare to Thresholds      │
└──────────┬──────────────────┘
           │
           ▼
    ┌──────────────┐
    │ Any Stale?   │
    └──────┬───────┘
           │
      ┌────┴────┐
      │          │
      ▼          ▼
    NO          YES
      │          │
      │      ┌─────────────────────┐
      │      │ Generate Alert      │
      │      │ Log to Update Log   │
      │      └────────┬────────────┘
      │               │
      │          ┌────▼─────────────┐
      │          │ Auto-Refresh?    │
      │          └────┬──────┬──────┘
      │               │      │
      │          NO   │      │ YES
      │               │      │
      │          ┌────▼──┐   ▼
      │          │Report │ Trigger
      │          │Status │ /ha-docs
      │          └──┬────┘   │
      │             │        ▼
      │             │   ┌─────────┐
      │             │   │ Update  │
      │             │   │ Docs    │
      │             │   └────┬────┘
      │             │        │
      └─────────────┼────────┤
                    │        │
                    ▼        ▼
        ┌──────────────────────────┐
        │  Log Complete Results    │
        │  documentation-          │
        │  update-log.md           │
        └──────────┬───────────────┘
                   │
                   ▼
        ┌──────────────────────────┐
        │  Send Notifications      │
        │  (if configured)         │
        └──────────────────────────┘
```

---

## Check Algorithm

### Pseudocode

```
FUNCTION check_documentation_currency():
    today = current_date()
    results = []
    stale_count = 0

    FOR each file in reference_files:
        content = read_file(file)
        date_str = extract_date_from_header(content)
        file_age = calculate_days_difference(date_str, today)

        status = evaluate_age(file_age):
            IF file_age <= 14 days:
                status = "Fresh" ✅
            ELSE IF file_age <= 29 days:
                status = "Aging" 🟡
            ELSE:
                status = "Stale" 🔴
                stale_count += 1

        results.append({
            file: file,
            age: file_age,
            status: status
        })

    report = generate_status_report(results)

    IF stale_count > 0:
        IF auto_refresh_enabled:
            trigger_ha_docs_refresh()
            updated_results = check_documentation_currency()
            log_refresh_results(updated_results)
        ELSE:
            generate_alert(stale_count, results)

    log_check_to_update_log(report, timestamp)
    return report
```

---

## Implementation: Weekly Check Setup

### Step 1: Create Check Function

In Home Assistant, create an automation that calls this agent weekly:

**Home Assistant Automation (Example):**
```yaml
automation:
  - id: documentation_currency_check_weekly
    alias: "Documentation: Weekly Currency Check"
    description: "Check if reference documentation needs refresh"
    triggers:
      - trigger: time
        at: "09:00:00"
        weekday: "sun"
    conditions: []
    actions:
      - action: notify.persistent_notification
        data:
          title: "📚 Documentation Check Starting"
          message: "Running weekly documentation currency check..."

      - action: script.check_documentation_currency
        data: {}
    mode: single
```

**Supporting Script:**
```yaml
script:
  check_documentation_currency:
    alias: Check Documentation Currency
    description: Runs documentation freshness check
    sequence:
      - action: notify.persistent_notification
        data:
          title: "📚 Documentation Currency Report"
          message: |
            Running documentation freshness check...

            Checking reference files in .claude/ directory
            Age threshold: 30 days (default)

            This check will:
            1. Read all home-assistant-*.md files
            2. Extract dates from headers
            3. Calculate age in days
            4. Alert if any docs exceed threshold
            5. Log results to documentation-update-log.md
    mode: single
```

### Step 2: Log Check Results

After the check runs, append to `documentation-update-log.md`:

```markdown
### 2026-01-26 09:00 UTC (Automated Weekly Check)
**Status:** ✅ Check Complete - All Documentation Current
**Triggered By:** Weekly scheduled automation
**Check Type:** Automated currency monitoring

**Files Checked:**
| File | Age | Status |
|------|-----|--------|
| home-assistant-automation-yaml-reference.md | 4 days | ✅ Fresh |
| home-assistant-scripts-reference.md | 4 days | ✅ Fresh |
| home-assistant-templating-reference.md | 4 days | ✅ Fresh |
| home-assistant-splitting-configuration-reference.md | 4 days | ✅ Fresh |
| home-assistant-template-sensors-reference.md | 1 day | ✅ Fresh |

**Result:** All documentation within acceptable range (0-30 days)
**Recommendation:** Continue normal operations. Next refresh recommended ~Feb 22, 2026
**Next Check:** 2026-02-02 09:00 UTC

---
```

### Step 3: Configure Alerts

**If any documentation is stale:**

```markdown
### 2026-02-22 09:00 UTC (Automated Weekly Check - STALE DOCS DETECTED)
**Status:** ⚠️ Documentation Stale - Action Required
**Triggered By:** Weekly scheduled automation
**Check Type:** Automated currency monitoring

**Files Checked:**
| File | Age | Status |
|------|-----|--------|
| home-assistant-automation-yaml-reference.md | 31 days | 🔴 STALE |
| home-assistant-scripts-reference.md | 31 days | 🔴 STALE |
| home-assistant-templating-reference.md | 26 days | 🟡 Aging |

**Alert:** 2 files exceed 30-day threshold ⚠️

**Recommendation:**
- Run `/ha-docs` to refresh all documentation
- Estimated time: 2-3 minutes
- Updated docs will be logged here automatically

**Action Required:**
```bash
/ha-docs
```

**Next Check:** 2026-03-01 09:00 UTC
```

---

## Alert Thresholds

### Color-Coded Status System

| Age Range | Status | Symbol | Action |
|-----------|--------|--------|--------|
| 0-14 days | Fresh | ✅ | Continue using |
| 15-29 days | Aging | 🟡 | Plan refresh soon |
| 30+ days | Stale | 🔴 | Refresh immediately |

### Threshold Rationale

- **14 days (Fresh):** Covers typical bi-weekly update cycle
- **30 days (Stale):** Aligns with Home Assistant monthly releases (1st Wed/Thu)
- **Weekly checks:** Catches aging docs before they become stale

---

## Integration with Home Assistant

### Notification Integration

Connect agent output to Home Assistant notifications:

```yaml
# .claude/skills/notification-bridge.yaml (concept)

automation:
  - id: documentation_alert_to_notification
    alias: "Documentation Alert Handler"
    triggers:
      - trigger: event
        event_type: documentation_check_complete
    conditions:
      - condition: state
        entity_id: input_boolean.documentation_has_alerts
        state: "on"
    actions:
      - action: notify.mobile_app_danny_phone
        data:
          title: "⚠️ Documentation Alert"
          message: "{{ state_attr('input_text.documentation_alert_message', 'value') }}"
          data:
            tag: documentation_alert
            priority: high

      - action: notify.persistent_notification
        data:
          title: "📚 Documentation Needs Refresh"
          message: "{{ state_attr('input_text.documentation_alert_message', 'value') }}"
    mode: single
```

---

## Metrics & Reporting

### Check History Tracking

The agent maintains metrics in `documentation-update-log.md`:

```markdown
## Automated Check History

| Date | Status | Files Fresh | Files Stale | Action Taken |
|------|--------|-------------|-------------|--------------|
| 2026-01-26 | ✅ Fresh | 5/5 | 0 | None |
| 2026-02-02 | ✅ Fresh | 5/5 | 0 | None |
| 2026-02-09 | 🟡 Aging | 4/5 | 0 | Flagged for planning |
| 2026-02-16 | 🟡 Aging | 3/5 | 1 | Partial refresh |
| 2026-02-22 | 🔴 Stale | 0/5 | 5 | Auto-refresh triggered |
| 2026-02-23 | ✅ Fresh | 5/5 | 0 | Auto-refresh complete |

**Average Check Interval:** 7 days
**Longest Without Refresh:** 31 days (Feb 22 alert triggered)
**Total Checks:** 6
**Alerts Generated:** 1
**Auto-Refreshes:** 1
```

---

## Comparison: Manual vs Automated

### Manual Checking (Phase 1)

**Workflow:**
1. User runs `/ha-docs` manually
2. User decides when to refresh
3. Checks happen ad-hoc
4. Easy to forget

**Pros:**
- ✅ Full user control
- ✅ On-demand refreshes
- ✅ No unnecessary updates

**Cons:**
- ❌ Easy to forget documentation updates
- ❌ Docs may become stale without notice
- ❌ No audit trail of staleness

### Automated Checking (Phase 2 - This Agent)

**Workflow:**
1. Agent checks documentation weekly
2. Agent alerts if docs stale
3. Optional automatic refresh
4. Automatic logging

**Pros:**
- ✅ Never forget documentation updates
- ✅ Proactive alerts
- ✅ Automatic audit trail
- ✅ Optional auto-refresh capability
- ✅ Compliance-friendly logging

**Cons:**
- ❌ Requires scheduling setup
- ❌ May trigger unnecessary alerts (if HA hasn't released)

---

## Deployment Timeline

### Week 1: Basic Monitoring
- ✅ Set up weekly check automation
- ✅ Log results to documentation-update-log.md
- ✅ Manual refresh when alerted

### Week 2-4: Reporting Refinement
- Configure Home Assistant notifications
- Add metrics tracking to log
- Verify check accuracy

### Month 2: Optional Auto-Refresh
- Enable automatic `/ha-docs` trigger on stale detection
- Test refresh workflow
- Monitor for false positives

---

## Troubleshooting

### Issue: Agent reports "Reference file not found"

**Cause:** Reference file missing from `.claude/` directory

**Solution:**
```bash
/ha-docs
```
This will create all missing reference files.

---

### Issue: Agent skips checking certain files

**Cause:** File doesn't have `Date:` field in header

**Solution:** Ensure all reference files have proper header:
```markdown
# Home Assistant [Feature] Reference

**Source:** https://www.home-assistant.io/docs/[path]/
**Date:** 2026-01-26
**Purpose:** [Description]
```

---

### Issue: Alerts trigger too frequently

**Cause:** Threshold too aggressive (documentation just over 30 days)

**Solution:** Adjust in automation:
- Increase threshold to 35 days if HA hasn't released
- Or adjust check frequency (biweekly instead of weekly)

---

## Related Documentation

- **Phase 1 Manual Checking:** `.claude/skills/ha-doc-currency-checker.md`
- **Manual Documentation Updater:** `.claude/skills/ha-documentation-updater.md`
- **Update Log:** `.claude/documentation-update-log.md`
- **Validators Using Docs:**
  - `.claude/skills/ha-yaml-quality-reviewer.md`
  - `.claude/skills/ha-entity-reference-validator.md`

---

## FAQ

### Q: How is this different from Phase 1?

**A:** Phase 1 (ha-doc-currency-checker) provides the checking logic that validators can use manually. Phase 2 (this agent) automates those checks on a schedule without user intervention.

### Q: Can I customize the check schedule?

**A:** Yes. Modify the Home Assistant automation trigger:
```yaml
- trigger: time
  at: "09:00:00"        # Change time
  weekday: "sun"        # Change day (mon-sun)
```

Or use time_pattern for more complex schedules:
```yaml
- trigger: time_pattern
  hours: "*/12"         # Every 12 hours
```

### Q: What if I want to disable the agent?

**A:** In Home Assistant, disable the automation:
- Go to Settings > Automations
- Find "Documentation: Weekly Currency Check"
- Click the toggle to disable

### Q: Can I run manual checks while automation is active?

**A:** Yes. Both manual `/ha-docs` and automated checks can coexist. The agent simply logs whatever it finds.

### Q: How much time does each check take?

**A:**
- **Status check only:** <1 second (just reads file dates)
- **With auto-refresh:** 30-90 seconds (depends on internet speed)

### Q: What if documentation refresh fails?

**A:** The agent logs the failure:
```markdown
### 2026-02-22 09:05 UTC (Automated Refresh - FAILED)
**Status:** ❌ Refresh Failed
**Reason:** Network timeout on home-assistant.io
**Action:** Manual refresh required
**Next Attempt:** 2026-03-01 09:00 UTC
```

---

## Implementation Status

### Phase 2 (Current)

- ✅ Agent design documented
- ✅ Workflow defined
- ✅ Deployment models described
- ✅ Check algorithm documented
- ⏳ **READY FOR DEPLOYMENT:** Set up Home Assistant automation

### Future Enhancements

- Email notifications on stale alerts
- Slack/Discord integration
- Custom threshold per validator
- Documentation diff reporting (what changed)
- Version tracking for HA compatibility

---

**Agent Created:** 2026-01-26
**Status:** Ready for Home Assistant Integration
**Priority:** Low - Optional Enhancement (Phase 2)
**Recommendation:** Deploy in Month 2 after Phase 1 stabilizes

