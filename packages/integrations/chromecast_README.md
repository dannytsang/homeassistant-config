[<- Back to Integrations README](README.md) · [Packages README](../README.md) · [Main README](../../README.md)

# Chromecast — Cast and Google TV Management

*Last updated: 2026-04-05*

Manages Chromecast devices and Google TV media players. The Magic Mirror automation keeps the stairs display showing the Home Assistant Lovelace dashboard when people are home. Google TV automations log playback details including media title, app, and progress position.

Integration reference: <https://www.home-assistant.io/integrations/cast/>

---

## Automations

| Name | ID | Trigger | Conditions | Action |
|---|---|---|---|---|
| Stairs: Check Magic Mirror Is Casting Home Assistant | `1647307174048` | Time pattern — every hour (`:00`) | Someone home OR guest mode; alarm NOT armed away | Cast Lovelace dashboard (`lovelace-magicmirror/home`) to `media_player.stairs_chromecast` |
| Chromecast: Google TV Turned Playing | `1672397019959` | `media_player.lounge_tv` or `media_player.bedroom_tv` → `playing` state, `media_title`, or `app_name` | `media_position` attribute is not `none` | Call `script.google_tv_playing_notification` with the triggering entity ID |

### Magic Mirror Conditions Detail

| Condition | Value |
|---|---|
| `input_select.home_mode` | `guest` OR |
| `group.tracked_people` | `home` |
| `alarm_control_panel.house_alarm` | NOT `armed_away` |

---

## Scripts

### `google_tv_playing_notification`

Alias: *Google TV Basic Notification*

Logs playback details to the home log. When both `media_position` and `media_duration` are available, the log entry includes title, app name, current position, total duration, and percentage complete. Otherwise logs title and app name only.

| Field | Required | Description |
|---|---|---|
| `entity_id` | Yes | Entity ID of the Google TV media player |

**Supported entities:**

| Entity ID | Label |
|---|---|
| `media_player.lounge_tv` | Living Room |
| `media_player.bedroom_tv` | Bedroom |

---

## Entities

| Entity | Type | Purpose |
|---|---|---|
| `media_player.stairs_chromecast` | Media player | Magic Mirror display on the stairs |
| `media_player.lounge_tv` | Media player | Living Room Google TV |
| `media_player.bedroom_tv` | Media player | Bedroom Google TV |

---

## Dependencies

- `cast.show_lovelace_view` — casts a specific dashboard view to a Chromecast device
- `group.tracked_people` — presence detection group
- `input_select.home_mode` — home mode selector
- `alarm_control_panel.house_alarm` — alarm state guard
- `script.send_to_home_log` — structured logging
