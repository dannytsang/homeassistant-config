# Home Assistant Repository Status Review

**Skill Name:** ha-repo-status
**Purpose:** Comprehensive review of repository state including commits, PRs, issues, and file changes
**Use When:** Starting new work, after breaks, or before planning major changes

---

## Instructions

When this skill is invoked, perform a systematic review of the repository state to understand current work, pending changes, and open tasks.

### Phase 1: Git State Analysis (5 minutes)

1. **Check Current Branch & Status**
   ```bash
   git status
   git branch -a | grep -E "refactor|feature|fix"
   ```
   - Note current branch
   - Identify untracked files
   - Check for uncommitted changes
   - List active feature/refactor branches

2. **Recent Commit History**
   ```bash
   git log --oneline -15
   ```
   - Review last 15 commits for context
   - Identify recent work patterns
   - Note commit message conventions being followed

3. **Unpushed Commits**
   ```bash
   git log origin/main..HEAD --oneline
   ```
   - Check if local commits need pushing
   - Verify commit quality before push

### Phase 2: Pull Requests Review (5 minutes)

1. **List Open PRs**
   ```bash
   gh pr list --state open --json number,title,headRefName,createdAt,isDraft | jq .
   ```
   - Note PR numbers and titles
   - Check which branches have open PRs
   - Identify draft vs ready PRs

2. **For Each Open PR, Check:**
   - Branch name and purpose
   - Related issue numbers
   - Whether it needs review/testing
   - CI/check status (if applicable)

### Phase 3: Issues Analysis (10 minutes)

1. **List Open Issues**
   ```bash
   gh issue list --state open --limit 50 --json number,title,labels,createdAt | jq .
   ```
   - Group by labels (bug, enhancement, integration)
   - Note recently created issues
   - Identify high-priority items

2. **Categorize Issues:**
   - **Bugs:** Issues labeled "bug"
   - **Partially Complete:** Check issue body for checklist progress
   - **New Features:** Enhancement requests
   - **Blocked:** Issues with "blocked" label
   - **Quick Wins:** Simple tasks (1-2 hours estimate)

3. **Cross-Reference with PRs:**
   - Match open PRs to their issues
   - Identify issues being worked on
   - Find issues without PRs (available work)

### Phase 4: File Changes Review (5 minutes)

1. **Untracked Files**
   ```bash
   git status --short
   ```
   - Note documentation files (README, claude.md, review files)
   - Check for config backups or temp files
   - Identify generated files (.claude/plans/*)

2. **Modified But Uncommitted**
   - Review changes with `git diff`
   - Determine if changes should be committed or reverted

3. **Recent File Activity**
   ```bash
   git log --name-status --oneline -10
   ```
   - Identify most actively modified files
   - Note packages/areas being worked on

### Phase 5: Documentation Review (3 minutes)

1. **Check for Local Documentation**
   - `claude.md` - Technical guide (may be untracked)
   - `*_review.md` - Review documents (may be untracked)
   - `.claude/plans/*` - Active plans
   - `.claude/skills/*` - Available skills

2. **Review Plan Files**
   ```bash
   ls -lht .claude/plans/ | head -5
   ```
   - Check for recent or active plans
   - Note plan file names (contain context)

### Phase 6: Generate Summary Report

Compile findings into structured summary:

```markdown
## Repository Status Report
**Date:** [Current Date]
**Branch:** [Current Branch]

### Recent Activity
- Last commit: [Hash] - [Message] ([Date])
- Commits since last push: [Count]
- Active branches: [List]

### Open Pull Requests ([Count])
1. PR #XXX - [Title] - Branch: [name]
2. ...

### Open Issues ([Count])
**High Priority / Bugs:**
- #XXX - [Title]

**In Progress (Have PRs):**
- #XXX - [Title] → PR #YYY

**Quick Wins (1-2 hours):**
- #XXX - [Title]

**Blocked:**
- #XXX - [Title] - [Reason]

### Uncommitted Changes
- Untracked: [List files]
- Modified: [List files]
- Documentation: [List local docs]

### Recommendations
[Based on findings, suggest next actions]
```

---

## Output Format

Present findings in a clear, scannable format:
- Use headers and bullet points
- Highlight important items (bugs, blocked issues)
- Group related information
- Include file paths and line numbers where relevant
- Provide actionable recommendations

---

## Success Criteria

✅ Complete picture of repository state
✅ All open PRs identified and contextualized
✅ Issues categorized by priority and status
✅ Uncommitted changes reviewed
✅ Clear recommendations for next steps
✅ Cross-references between PRs, issues, and commits

---

## Follow-Up Actions

After generating the report:
1. **If gh auth failed:** Remind user to authenticate with `gh auth login`
2. **If commits unpushed:** Ask if they should be pushed
3. **If PRs open:** Ask if any need review/testing
4. **If untracked docs:** Ask if they should be committed
5. **Recommend next task:** Based on quick wins or high priority items

---

## Example Usage

**User:** "Run ha-repo-status skill" or "Review repository state"

**Assistant:**
- Executes all 6 phases systematically
- Generates comprehensive status report
- Provides context-aware recommendations
- Asks clarifying questions about next steps

---

## Notes

- **Authentication:** Requires `gh` CLI authenticated for PR/issue data
- **Permissions:** Read-only operations, no modifications
- **Time Estimate:** 10-15 minutes for full review
- **Frequency:** Run at session start, after long breaks, or before major work

---

## Integration with Other Skills

- **ha-package-review:** Use after identifying which package to review
- **Before implementation:** Always run this to avoid conflicts
- **After breaks:** Refresh context on current work

---

## Maintenance

Update this skill when:
- New git workflow patterns emerge
- Additional repository metadata becomes relevant
- Integration with new tools (CI/CD, project boards)
- User preferences for status reporting change
