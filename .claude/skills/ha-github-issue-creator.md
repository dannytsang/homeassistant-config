# Claude Skill: Home Assistant GitHub Issue Creator

**Status:** Production Ready
**Version:** 1.0
**Created:** 2026-01-25
**Purpose:** Create GitHub enhancement issues with proper labeling and assignment

---

## Purpose

Create GitHub enhancement issues for the Home Assistant configuration repository with automated label detection, validation, and assignment to the repository owner (dannytsang).

---

## When to Use

- **Planning enhancement discussions** - Turn planning documents into trackable issues
- **Feature requests identified during review** - Capture new ideas as issues
- **After smoke testing or validation** - Document findings that need implementation
- **Consolidation opportunities** - Create enhancement issues for identified improvements
- **Documentation improvements** - Turn documentation gaps into action items
- **Refactoring/optimization work** - Track planned technical improvements

---

## How It Works

### Step 1: Check Available Labels

Before creating any issue, the skill:
1. Fetches all available labels from the repository
2. Validates 'enhancement' exists (it always does in GitHub repos)
3. Identifies other applicable labels that exist
4. Prevents errors from attempting to apply non-existent labels

**Command:**
```bash
gh label list
```

**Output Used For:**
- Confirming 'enhancement' is available
- Finding other matching labels to apply
- Preventing "label not found" errors

### Step 2: Determine Applicable Labels

Based on issue type and content, identify which of the available labels apply:

**Label Matching Rules:**

| Issue Type | Look For | Apply If Available |
|-----------|----------|------------------|
| Room-related | `rooms`, `kitchen`, `living_room`, `bedroom`, `office`, `stairs`, etc. | Exact room name match |
| Integration | `integration: *` labels | Matches integration mentioned |
| Feature | `feature`, `enhancement` | Always apply enhancement |
| Documentation | `documentation`, `docs` | Documentation updates |
| Automation | `automations`, `automation` | Automation-related work |
| Script | `scripts`, `script` | Script modifications |
| Testing | `testing`, `test` | Testing/validation work |
| Package | `packages`, `package` | Package structure changes |
| Config | `config`, `configuration` | Configuration changes |
| Performance | `performance`, `optimization` | Performance improvements |
| Bug-related | `bug` | Only if fixing a bug |

### Step 3: Create the Issue

The skill creates a GitHub issue with:

```bash
gh issue create \
  --title "Enhancement: <Issue Title>" \
  --body "$(cat issue_body.md)" \
  --label enhancement,<other_labels>
  --assignee dannytsang
```

**Issue Structure:**

```markdown
## Summary
[1-3 sentence overview of enhancement]

## Problem / Motivation
[Why this enhancement is needed]

## Proposed Solution
[What should be implemented]

## Benefits
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

## Files Involved
- [File 1]
- [File 2]
- [File 3]

## Related Issues
- Closes #XXX (if applicable)
- Related to #YYY (if applicable)

## Additional Context
[Any other relevant information]
```

---

## Pre-Issue Checklist

Before creating an issue, verify:

- ✅ Issue is an enhancement (not a bug)
- ✅ Title is clear and specific
- ✅ Summary explains what should be done
- ✅ Benefits/motivation are documented
- ✅ Related files are identified
- ✅ No similar open issues exist
- ✅ Labels have been checked against available labels
- ✅ Issue is assigned to dannytsang

---

## Label Detection Algorithm

### Pseudo-code
```
available_labels = gh label list
applicable_labels = ["enhancement"]

for issue_mention in issue_content:
  for available_label in available_labels:
    if issue_mention.matches(available_label):
      applicable_labels.append(available_label)
      break

return applicable_labels (deduplicated)
```

### Example: Kitchen Automation Enhancement

**Issue mentions:** Kitchen, motion detection, automations, lighting

**Available labels check:**
```
✅ enhancement (always apply)
✅ automations (mentioned in issue)
✅ kitchen (mentioned in issue)
❌ motion (not in label list)
✅ integration: nest protect (mentioned in content)
```

**Final labels:** `enhancement,automations,kitchen,integration: nest protect`

---

## Common Scenarios

### Scenario 1: Motion Consolidation Opportunity

**Input:**
```
Enhancement: Consolidate stairs motion automations
The stairs package has 7 motion-related automations that can be consolidated.
Uses motion sensor, multiple light states, time-based conditions.
Related to stairs, automations, consolidation optimization.
```

**Label Check:**
```
gh label list
→ enhancement ✅
→ automations ✅
→ stairs ✅
→ optimization ❌ (not available)
```

**Issue Created:**
```
gh issue create \
  --title "Enhancement: Consolidate stairs motion automations" \
  --label enhancement,automations,stairs \
  --assignee dannytsang
```

### Scenario 2: Documentation Gap

**Input:**
```
Enhancement: Add setup documentation for office package
Office package lacks comprehensive documentation. Should include
device inventory, automation workflows, and configuration reference.
```

**Label Check:**
```
gh label list
→ enhancement ✅
→ documentation ✅
→ office ✅
```

**Issue Created:**
```
gh issue create \
  --title "Enhancement: Add setup documentation for office package" \
  --label enhancement,documentation,office \
  --assignee dannytsang
```

### Scenario 3: Integration-Related Enhancement

**Input:**
```
Enhancement: Add CO detection to heating safety system
Extend existing smoke detection heating safety override to include
CO detection using Nest Protect CO sensors.
```

**Label Check:**
```
gh label list
→ enhancement ✅
→ integration: nest protect ✅
→ hvac ❌ (not available)
→ safety ❌ (not available)
```

**Issue Created:**
```
gh issue create \
  --title "Enhancement: Add CO detection to heating safety system" \
  --label "enhancement,integration: nest protect" \
  --assignee dannytsang
```

---

## Error Handling

### Error: Label Not Found
```
Error: could not add label: '[label-name]' not found
```

**Solution:**
1. Re-run label check
2. Remove invalid label from issue
3. Use only labels from available list
4. Retry creation

### Error: User Not Found
```
Error: could not assign: '[username]' not found
```

**Solution:**
1. Verify username is 'dannytsang'
2. Check if account has permissions
3. Try without assignment first
4. Manually assign after creation

### Error: Issue Already Exists
```
Check for duplicate issues before creation
```

**Solution:**
1. Search existing issues: `gh issue list --search "exact title"`
2. If duplicate exists, comment on existing instead
3. Link to existing if related

---

## Process Workflow

### Complete Workflow

```
1. USER PROVIDES ISSUE DETAILS
   ├─ Title
   ├─ Description/body
   └─ Context/related items

2. CLAUDE VALIDATES
   ├─ Confirms it's an enhancement
   ├─ Checks for existing similar issues
   └─ Asks for approval to proceed

3. CHECK LABELS
   ├─ Run: gh label list
   ├─ Match against available labels
   └─ Determine applicable labels

4. DRAFT ISSUE
   ├─ Create detailed body
   ├─ Include all relevant sections
   └─ Show to user for approval

5. CREATE ISSUE
   ├─ Execute: gh issue create
   ├─ Apply labels: enhancement + matched labels
   ├─ Assign: dannytsang
   └─ Confirm: Show issue URL

6. RETURN RESULT
   ├─ Issue number
   ├─ Issue URL
   └─ Labels applied
```

---

## Usage Examples

### Example 1: From Planning Document

```
User: "Create a GitHub issue from the smoke detection heating safety
override plan we wrote earlier."

Claude: "I'll create an enhancement issue for the smoke detection heating
safety override. Let me check available labels first."

[Runs label check]
[Drafts issue with proper sections]
[Shows draft for approval]
[Creates issue if approved]
[Returns: Issue #180, URL, and labels applied]
```

### Example 2: From Validation Findings

```
User: "Create an enhancement issue for the performance optimization
opportunity you identified in the kitchen package."

Claude: "I'll create an enhancement issue for kitchen consolidation.
Checking available labels..."

[Checks labels - finds: enhancement, automations, kitchen]
[Drafts issue]
[Creates: gh issue create --label enhancement,automations,kitchen]
[Returns: Issue #181]
```

### Example 3: Batch Issue Creation

```
User: "Create issues for these 3 enhancements:"
[Lists 3 enhancements]

Claude: "I'll create 3 enhancement issues. Checking labels once..."

[Single label check - reused for all 3]
[Creates issue 1: enhancement,label1,label2]
[Creates issue 2: enhancement,label3,label4]
[Creates issue 3: enhancement,label5,label6]
[Returns all 3 URLs and status]
```

---

## Best Practices

### DO ✅
- ✅ Always check labels first
- ✅ Match labels carefully to issue content
- ✅ Use specific, descriptive titles
- ✅ Include all relevant sections in body
- ✅ Always assign to dannytsang
- ✅ Ask user to approve draft before creating
- ✅ Link related issues
- ✅ Include implementation notes/context

### DON'T ❌
- ❌ Create issues for bugs (use bug label instead)
- ❌ Create duplicate issues (check first)
- ❌ Apply labels that don't exist
- ❌ Create issues without user approval
- ❌ Skip the label validation step
- ❌ Create vague, unclear titles
- ❌ Forget to assign to dannytsang
- ❌ Leave out relevant context/files

---

## Integration with Other Skills

### Works With:
- **Consolidation Analyzer** - Create issues for identified opportunities
- **YAML Quality Reviewer** - Create issues for systemic improvements
- **Room Documentation Generator** - Create issues for documentation
- **Known Error Detector** - Create issues for preventing known patterns
- **Package Review** - Create issues for quality improvements
- **Reflection Reviewer** - Create issues from reflection findings

### Example Integration:
```
1. Run Consolidation Analyzer → Identify 3 opportunities
2. For each high-scoring opportunity:
   a. Run Package Review → Assess quality
   b. Use GitHub Issue Creator → Create enhancement issue
3. Track in GitHub instead of notes
```

---

## Label Reference

### Always Present
- `enhancement` - Always applied to every issue created by this skill

### Common Labels (Check Before Use)
- `automations` - Automation-related work
- `scripts` - Script modifications
- `documentation` - Documentation updates
- `testing` - Testing/validation work
- `integration: *` - Integration-specific (e.g., `integration: nest protect`)
- `<room-name>` - Room-specific (e.g., `kitchen`, `stairs`, `bedroom`)

### Rare Labels (Verify Existence)
- `performance`, `optimization`
- `configuration`, `config`
- `blueprints`, `templates`
- `add-ons`
- `esphome`, `mqtt`

---

## Troubleshooting

### Issue: Label Check Fails
```bash
gh label list
# Error: not authenticated
```
**Solution:** User needs to run `gh auth login` first

### Issue: Can't Find Matching Labels
**Solution:** Use only 'enhancement' if unsure. Better safe than creating invalid labels.

### Issue: Assignment Fails
**Solution:** Create without assignment, then manually assign: `gh issue edit #123 --assignee dannytsang`

### Issue: Need to Edit Created Issue
```bash
# View issue
gh issue view #123

# Edit title
gh issue edit #123 --title "New title"

# Edit body
gh issue edit #123 --body "$(cat new_body.md)"

# Add labels
gh issue edit #123 --add-label "new-label"
```

---

## Future Enhancements

### Version 1.1 (Planned)
- Support for issue templates
- Automatic related issue linking
- Custom assignee support
- Milestone assignment
- Priority indication

### Version 2.0 (Planned)
- Batch issue creation from analysis output
- Issue template generation from YAML
- Automatic issue numbering in YAML
- Integration with project boards
- Automated issue closure on merge

---

## Quick Reference

### Create Issue Command Template
```bash
gh issue create \
  --title "Enhancement: <specific title>" \
  --body "$(cat issue_body.md)" \
  --label enhancement<,other_labels> \
  --assignee dannytsang
```

### Label Check Command
```bash
gh label list
```

### View Existing Issue
```bash
gh issue view #<number>
```

### Search Issues
```bash
gh issue list --search "search term"
```

---

## Process Summary

1. **Get Issue Details** - Title, description, context
2. **Check Labels** - `gh label list`
3. **Match Labels** - enhancement + relevant available labels
4. **Draft Issue** - Structured body with all sections
5. **Get Approval** - Show draft, ask to proceed
6. **Create Issue** - `gh issue create` with labels and assignment
7. **Return Result** - Issue URL and confirmation

---

## Success Criteria

✅ Enhancement issues created with proper structure
✅ 'enhancement' label always applied
✅ All applicable labels from available list applied
✅ No errors from invalid labels
✅ Assigned to dannytsang
✅ Clear, actionable titles and descriptions
✅ Related issues linked
✅ User approval obtained before creation

---

**Skill Created:** 2026-01-25
**Status:** Production Ready
**Maintained By:** User
**Version:** 1.0

