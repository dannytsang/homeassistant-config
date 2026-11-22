[<- Back to Integrations README](README.md) · [Packages README](../README.md) · [Main README](../../README.md)

# OpenDisplay Package Documentation

`opendisplay.yaml` maintains a compact household summary on the OpenDisplay e-paper device. It uses the OpenDisplay custom integration's `opendisplay.drawcustom` action, rendering directly from Home Assistant data rather than depending on a static image.

## Everyday Behavior

The display shows:

- The local House of Tsang brand logo, today's date, and a small `LAST UPDATED` timestamp at the lower right.
- Current weather with condition-aware icon colouring, wind speed, and today's high/low temperatures, plus an outlined four-day forecast strip with condition icons, abbreviated dates, and high/low values, from `weather.home`.
- The currently playing Spotify track and artist beneath the forecast, when `media_player.spotify_danny` is playing.
- Compact, colour-coded front-door, house-alarm, exterior-opening, people-home, and heating status icons with concise labels.
- A compact current-to-target heating-temperature readout with thermometer and target symbols from `climate.hive_receiver_heat`.
- The next eight family and children events grouped by blue date headings, with aligned start-time, end-time, and title columns; concurrent active events appear together under their date heading in one red outline box.
- Today's solar generation, household consumption, grid export, and home-battery state of charge, with live solar, battery, and grid-flow arrows, compact 24-hour power-history lines, and peak-power labels above each line.

The 1200 × 1600 E1004 canvas is rotated 90° counter-clockwise for its landscape mounting. It uses blue, green, and red for labels and state meaning; the less-legible yellow is reserved for weather, active lights, and battery level, with black edging on yellow status icons. Energy totals use kWh and the battery is shown as a yellow charge gauge.

The display refreshes when Home Assistant starts, every 30 minutes, or when the people-home count changes. The automation uses `single` mode so an e-paper transfer is never interrupted by a competing refresh.

## Technical Reference

| Automation | ID | Trigger | Action |
|------------|----|---------|--------|
| `OpenDisplay: Home Summary` | `1769277054493` | Home Assistant start, every 30 minutes, or a people-home count change | Gets a time window covering current and next-72-hour calendar events, then calls `opendisplay.drawcustom` with a 90° counter-clockwise rotation. |

### Dependencies

| Dependency | Purpose |
|------------|---------|
| OpenDisplay custom integration | Provides the `opendisplay.drawcustom` action and display device target. |
| `media/house-of-tsang-logo.png` | Transparent local logo rendered beside the title. |
| `weather.home` | Current weather condition, unit, and daily high/low forecasts. |
| `sensor.gw2000a_outdoor_temperature` | Top-right current outdoor temperature and unit. |
| `media_player.spotify_danny` | Current Spotify track and artist, shown only while music is playing. |
| `calendar.family` | Family event shown in the first agenda row. |
| `calendar.tsang_children` | Children's event shown in the second agenda row. |
| `lock.front_door` / `alarm_control_panel.house_alarm` | Front-door lock and house-alarm state. |
| `binary_sensor.external_doors_and_windows` | Open count and brown/green status for external doors, windows, and entrances. |
| `climate.hive_receiver_heat` | Current and target heating temperatures. |
| Growatt SPH energy/power sensors, `sensor.house_grid_import_power`, and grid import/export helpers | Daily solar generation, household use, grid export, battery state of charge, live flow directions, 24-hour power charts, and local statistics sensors for their peak-power labels. |
| Growatt SPH battery state-of-charge sensor | Battery charge gauge. |

## Troubleshooting

| Symptom | Check |
|---------|-------|
| Display does not update | Confirm the OpenDisplay device is online and its integration exposes `opendisplay.drawcustom`; check the automation trace for a queued or failed transfer. |
| Calendar row says no upcoming events | Check that the relevant calendar has an event in the next 24 hours and inspect the `calendar.get_events` action response in the trace. |
| Weather is unknown or zero | Check the state and `temperature` attribute on `weather.home`. |

*Last updated: 2026-11-22*
