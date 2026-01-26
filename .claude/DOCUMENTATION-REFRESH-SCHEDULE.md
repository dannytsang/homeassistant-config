# Home Assistant Documentation Refresh Schedule

**Document Version:** 1.0
**Created:** 2026-01-26
**Status:** Active - Guiding quarterly documentation updates
**Related:** Skills #0 (ha-documentation-updater), #0.3 (ha-documentation-reference-agent)

---

## Purpose

Establish a predictable schedule for refreshing Home Assistant reference documentation to ensure our local cache stays aligned with official HA releases and new features.

---

## HA Release Schedule

Home Assistant releases new versions on a **monthly cycle**:
- **Pattern:** First Wednesday or Thursday of each month (typically Wed)
- **Time:** Usually released mid-morning UTC
- **Versions:** X.Y.0 format (major.minor.patch)

**2026 Release Dates (Projected):**
| Month | Projected Release | Friday Refresh |
|-------|-------------------|-----------------|
| January | Wed, Jan 1 | Fri, Jan 3 |
| February | Thu, Feb 5 | Fri, Feb 6 |
| March | Wed, Mar 4 | Fri, Mar 6 |
| April | Wed, Apr 1 | Fri, Apr 3 |
| May | Thu, May 7 | Fri, May 8 |
| June | Wed, Jun 4 | Fri, Jun 6 |
| July | Wed, Jul 2 | Fri, Jul 4 |
| August | Thu, Aug 7 | Fri, Aug 8 |
| September | Wed, Sep 3 | Fri, Sep 5 |
| October | Thu, Oct 2 | Fri, Oct 3 |
| November | Wed, Nov 5 | Fri, Nov 7 |
| December | Thu, Dec 4 | Fri, Dec 5 |

---

## Documentation Refresh Strategy

### Phase 1: Quarterly Manual Refreshes (Current)

**Trigger:** Every 3 months, starting April 2026

**Schedule:**
- **Q2 2026** - Friday, April 3 (after April release)
- **Q3 2026** - Friday, July 4 (after July release)
- **Q4 2026** - Friday, October 3 (after October release)
- **Q1 2027** - Friday, January 2 (after January release)

**How to Execute:**
1. Run the `/ha-docs` skill manually
2. Skill fetches latest HA documentation from home-assistant.io
3. Compare with local cache (`.claude/home-assistant-*.md` files)
4. Update any files that changed
5. Log results to `documentation-update-log.md`
6. Review new features/deprecations listed in audit trail

**Command:**
```
/ha-docs
```

**Expected Output:**
- Status of each reference file (fresh, aged, stale)
- What changed (new features, deprecated patterns, syntax changes)
- List of files updated with byte changes
- Audit trail entry created

---

### Phase 2: Automated Weekly Checks (Future - ~April 2026)

**When Available:** After Phase 2 agent (ha-documentation-reference-agent) is deployed to Home Assistant

**Deployment:** Use Home Assistant automation to run weekly checks:
- **Trigger:** Every Sunday 9 AM UTC
- **Action:** Check documentation age, alert if stale (>30 days)
- **Optional:** Auto-refresh if stale
- **Result:** Proactive monitoring with audit logging

**Status:** Planned but not yet active
**Related:** `.claude/skills/ha-documentation-reference-agent.md`

---

## Reference Files Covered

The documentation refresh updates these reference files:

| File | Purpose | Last Updated | Age |
|------|---------|--------------|-----|
| `home-assistant-automation-yaml-reference.md` | Automation syntax and patterns | 2026-01-22 | 4 days |
| `home-assistant-scripts-reference.md` | Script syntax and examples | 2026-01-22 | 4 days |
| `home-assistant-templating-reference.md` | Jinja2 templating reference | 2026-01-22 | 4 days |
| `home-assistant-splitting-configuration-reference.md` | Configuration splitting guide | 2026-01-22 | 4 days |
| `home-assistant-template-sensors-reference.md` | Template sensor integration | 2026-01-25 | 1 day |

**Total Cache:** ~119 KB of reference documentation

---

## What Triggers a Refresh

### Recommended Refresh Times

**✅ DO refresh documentation when:**
1. **Monthly HA release occurs** (1st Wed/Thu of month)
2. **Quarterly audit scheduled** (Q2/Q3/Q4/Q1)
3. **Before major automation work** (ensure latest features known)
4. **When notified of deprecations** (during skill usage)
5. **When documentation >30 days old** (Phase 2 agent alerts)

### What Triggers Automatic Alerts

**Phase 1 (Manual):**
- Validators check doc age before running (ha-doc-currency-checker utility)
- If docs >30 days old: Alert displayed, optional to proceed or refresh first

**Phase 2 (Automated - Future):**
- Weekly automatic check (Sundays 9 AM UTC)
- Proactive alert if docs exceed 30-day threshold
- Optional auto-refresh capability

---

## Documentation Update Audit Trail

All refresh executions are logged in `.claude/documentation-update-log.md`:

**Log Entry Format:**
```markdown
### 2026-04-03 14:30 UTC (Quarterly Refresh - Q2)
**Status:** ✅ Updated
**Trigger:** Quarterly refresh (after April 2026 HA release)

**Files Updated:**
- home-assistant-automation-yaml-reference.md (+/- bytes)
- home-assistant-scripts-reference.md (unchanged)
- (etc.)

**Changes Detected:**
- New: Feature X in automation docs
- Deprecated: Old pattern Y (replaced with Z)
- Modified: Section description updated

**Docs Age Before:** 90 days
**Docs Age After:** 0 days
**Next Scheduled:** 2026-07-04
```

---

## Integration with Skills

### Phase 1: Manual Refresh Skill

**Skill:** ha-documentation-updater.md
**Status:** Production ready (tested 2026-01-25)
**Usage:** `Command /ha-docs`

**Capabilities:**
- ✅ Fetch latest HA docs from home-assistant.io
- ✅ Compare with local cache
- ✅ Auto-update changed files
- ✅ Create audit trail entries
- ✅ Report new features and deprecations

### Phase 2: Automated Monitoring Agent

**Agent:** ha-documentation-reference-agent.md (Skill #0.3)
**Status:** Ready for deployment (~April 2026)
**Integration:** Home Assistant automation

**Capabilities:**
- ✅ Weekly automatic checks (configurable)
- ✅ Color-coded status reporting (Fresh/Aging/Stale)
- ✅ Alerts when docs exceed 30-day threshold
- ✅ Optional auto-refresh on stale detection
- ✅ Continuous audit logging

**Deployment:** Create Home Assistant automation using examples from skill documentation

---

## Responsibilities & Ownership

### Documentation Maintenance Owner
- **Primary:** User (danny)
- **Frequency:** Quarterly manual refreshes
- **Timeline:** April 3, July 4, October 3, January 2
- **Tools:** `/ha-docs` skill

### Phase 2 Automated Monitoring (Future)
- **Setup Owner:** User
- **Deployment Date:** ~April 2026 (target)
- **Ongoing:** Home Assistant automation runs independently
- **Alerts:** Notifications via Home Assistant + documentation-update-log.md

---

## Getting Started: April 2026 Refresh

**Timeline:**
1. **April 1 (Tue)** - HA 2026.04 releases (projected)
2. **April 3 (Fri)** - Execute first quarterly refresh:
   ```
   /ha-docs
   ```
3. **April 3 (Fri) - Same day** - Review output:
   - Check what changed in automation docs
   - Verify scripts syntax is current
   - Note any deprecations
4. **April 3 (Fri)** - Optional: Update team with findings

**Expected Output:**
- Refreshed reference files (dates updated to 2026-04-03)
- Audit entry in documentation-update-log.md
- Report of new features/deprecations found
- Ready for next quarterly refresh (July 4)

---

## Quarterly Schedule Summary

**Q2 2026 (April-June)**
- Refresh Date: Friday, April 3, 2026
- Trigger: Post-April HA release (v2026.04)
- Status: ⏳ Scheduled

**Q3 2026 (July-September)**
- Refresh Date: Friday, July 4, 2026
- Trigger: Post-July HA release (v2026.07)
- Status: ⏳ Scheduled

**Q4 2026 (October-December)**
- Refresh Date: Friday, October 3, 2026
- Trigger: Post-October HA release (v2026.10)
- Status: ⏳ Scheduled

**Q1 2027 (January-March)**
- Refresh Date: Friday, January 2, 2027
- Trigger: Post-January HA release (v2027.01)
- Status: ⏳ Scheduled (beyond current quarter)

---

## Pre-Refresh Checklist

Before executing a quarterly refresh:

- [ ] Confirm HA release happened (check home-assistant.io)
- [ ] Read current documentation-update-log.md (understand what's stale)
- [ ] Check if docs are already current (run `/ha-docs` to see status)
- [ ] If docs >30 days old: Proceed with refresh
- [ ] If docs <14 days old: Optional - can skip or refresh anyway for completeness
- [ ] Set aside 5-10 minutes for refresh execution
- [ ] Plan to review new features/deprecations found

---

## Post-Refresh Actions

After executing a quarterly refresh:

1. **Review audit trail** - Check documentation-update-log.md for changes
2. **Note new features** - Add to team awareness
3. **Flag deprecations** - Alert if old patterns need updating
4. **Update validators** (if needed) - Ensure validation skills reflect new capabilities
5. **Document findings** - Keep notes for quarterly reflection
6. **Log in TODO.md** - Record when refresh was executed
7. **Commit changes** - Git commit for documentation-update-log.md entry

**Example Post-Refresh Commit:**
```
chore: refresh documentation for Q2 2026 (April release)

- Updated reference files from home-assistant.io
- New features identified: [list]
- Deprecations noted: [list]
- Audit trail entry created in documentation-update-log.md
- Docs age reset to 0 days (2026-04-03)
```

---

## FAQ

### Q: What if I miss a quarterly refresh date?

**A:** No problem - documentation is still usable. Just run the refresh when you remember:
- If <30 days overdue: Low priority, can defer a few days
- If 30+ days overdue: Should refresh before major work
- Validators will alert if docs are stale (Phase 1) or automated agent will alert (Phase 2)

### Q: What if HA releases an emergency patch?

**A:** Our quarterly schedule is based on major releases (X.Y.0). Emergency patches (X.Y.Z) don't require refreshes unless they introduce new automation syntax. Just proceed normally with next quarterly refresh.

### Q: Can I refresh more frequently than quarterly?

**A:** Yes! Feel free to run `/ha-docs` anytime:
- Before major automation work
- After seeing new HA announcements
- To get latest documentation
- Just run the skill manually

### Q: What's the difference between Phase 1 and Phase 2?

**A:**
- **Phase 1 (Current):** Manual quarterly refreshes (you run `/ha-docs`)
- **Phase 2 (Future):** Automated weekly checks + optional auto-refresh

Both can coexist. Phase 1 ensures quarterly updates, Phase 2 provides proactive monitoring.

### Q: How do I know if docs are stale?

**A:** Multiple ways:
1. **Validators alert** - When running review/validation skills
2. **Manual check** - Run `/ha-docs` to see status
3. **Visual check** - Look at `.claude/documentation-update-log.md` for last update
4. **Phase 2 agent** (future) - Automatic weekly alerts

### Q: What if documentation on home-assistant.io is down?

**A:** The `/ha-docs` skill will report the error. Either:
- Retry in a few hours
- Skip refresh for now (docs remain as-is)
- Continue working with current documentation

This is rare but possible during HA.io maintenance.

---

## Integration with Task Management

### Related Tasks

- **Task #1** ✅ - Test ha-documentation-updater skill (COMPLETED 2026-01-25)
- **Task #2** ✅ - Create Phase 2 agent (COMPLETED 2026-01-26)
- **Task #3** 🎯 - Establish refresh schedule (THIS TASK - 2026-01-26)

### Upcoming Work

- **Deploy Phase 2 agent:** Home Assistant automation setup (~April 2026)
- **Execute Q2 refresh:** First quarterly refresh (April 3, 2026)
- **Continue quarterly:** July 4, October 3, January 2 (ongoing)

---

## References

- **Documentation Updater Skill:** `.claude/skills/ha-documentation-updater.md`
- **Reference Agent (Phase 2):** `.claude/skills/ha-documentation-reference-agent.md`
- **Currency Checker Utility:** `.claude/skills/ha-doc-currency-checker.md`
- **Update Audit Log:** `.claude/documentation-update-log.md`
- **HA Official Docs:** https://www.home-assistant.io/docs/

---

**Schedule Created:** 2026-01-26
**First Refresh:** April 3, 2026
**Frequency:** Quarterly (every ~90 days)
**Automation Level:** Manual (Phase 1) → Automated (Phase 2 planned)
**Owner:** User

