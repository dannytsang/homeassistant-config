# Commit Conventions & Claude Collaboration Rules

**Status:** Active Policy
**Created:** 2026-01-25
**Enforcement Level:** IRON CLAD LAW

---

## 🚨 Critical Rule: No Claude Attribution in Commits

### The Law
**NEVER include Claude AI attribution in commit messages.**

**Violations include:**
- ❌ `Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>`
- ❌ `Co-Authored-By: Claude <claude@anthropic.com>`
- ❌ `Authored by Claude`
- ❌ `Assistant: Claude`
- ❌ Any variant suggesting Claude is a commit author

### Why This Rule Exists
1. **Accuracy:** User (Danny) is the sole author of all changes
2. **Clarity:** Commits are user work, Claude is a tool/assistant
3. **Version Control:** Git history should reflect human decision-makers
4. **Professional:** Code commits are authored by the person making decisions
5. **Accountability:** User retains full responsibility for all changes

### What This Means
- Claude may assist with code generation, planning, and validation
- Claude may suggest commit messages
- Claude may identify what changed and why
- **But:** The user is always the author in `git commit`
- **All commits** are authored solely by the user

---

## Commit Message Structure

### Standard Format
```
<type>: <subject>

<detailed description>
```

### Commit Types
- `feat:` - New feature or automation
- `fix:` - Bug fix or correction
- `refactor:` - Code restructuring without behavior change
- `docs:` - Documentation updates
- `chore:` - Maintenance, cleanup, dependency updates
- `test:` - Test additions or updates

### Subject Line Rules
- ✅ Use imperative mood: "Add feature" not "Added feature"
- ✅ Start with lowercase: "add feature" not "Add feature"
- ✅ No period at end
- ✅ Keep under 50 characters when possible
- ✅ Clear and specific

### Body Rules
- ✅ Explain **what** changed and **why**
- ✅ Not just **what** (that's in the code diff)
- ✅ Wrapped at 72 characters
- ✅ Blank line between subject and body
- ✅ Multiple paragraphs for complex changes

### Examples

#### Good ✅
```
docs: update skills README with undocumented skills

Added comprehensive documentation for 6 previously undocumented skills
in the .claude/skills directory. Updated version to 1.1 and enhanced
workflow documentation with 4 complete paths (Quick/Full/Critical/Daily).

Skills documented:
- HA Known Error Detector
- HA Consolidation Pre-Check
- HA Automation ID Manager
- HA Entity Reference Validator
- HA Package Review
- HA Repository Status
```

#### Bad ❌
```
Updated docs

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

---

## When Claude Assists with Commits

### Claude CAN:
1. ✅ Suggest commit message structure
2. ✅ Identify what files changed and why
3. ✅ Review diffs for accuracy
4. ✅ Help draft detailed descriptions
5. ✅ Validate message clarity
6. ✅ Create the commit **if user approves the message**

### Claude CANNOT:
1. ❌ Add Claude attribution
2. ❌ Suggest co-authorship
3. ❌ Use "we" as if Claude is a contributor
4. ❌ Imply Claude authored changes
5. ❌ Skip user review of commit messages

### Process When Claude Creates Commit
1. Claude drafts commit message (no attribution)
2. Claude asks for approval: "Create commit with this message?"
3. User approves or requests changes
4. Claude creates commit with **user-only authorship**
5. User retains all responsibility for commit content

---

## Examples of Correct Collaboration

### Example 1: Claude-Assisted Commit
```
User: "Create a commit for the skills documentation updates"

Claude: "I'll create a commit with this message:
[Shows message - NO Claude attribution]

Approve? Yes/No"

User: "Yes, create it"

Claude: [Creates commit with user authorship only]
```

### Example 2: Wrong Approach (Never Do This)
```
User: "Create a commit"

Claude: [Creates commit with "Co-Authored-By: Claude..."]

WRONG! ❌ Remove Claude attribution immediately.
```

---

## Checking for Violations

### How to Verify
```bash
# View last commit
git log -1

# Check for Claude attribution
git log --pretty=format:"%B" | grep -i claude
```

### If Violation Found
1. Amend the commit: `git commit --amend`
2. Remove Claude attribution
3. Save and push

---

## FAQ

**Q: Can Claude help write commit messages?**
A: Yes, absolutely. Claude can draft, suggest, and refine messages.

**Q: Can Claude create commits?**
A: Yes, but only after user approves the message and confirms it has no Claude attribution.

**Q: What if Claude tries to add attribution?**
A: Stop and correct immediately. Remind Claude of this iron clad law.

**Q: Is this about credit?**
A: No. It's about accuracy. User makes all decisions about what to commit. Claude is a tool.

**Q: Can I credit Claude in commit message body?**
A: Not as a co-author. You could note "generated with Claude Code" but never as authorship.

---

## References

- This policy: `.claude/COMMIT-CONVENTIONS.md`
- Skills documented: `.claude/skills/README.md` (v1.1)
- Context guide: `.claude/README.md`
- Home Assistant config: `/packages/`

---

## Revision History

| Date | Change |
|------|--------|
| 2026-01-25 | Established iron clad law: No Claude attribution in commits |

---

**Status:** Active - All future commits must follow this rule
**Enforcement:** Automatic - Claude will check before creating commits
**Questions:** Refer to this file

