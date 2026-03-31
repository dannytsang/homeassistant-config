[<- Back](README.md)
# Heating, Ventilation, and Air Conditioning 🌬
Integrations related HVAC. There were enough stuff to separate these out into their own sub folder.

## Hive (Home)
Controls the central heating and hot water via a gas boiler. It also has thermostat to measure the room temperature.

### Central Heating Schedule Methodology

The heating schedule is designed around occupancy patterns and measured heating performance. This section documents how the schedule was built so future changes can be made with context.

#### Heating Performance Data

Based on historical temperature data from InfluxDB (living room area mean temperature):

| Metric | Value |
|--------|-------|
| **Average heating rate** | 0.70°C/hour |
| **Maximum heating rate** | 2.40°C/hour |
| **Average cooling rate** | 0.52°C/hour |
| **Pre-heat time for 1°C rise** | ~90 minutes |

#### Occupancy Rules

The schedule follows these principles:

1. **20°C** when one adult is home alone
2. **22°C** when the whole household is home for >1 hour
3. **20°C** during regular absences (activities, outings)
4. Pre-heat starts ~90 minutes before 22°C periods

#### Weekday Pattern

- **06:30–08:00**: Pre-heat to 20°C for morning routine
- **08:00–14:00**: Maintain 20°C (reduced occupancy)
- **14:00–22:00**: 22°C (pre-heat before full occupancy)
- **Evening gaps**: 20°C during regular absences (varies by day)

#### Weekend Pattern

- Later start (07:30) due to no school schedule
- 20°C blocks during regular Saturday morning and Sunday evening absences
- Simpler structure with fewer transitions

#### Data Sources

- Temperature history: InfluxDB (`living_room_area_mean_temperature`)
- Heating action: `sensor.thermostat_action` state changes
- Analysis period: 30 days of historical data
- Calendar analysis: 3-month period for occupancy pattern validation

### Hot Water

The hot water schedule operates independently and considers:
- Solar diverter (Eddi) priority
- Octopus Agile tariff rates
- Holiday mode overrides

## MyEnergi
[Eddi](https://github.com/CJNE/ha-myenergi) is connected to the immersion heater in the hot water tank and can be controlled independently to the boiler. The main use is to soak up the additional solar electricity rather than exporting it. However, using Octopus Agile 0 or negative rates has allowed automated heating of the water and get paid for it without having to stay up at night or remembering to set a schedule in the app.

Zappi EV charger from MyEnergi also uses this integration.
