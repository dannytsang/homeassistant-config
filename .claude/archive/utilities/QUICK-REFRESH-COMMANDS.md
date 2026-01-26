# Quick Context Refresh Commands

**Print this page or bookmark it for easy access in new sessions**

---

## Copy-Paste Commands

### 🟢 Minimal Refresh (Recommended Every Session)
```
Read .claude/skills/README.md and .claude/skills/ha-known-error-detector.md
```
**Time:** 2 minutes | **Cost:** 12K tokens | **Gives:** Full skill index + error patterns

---

### 🔵 Full Refresh (After 1+ Week Break)
```
Read .claude/skills/README.md, .claude/skills/ha-known-error-detector.md, .claude/REFLECTION-METRICS.md, and .claude/ROOM-DOCUMENTATION-PROGRESS.md
```
**Time:** 5 minutes | **Cost:** 30K tokens | **Gives:** Skills + errors + metrics + project status

---

## Task-Specific Additions

### 📝 Automation Review/Validation
After minimal refresh, add:
```
Load validation context: Read .claude/skills/ha-yaml-quality-reviewer.md and .claude/skills/ha-consolidation-analyzer.md
```

### 🛏️ Room Documentation
After minimal refresh, add:
```
Load documentation context: Read .claude/ROOM-DOCUMENTATION-PROGRESS.md and .claude/AGENT-HA-ROOM-DOCUMENTATION.md
```

### 🔄 Consolidation Work
After minimal refresh, add:
```
Load consolidation context: Read .claude/skills/ha-motion-consolidator.md and .claude/skills/ha-consolidation-analyzer.md
```

### 📊 Monthly Reflection
After minimal refresh, add:
```
Load reflection context: Read .claude/skills/ha-reflection-reviewer.md and .claude/REFLECTION-METRICS.md
```

### 📚 Documentation System
After minimal refresh, add:
```
Load doc system context: Read .claude/skills/ha-documentation-updater.md, .claude/documentation-update-log.md, and .claude/HA-DOCUMENTATION-PROJECT-STATUS.md
```

---

## What Gets Loaded

### Minimal Refresh Includes:
- ✅ All 13 skill names and descriptions
- ✅ When to use each skill
- ✅ Standard workflows
- ✅ 7 critical error patterns
- ✅ Error examples and prevention
- ✅ Quick reference checklists

### What You Can Do After Minimal Refresh:
- ✅ Ask "What skills are available?"
- ✅ Ask "What error patterns should I avoid?"
- ✅ Start most automation work
- ✅ Request task-specific context
- ✅ Direct new work sessions

---

## Error Patterns You'll Know (Minimal Refresh)

After loading minimal context, you can prevent these 7 errors:

1. **response_variable syntax** - Use `response_variable:` (singular)
2. **Entity domain mismatch** - Action domain must match entity
3. **Condition descriptions** - Use `alias:` not `description:`
4. **Unquoted emojis** - Quote emoji strings like "🔔"
5. **Automation ID format** - Must be 13-digit numeric strings
6. **Timer placement** - Must be at top-level, unconditional
7. **Unsafe attribute access** - Use `|int(0)` or `|default()` filters

---

## Project Status You'll Know (Full Refresh)

After loading full context, you'll know:
- Room documentation: 6/11 complete (next: bathroom, garden, etc.)
- Error rate: Currently 30% (working to improve)
- Validation rules: Updated monthly
- Active projects: What's being worked on

---

## When to Load Full vs Minimal

**Use Minimal When:**
- ✅ Continuing in the same session
- ✅ Starting a new session with clear task
- ✅ First time loading after compaction
- ✅ Context refreshing mid-session

**Use Full When:**
- ✅ Returning after 1+ week break
- ✅ Need project status/metrics
- ✅ Don't remember what's active
- ✅ Starting major new initiative

---

## Pro Tips

### Tip 1: Load Incrementally
Start minimal, then add task-specific as you go. More efficient.

### Tip 2: Check Project Status First
Always ask "What's the status?" after loading full context. Prevents duplicated work.

### Tip 3: Trust Error Detection
After loading, Claude automatically detects error patterns. No need to manually reference.

### Tip 4: HA References Load On-Demand
Don't load HA reference docs unless validating syntax. They're available via skills.

### Tip 5: Create New Task File Early
When starting new work, create a PROGRESS or STATUS file immediately. Easier to track.

---

## Quick Decision Tree

```
New session after compaction?
  ├─ Remember what you're doing?
  │   ├─ Yes → Minimal refresh
  │   └─ No → Full refresh
  │
  ├─ First session with no context?
  │   ├─ Specific task known → Minimal refresh
  │   └─ Just getting started → Full refresh
  │
  └─ Continuing same day?
      └─ (Don't need refresh, context still fresh)
```

---

## File Organization Reminder

**Always loaded from:**
- `skills/` - All 13 skill files
- `ha-*-reference.md` - Syntax references
- Main `.claude/` directory - Current projects

**Historical files in:**
- `archive/reflections/[YYYY-MM]/` - Old reflections
- `archive/scans/[YYYY]/` - Old scan reports
- `archive/projects/[name]/` - Completed projects

---

## Next Steps After Loading Context

1. **After Minimal:**
   - Confirm: "List all available skills"
   - Confirm: "List error patterns to prevent"
   - Ask: "What would you like to work on?"

2. **After Full:**
   - Ask: "What's the status of active projects?"
   - Ask: "What should we work on next?"
   - Plan: Next session goals

3. **During Work:**
   - Load task-specific context as needed
   - Ask for HA reference docs when validating
   - Request skill tutorials for unfamiliar work

---

## Emergency: Lost Context

If you're confused about what's been done:
```
Tell me everything. Read .claude/README.md, then read
.claude/ROOM-DOCUMENTATION-PROGRESS.md and .claude/REFLECTION-METRICS.md
```

This gives you:
- Complete context refresh strategy
- Current project status
- Error trends and improvements
- Enough to figure out what's active

---

## Need Help?

- **"What's in my context?"** → Read `README.md` to understand the strategy
- **"What should I load?"** → Check task-specific section above
- **"Where's the documentation?"** → Check `archive/` if not in main
- **"How do I archive?"** → Read `ARCHIVING-STRATEGY.md`
- **"What's the error?"** → Check `ha-known-error-detector.md` in minimal context

---

## Created: 2026-01-25
Version: 1.0
Last Updated: 2026-01-25
