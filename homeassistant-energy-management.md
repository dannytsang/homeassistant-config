# Home Assistant Energy Management System

**Last Updated:** 2026-01-22
**Flagship Feature:** Sophisticated solar, battery, and cost-aware automation

---

## Energy Management System Overview

This is the most sophisticated system in the configuration, combining multiple integrations for intelligent energy optimization.

---

## Solar & Battery Infrastructure

### Hardware
- **Growatt SPH3000-6000 Solar Inverter** + **GBLI Battery**
- **Solar Assistant** for local/faster solar data (replaces Growatt integration)
- **Solcast** for solar forecasting
- **myEnergi Zappi** (EV charger)
- **myEnergi Eddi** (solar diverter/relay for water heating)
- **EcoFlow** battery system with power monitoring
- Real-time grid import/export monitoring

### Key Entities
- Battery SoC: `sensor.growatt_battery_soc`
- Inverter Mode: `select.growatt_mode`
- Current Rate: `sensor.octopus_energy_electricity_current_rate`
- Grid Import/Export: Real-time monitoring

---

## Energy Integrations

### Octopus Energy (UK Agile Tariff)
- Entity: `sensor.octopus_energy_electricity_current_rate`
- Unit: GBP/kWh
- Updates: Every 30 minutes
- Usage: Rate-based automation decisions
- **Pattern:** Check if rate is ≤ 0 or below threshold before appliance start

### Predbat (Battery Prediction)
- Daily summaries via notification
- Battery charge/discharge predictions
- Integration with Octopus Energy tariffs
- Forecasts next 24-48 hours

### Solar Assistant
- Local polling for faster updates (replaces Growatt integration)
- Real-time solar generation data
- Comparison with Solcast forecast

### Solcast
- Solar forecasting integration
- Predicts excess solar generation
- Used for day-ahead scheduling

---

## Intelligent Energy Features

### 1. Battery Mode Switching
Manually controlled modes to optimize energy usage:

```yaml
# Three main modes
- "Battery First" mode: Use stored energy first
- "Load First" mode: Use grid when needed
- "Grid First" mode: Charge battery from grid on cheap rates
```

**Implementation:**
- Mode set via `select.growatt_mode`
- Validation automation alerts if inverter not in correct mode
- Different modes for different times of day/seasons

**Usage Pattern:**
```yaml
automation:
  - alias: "Battery Mode Validation"
    triggers:
      - trigger: state
        entity_id: select.growatt_mode
        for: "00:05:00"
    conditions:
      - condition: template
        value_template: >
          {{ states('select.growatt_mode') != 'expected_mode' }}
    actions:
      - action: script.send_direct_notification
        data:
          message: "⚠️ Battery mode is {{ states('select.growatt_mode') }}, expected 'expected_mode'"
          title: "Battery Mode Alert"
```

### 2. Solar Optimization
Real-time and forecast-based optimization:

- **Monitor battery state of charge** - Decide if to hold charge or discharge
- **Forecast excess solar** → notify user to shift appliance usage
- **Track consecutive low-forecast days** - Adjust heating/water heating schedules
- **Daily Predbat summary notifications** - What tomorrow's generation looks like
- **Inverter mode validation** - Ensure correct mode for time of day

**Example Logic:**
```yaml
# If tomorrow's forecast is low 3 days in a row
condition: template
value_template: >
  {{ consecutive_low_forecast_days | int >= 3 }}
actions:
  - action: script.send_to_home_log
    data:
      message: "⚠️ Low solar forecast 3+ days. Reducing hot water schedule."
      title: "🔋 Energy"
```

### 3. Hot Water Control (Eddi Solar Diverter)

Smart water heating based on solar availability:

- **Morning decision:** Turn off boiler if hot day expected
- **Afternoon decision:** Turn on boiler based on generation forecast
- **Eddi diverter:** Cuts off boiler when enough solar heating done
- **Track consecutive low-generation days** - Override automation on poor solar

**Implementation:**
```yaml
automation:
  - alias: "Hot Water: Morning Decision"
    triggers:
      - trigger: time
        at: "07:00:00"
    actions:
      - choose:
          # Good solar expected - turn off boiler
          - conditions:
              - condition: template
                value_template: "{{ solcast_forecast > 20 }}"  # 20 kWh forecast
            sequence:
              - action: switch.turn_off
                target:
                  entity_id: switch.boiler
              - action: script.send_to_home_log
                data:
                  message: "☀️ Good solar expected. Boiler off."

          # Poor solar - keep boiler on
          default:
            - action: script.send_to_home_log
              data:
                message: "🌧️ Poor solar forecast. Keeping boiler on."
```

### 4. EV Charging (Zappi)

Integrated with solar forecasting:

- Intelligent charging timing based on solar forecast
- Rate-based charging decisions during cheap rates
- Smart charge scheduling with Predbat integration
- Battery SoC awareness

### 5. Cost-Aware Appliance Automation

Only run appliances during cheap/free electricity:

**Pattern:**
```yaml
automation:
  - alias: "Appliance: Cost-Aware Scheduling"
    triggers:
      - trigger: numeric_state
        entity_id: sensor.octopus_energy_electricity_current_rate
        below: 0.10  # Less than 10p/kWh
    actions:
      - action: switch.turn_on
        target:
          entity_id: switch.appliance
```

**Real-world Example - Conservatory Airer:**
```yaml
automation:
  - alias: "Conservatory Airer: Cost-Aware Start"
    triggers:
      - trigger: time_pattern
        hours: "*/2"  # Check every 2 hours
    conditions:
      - condition: state
        entity_id: input_boolean.enable_conservatory_airer_schedule
        state: "on"
      - condition: template
        value_template: >
          {{ states('sensor.octopus_energy_electricity_current_rate') | float <= 0 }}
      - condition: numeric_state
        entity_id: sensor.conservatory_temperature
        above: 15
      - condition: numeric_state
        entity_id: sensor.conservatory_humidity
        above: 60
        below: 90
    actions:
      - action: switch.turn_on
        target:
          entity_id: switch.conservatory_airer
      - action: script.send_to_home_log
        data:
          message: "💨 Free electricity. Running airer."
          title: "⚡ Energy"
```

---

## Automation Patterns for Energy

### Rate-Based Decision Pattern

```yaml
automation:
  - alias: "Device: Check Cost Before Running"
    sequence:
      - variables:
          current_rate: "{{ states('sensor.octopus_energy_electricity_current_rate') }}"
      - choose:
          - conditions:
              - condition: template
                value_template: "{{ current_rate | float <= 0 }}"
            sequence:
              - action: switch.turn_on
                target:
                  entity_id: switch.device
          - conditions:
              - condition: template
                value_template: "{{ current_rate | float > 0 }}"
            sequence:
              - action: script.send_to_home_log
                data:
                  message: "Rate too high (£{{ current_rate }}/kWh). Not running device."
```

### Solar Forecast Usage

```yaml
condition: template
value_template: >
  {% set forecast = states('sensor.solcast_forecast_kw') | float(0) %}
  {{ forecast > 5 }}  # Only if forecasted to generate > 5kW
```

### Battery SoC Thresholds

```yaml
# Don't discharge battery below 20%
condition: numeric_state
entity_id: sensor.growatt_battery_soc
above: 20

# Charge battery when cheap rates
condition: template
value_template: >
  {{ states('sensor.octopus_energy_electricity_current_rate') | float <= 0 }}
```

---

## Energy Tracking & Monitoring

- **InfluxDB** time-series database (30-day retention)
- **Grafana** external dashboards for energy visualization
- **Power consumption monitoring** across 493 devices
- **Real-time cost calculation** based on current rates
- **Daily summaries** with energy usage and cost

---

## Cost Optimization Philosophy

The system prioritizes:
1. **Renewable energy maximization** - Use solar when available
2. **Rate awareness** - Shift appliance usage to cheap windows
3. **Battery optimization** - Hold charge during expensive hours
4. **Forecast integration** - Plan ahead for poor weather
5. **User transparency** - Daily notifications of energy decisions

This multi-layered approach achieves significant cost savings while maintaining comfort and convenience.
