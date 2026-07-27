# Bedroom Setup Guide

This is the setup and troubleshooting checklist for the bedroom package. For the full behavior reference, see [`README.md`](README.md).

## Package Files

| File | What To Check |
|------|---------------|
| `bedroom.yaml` | Main blinds, motion lighting, fan, TV, remote, child-door alerts, scenes, scripts, TV uptime, and bed occupancy. |
| `sleep_as_android.yaml` | Webhook receiver, sleep timer, alarm routine, `binary_sensor.danny_asleep`. |
| `awtrix_light.yaml` | MQTT notification helper for the bedroom AWTRIX clock. |

## Core Devices

| Area | Entities |
|------|----------|
| Blinds | `cover.bedroom_blinds`, `binary_sensor.bedroom_window_contact` |
| Bed occupancy | `binary_sensor.bed_occupied`, `sensor.bed_top_left`, `sensor.bed_top_right`, `sensor.bed_bottom_left`, `sensor.bed_bottom_right` |
| Motion | `binary_sensor.bedroom_motion_occupancy`, `binary_sensor.bedroom_area_motion`, `binary_sensor.bedroom_motion_3_presence` |
| Lighting | `light.under_bed_left`, `light.under_bed_right`, `light.bedroom_lamps`, `light.bedroom_main_light`, `light.bedroom_main_light_2`, `light.bedroom_clock_matrix` |
| TV | `binary_sensor.bedroom_tv_powered_on`, `sensor.bedroom_tv_plug_power`, `media_player.bedroom_tv` |
| Fan | `switch.bedroom_fan`, `sensor.bedroom_area_mean_temperature` |
| Sleep tracking | `input_text.sleep_as_android`, `binary_sensor.danny_asleep`, `timer.sleep`, `person.danny` |
| Child-door alerts | `binary_sensor.leos_bedroom_door_contact`, `binary_sensor.ashlees_bedroom_door_contact`, `input_datetime.childrens_bed_time`, `input_select.home_mode` |
| AWTRIX | `sensor.bedroom_clock_device_topic`, `light.bedroom_clock_matrix` |

## Enable Switches And Tunables

| Entity | Expected Use |
|--------|--------------|
| `input_boolean.enable_bedroom_blind_automations` | Turn off before manually positioning bedroom blinds for an extended period. |
| `input_boolean.enable_bedroom_motion_trigger` | Turn off to stop under-bed lights reacting to bedroom motion. |
| `input_boolean.enable_bed_sensor` | Turn off if bed pressure sensors are noisy or being serviced. |
| `input_boolean.enable_direct_notifications` | Allows the daytime TV/window-open blind prompt. |
| `input_select.sleep_as_android_notification_level` | Controls Sleep as Android event logging volume. |
| `input_number.blind_open_position_threshold` | Shared open-position threshold for blind logic. |
| `input_number.blind_closed_position_threshold` | Shared closed-position threshold for blind logic. |
| `input_number.bedroom_blind_closed_threshold` | Bedroom-specific closed threshold used by some routines. |
| `input_number.forecast_high_temperature` | Temperature threshold used when deciding whether to keep blinds closed after TV use. |
| `input_number.sleep_timer_duration` | Starting duration for `timer.sleep`. |
| `input_number.sleep_as_android_time_to_add` | Minutes added when Danny falls back asleep. |
| `input_number.sleep_as_android_time_to_subtract` | Minutes subtracted after 15 minutes asleep. |

## Setup Checklist

1. Confirm the window contact reports `on` when open and `off` when closed.
2. Confirm `cover.bedroom_blinds` has a useful `current_position` attribute and respects open, close, and set-position commands.
3. Confirm all four bed pressure sensors change enough to trip `binary_sensor.bed_occupied` at the configured thresholds: top left, top right, and bottom left at `0.15`; bottom right at `0.1`.
4. Confirm `sensor.bedroom_tv_plug_power` rises above `40` when the TV is on so `binary_sensor.bedroom_tv_powered_on` changes to `on`.
5. Confirm the bedroom remote sends the configured MQTT device actions for buttons 1-4 and dial movement.
6. Confirm Sleep as Android posts to webhook ID `sleep_as_android` and updates `input_text.sleep_as_android`.
7. Confirm `sensor.bedroom_clock_device_topic` contains the AWTRIX MQTT base topic before using `script.send_bedroom_clock_notification`.
8. Confirm `calendar.work` and `calendar.tsang_children` are available for morning blind schedule decisions.

## Troubleshooting

| Issue | Check |
|-------|-------|
| Blinds will not close | Check the window contact, `input_boolean.enable_bedroom_blind_automations`, current blind position, and open/closed thresholds. |
| Blinds open too early or too late | Check `binary_sensor.workday_sensor`, `calendar.work`, `calendar.tsang_children`, and `input_select.home_mode`. |
| TV glare behavior is wrong | Check `binary_sensor.bedroom_tv_powered_on`, `sensor.bedroom_tv_plug_power`, sun state, and the window contact. |
| Motion lighting is too bright at night | Check `scene.bedroom_dim_ambient_light` and whether the blinds are below position `31`. |
| Fan switches off unexpectedly | Check the 2-hour fan timeout and the 5-minute no-presence timeout from `binary_sensor.bedroom_motion_3_presence`. |
| Sleep timer does not start | Check `person.danny` is `home` and `input_text.sleep_as_android` becomes `sleep_tracking_started`. |
| Sleep alarm does not open blinds | Check Danny is home, bedroom blind automations are enabled, and blind position is below `input_number.blind_closed_position_threshold`. |
| Children door warnings do not flash lamps | Check bedroom lamps/main light state, bedtime, home mode, and the child door contact state. |
