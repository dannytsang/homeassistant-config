[<- Back to Integrations README](../README.md) · [Packages README](../../README.md) · [Main README](../../../README.md)

# Git — GitHub CI/CD Integration

*Last updated: 2026-04-05*

Receives GitHub Actions webhook callbacks and triggers an automatic configuration pull when a build passes. Validates a shared secret key before acting; sends a direct alert if the key is incorrect.

Community reference: <https://community.home-assistant.io/t/guide-to-setting-up-a-fully-automated-ci-for-hassio/51576>

---

## Automations

| Name | ID | Trigger | Conditions | Action |
|---|---|---|---|---|
| Home Assistant CI | `1613937312554` | Webhook POST → `git_pull` (public, not local-only) | `input_boolean.enable_github_integration` on | See logic below |

### Webhook Handling Logic

| Key Token Valid? | Response |
|---|---|
| Yes | Log "build passed, pulling changes" + start `hassio.addon_start` → `core_git_pull` |
| No | `script.send_direct_notification` — alert that build passed but incorrect key was received |

---

## Configuration

| Input | Purpose |
|---|---|
| `input_boolean.enable_github_integration` | Master enable/disable for the CI integration |
| `input_text.github_pull_key` | Shared secret token validated against `trigger.json.key_token` |

---

## Dependencies

- `hassio.addon_start` with `addon: core_git_pull` — triggers the Git Pull add-on to fetch latest config
- `script.send_to_home_log` — structured logging on successful pull
- `script.send_direct_notification` — alert on key mismatch
- GitHub Actions — sends the webhook after a successful CI run
