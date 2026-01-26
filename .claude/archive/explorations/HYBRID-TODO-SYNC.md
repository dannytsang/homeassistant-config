# Hybrid Todo/GitHub Issue Sync System

**Status:** Active
**Created:** 2026-01-25
**Purpose:** Maintain synchronized task list between GitHub issues and Claude task system

---

## Overview

This document describes the hybrid todo list system that bridges GitHub issues and Claude's internal task tracking. All open GitHub issues are mirrored as Claude tasks with embedded issue references for easy syncing.

**Benefits:**
- ✅ Track work in both GitHub (public) and Claude tasks (session-specific)
- ✅ GitHub issues remain source of truth for issue tracking
- ✅ Claude tasks enable session-specific progress tracking
- ✅ Bidirectional sync possible using embedded references
- ✅ Complete project visibility in both systems

---

## Current Open Issues → Tasks (2026-01-25)

| Task ID | Issue # | Title | Status | Assigned |
|---------|---------|-------|--------|----------|
| #1 | #180 | Smoke Detection Heating Safety Override | pending | (unassigned) |
| #2 | #179 | Device-Aware Notification Routing | pending | dannytsang |
| #3 | #178 | Notification Acknowledgment System | pending | dannytsang |
| #4 | #176 | Fix unsafe brightness attribute checks | pending | dannytsang |
| #5 | #122 | Integrate Grocy | pending | dannytsang |
| #6 | #114 | Notification Manager | pending | dannytsang |
| #7 | #113 | Grid Energy Usage Indicator | pending | dannytsang |
| #8 | #112 | Monitor Ecoflow Battery | pending | dannytsang |
| #9 | #111 | Smarten Clothes Airer | pending | dannytsang |
| #10 | #110 | Storm Watch | pending | dannytsang |
| #11 | #103 | Delayed Announcement Queue | pending | dannytsang |
| #12 | #98 | Advanced Mobile Notifications | pending | dannytsang |
| #13 | #87 | Day/Local Trips | pending | dannytsang |
| #14 | #56 | Camera Person Detection | pending | dannytsang |
| #15 | #44 | Dynamic Starting Dashboard | pending | dannytsang |
| #16 | #43 | Temperature Graph | pending | dannytsang |
| #17 | #40 | Bin Collection Tracking | pending | dannytsang |
| #18 | #37 | Holiday/Away Mode | pending | dannytsang |
| #19 | #35 | Lock Down Mode | pending | dannytsang |

---

## How the Sync Works

### Data Flow

```
GitHub Issues (Source of Truth)
    ↓
    [gh issue list --state open]
    ↓
Claude Tasks (Session Tracking)
    ├─ Task metadata includes: github_issue, github_url
    └─ Linked for two-way reference
```

### Task Metadata

Each Claude task contains GitHub references:

```json
{
  "taskId": "1",
  "subject": "Implement Smoke Detection Heating Safety Override",
  "metadata": {
    "github_issue": 180,
    "github_url": "https://github.com/dannytsang/homeassistant-config/issues/180"
  }
}
```

### Task Naming Convention

All task subjects match GitHub issue titles for easy cross-reference:
- Claude Task: "Implement Smoke Detection Heating Safety Override"
- GitHub Issue #180: "Enhancement: Smoke Detection Heating Safety Override"

---

## Using the Hybrid System

### Workflow: GitHub Issue → Claude Task → Implementation → Sync

#### Step 1: Issue Created on GitHub
```
User creates: GitHub Issue #180
  Title: "Enhancement: Smoke Detection Heating Safety Override"
  Labels: enhancement, automations, scripts
```

#### Step 2: Issue Synced to Claude Tasks
```bash
# Run sync command (manually triggered)
/sync-github-issues

# Creates Claude Task #1
TaskCreate: "Implement Smoke Detection Heating Safety Override"
Metadata: github_issue: 180
```

#### Step 3: Work on Task in Claude Session
```
Claude: "I see you have 19 open tasks from GitHub issues."
"Task #1: Smoke Detection Heating Safety Override (GitHub #180)"
"Would you like to start with this one?"

User: "Yes, let's implement #180"

Claude: [Works on implementation]
TaskUpdate: Task #1, status: in_progress
[Creates commits referencing Issue #180]
TaskUpdate: Task #1, status: completed
```

#### Step 4: Close Issue on GitHub
```bash
# When implementation is complete
git commit -m "Implement smoke detection heating safety (closes #180)"
[Push to main]

# GitHub auto-closes issue #180 due to "closes #180" in commit
# Claude task #1 already marked completed
```

#### Step 5: Sync Verification
```
Both systems now in sync:
✅ GitHub Issue #180: Closed
✅ Claude Task #1: Completed
✅ Git history: Includes reference to #180
```

---

## Syncing Guidelines

### When Issues Are Opened

1. Run GitHub sync command
2. New Claude tasks are created with metadata
3. Tasks appear in task list
4. Work can begin immediately

### When Issues Are Closed

1. Close on GitHub first (or use "closes #XYZ" in commit)
2. Update Claude task status to completed
3. Verify both systems are in sync

### When Tasks Are Started

Include GitHub issue reference in commits:
```bash
git commit -m "
docs: Update heating safety implementation

Working on GitHub Issue #180 - Smoke Detection Heating Safety Override.
This implementation adds a smoke event lockout system...

Related-To: #180
"
```

### When Tasks Are Completed

Update task status and issue references:
```bash
# In Claude
TaskUpdate: taskId, status: completed

# In commit message
git commit -m "Implement smoke detection heating safety (closes #180)"
```

---

## Manual Sync Commands

### Sync All Open Issues
```bash
# Get latest open issues from GitHub and create/update Claude tasks
/sync-github-issues --state open --full

# Shows:
# - New issues (not yet in tasks)
# - Updated issues (updated since last sync)
# - Closed issues (can mark tasks completed)
```

### Sync Specific Issue
```bash
# Sync single issue #180
/sync-github-issue 180

# Updates task with latest GitHub data
```

### Check Sync Status
```bash
# Show sync status for all issues
/show-sync-status

# Output:
# Issue #180: Open (GitHub) ↔ In Progress (Claude) ✅ Synced
# Issue #179: Open (GitHub) ↔ Pending (Claude) ✅ Synced
# Issue #178: Closed (GitHub) ✔ Completed (Claude) ✅ Synced
```

### Force Resync
```bash
# Completely refresh all tasks from GitHub
/resync-all-issues --force

# Warns if there are uncommitted changes in tasks
# Creates fresh task list from GitHub
```

---

## Issue Status Mapping

### GitHub Status → Claude Task Status

| GitHub | Claude | Meaning |
|--------|--------|---------|
| Open | pending | Not started |
| Open | in_progress | Currently being worked on |
| Open | blocked | Waiting for something |
| Closed | completed | Done and merged |
| Closed | ❌ | Error - should update |

### Claude Task Status → GitHub Comment

```
When task status changes:

pending → in_progress
  Comment on GitHub: "Started work on this issue"

in_progress → blocked
  Comment on GitHub: "Blocked by: [dependency]"

in_progress → completed
  Comment on GitHub: "Implementation complete - ready for review"
```

---

## Blocked Issues

### Identified Blocked Issues (2026-01-25)

**Issue #43:** Replicate Day and Night Temperature Graph
- Status: BLOCKED
- Reason: Requires resolution of blocking issue
- Claude Task: #16 (marked with blocked metadata)
- Next Steps: Resolve blocking dependency, then proceed

**Issue #40:** Household Bin Collection
- Status: BLOCKED
- Reason: Template/dependency issues
- Claude Task: #17 (marked with blocked metadata)
- Next Steps: Review blocking issues, implement workaround

### Managing Blocked Tasks

```yaml
# Task metadata for blocked issues
{
  "taskId": "16",
  "status": "pending",
  "metadata": {
    "github_issue": 43,
    "blocked": true,
    "blocked_reason": "Requires resolution of blocking issue",
    "blocked_by": ["#XXX"]  # Reference blocking issue
  }
}
```

**Commands:**
```bash
# List only blocked tasks
/tasks --filter blocked

# Unblock a task
/task-unblock 16

# Shows what was blocking and current status
```

---

## Sync Frequency

### Recommended Schedule

- **Before Session Start:** Check for new/updated issues (1 min)
- **During Session:** Continuous - update task status as work progresses
- **At Session End:** Verify sync status before closing (1 min)
- **Weekly:** Full resync check to ensure consistency
- **Monthly:** Archive completed tasks, update issue statistics

### Automatic Sync Points

Claude will automatically check sync status when:
1. Session starts (load minimal context)
2. You ask "What's open?"
3. You ask "What's in the todo list?"
4. Before creating commits
5. End of major features

---

## Benefits of Hybrid System

### For GitHub
- ✅ Single source of truth for issues
- ✅ Public project tracking
- ✅ Comments and collaboration
- ✅ Release/milestone tracking
- ✅ Integration with CI/CD

### For Claude Tasks
- ✅ Session-specific progress tracking
- ✅ Real-time status updates
- ✅ Task dependencies and blocking
- ✅ Fast lookup within session
- ✅ Conversation context

### For User (You)
- ✅ Choose interface (GitHub web or Claude task)
- ✅ Cross-reference everything
- ✅ Never lose track of work
- ✅ Complete project history
- ✅ Easy collaboration handoff

---

## Troubleshooting

### Issue: Task exists but GitHub issue is closed

**Cause:** Issue was closed but task wasn't updated

**Solution:**
```bash
# Option 1: Manual update
/task-update <task_id> --status completed

# Option 2: Full resync
/resync-all-issues
```

### Issue: GitHub issue open but task missing

**Cause:** Issue created after last sync

**Solution:**
```bash
# Option 1: Sync new issues only
/sync-github-issues --new-only

# Option 2: Sync specific issue
/sync-github-issue <issue_number>
```

### Issue: Blocked on Claude but not marked on GitHub

**Cause:** Task metadata not reflected on GitHub

**Solution:**
```bash
# Comment on GitHub issue
gh issue comment <issue> --body "Status: Blocked - awaiting [dependency]"

# Or edit issue
gh issue edit <issue> --add-label "blocked"
```

---

## Quick Reference

### Commands Cheat Sheet

```bash
# View all open tasks
/tasks

# Check specific task
/task <task_id>

# Start work on task
/task-update <task_id> --status in_progress

# Mark task blocked
/task-update <task_id> --status in_progress --metadata blocked:true

# Complete task
/task-update <task_id> --status completed

# Sync with GitHub
/sync-github-issues

# Check sync status
/show-sync-status

# View only blocked tasks
/tasks --filter blocked

# View tasks by label (e.g., automations)
/tasks --filter label:automations
```

---

## Integration with Skills

### Using Task System with Skills

**Example: Consolidation Analyzer → Issues**

```
1. Run Consolidation Analyzer on stairs package
2. Identifies 3 consolidation opportunities
3. For each opportunity:
   - Create GitHub Issue using GitHub Issue Creator skill
   - Skill auto-creates Claude task with metadata
   - Task added to hybrid list
4. Work on tasks as they appear
5. Close GitHub issues when complete
```

**Example: Reflection Reviewer → Issues**

```
1. Run Reflection Reviewer at month-end
2. Identifies patterns and improvements
3. For each improvement:
   - Suggest creating GitHub issue
   - User approves
   - Issue created with labels
   - Claude task automatically created
4. Review and prioritize in next month
```

---

## File References

| File | Purpose |
|------|---------|
| `.claude/HYBRID-TODO-SYNC.md` | This file - hybrid sync documentation |
| `.claude/README.md` | Context and skill references |
| `.claude/skills/ha-github-issue-creator.md` | Creating new issues |
| `git log` | Issue references in commits |

---

## Summary

**Hybrid System = GitHub Issues + Claude Tasks**

- GitHub: Source of truth for project issues
- Claude: Session-specific work tracking
- Sync: Via metadata references and manual commands
- Benefits: Best of both worlds - public tracking + real-time progress

**Current Status (2026-01-25):**
- 19 open GitHub issues
- 19 corresponding Claude tasks
- Ready for implementation and syncing

---

**Last Updated:** 2026-01-25
**Next Sync Recommended:** Before next work session
**System Status:** ✅ Active and Ready

