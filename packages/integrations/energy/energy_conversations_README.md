[<- Back to Integrations README](README.md) · [Packages README](../README.md) · [Main README](../../README.md)

# Energy Conversations

Voice and LLM conversation intent handlers for querying the home energy system. Defined in `../energy_conversations.yaml`.

Integrations used: [Growatt / Solar Assistant](solar_assistant_README.md), [Octopus Energy](octopus_energy_README.md), and [Solcast](solcast_README.md).

---

## Overview

Thirteen intent handlers cover battery status, electricity rates, charging and export schedules, inverter mode, and solar forecast queries. Each handler responds with a spoken sentence built from live sensor data.

---

## Intent Handlers

### Battery

#### getBatteryLevel

**Phrases:**
- "How much battery is left"
- "What is the battery level"
- "What is the charge remaining"

**Response:** Current state of `sensor.growatt_sph_battery_state_of_charge` with unit (e.g., `45 %`).

---

#### getBatteryRunTime

**Phrases:**
- "How long will the battery last"
- "How long will the battery run for"
- "What is the battery run time"
- "When will the battery run out"

**Response:** Value of `sensor.battery_charge_remaining_hours`.

---

#### getBatterySummary

**Phrases:**
- "Battery summary"

**Response:** Combines battery state of charge with a human-readable time until depletion. Uses Jinja2 to format the runtime as a time today ("at HH:MM"), tomorrow ("tomorrow at HH:MM"), or with a full date for later.

```
{battery_soc}% and will run out
  → today      : at HH:MM
  → tomorrow   : tomorrow at HH:MM
  → later      : at DD/MM/YYYY HH:MM
```

---

### Charging & Inverter

#### getChargingScheduleSummary

**Phrases:**
- "What is the charging schedule summary"
- "How is the charging schedule set"

**Response:** A multi-section summary of all active charging schedule groups:

| Section | Group entity |
|---------|-------------|
| Cost nothing | `input_boolean.solar_assistant_charge_electricity_cost_nothing` |
| Cost below nothing | `input_boolean.solar_assistant_charge_electricity_cost_below_nothing` |
| Forecast based | `input_boolean.enable_forecast_based_charging` |
| Below export | `group.below_export_charging_schedules` |
| Battery first | `group.battery_first_charging_schedules` |
| Grid first | `group.grid_first_charging_schedules` |
| Maintain charge | `group.maintain_battery_first_charging_schedules` |

For each group that is `on`, the response iterates over enabled schedules and reports their `after`, `before`, and `next_update` timestamps.

---

#### getExportSchedule

**Phrases:**
- "What is the export schedule"

**Response:** State and active schedule windows for `group.grid_first_charging_schedules`, including `after`, `before`, and `next_update` for each enabled schedule entry.

---

#### getInverterMode

**Phrases:**
- "What is the inverter mode"

**Response:** Current state of `sensor.growatt_sph_inverter_mode` (e.g., `Battery first`, `Grid first`, `Load first`).

---

### Electricity Rates

#### getCurrentElectricityRates

**Phrases:**
- "What is the current electricity rate"
- "What is the current unit rate"

**Response:** `sensor.octopus_energy_electricity_current_rate` rounded to 2 decimal places with its unit of measurement (e.g., `24.5 p/kWh`).

---

#### getNextElectricityRates

**Phrases:**
- "What is the next electricity rate"
- "What is the next unit rate"

**Response:** `sensor.electricity_next_rate` rounded to 2 decimal places with unit.

---

#### getPreviousElectricityRates

**Phrases:**
- "What was the previous electricity rate"
- "What was the old unit rate"

**Response:** `sensor.electricity_previous_rate` rounded to 2 decimal places with unit.

---

### Solar

#### getSolarForecastLeft

**Phrases:**
- "How much solar generation is left today"
- "Remaining solar forecast today"

**Response:** Difference between today's total forecast (`sensor.total_solar_forecast_estimated_energy_production_today`) and actual generation so far (`sensor.growatt_sph_pv_energy`), rounded to 2 decimal places with unit.

---

#### getSolarForecastToday

**Phrases:**
- "What is the solar forecast today"

**Response:** `sensor.total_solar_forecast_estimated_energy_production_today` with unit (e.g., `12.4 kWh`).

---

#### getSolarForecastTomorrow

**Phrases:**
- "What is the solar forecast"

**Response:** `sensor.total_solar_forecast_estimated_energy_production_tomorrow` with unit.

---

#### getSolarGeneratedToday

**Phrases:**
- "How much solar has generated today"
- "How much solar so far"

**Response:** `sensor.growatt_sph_pv_energy` with unit (e.g., `8.1 kWh`).

---

## Sensor Reference

| Sensor | Source | Used by |
|--------|--------|---------|
| `sensor.growatt_sph_battery_state_of_charge` | Growatt / Solar Assistant | getBatteryLevel, getBatterySummary |
| `sensor.battery_charge_remaining_hours` | Template | getBatteryRunTime, getBatterySummary |
| `sensor.growatt_sph_inverter_mode` | Growatt / Solar Assistant | getInverterMode |
| `sensor.octopus_energy_electricity_current_rate` | Octopus Energy | getCurrentElectricityRates |
| `sensor.electricity_next_rate` | Octopus Energy | getNextElectricityRates |
| `sensor.electricity_previous_rate` | Octopus Energy | getPreviousElectricityRates |
| `sensor.total_solar_forecast_estimated_energy_production_today` | Solcast / Forecast.io | getSolarForecastLeft, getSolarForecastToday |
| `sensor.total_solar_forecast_estimated_energy_production_tomorrow` | Solcast / Forecast.io | getSolarForecastTomorrow |
| `sensor.growatt_sph_pv_energy` | Growatt / Solar Assistant | getSolarForecastLeft, getSolarGeneratedToday |
| `input_boolean.solar_assistant_charge_electricity_cost_nothing` | Input | getChargingScheduleSummary |
| `input_boolean.solar_assistant_charge_electricity_cost_below_nothing` | Input | getChargingScheduleSummary |
| `input_boolean.enable_forecast_based_charging` | Input | getChargingScheduleSummary |
| `input_boolean.enable_permanent_charge_below_export` | Input | getChargingScheduleSummary |
| `group.below_export_charging_schedules` | Group | getChargingScheduleSummary |
| `group.battery_first_charging_schedules` | Group | getChargingScheduleSummary |
| `group.grid_first_charging_schedules` | Group | getChargingScheduleSummary, getExportSchedule |
| `group.maintain_battery_first_charging_schedules` | Group | getChargingScheduleSummary |

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [Energy README](README.md) | Energy package overview |
| [Solar Assistant README](solar_assistant_README.md) | Growatt inverter details |
| [Octopus Energy README](octopus_energy_README.md) | Rate sensor details |
| [Solcast README](solcast_README.md) | Solar forecast details |

---

*Last updated: 2026-04-05*
