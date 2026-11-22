[<- Back to Integrations README](README.md) · [Packages README](../README.md) · [Main README](../../README.md)

# OpenDisplay Package Documentation

`opendisplay.yaml` maintains a compact household summary on the OpenDisplay e-paper device. It uses the OpenDisplay custom integration's `opendisplay.drawcustom` action, rendering directly from Home Assistant data rather than depending on a static image.

## Everyday Behavior

The display shows:

- A small `LAST UPDATED` timestamp beneath the dashboard title.
- Current weather plus tomorrow's daily forecast from `weather.home`.
- Colour-coded front-door, house-alarm, and heating status with text labels.
- A current-to-target heating-temperature readout from `climate.hive_receiver_heat`.
- The next five events across the family and children calendars, grouped by date with each event's time and title.
- Today's solar generation, household consumption, grid export, and home-battery state of charge.

The 1200 × 1600 E1004 canvas is rotated 90° counter-clockwise for its landscape mounting. It uses the display's blue, green, red, and yellow channels to distinguish weather, normal states, attention states, and solar generation; energy totals use kWh and the battery is shown as a green charge gauge.

The display refreshes when Home Assistant starts, every 30 minutes, and when any displayed source changes. The automation uses `single` mode so an e-paper transfer is never interrupted by a competing refresh.

## Technical Reference

| Automation | ID | Trigger | Action |
|------------|----|---------|--------|
| `OpenDisplay: Home Summary` | `1769277054493` | Home Assistant start, every 30 minutes, or a displayed source changes | Gets the next 72 hours of calendar events, then calls `opendisplay.drawcustom` with a 90° counter-clockwise rotation. |

### Dependencies

| Dependency | Purpose |
|------------|---------|
| OpenDisplay custom integration | Provides the `opendisplay.drawcustom` action and display device target. |
| `weather.home` | Current weather condition, temperature, unit, and tomorrow's daily forecast. |
| `calendar.family` | Family event shown in the first agenda row. |
| `calendar.tsang_children` | Children's event shown in the second agenda row. |
| `lock.front_door` / `alarm_control_panel.house_alarm` | Front-door lock and house-alarm state. |
| `climate.hive_receiver_heat` | Current and target heating temperatures. |
| Growatt SPH daily energy sensors | Solar generation, household use, grid export, and battery state of charge. |

## Troubleshooting

| Symptom | Check |
|---------|-------|
| Display does not update | Confirm the OpenDisplay device is online and its integration exposes `opendisplay.drawcustom`; check the automation trace for a queued or failed transfer. |
| Calendar row says no upcoming events | Check that the relevant calendar has an event in the next 24 hours and inspect the `calendar.get_events` action response in the trace. |
| Weather is unknown or zero | Check the state and `temperature` attribute on `weather.home`. |

*Last updated: 2026-11-22*
