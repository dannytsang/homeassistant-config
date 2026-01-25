# Claude Skill: Home Assistant Git Commit Safety

**Status:** Production Ready
**Version:** 1.0
**Created:** 2026-01-25
**Purpose:** Safely commit changes with security validation, repo visibility checks, and enforcement of commit conventions

---

## Purpose

Provide a safe, validated workflow for committing changes to the Home Assistant repository with comprehensive checks for:
- Sensitive information (credentials, API keys, tokens)
- Repository visibility (prevents public exposure of secrets)
- Commit message conventions (no Claude attribution - iron clad law)
- Known error patterns
- Change preview and confirmation

---

## When to Use

- **Before every commit** - Safe default workflow
- **When unsure about file contents** - Security scanning
- **After major changes** - Validation before deployment
- **When working with credentials** - Verify nothing sensitive was staged
- **Before pushing to public repo** - Check visibility and safety

---

## 🚨 IRON CLAD LAW: NO CLAUDE ATTRIBUTION

**CRITICAL:** Never include Claude attribution in commit messages.

```bash
# ❌ WRONG - NEVER DO THIS
git commit -m "Add feature

Co-Authored-By: Claude <noreply@anthropic.com>"

# ✅ CORRECT - ALL COMMITS ARE YOUR WORK
git commit -m "Add feature"
```

**Why:** This is a deliberate policy decision. All commits are authored by the human user. Claude is a tool, not a co-author. See `.claude/COMMIT-CONVENTIONS.md` for details.

**Enforcement:** This skill will REJECT any commit message containing:
- "Claude"
- "Co-Author"
- "noreply@anthropic"
- Any attribution to Claude or AI assistance

---

## How This Skill Works

### Step 1: Pre-Commit Security Scan

Before allowing any commit, scan for sensitive information:

#### Check 1: Environment Files
```bash
# FAIL if any of these are staged:
.env
.claude/.env
.env.local
.env.*.local
secrets.yaml
.google.token
SERVICE_ACCOUNT.json
```

**Action:** If found, unstage immediately with error message showing which files contain secrets.

#### Check 2: Hardcoded Credentials (Diff Scan)
```bash
# Regex patterns to detect in staged changes:
- API_KEY\s*=\s*['\"]?[a-zA-Z0-9_-]{20,}['\"]?
- TOKEN\s*=\s*['\"]?[a-zA-Z0-9_-]{30,}['\"]?
- password\s*:\s*['\"]?[^\"'\s]{8,}['\"]?
- https?://[a-z0-9._-]+:[a-z0-9._-]+@
- -----BEGIN.*PRIVATE KEY-----
```

**Action:** Flag matches, show context, ask for confirmation to exclude file from commit or stash credentials.

#### Check 3: Verify .gitignore Coverage
```bash
# Verify these patterns exist in .gitignore:
.env
.claude/.env
secrets.yaml
*.key
*.token
SERVICE_ACCOUNT.json
```

**Action:** If missing, warn and add to .gitignore before proceeding.

### Step 2: Repository Visibility Check

```bash
# Get repository visibility
gh api repos/{owner}/{repo} --jq '.private'

# Result: true = private (safe), false = public (risky)
```

**If PUBLIC repository:**
- Show warning: "⚠️  This is a PUBLIC repository"
- List all files being committed
- Ask for explicit confirmation
- Offer to redact sensitive file names/paths

**If PRIVATE repository:**
- Proceed with reduced friction

### Step 3: Commit Message Validation

Check commit message for compliance:

#### Requirement 1: No Claude Attribution
```bash
if grep -qi "claude\|co-author\|noreply@anthropic" <<< "$MESSAGE"; then
  echo "❌ ERROR: Commit message contains Claude attribution"
  echo "🚨 IRON CLAD LAW: Do not attribute work to Claude"
  echo "All commits are authored by human developers only."
  exit 1
fi
```

**Error Message:**
```
❌ REJECTED: Claude Attribution Detected

Your commit message contains:
  "Co-Authored-By: Claude <noreply@anthropic.com>"

🚨 IRON CLAD LAW (Non-negotiable):
   Do not include Claude, AI, or assistant attribution in commits.

All commits represent YOUR work and decisions.
Claude is a tool you used, not a co-author.

Fix: Remove any attribution lines and try again.
Reference: See .claude/COMMIT-CONVENTIONS.md
```

#### Requirement 2: Proper Format
- Commit message present (not empty)
- First line is summary (under 72 characters recommended)
- Proper capitalization and grammar
- No excessive punctuation

#### Requirement 3: No Placeholder Messages
Reject:
- "WIP"
- "temp"
- "test"
- "fix"
- "update"
- "[TODO]"
- "[PLACEHOLDER]"

**These are development messages, not publication-ready commits.**

### Step 4: Known Error Pattern Scan

If user hasn't recently run error detection, offer to scan:

```
Would you like me to scan for the 7 known error patterns before committing?
(Takes ~30 seconds, prevents common mistakes)
- Response variable syntax errors
- Entity domain mismatches
- Invalid condition descriptions
- Unquoted emoji strings
- Automation ID format errors
- Timer placement errors
- Unsafe attribute access
```

### Step 5: Change Preview

Show what will be committed:

```bash
# Show modified files
git diff --cached --name-only

# Show file sizes and line changes
git diff --cached --stat

# Option to show full diff
git diff --cached
```

**Ask:** "Continue with this commit? [y/n]"

### Step 6: Execute Safely

```bash
# Standard git commit
git commit -m "$MESSAGE"

# Verify success
if [ $? -eq 0 ]; then
  echo "✅ Commit successful: $(git rev-parse --short HEAD)"
  echo "📝 Message: $MESSAGE"
else
  echo "❌ Commit failed"
  exit 1
fi
```

---

## Usage Examples

### Example 1: Simple Commit

```
User: "Commit this work with message: 'fix: motion detection logic'"

Skill:
1. ✅ Security scan - No secrets found
2. ✅ Repo visibility - PUBLIC repo, 15 files, user confirmed
3. ✅ Message validation - "fix: motion detection logic" (compliant)
4. ✅ Error scan - Optional (skipped)
5. 📋 Preview - 15 files, 342 insertions, 28 deletions
6. ✅ Execute - Commit successful

Result: Commit a1b2c3d created
```

### Example 2: Blocked - Credentials Detected

```
User: "Commit changes"

Skill:
1. ❌ SECURITY VIOLATION

   Found staged files containing secrets:
   - .claude/.env (InfluxDB token)
   - .env.local (API keys)

   Action: Unstaging credential files

   ⚠️  Only commit application code, not credentials.

   Credentials should be:
   - Stored in .env (local only, never committed)
   - Loaded via environment variables
   - Listed in .gitignore

   Please review your staged changes and try again.

User then fixes the issue, and skill allows commit.
```

### Example 3: Blocked - Claude Attribution

```
User: "Commit with message:

fix: clean up automations

Co-Authored-By: Claude <noreply@anthropic.com>"

Skill:
❌ REJECTED: Claude Attribution Detected

Your commit message contains:
  "Co-Authored-By: Claude <noreply@anthropic.com>"

🚨 IRON CLAD LAW (Non-negotiable):
   Do not include Claude, AI, or assistant attribution in commits.

All commits represent YOUR work and decisions.
Claude is a tool you used, not a co-author.

Fix the message and try again.
```

### Example 4: Public Repo Warning

```
User: "Commit changes"

Skill:
⚠️  PUBLIC REPOSITORY WARNING

This is a PUBLIC repository visible to anyone.
Double-checking for sensitive information...

Files to be committed (15 total):
✅ .claude/INFLUXDB-EXPLORATION-REPORT.md (redacted)
✅ .claude/scripts/influxdb-query.sh (no credentials)
✅ packages/kitchen/kitchen.yaml
✅ automations/motion.yaml
... 11 more files

Sensitive file check:
✅ No .env files
✅ No secrets.yaml
✅ No tokens or API keys
✅ No personal information exposed

Security status: ✅ SAFE TO COMMIT

Continue? [y/n]
```

---

## Configuration Checklist

Before first use, verify:

- [ ] `.gitignore` includes all sensitive patterns
- [ ] No `.env` files are tracked (check git log)
- [ ] `gh` CLI is installed and authenticated
- [ ] `.claude/COMMIT-CONVENTIONS.md` exists and documents policy
- [ ] User understands: No Claude attribution (iron clad law)

---

## Error Messages & Recovery

### "Sensitive Files Staged"
**Action:** Unstage with `git restore --staged <file>`
**Prevention:** Keep files in `.env` only, add to `.gitignore`

### "Hardcoded Credentials Detected"
**Action:** Remove from files, stage again
**Prevention:** Use environment variables, never hardcode

### "Claude Attribution Detected"
**Action:** Remove attribution line(s), try again
**Prevention:** Remember: All commits are your work only

### "Repository is Public"
**Action:** Review files, confirm safety, proceed
**Prevention:** Use private repo for sensitive work, public for released code

### "Message is Placeholder"
**Action:** Write meaningful commit message
**Prevention:** Describe what changed and why

---

## Safety Rules (Non-Negotiable)

1. **Never commit credentials** - Always use environment files
2. **Never attribute to Claude** - Iron clad law, all work is yours
3. **Always verify public repo safety** - Check before pushing secrets
4. **Always validate message** - Meaningful messages for audit trail
5. **Always show preview** - Know what you're committing

---

## Integration with Workflow

```
User Work → Stage Changes → /commit → Validation → Success/Failure
                                ↓
                    ┌─ Security Scan
                    ├─ Visibility Check
                    ├─ Message Validation
                    ├─ Error Pattern Scan (optional)
                    ├─ Change Preview
                    ├─ User Confirmation
                    └─ Execute
```

---

## Limitations

- Cannot detect all possible credential patterns (new formats may exist)
- Regex-based scanning may have false positives/negatives
- Requires `gh` CLI for repo visibility check
- Cannot scan binary files (only text)
- Relies on proper `.gitignore` setup

---

## Related Documentation

- `.claude/COMMIT-CONVENTIONS.md` - Commit message conventions
- `.gitignore` - Files to exclude from version control
- `README.md` - Git workflow documentation
- `.claude/skills/ha-known-error-detector.md` - Error pattern reference

---

## Recommendations for Use

1. **Always use this skill** - Make it your default commit workflow
2. **Review changes before staging** - Reduces need for security scan
3. **Keep .gitignore updated** - Add new sensitive patterns as discovered
4. **Test with private repo first** - Before committing to public repos
5. **Document secrets in local notes** - Never in version control

---

## Future Enhancements

- Integration with pre-commit hooks
- Automatic secret detection library (detect-secrets)
- Commit message template with best practices
- Integration with GitHub branch protection rules
- Automated security scanning (truffleHog, Semgrep)
- Commit signing with GPG keys
- Audit trail logging

---

**Skill Purpose:** Prevent accidental exposure of credentials and enforce proper commit practices
**Safety Level:** High - Blocks unsafe commits
**Recommended Frequency:** Every commit
**Learning Curve:** Low - Clear error messages and recovery steps

---

**Status:** Ready for Production Use
**Last Updated:** 2026-01-25
**Version:** 1.0
