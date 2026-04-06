[<- Back to Integrations README](../README.md) · [Packages README](../../README.md) · [Main README](../../../README.md)

# Nuki Smart Lock

*Last updated: 2026-04-05*

Manages the Nuki smart lock on the front door. Automations log every lock state transition and automatically reboot the Nuki hub if the lock becomes unavailable. Convenience scripts provide a single call-site for locking and unlocking with integrated home-log entries.

## Entities

| Entity | Type | Description |
|--------|------|-------------|
| `lock.front_door` | Lock | Nuki smart lock on the front door |
| `button.front_door_reboot_nuki` | Button | Reboots the Nuki hub |
| `binary_sensor.front_door` | Binary sensor | Door contact sensor (used as a condition) |
| `input_boolean.enable_front_door_lock_automations` | Input boolean | Master enable/disable switch for lock automations |

## Automations

| Automation | Trigger | Conditions | Description |
|------------|---------|------------|-------------|
| Porch: Front Door Lock Status Change | `lock.front_door` state change (not from `unlocked`) | Door closed; lock automations enabled | Logs every state transition; calls `script.front_door_lock_status` while the lock is in motion (locking/unlocking), then cancels the script once it reaches a resting state |
| Nuki: Unavailable | `lock.front_door` unavailable for 5 minutes | None | Presses `button.front_door_reboot_nuki` to restart the hub and logs the event |

### Lock Status Change — State Handling

| Lock state | Action |
|------------|--------|
| `locking` or `unlocking` | Run `script.front_door_lock_status` + log |
| `locked` or `unlocked` | Log only, then cancel `script.front_door_lock_status` |

## Scripts

| Script | Mode | Description |
|--------|------|-------------|
| `lock_front_door` | Queued (max 10) | Locks `lock.front_door` when `input_boolean.enable_front_door_lock_automations` is `on`; logs the action |
| `unlock_front_door` | Single | Unlocks `lock.front_door` unconditionally; logs the action |

## Notes

- `lock_front_door` is guarded by `input_boolean.enable_front_door_lock_automations`; `unlock_front_door` has no such guard to ensure the door can always be opened.
- The hub reboot automation runs regardless of whether lock automations are enabled — availability recovery is always desirable.
