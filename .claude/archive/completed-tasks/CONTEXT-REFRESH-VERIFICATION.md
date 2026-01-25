# Context Refresh Verification Tests

**Purpose:** Verify that the post-compaction context refresh strategy works correctly
**Created:** 2026-01-25
**Status:** Ready for Testing

---

## Test 1: Minimal Context Refresh

**Simulates:** New session after conversation compaction

**Command to Run:**
```
Read .claude/skills/README.md and .claude/skills/ha-known-error-detector.md
```

**After Running, Ask These Questions:**

1. **Skills Inventory:**
   ```
   Question: "How many skills are available and what are they?"
   Expected: Claude lists exactly 13 skills with brief descriptions

   Skills to verify:
   ✓ HA Documentation Updater
   ✓ HA Motion Consolidator
   ✓ HA YAML Quality Reviewer
   ✓ HA Consolidation Analyzer
   ✓ HA Reflection Reviewer
   ✓ HA Room Documentation Generator
   ✓ 7 other skills (check skills/README.md)
   ```

2. **Error Patterns:**
   ```
   Question: "What 7 critical error patterns should you prevent?"
   Expected: Claude lists all 7 patterns with examples

   Patterns to verify:
   ✓ Pattern 1: response_variable syntax
   ✓ Pattern 2: Entity domain mismatch
   ✓ Pattern 3: Condition descriptions
   ✓ Pattern 4: Unquoted emoji strings
   ✓ Pattern 5: Automation ID format
   ✓ Pattern 6: Timer placement
   ✓ Pattern 7: Unsafe attribute access
   ```

3. **Workflow Knowledge:**
   ```
   Question: "What's the standard optimization workflow?"
   Expected: Claude describes phases 0-6

   Phases to verify:
   ✓ Phase 0: Refresh docs (optional)
   ✓ Phase 1: Analyze
   ✓ Phase 2: Consolidate
   ✓ Phase 3: Review
   ✓ Phase 4: Document
   ✓ Phase 5: Commit & test
   ✓ Phase 6: Monthly reflection
   ```

**Pass Criteria:**
- ✓ Claude can list all 13 skills
- ✓ Claude can list all 7 error patterns
- ✓ Claude understands workflow phases
- ✓ Responses are immediate (no "I don't have context" messages)

**Token Cost:** ~12,000 tokens

---

## Test 2: Task-Specific Context Loading

**Simulates:** Starting specific work after minimal context

**Starting Point:** Complete Test 1 first (have minimal context loaded)

**Scenario 1: Automation Review**
```
User says: "I need to review the kitchen automations for quality."

Expected Claude response:
- Acknowledges task
- Says "Let me load validation context"
- Reads ha-yaml-quality-reviewer.md and ha-consolidation-analyzer.md
- Then asks about the kitchen.yaml file

Verification:
✓ Claude proactively loads validation skills
✓ Claude can reference severity levels (CRITICAL/MEDIUM/LOW)
✓ Claude can score consolidation opportunities
```

**Scenario 2: Room Documentation**
```
User says: "Continue documenting rooms."

Expected Claude response:
- Acknowledges task
- Says "Let me load documentation context"
- Reads ROOM-DOCUMENTATION-PROGRESS.md and AGENT-HA-ROOM-DOCUMENTATION.md
- Identifies completed rooms (6/11)
- Lists remaining rooms
- Asks which to document next

Verification:
✓ Claude knows 6/11 rooms are done
✓ Claude lists remaining rooms correctly
✓ Claude can reference room documentation template
✓ Claude knows methodology from agent spec
```

**Scenario 3: Error Correction**
```
User says: "I got an error about response_variable syntax."

Expected Claude response:
- Recognizes Pattern 1 from error detector
- Explains correct syntax: response_variable: (singular)
- Shows example of fix
- Prevents future occurrences

Verification:
✓ Claude identifies pattern immediately
✓ Claude provides correct syntax
✓ Claude explains why it was wrong
✓ Claude suggests validation to prevent future errors
```

**Pass Criteria:**
- ✓ Task-specific context loads automatically
- ✓ Claude knows what's been done (6/11 rooms)
- ✓ Claude recognizes error patterns
- ✓ No manual context specification needed

**Token Cost:** 3-8K tokens per task-specific load

---

## Test 3: Full Context Refresh

**Simulates:** Returning after 1+ week break

**Command to Run:**
```
Read .claude/skills/README.md, .claude/skills/ha-known-error-detector.md,
.claude/REFLECTION-METRICS.md, and .claude/ROOM-DOCUMENTATION-PROGRESS.md
```

**After Running, Ask These Questions:**

1. **Skills + Errors (Same as Test 1):**
   ```
   Question: "What skills and error patterns do you know?"
   Expected: Same as Test 1 (all 13 skills, all 7 patterns)
   ```

2. **Project Status:**
   ```
   Question: "What's the status of room documentation?"
   Expected: Claude states 6/11 rooms complete

   Details to verify:
   ✓ 6 completed rooms: Kitchen, Office, Living Room, Bedroom, Stairs, Porch
   ✓ 5 remaining rooms: Bathroom, Garden, Guest Bedroom, Hallway, Utility
   ✓ Knows which room is next
   ✓ Can reference methodology
   ```

3. **Improvement Metrics:**
   ```
   Question: "What are the current error trends?"
   Expected: Claude references January reflection data

   Data to verify:
   ✓ Error rate: 30% (January)
   ✓ Top issues: response_variable, entity mismatches, etc.
   ✓ Validation rules: Latest updates
   ✓ Improvement target: Reduce to <20% by end of Q1
   ```

4. **Next Steps:**
   ```
   Question: "What should we work on next?"
   Expected: Claude suggests based on status

   Could suggest:
   ✓ Continue room documentation (bathroom next)
   ✓ Run reflection on newer commits
   ✓ Quality review on in-progress room
   ✓ Continue other active work
   ```

**Pass Criteria:**
- ✓ All 13 skills and 7 patterns known (Test 1 criteria)
- ✓ Project status is accurate (6/11 rooms)
- ✓ Improvement metrics are cited
- ✓ Claude can recommend next steps
- ✓ Session is immediately productive

**Token Cost:** ~30,000 tokens

---

## Test 4: Automatic Context Detection

**Simulates:** Claude proactively loading context based on user words

**After minimal context load, say these things and observe:**

| User Says | Expected Detection | Expected Load |
|-----------|-------------------|----------------|
| "Review the office automations" | Automation validation | ha-yaml-quality-reviewer.md |
| "Continue the bedroom docs" | Room documentation | ROOM-DOCUMENTATION-PROGRESS.md |
| "Error about entity domain" | Error pattern match | Cites Pattern 2 from detector |
| "Consolidate these 5 automations" | Consolidation work | ha-motion-consolidator.md |
| "Monthly reflection time" | First of month | ha-reflection-reviewer.md |
| "I found a pattern..." | Pattern analysis | Matches against known patterns |

**Pass Criteria:**
- ✓ Claude detects task from user words
- ✓ Loads relevant context without asking
- ✓ Refers to loaded skills in responses
- ✓ Prevents errors using known patterns

---

## Test 5: Context Persistence Within Session

**Simulates:** Context staying available without re-loading

**Procedure:**
```
1. Load minimal context (Test 1)
2. Ask skill question → Should answer from loaded context
3. Ask error pattern question → Should answer from loaded context
4. Ask skill question again → Should still know, no re-load needed
5. Continue working for 10+ messages → Context should remain
```

**Pass Criteria:**
- ✓ No need to re-load context during single session
- ✓ Can reference skills and patterns consistently
- ✓ Work continues smoothly
- ✓ Context doesn't need manual refresh

---

## Test 6: Archive & Retrieval

**Simulates:** Finding archived files when needed

**Command to Run (When needed):**
```
For historical reflection from October 2025:
Read .claude/archive/reflections/2025-10/REFLECTION-KITCHEN-2025-10-15.md
```

**Pass Criteria:**
- ✓ Archive directories exist with correct structure
- ✓ Files can be found and loaded
- ✓ User doesn't need to manually organize
- ✓ Historical context is available

---

## Full Verification Workflow

**Simulate complete user experience:**

### Session 1: New Session After Compaction
1. ✓ Run minimal context refresh
2. ✓ Complete Test 1 (verify skills and errors)
3. ✓ Ask 2-3 work questions
4. ✓ Observe automatic context detection (Test 4)
5. **Result:** Productive session despite context loss

### Session 2: After 1 Week Break
1. ✓ Run full context refresh
2. ✓ Complete Test 3 (verify skills, errors, metrics, status)
3. ✓ Ask "What's next?" and get project-aware suggestion
4. ✓ Continue work immediately
5. **Result:** Full awareness restored, productivity maintained

### Session 3: Within Same Day
1. ✓ NO refresh needed (context still loaded)
2. ✓ Complete Test 5 (persistence check)
3. ✓ Continue working from where you left off
4. **Result:** Seamless continuation

---

## Success Criteria Summary

**Minimal Refresh (Test 1):**
- ✓ All 13 skills accessible
- ✓ All 7 error patterns known
- ✓ Workflow phases understood
- ✓ Ready for most tasks

**Task-Specific (Test 2):**
- ✓ Automatic loading works
- ✓ Context matches task
- ✓ Error patterns detected
- ✓ No manual specification needed

**Full Refresh (Test 3):**
- ✓ All minimal + project status
- ✓ Improvement metrics known
- ✓ Next steps identified
- ✓ Session immediately productive

**Automatic Detection (Test 4):**
- ✓ Claude infers task from words
- ✓ Loads relevant context
- ✓ Prevents errors using patterns
- ✓ Seamless experience

**Overall Strategy:**
- ✓ Minimal context: 12K tokens, 2 minutes
- ✓ Full context: 30K tokens, 5 minutes
- ✓ Effective immediately
- ✓ Minimal token cost
- ✓ Maximal productivity

---

## Test Execution Log

**When you run the tests, record results here:**

| Test | Date | Result | Notes |
|------|------|--------|-------|
| Test 1: Minimal | TBD | PENDING | |
| Test 2: Task-Specific | TBD | PENDING | |
| Test 3: Full | TBD | PENDING | |
| Test 4: Auto-Detection | TBD | PENDING | |
| Test 5: Persistence | TBD | PENDING | |
| Test 6: Archive | TBD | PENDING | |

---

## Known Limitations & Workarounds

### Limitation 1: Compaction Timing
**Issue:** Conversation compaction happens automatically; timing unpredictable
**Workaround:** Keep `.claude/README.md` bookmarked; refresh proactively when changing topics

### Limitation 2: File Size Limits
**Issue:** Can't load entire codebase in context
**Workaround:** Load `.claude/` files first (provide index), then specific code files as needed

### Limitation 3: Cross-Session Memory
**Issue:** Context doesn't persist between completely separate sessions
**Workaround:** Use `.claude/` files as authoritative source of truth; re-load each session

---

## Iteration & Improvement

**If tests reveal issues:**
1. Document the issue
2. Update strategy file
3. Adjust commands/workflow
4. Re-test
5. Commit changes

**This strategy is not static.** It improves monthly as we learn what works best.

---

## Created: 2026-01-25
Status: Ready for Testing
Last Updated: 2026-01-25
