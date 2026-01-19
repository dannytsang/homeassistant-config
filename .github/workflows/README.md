# CI/CD Pipeline Documentation

This document explains the GitHub Actions workflows for this Home Assistant configuration repository.

---

## Workflows Overview

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `push.yml` | Push to main, weekly schedule, manual | Validates config and deploys to production HA |
| `pull.yml` | Pull requests | Validates config before merge |
| `_ha-validate.yml` | Called by push/pull | Reusable validation logic (yamllint, ESPHome, HA stable/beta/dev) |
| `security.yml` | Push, PR, weekly Monday | Secret scanning (TruffleHog, Gitleaks) + Python security (Bandit) |
| `metrics.yml` | Push, weekly Sunday | Config statistics and health checks |
| `labeler.yml` | Pull requests | Auto-applies labels based on file changes |
| `stale.yml` | Daily | Marks stale issues/PRs for closure |

---

## Known Issues & Limitations

### Pip Caching

**Status:** ❌ Disabled

**Why:** The `actions/setup-python` action's `cache: 'pip'` option requires a dependency manifest file (e.g., `requirements.txt`, `setup.py`, `pyproject.toml`) to generate cache keys. Without one, the action fails.

**History:** Removed in commit `0d2395fc` (September 2024) - "Removed cached PIP to fix pipeline build errors"

**Context:** Dependencies are installed dynamically:
- ESPHome: Direct `pip install esphome`
- Custom components: Extracted from `manifest.json` at runtime

**Workaround (if needed in future):**
```yaml
# Generate requirements.txt before caching
- name: Generate requirements file
  run: |
    echo "esphome" > requirements.txt
    for manifest in custom_components/*/manifest.json; do
      jq -r '.requirements[]? // empty' "$manifest" >> requirements.txt
    done

- uses: actions/setup-python@v6
  with:
    python-version: '3.12'
    cache: 'pip'
```

**Current Performance:** Workflows complete within 5-minute timeout without caching, so performance is acceptable.

---

### Device Triggers in CI

**Issue:** Device triggers reference device IDs from the production Home Assistant device registry. In CI, the device registry is empty, causing validation errors:

```
ERROR: Unknown device '7da5565cc39ea45df83d982a085622b6'
```

**Solution:** Device trigger blocks are replaced with dummy time triggers during CI preparation (see `.github/scripts/prepare-config-for-ci.sh`):

```yaml
# Before (production)
triggers:
  - trigger: device
    domain: mqtt
    device_id: 7da5565cc39ea45df83d982a085622b6
    type: action
    subtype: on_press_release

# After (CI)
triggers:
  - trigger: time
    at: "00:00:00"  # Dummy trigger for CI validation
```

**Affected files:** bedroom.yaml, bedroom2.yaml, bedroom3.yaml, office.yaml

---

### Stripped Integrations

The following integrations are removed from `configuration.yaml` during CI validation because they can't initialize in the CI environment:

| Integration | Reason | Channels Affected |
|-------------|--------|-------------------|
| `battery_notes` | Not in base HA image | All |
| `a_file_logger` | Custom component, not in repo | All |
| `openid` | Custom component, not in repo | All |
| `sonoff` | Requires hardware/cloud API | All |
| `powercalc` | Compatibility issues | Beta/Dev only |

**Implementation:** See `.github/scripts/prepare-config-for-ci.sh`

#### Previously Stripped (Now Validates Successfully)

| Integration | Date Tested | Result |
|-------------|-------------|--------|
| `delete` | 2026-01-19 | ✅ Validates successfully - No external dependencies, only uses Python built-ins and HA core |

**Testing methodology:** Removed integration from strip list, ran full validation suite (stable + beta/dev). All tests passed without errors.

---

## CI Scripts

### `.github/scripts/install-custom-component-deps.sh`

Installs Python dependencies from custom component manifests:
1. Iterates through `custom_components/*/manifest.json`
2. Extracts `requirements` array using `jq`
3. Installs each dependency via pip

**Currently installs:**
- **alexa_media:** alexapy==1.29.14, packaging>=20.3, wrapt>=1.14.0, dictor>=0.1.12,<0.2

**Components without manifests** (no dependencies): delete, llmvision, myenergi, retry

### `.github/scripts/prepare-config-for-ci.sh`

Prepares config for CI validation:
1. Creates required directories (`camera/`)
2. Strips problematic integrations from `configuration.yaml`
3. Replaces device triggers with dummy time triggers
4. Handles channel-specific logic (beta/dev strip `powercalc`)

**Environment variables:**
- `HA_CHANNEL` - Set to `beta` or `dev` for channel-specific handling (defaults to `stable`)

---

## Deployment

### How Deployment Works (push.yml)

After successful validation on push to `main`:

1. **Connect via Tailscale** - Establishes secure connection to home network
   - Uses OAuth secrets: `TS_OAUTH_CLIENT_ID`, `TS_OAUTH_SECRET`
   - Tagged with: `tag:homeassistant-ci`

2. **POST to Webhook** - Triggers Home Assistant to pull changes
   - URL: `DEPLOYMENT_URL` (secret)
   - Auth: `PULL_KEY` (secret)
   - Retries: 5 attempts with 3s delay between

3. **Home Assistant** - Presumably pulls git repo and reloads configuration

---

## Maintenance

### Adding New Custom Components

1. If component has `manifest.json` with requirements → dependencies auto-install
2. If validation fails → add integration to strip list in `prepare-config-for-ci.sh`
3. If component uses device triggers → already handled by script

### Updating Home Assistant Version

1. Monitor beta/dev validation runs for compatibility warnings
2. Add problematic integrations to channel-specific strip logic if needed
3. Test with `workflow_dispatch` before merging

### Modifying Validation Logic

Both scripts (`.github/scripts/*.sh`) are called by multiple workflow jobs. Changes apply to:
- `ha-stable` validation
- `ha-future` validation (beta + dev matrix)

---

## Required Secrets

| Secret | Purpose | Used By |
|--------|---------|---------|
| `TS_OAUTH_CLIENT_ID` | Tailscale OAuth client ID | push.yml (deployment) |
| `TS_OAUTH_SECRET` | Tailscale OAuth secret | push.yml (deployment) |
| `DEPLOYMENT_URL` | Home Assistant webhook URL | push.yml (deployment) |
| `PULL_KEY` | Webhook authentication token | push.yml (deployment) |

---

## Troubleshooting

### Validation Fails with "Unknown device" Error
- Device trigger in automation → Already handled by `prepare-config-for-ci.sh`
- Check logs to confirm device trigger replacement worked

### Validation Fails with "Integration not found"
- Add integration to strip list in `prepare-config-for-ci.sh`
- Ensure integration is in correct section (all channels vs beta/dev only)

### Custom Component Dependency Install Fails
- Check `manifest.json` syntax (valid JSON)
- Verify PyPI package exists and version is available
- Review `install-custom-component-deps.sh` logs for details

### Deployment Not Triggering
- Verify Tailscale connection succeeded
- Check `DEPLOYMENT_URL` and `PULL_KEY` secrets are correct
- Review Home Assistant automation logs for webhook reception
