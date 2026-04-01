[<- Back to Integrations README](../README.md) · [Packages README](../../README.md) · [Main README](../../../README.md)

# Heating, Ventilation, and Air Conditioning 🌬

Integrations related to HVAC. There were enough components to separate these out into their own sub folder.

## Quick Links

| Document | Purpose |
|----------|---------|
| [Integrations Overview](../README.md) | Overview of all integration packages |
| [Main Packages README](../../README.md) | Architecture and organization guidelines |

## Related Integrations

| Integration | Connection |
|-------------|------------|
| [Energy](../energy/README.md) | Octopus Agile rate-based heating optimization |
| [Rooms](../../rooms/conservatory/README.md) | Underfloor heating control |
| [Rooms](../../rooms/stairs/README.md) | Central heating door open/close triggers |

## Hive (Home)

Controls the central heating and hot water via a gas boiler. It also has a thermostat to measure the room temperature.

### Central Heating Schedule Methodology

The heating schedule is designed around measured heating performance and general occupancy patterns. This section documents the approach for future reference.

#### Heating Performance Data

Based on historical temperature data from InfluxDB:

| Metric | Value |
|--------|-------|
| **Average heating rate** | 0.70°C/hour |
| **Maximum heating rate** | 2.40°C/hour |
| **Average cooling rate** | 0.52°C/hour |
| **Pre-heat time for 1°C rise** | ~90 minutes |

#### Temperature Setpoint Logic

- **20°C**: Baseline / reduced occupancy periods
- **22°C**: Full occupancy periods
- Pre-heat starts ~90 minutes before 22°C periods

#### Schedule Structure

**Weekdays:**
- Morning: 06:30–08:00 pre-heat to 20°C
- Day: 08:00–14:00 at 20°C
- Evening: 14:00–22:00 at 22°C (with variations by day)

**Weekends:**
- Later 07:30 start
- Simplified block structure
- Varies by day

#### Data Sources

- Temperature history: InfluxDB (living room sensors)
- Heating rate calculated from 30 days of historical data
- Pre-heat timing validated against measured performance

### Hot Water

The hot water schedule operates independently and considers:
- Solar diverter (Eddi) priority
- Octopus Agile tariff rates
- Holiday mode overrides

## MyEnergi

[Eddi](https://github.com/CJNE/ha-myenergi) is connected to the immersion heater in the hot water tank and can be controlled independently to the boiler. The main use is to soak up the additional solar electricity rather than exporting it. However, using Octopus Agile 0 or negative rates has allowed automated heating of the water and get paid for it without having to stay up at night or remembering to set a schedule in the app.

Zappi EV charger from MyEnergi also uses this integration.

### External Documentation

- [MyEnergi Eddi Integration](https://github.com/CJNE/ha-myenergi)
- [Home Assistant Hive Integration](https://www.home-assistant.io/integrations/hive/)
