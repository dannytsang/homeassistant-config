[<- Back to Integrations README](README.md) · [Packages README](../README.md) · [Main README](../../README.md)

# Git CI Pull Integration

This package lets a successful external CI workflow ask Home Assistant to pull the latest configuration. It only starts the Git Pull add-on when the integration is enabled and the webhook payload includes the expected shared token.

Community reference: <https://community.home-assistant.io/t/guide-to-setting-up-a-fully-automated-ci-for-hassio/51576>

## Quick Summary

| Area | What Happens |
|------|--------------|
| Webhook | Receives public `POST` requests on webhook ID `git_pull`. |
| Safety gate | Requires `input_boolean.enable_github_integration` to be on. |
| Token check | Compares `trigger.json.key_token` with `input_text.github_pull_key`. |
| Valid token | Logs success, starts the `core_git_pull` add-on, then reloads statistics sensors, scripts, and automations after its run finishes. |
| Invalid token | Sends Danny a direct notification through `script.send_direct_notification`. |

## Package Contents

| File | Purpose | Contents |
|------|---------|----------|
| `git.yaml` | CI webhook handling | 1 automation |

## Flow

```mermaid
flowchart TD
    Webhook[POST webhook git_pull] --> Enabled{GitHub integration enabled?}
    Enabled -->|No| Stop[Ignore request]
    Enabled -->|Yes| Token{key_token matches input_text.github_pull_key?}
    Token -->|Yes| Log[Log build passed]
    Token -->|Yes| Pull[Start add-on core_git_pull]
    Pull --> Running{Git Pull running sensor turns on?}
    Running -->|No: 1 minute timeout| Stop[Do not reload]
    Running -->|Yes| Complete{Git Pull running sensor turns off?}
    Complete -->|No: 5 minute timeout| Stop
    Complete -->|Yes| Statistics[Reload statistics sensors]
    Statistics --> Scripts[Reload scripts]
    Scripts --> Automations[Reload automations]
    Token -->|No| Alert[Send direct notification to Danny]
```

## Automation

| Automation | ID | Trigger | Mode | Result |
|------------|----|---------|------|--------|
| `Home Assistant CI` | `1613937312554` | Webhook `git_pull`, `POST`, `local_only: false` | `single` | Validates the token, starts Git Pull, then reloads statistics sensors, scripts, and automations once the pull finishes. |

## Entities And Services

| Entity or Service | Purpose |
|-------------------|---------|
| `input_boolean.enable_github_integration` | Master enable switch for this webhook. |
| `input_text.github_pull_key` | Shared token used to validate webhook payloads. |
| `hassio.addon_start` with `addon: core_git_pull` | Starts the Git Pull add-on. |
| `binary_sensor.git_pull_running` | Supervisor-provided Git Pull app running state; gates reloads until the pull completes. |
| `statistics.reload` | Reloads YAML statistics sensors after a completed pull. |
| `script.reload` | Reloads YAML scripts after a completed pull. |
| `automation.reload` | Reloads YAML automations after scripts have reloaded. |
| `script.send_to_home_log` | Logs valid build/pull events. |
| `script.send_direct_notification` | Alerts Danny when a request has the wrong token. |

## Troubleshooting

| Symptom | Check |
|---------|-------|
| Webhook arrives but nothing happens | Confirm `input_boolean.enable_github_integration` is `on`. |
| Token mismatch notification appears | Compare the CI secret with `input_text.github_pull_key`. |
| Git does not pull after a valid webhook | Check the `core_git_pull` add-on and the automation trace for `hassio.addon_start`. |
| Reloads do not run | Enable the Git Pull app's **Running** binary sensor in its Supervisor device, then verify it becomes `on` while the app runs and `off` when it completes. |
