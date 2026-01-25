# InfluxDB v2 Home Assistant Integration - Exploration Report

**Generated:** 2026-01-25 17:28:10 UTC

**⚠️ NOTE:** This is a redacted version for public repository distribution. Sensitive information including InfluxDB URLs, organization names, bucket IDs, and specific entity identifiers have been removed. A full unredacted version is retained locally for reference.

## Executive Summary

This report documents the data structure and content of the Home Assistant integration with InfluxDB v2. The database contains comprehensive time-series data for all Home Assistant entities, including sensors, switches, lights, climate controls, and numerous automations.

## Connection Details

- **InfluxDB URL:** `[redacted]`
- **Organization:** `[redacted]`
- **Bucket:** `home-assistant` (custom user bucket)
- **Bucket Type:** User (custom)
- **Bucket ID:** `[redacted]`
- **Created:** 2023-11-05
- **Authentication:** Token-based (configured, stored in .env - NOT committed to repo)

## Data Retention Policy

| Policy Type | Duration |
|---|---|
| Expire | Infinite (no automatic data deletion) |
| Shard Duration | 7 days |

**Note:** Data is retained indefinitely, allowing for long-term historical analysis and trend detection.

## Data Overview

- **Total Sample Records Analyzed:** 824,132
- **Time Range:** Last 24 hours
- **Unique Measurements:** 3,622
- **Unique Domains:** 43

## Data by Domain

| Domain | Record Count | Notes |
|---|---|---|
| sensor | 397,146 | Standard sensor values |
| device_tracker | 78,943 | Location/presence tracking |
| binary_sensor | 63,545 | On/off state sensors |
| predbat | 56,797 | Battery management integration |
| light | 36,723 | Light control and state |
| automation | 34,405 | Automation triggers/states |
| update | 18,582 | Software update tracking |
| domain | 17,515 | Domain/integration metadata |
| script | 16,556 | Script execution tracking |
| event | 14,194 | Event logs |
| switch | 13,857 | Switch control/state |
| number | 13,552 | Numeric control entities |
| calendar | 12,452 | Calendar events |
| camera | 12,230 | Camera state/snapshots |
| climate | 5,989 | HVAC/thermostat control |
| select | 5,893 | Dropdown selection entities |
| timer | 5,754 | Timer entities |
| media_player | 4,411 | Media playback control |
| scene | 4,220 | Scene activation |
| weather | 2,901 | Weather integration |
| cover | 2,802 | Blinds/cover control |
| sun | 1,800 | Sun position tracking |
| image | 600 | Image entity states |
| input_text | 531 | Text input helpers |
| vacuum | 528 | Vacuum control/state |
| group | 368 | Entity groups |
| person | 327 | Person/user presence |
| input_number | 260 | Numeric input helpers |
| text | 239 | Text entity states |
| lock | 186 | Door lock control |
| alarm_control_panel | 173 | Alarm system state |
| button | 128 | Button press tracking |
| todo | 126 | Todo list items |
| schedule | 104 | Schedule configurations |
| input_boolean | 95 | Boolean input helpers |
| remote | 62 | Remote control state |
| zone | 45 | Geographic zones |
| counter | 42 | Counter values |
| fan | 12 | Fan control |
| tts | 12 | Text-to-speech events |
| tag | 11 | NFC tag readings |
| ai_task | 8 | AI task execution |
| conversation | 8 | Conversation logs |

## Key Measurements & Structure

The database uses a unit-based measurement naming scheme combined with entity-specific measurements. Below are the most important measurement patterns:

### Unit-Based Measurements (Physical Quantities)

These measurements group related sensor values by their physical unit:

| Measurement | Records | Domains | Entity ID Pattern | Fields |
|---|---|---|---|---|
| kWh | 95,312 | input_number, predbat, sensor | Energy (grid import/export, solar, batteries) | 97 |
| W | 30,459 | input_number, number, sensor | Power consumption (appliances, devices) | 37 |
| % | 45,945 | input_number, number, sensor | Percentage values (battery, humidity, etc.) | 58 |
| °C | 31,270 | number, sensor | Temperature readings (rooms, devices) | 19 |
| V | 14,432 | sensor | Voltage (batteries, grid) | 7 |
| kW | 16,243 | input_number, predbat, sensor | Power (generation, thresholds) | 26 |
| lx | 9,939 | number, sensor | Illuminance/Light levels | 11 |
| dBm | 4,422 | number, sensor | WiFi signal strength | 14 |
| A | 6,002 | number, sensor | Current (chargers, devices) | 12 |
| GBP | 4,724 | sensor | Energy costs (electricity rates) | 26 |
| mm | 8,728 | number, sensor | Distance/Position measurements | 10 |
| dB | 1,000 | sensor | Sound level / Signal strength | 7 |

### Entity-Specific Measurements

Many entities (especially lights, climate, media players) have dedicated measurements named after their entity_id:

#### Light Entities

| Measurement | Records | Fields | Description |
|---|---|---|---|
| light.all_lights | 2,335 | 24 | All lights aggregated control state |
| light.[room]_lights | 2,322 | ~20 | Main room lighting |
| light.[room]_ambient_lights | 2,209 | ~20 | Room ambient lighting |
| light.[room]_accent_lights | 2,207 | ~20 | Room accent lighting |
| light.[room]_down_lights | 1,983 | ~20 | Room downlights |
| light.[room]_cabinets | 1,983 | ~20 | Room cabinet lighting |

**Light Entity Fields Typically Include:**
- brightness, brightness_str
- color_mode, color_mode_str
- color_temp_kelvin, hs_color, rgb_color
- friendly_name_str
- max_color_temp_kelvin, min_color_temp_kelvin
- state, effect, effect_list
- icon_str, supported_features, supported_color_modes

#### Climate Entities

| Measurement | Records | Fields | Description |
|---|---|---|---|
| climate.[room]_radiator | 33 | 11 | Room heating control |
| climate.[room]_radiator | ~30 | ~11 | Room heating control |
| climate.[room]_thermostat | ~25 | ~11 | Room thermostat control |

**Climate Entity Fields Typically Include:**
- current_temperature
- target_temperature
- temperature_step
- preset_mode (eco, comfort, heat, etc.)
- preset_modes_str (available presets)
- state (heating/idle)
- friendly_name_str
- supported_features, min_temp, max_temp

#### Binary Sensor Entities

| Measurement | Records | Fields | Description |
|---|---|---|---|
| binary_sensor.[device]_battery_low | 32 | 16 | Door/window battery low indicator |
| binary_sensor.[device]_presence | ~20 | ~6 | Motion presence detector |
| binary_sensor.security_alarm_composite | ~15 | ~5 | Security alarm composite |

**Binary Sensor Fields Typically Include:**
- value (on/off state)
- friendly_name_str
- battery_low_threshold, battery_level
- device_id, device_class_str

#### Media Player Entities

| Measurement | Records | Fields | Description |
|---|---|---|---|
| media_player.spotify_[user] | 2,246 | ~15 | Spotify player for user |

**Media Player Fields Typically Include:**
- state (playing/paused/idle)
- media_title, media_artist, media_album_name
- volume_level
- supported_features

## Field Analysis

### Field Types

Home Assistant stores various field types in InfluxDB:

1. **Numeric Fields** - Physical measurements with units
   - Examples: temperature (°C), power (W), energy (kWh), voltage (V)
   - Type: Float/Integer values

2. **String Fields** - Metadata and state information
   - Naming convention: `*_str` suffix for string fields
   - Examples: `friendly_name_str`, `state_str`, `device_class_str`
   - Type: Text values

3. **Configuration Fields** - Device and entity configuration
   - Examples: `min_temp`, `max_temp`, `step`, `icon`
   - Type: Mixed (numeric or string)

4. **Relationship Fields** - Links to other entities
   - Examples: `entity_id_str`, `source_entity_id_str`, `device_id_str`
   - Type: Text identifiers

### Common Field Patterns

Across most measurements, you'll find these consistent fields:

| Field Pattern | Type | Example Values | Purpose |
|---|---|---|---|
| `friendly_name_str` | String | "Bedroom Temperature" | Human-readable entity name |
| `friendly_name` | Numeric | ID reference | Numeric ID for the entity |
| `device_class_str` | String | "temperature", "humidity" | Semantic entity type |
| `state_class_str` | String | "measurement", "total_increasing" | Measurement class |
| `icon_str` | String | "mdi:thermometer" | Icon for UI display |
| `integration_str` | String | Various integration types | Data source (e.g., MQTT, wireless, REST) |
| `value` | Numeric/String | Varies | Current entity value |
| `last_reset_str` | String | ISO timestamp | Last value reset time |
| `last_changed_str` | String | ISO timestamp | Last state change time |

## Data Categories

### 1. Energy Management
- Power generation (renewable: kW, kWh)
- Power consumption (appliances: W, kW)
- Energy accumulation (daily/total: kWh)
- Cost tracking (currency units)
- Battery management (SOC %, voltage)
- Grid import/export tracking

### 2. Climate Control
- Temperature readings (°C)
- Humidity (%)
- Pressure (Pa, hPa)
- Target temperatures
- Heating/cooling states
- Radiator controls
- HVAC system state

### 3. Lighting
- Brightness levels
- Color temperature
- Color modes (RGB, HSV)
- On/off states
- Light effects
- Scene configurations

### 4. Security & Presence
- Binary sensors (doors, windows, motion)
- Cameras
- Alarms
- Battery levels (zigbee/zwave devices)
- Location tracking
- Entry detection

### 5. Utilities & Devices
- Network devices (access points, routers)
- Storage and backup systems
- Smart plugs and power monitoring
- Appliances and robotic devices
- Vehicle integration

### 6. Automations & Helpers
- Automation triggers/states
- Input numbers and selects
- Binary sensor states
- Scene activations
- Timers and counters

## Data Quality Observations

### Strengths
1. **Comprehensive Coverage:** Nearly all Home Assistant entities are recorded
2. **Rich Metadata:** Each entity includes extensive attribute information
3. **Long Retention:** Infinite retention allows historical analysis
4. **Consistent Schema:** Standard field naming patterns across similar entities
5. **High Frequency:** Data points captured on state changes and regular intervals

### Potential Issues & Recommendations

#### 1. Measurement Naming Inconsistency
**Issue:** Units (kWh, W, %, °C) used as measurement names can cause schema collisions.
**Example:** The measurement "%" contains numeric values (battery %), strings (mode), and other mixed types.
**Recommendation:** Consider migrating to entity-based measurements with unit as a tag:
```flux
measurement: "sensor"
tags: entity_id="bedroom_temperature", unit="°C"
fields: value=21.5
```

#### 2. Schema Collisions
**Error Found:** "Schema collision: cannot group string and float types together"
**Cause:** String fields (friendly_name_str) mixed with numeric fields (value) in same measurement
**Impact:** Limits certain Flux query patterns, particularly grouping operations
**Recommendation:** Use separate fields for numeric vs. string data or use tags for metadata

#### 3. Field Explosion
**Issue:** Single measurements contain 50-100+ fields (observed in kWh: 97 fields, W: 37 fields)
**Example:** "kWh" measurement has 97 different fields across all entities
**Impact:** Increased query complexity and schema management overhead
**Recommendation:** Use tags for entity_id and attributes, keep measurements focused on actual values

#### 4. Data Volume
**Impact:** ~850K records in last 24 hours (24-hour sample window)
**Projection:** ~310 million records annually at current rate
**Performance Note:** Query responsiveness is acceptable for 7-day ranges
**Recommendation:** Consider implementing downsampling policies for archived data older than 6 months

#### 5. Query Performance
**Observation:** Queries with limits work well; unbounded queries fail as expected
**Note:** Schema collisions prevent use of some Flux functions (group, distinct on mixed-type measurements)
**Recommendation:** Document query patterns and limitations for team reference

## Query Examples for Common Use Cases

### Get all temperature sensors from last hour
```flux
from(bucket:"home-assistant")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "°C")
  |> filter(fn: (r) => r.entity_id =~ /temperature/)
```

### Get power generation trend (last 7 days)
```flux
from(bucket:"home-assistant")
  |> range(start: -7d)
  |> filter(fn: (r) => r._measurement == "kW")
  |> filter(fn: (r) => r.entity_id =~ /generation|solar/)
  |> aggregateWindow(every: 1h, fn: mean)
```

### Get battery status for all wireless devices
```flux
from(bucket:"home-assistant")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "%")
  |> filter(fn: (r) => r._field == "battery")
```

### Monitor light on/off patterns
```flux
from(bucket:"home-assistant")
  |> range(start: -7d)
  |> filter(fn: (r) => r._measurement =~ /^light./)
  |> filter(fn: (r) => r._field == "state")
  |> group(columns: ["_measurement"])
  |> count()
```

### Get power consumption by device
```flux
from(bucket:"home-assistant")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "W")
  |> filter(fn: (r) => r._field == "value")
  |> aggregateWindow(every: 1h, fn: mean)
  |> sort(columns: ["_value"], desc: true)
```

## Script Assessment

### Current Script Location
- **Path:** `.claude/scripts/influxdb-query.sh`
- **Status:** Functional and tested
- **Last Used:** Query exploration in this session

### Script Capabilities
- Loads credentials from `.claude/.env` (secure local storage)
- Accepts Flux query as first argument
- Supports time range specification (default: -24h)
- Properly URL-encodes organization name
- Uses token authentication
- Returns CSV format output
- Includes error messages for invalid queries

### Script Strengths
- Simple one-liner invocation
- Secure credential handling
- Flexible query support
- Built for bash automation

### Potential Improvements
1. **Error Handling:** Add check for empty responses and HTTP errors
2. **Output Format:** Option to return JSON vs CSV via flag
3. **Query Templates:** Built-in templates for common queries
4. **Timeout:** Add configurable timeout (currently uses curl default ~120s)
5. **Validation:** Verify token is valid before executing query
6. **Caching:** Optional local cache for frequently run queries
7. **Query Help:** Built-in examples and usage documentation

### Example Enhanced Script Features
```bash
# Check connection before querying
query-influxdb --check

# Use built-in template
query-influxdb --template temperature --last 7d

# Export as JSON
query-influxdb --format json "[flux query]"

# Cache result for 1 hour
query-influxdb --cache 3600 "[flux query]"
```

## Recommendations for Future Work

### Short Term (1-2 weeks)
1. Create quick reference guide of top 50 entity measurements
2. Document entity-to-measurement mapping for common integrations
3. Set up test Grafana dashboard for energy visualization
4. Create query templates for energy analysis

### Medium Term (1 month)
1. Implement data schema optimization to address collisions
2. Create downsampling policies for data older than 6 months
3. Build Python helper library for common queries (pandas integration)
4. Develop documentation on query performance best practices
5. Set up automated health checks for data integrity

### Long Term (2-3 months)
1. Migrate to cleaner measurement schema (entity-based with tags)
2. Implement time-series analysis for predictive insights
3. Build data export pipeline for data warehousing
4. Setup automated alerting for anomalous patterns
5. Create interactive query tool with web UI
6. Implement data compression for archived records

## Conclusion

The InfluxDB v2 integration with Home Assistant is **comprehensive and functional**, with rich historical data spanning from November 2023. The current schema captures all entity attributes and states effectively. While there are optimization opportunities (particularly around measurement naming and schema design), the database is suitable for:

- Historical analysis (trend detection, pattern recognition)
- Real-time monitoring (active status dashboards)
- Energy analytics (consumption patterns, generation optimization)
- Anomaly detection (threshold alerts, unusual behavior)
- Capacity planning (data growth projections)

### Key Findings

| Aspect | Status | Notes |
|---|---|---|
| Data Completeness | Excellent | 3,622 unique measurements, 43 domains |
| Data Integrity | Good | Consistent schema within domain types |
| Query Performance | Good | Responsive for -1d to -7d ranges |
| Long-term Retention | Excellent | Infinite retention configured |
| Schema Design | Fair | Optimization needed for mixed-type fields |
| Documentation | None | Consider creating entity reference guide |

The main areas for improvement focus on **query patterns and schema optimization** rather than data completeness or availability.

---

**Report Details:**
- **Generated:** 2026-01-25 17:28:10 UTC
- **Data Sampled:** Last 24 hours
- **Sample Size:** 824,132 records
- **Session:** Isolated exploration (sub-agent)
- **Status:** Complete without errors
