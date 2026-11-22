[<- Back to Integrations README](README.md) · [Packages README](../README.md) · [Main README](../../README.md)

# OpenDisplay Package Documentation

`opendisplay.yaml` maintains a compact household summary on the OpenDisplay e-paper device. It uses the OpenDisplay custom integration's `opendisplay.drawcustom` action, rendering directly from Home Assistant data rather than depending on a static image.

## Everyday Behavior

The display shows:

- Current local date and time.
- The condition and temperature from `weather.home`.
- Up to three events in the next 72 hours from `calendar.family`.
- Up to three events in the next 72 hours from `calendar.tsang_children`.

The 1200 × 1600 E1004 canvas is rotated 90° counter-clockwise for its landscape mounting, and uses the display accent colour for weather and section labels.

The display refreshes when Home Assistant starts, every 30 minutes, and when the weather or either calendar's active-event state changes. The automation uses `single` mode so an e-paper transfer is never interrupted by a competing refresh.

## Technical Reference

| Automation | ID | Trigger | Action |
|------------|----|---------|--------|
| `OpenDisplay: Home Summary` | `1769277054493` | Home Assistant start, every 30 minutes, or source state changes | Gets the next 72 hours of calendar events, then calls `opendisplay.drawcustom` with a 90° counter-clockwise rotation. |

### Dependencies

| Dependency | Purpose |
|------------|---------|
| OpenDisplay custom integration | Provides the `opendisplay.drawcustom` action and display device target. |
| `weather.home` | Current weather condition, temperature, and temperature unit. |
| `calendar.family` | Family event shown in the first agenda row. |
| `calendar.tsang_children` | Children's event shown in the second agenda row. |

## Troubleshooting

| Symptom | Check |
|---------|-------|
| Display does not update | Confirm the OpenDisplay device is online and its integration exposes `opendisplay.drawcustom`; check the automation trace for a queued or failed transfer. |
| Calendar row says no upcoming events | Check that the relevant calendar has an event in the next 24 hours and inspect the `calendar.get_events` action response in the trace. |
| Weather is unknown or zero | Check the state and `temperature` attribute on `weather.home`. |

*Last updated: 2026-11-22*
