# Kitchen Setup Documentation

**Created:** 2026-01-24
**Room:** Kitchen (Cooking, Appliance Monitoring, Dining)
**Focus:** Appliance Integration, Motion Lighting, Food Safety

---

## Device Inventory

| Category | Device | Type | Function |
|----------|--------|------|----------|
| **Lighting** | light.kitchen_table_white, light.kitchen_cooker_white | Color Temperature Lights | Main white lighting with brightness & color control |
| | light.kitchen_table_rgb, light.kitchen_cooker_rgb | RGB Lights | Ambient mood lighting (pink, blue, red) |
| | light.kitchen_ambient_lights, light.kitchen_cabinets, light.kitchen_down_lights, light.kitchen_draws | Accent Lights | Cabinet and drawer accent illumination |
| **Motion** | binary_sensor.kitchen_area_motion, binary_sensor.kitchen_motion_ld2412_presence | Motion Detectors | Primary presence detection |
| | binary_sensor.kitchen_motion_ld2450_presence, binary_sensor.kitchen_motion_2_occupancy | Occupancy Sensors | Secondary occupancy tracking |
| **Environment** | sensor.kitchen_motion_temperature, sensor.kitchen_motion_humidity | Thermometer/Humidity | Temperature and humidity monitoring |
| | sensor.kitchen_motion_ltr390_light, sensor.kitchen_motion_2_illuminance | Light Sensors | Ambient brightness measurement for lighting decisions |
| **Door/Contact** | binary_sensor.kitchen_fridge_door_contact, binary_sensor.kitchen_freezer_door_contact | Contact Sensors | Fridge/freezer door open detection |
| | binary_sensor.kitchen_paper_draw_contact | Contact Sensor | Paper drawer access tracking |
| **Appliances** | sensor.oven_channel_1_power, binary_sensor.oven_powered_on | Smart Oven | Power monitoring and operational state |
| | sensor.kettle_plug_power, sensor.kettle_status | Smart Kettle | Power tracking and heating/standby state |
| | sensor.dishwasher_switch_0_power, binary_sensor.dishwasher_powered_on | Smart Dishwasher | Cycle detection and completion |
| | sensor.dishwasher_tablet_stock | Dishwasher Tablets | Inventory tracking with alerts |
| **Utilities** | sensor.grid_power, sensor.growatt_sph_battery_state_of_charge | Power Grid & Battery | Self-sufficiency monitoring (pulse lights when using grid) |
| | sensor.water_softener_salt_level_average | Water Softener | Salt level with low/critical alerts |
| **Control** | binary_sensor.kitchen_cooker_light_input, binary_sensor.kitchen_table_light_input | Physical Switches | Manual light toggle inputs |
| | switch.ecoflow_kitchen_plug | Smart Outlet | Fridge/freezer backup power control |
| **Safety** | binary_sensor.kitchen_smoke_alarm_smoke, camera.kitchen_high_resolution_channel | Smoke Detector + Camera | Smoke alarm with snapshot capability |

---

## Automation Functions

### 🔆 Motion-Based Lighting

**Triggers:** Motion detected (binary_sensor.kitchen_area_motion or occupancy sensors)

**Logic:**
- Detects motion → checks light level threshold
- **If motion:** Turn on table lights AND cooker lights (if off or dim <100 brightness)
- **If dark:** Check illuminance sensors (LTR390 + secondary) vs thresholds
- **Already on but dim:** Increase brightness
- **Smart decision:** Conditional turn-on for ambient lights based on current state
- Cancels light-off timers on re-detection

**Safety Features:**
- Motion trigger enable boolean (can disable all motion lighting)
- Progressive dimming after motion stops (5-min dim, 5-min off)
- Illuminance thresholds prevent unnecessary lights in bright conditions

**Related Automations:**
- `ID 1606158191303` - Motion Detected - Lights
- `ID kitchen_no_motion_start_timers` - No Motion - Start Timers
- `ID kitchen_no_motion_timer_events` - No Motion - Timer Events

---

### ⏱️ Progressive Dimming Timer Sequence

**Triggers:** Motion sensor turns OFF, or timer completions

**Logic:**
- **Motion stops:** Start 5-minute cooker light dim timer
- **After dim timer:** Dimmed main lights via scene, start 5-minute off timer
- **Conditions for ambient:**
  - Before sunset: Turn off ambient
  - After sunset (before 23:59): Dim ambient lights
- **After off timer:** Turns off main lights completely

**Features:**
- Timer-based gradual light reduction (not abrupt)
- Re-detection of motion cancels entire timer sequence
- Time-aware dimming (different behavior before/after sunset)

**Related Automations:**
- `ID kitchen_no_motion_start_timers` - Start 5m timers
- `ID kitchen_no_motion_timer_events` - Handle timer completion

---

### 🍳 Appliance Monitoring (Oven)

**Triggers:** Oven power consumption changes

**Detection Logic:**
1. **Preheat Detection:** Power drops below 100W (preheat phase)
   - Sets `oven_preheated` flag
   - Notifies: "Oven preheated"
   - Targets: People at home

2. **Preheat Timeout Alert:** Oven on for 1h 10m
   - Triggers if preheat flag still set
   - Warns: "Oven left on too long"
   - Targets: All users

3. **Preheat Reset:** Powered off for 5m 30s
   - Clears `oven_preheated` flag
   - Automation ID: 1694521864037

**Related Automations:**
- `ID 1694521590170` - Oven Preheated
- `ID 1694521864037` - Reset Oven Preheated
- `ID 1763292351760` - Oven On For Long Time

---

### 🍽️ Appliance Monitoring (Dishwasher)

**Triggers:** Dishwasher power consumption and cycle state

**Cycle Logic:**
1. **Cycle Start:** Power >3W for 1+ minute
   - Sets `dishwasher_cycle_in_progress` flag
   - Consumes one dishwasher tablet
   - Checks stock: Alert if <9 tablets

2. **Cycle Completion:** Power <4W for 20+ seconds
   - Clears cycle flag
   - Notifies completion
   - Conditional on presence: Announce if home, log if away

3. **Tablet Tracking:**
   - Consumes tablet on cycle start
   - Warns when stock <9
   - Critical alert when stock = 0

**Safety Features:**
- 30-minute reset timer (clears cycle if stuck)
- Presence-aware notifications
- Tablet inventory alerts

**Related Automations:**
- `ID 1694521590172` - Dishwasher Cycle Starts
- `ID 1694521864038` - Reset Dishwasher Cycle
- `ID 1595679010797` - Dishwasher Started (tablet consumption)
- `ID 1595679010798` - Dishwasher Finished

---

### 🚪 Appliance Door Monitoring (Fridge/Freezer)

**Triggers:** Contact sensor state changes

**Logic:**
- **Door Opened:** Log event with appliance name detection
- **Door Open Long:** Multiple timeouts (4m, 30m, 45m, 1h) with escalating alerts
  - 4m: Warning log
  - 30m: Notification + voice alert
  - 45m+: Escalation to all users
- **Power Loss:** Fridge/freezer becomes unavailable → Alert users

**Safety Features:**
- Prevents food spoilage from open doors
- Escalating alerts (don't overwhelm immediately)
- Power loss detection for emergency response

**Related Automations:**
- `ID appliance_door_opened` - Door Opened
- `ID appliance_door_closed` - Door Closed
- `ID appliance_door_open_long` - Long Open Alert
- `ID 1657801925107` - Plug Turned Off

---

### 🫖 Kettle Automation

**Triggers:** Kettle status transitions

**Logic:**
- **Kettle Boiled:** Status changes from "heating" to "standby"
- **Action:** Announce "Kettle boiled" via Alexa

**Related Automations:**
- `ID 1759577733332` - Kettle Boiled

---

### 💧 Water Softener Monitoring

**Triggers:** Salt level thresholds exceeded

**Detection Logic:**
1. **Low Salt:** Level above warning threshold for 2+ hours
   - Sends notification: "Refill water softener salt soon"

2. **No Salt:** Level reaches zero
   - Critical alert: "Water softener salt depleted - refill immediately"

**Related Automations:**
- `ID 1688681085048` - Low Water Softener Salt
- `ID 1688681085049` - No Water Softener Salt

---

### 🌐 Grid Power & Battery Status

**Triggers:** Grid power consumption measurement

**Logic:**
- **Using Grid:** grid_power >100W AND battery has charge
  - Pulse pink RGB ambient lights (5 pulses, 1-sec interval)
  - Visual indicator: "Kitchen is drawing from grid"

- **Off Grid:** grid_power <100W
  - Turn off RGB ambient lights
  - Indicates: "Kitchen running on solar/battery"

**Purpose:** Visual feedback on energy source

**Related Automations:**
- `ID 1735567472488` - Using Power From The Grid
- `ID 1735567472489` - Stops using Power From The Grid

---

### 🔥 Smoke Alarm Detection

**Triggers:** Smoke alarm triggers

**Actions:**
1. Snapshot camera (kitchen_high_resolution_channel)
2. Announce via Alexa: "Smoke detected in kitchen"
3. Send notification to all users
4. Store snapshot for reference

**Safety Features:**
- Immediate notification and voice alert
- Photo evidence captured
- Emergency response coordination

**Related Automations:**
- `ID 1757836826541` - Smoke Alarm

---

### 🔌 Manual Light Control

**Triggers:** Physical switch input changes

**Logic:**
- **Cooker Light Toggle:** Switch toggles cooker white light on/off
- **Table Light Toggle:** Switch toggles table white light on/off
- Overrides motion automation when manually activated

**Related Automations:**
- `ID 1721248529363` - Cooker Light Switch Toggle
- `ID 1721248529364` - Table Light Switch Toggle

---

### 🗂️ Utility Monitoring

**Triggers:** Paper drawer contact changes

**Logic:**
- **Drawer Opened:** Log access event
- Tracks usage patterns
- Can identify over-use

**Related Automations:**
- `ID 1716112515827` - Paper Draw Opened

---

### ⏰ Time-Based Scheduling

**Night Light Off:** 23:30:00
- Turns off main lights at night
- Applicable to weekdays and weekends
- Automation ID: 1583797341647

**Morning Light Off:** 08:50 (weekday) / 09:00 (weekend)
- Turns off main lights in morning
- Smart scheduling based on day type
- Automation ID: 1606294735952

**Evening Dim:** Sunset or 06:45:00
- Dims accent lights
- Prep for evening mode
- Automation ID: 1588197104336

---

## Room Layout & Device Placement

```
                    NORTH (Patio/Garden)
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║  🪟 Patio Door/Window         Table Area             ║
    ║                          ┌──────────────────┐        ║
    ║                          │  🍽️ Dining Table │        ║
    ║                          │  💡 Lights       │        ║
    ║                          │  📏 Motion       │        ║
    ║                          │  🌡️ Sensors      │        ║
    ║                          └──────────────────┘        ║
    ║                                                       ║
    ║  Paper Draw        Kitchen Central                    ║
    ║  📥 Draws          ════════════════                   ║
    ║  ┌──────┐         💡 Cooker Light                    ║
    ║  │Stock │         💡 Cooker RGB                      ║
    ║  └──────┘         🍳 Oven (power monitor)            ║
    ║                  🍽️ Dishwasher (power monitor)      ║
    ║                  🫖 Kettle (power monitor)           ║
    ║                                                       ║
    ║  Appliances      Refrigeration Zone                  ║
    ║  🧊 Fridge       ❄️ Fridge/Freezer                  ║
    ║  ❄️ Freezer      🚪 Door Sensors                     ║
    ║  🚪 Door Sensors  💨 Power Monitoring               ║
    ║                                                       ║
    ║  💧 Water Softener Salt Monitor                      ║
    ║  🔋 Grid/Battery Status (visual via pink lights)     ║
    ║  🌐 Smart Outlet Control (ecoflow plug)              ║
    ║  🔥 Smoke Alarm with Camera Snapshot                 ║
    ║                                                       ║
    ║  Ambient Lighting                                     ║
    ║  💡 Cabinet accent lights                            ║
    ║  💡 Down lights                                      ║
    ║  💡 Drawer accent lights                             ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
                 SOUTH (Main Kitchen Area)
```

---

## Key Automation Workflows

### Morning Routine (08:50-09:00 AM)

```
Weekday (08:50)                    Weekend (09:00)
   ↓                                    ↓
Turn Off Lights Automation
   ├─ Check day type
   ├─ Turn off main lights
   └─ Log morning routine
```

**Decision Tree:**
1. Is it time? (08:50 weekday or 09:00 weekend)
2. Execute: Turn off lights scene
3. Log action

---

### Motion Detected (Any Time of Day)

```
Motion Sensor: ON
   ↓
Check Enable Switch
   ├─ Disabled → Skip all actions
   └─ Enabled → Continue
       ↓
    Check Illuminance
    ├─ Very Bright → Skip (daylight sufficient)
    ├─ Medium → Turn on dim lights
    └─ Dark → Turn on full brightness
         ↓
      Evaluate Each Light Zone:
      ├─ Table lights: On if off or <100 brightness
      ├─ Cooker lights: Same as table (with brightness check)
      └─ Ambient lights: Complex conditional based on time
                            ├─ Before sunset: Dim
                            ├─ After sunset: On or dim
                            └─ After 23:59: Off
           ↓
      Cancel Any Existing Timers
           ↓
      Log with timestamp emoji
```

---

### Motion Stops (Timer Sequence)

```
Motion Sensor: OFF
   ↓
Start 5-minute Dim Timer
   ├─ If motion detected during timer: Cancel
   └─ If timer completes → Dim Phase
       ↓
    Dim main lights via scene
    Dim or turn off ambient lights (time-aware)
    Start 5-minute Off Timer
       ├─ If motion detected: Cancel
       └─ If timer completes → Off Phase
           ↓
        Turn off main lights
        Turn off ambient lights
        Complete shutdown
```

---

### Appliance Usage: Oven

```
Oven powered ON (>100W)
   ↓
Continue monitoring power
   ├─ If power >100W → Still preheating
   └─ If power drops <100W
       ├─ Set oven_preheated = True
       ├─ Notify: "Oven preheated"
       └─ Log with timestamp
            ↓
         Monitor Duration
         ├─ If 1h 10m passes with flag on
         │  └─ Alert: "Oven left on too long"
         │
         └─ If powered off for 5m 30s
            └─ Set oven_preheated = False
               └─ Clear flag
```

---

### Appliance Usage: Dishwasher

```
Dishwasher: Power >3W for 1+ minute
   ↓
Set cycle_in_progress = True
Consume 1 tablet
Check stock
   ├─ Stock <9 → Send warning alert
   └─ Stock 0 → Send critical alert
       ↓
    Continue monitoring power
    ├─ If power <4W for 20+ seconds
    │  └─ Set cycle_in_progress = False
    │     ├─ Announce: "Dishwasher finished"
    │     └─ Check presence:
    │         ├─ At home → Voice + notification
    │         └─ Away → Log only
    │
    └─ If 30+ minutes pass without state change
       └─ Force reset flag (safety)
```

---

### Fridge Door Monitoring

```
Door Contact: OPEN
   ↓
Log: "Fridge opened at [TIME]"
   ├─ If door closes within 4m: Log "Closed"
   │
   ├─ If door open 4-30m: Log warning
   │
   ├─ If door open 30-45m: Notify + voice
   │
   ├─ If door open 45m+: Escalate to all users
   │
   └─ Monitor power continuously
       └─ If power lost: Alert "Fridge unplugged"
```

---

## Configuration Parameters

### Light Level Thresholds
- `input_number.kitchen_light_level_threshold` - Primary motion trigger level (lux)
- `input_number.kitchen_light_level_2_threshold` - Secondary light level threshold

### Appliance Thresholds
- `input_number.low_water_softener_salt_level` - Warning threshold (%)
- `input_number.no_water_softener_salt_level` - Critical threshold (%)
- `input_number.growatt_battery_discharge_stop_soc` - Battery reserve level

### Time Schedules
- Motion-activated lights: Turn on immediately, dim after 5-10 min no motion
- Night mode: 23:30 (disable motion lighting)
- Morning shutdown: 08:50 (weekday) / 09:00 (weekend)
- Evening dim: Sunset or 06:45

### Appliance Thresholds
- Oven preheat: <100W power
- Oven timeout: 1h 10m
- Dishwasher cycle detect: >3W for 1+ min
- Kettle: Status transition from heating to standby

---

## Helper Entities

### Input Booleans
- `input_boolean.enable_kitchen_motion_triggers` - Master enable for motion lighting
- `input_boolean.oven_preheated` - Oven preheat status flag
- `input_boolean.enable_oven_automations` - Enable/disable oven automations
- `input_boolean.dishwasher_cycle_in_progress` - Track dishwasher cycle state
- `input_boolean.enable_dishwasher_automations` - Enable/disable dishwasher automations
- `input_boolean.dishwasher_clean_cycle` - Flag for clean cycle vs normal

### Timers
- `timer.kitchen_cooker_light_dim` - 5-minute cooker light dim timer
- `timer.kitchen_cooker_light_off` - 5-minute cooker light off timer
- `timer.kitchen_table_light_dim` - 5-minute table light dim timer
- `timer.kitchen_table_light_off` - 5-minute table light off timer
- `timer.check_smoke_alarms` - Smoke alarm check interval

### Input Numbers
- `input_number.kitchen_light_level_threshold` - Motion lighting threshold
- `input_number.kitchen_light_level_2_threshold` - Secondary threshold
- `input_number.low_water_softener_salt_level` - Warning level
- `input_number.no_water_softener_salt_level` - Critical level
- `input_number.growatt_battery_discharge_stop_soc` - Battery reserve

### Input Text
- `input_text.camera_external_folder_path` - Path for camera snapshots

---

## Scripts

### Light Management Scripts
- `script.kitchen_cancel_all_light_timers` - Cancel all dim/off timers
- `script.kitchen_toggle_kitchen_ambient_lights` - Toggle ambient light group
- `script.kitchen_toggle_accent_lights` - Toggle accent lights
- `script.kitchen_pulse_ambient_light_pink` - Pulse pink 5x (grid power indicator)

### Notification Scripts
- `script.kitchen_oven_preheated_notification` - Notify when oven ready
- `script.dishwashing_complete_notification` - Notify when dishwasher done
- `script.send_to_home_log` - Log to home log system
- `script.send_direct_notification` - Direct mobile notification
- `script.log_with_clock` - Log with timestamp emoji
- `script.alexa_announce` - Alexa voice announcement

---

## Sensors

### PC/Appliance Usage Tracking
- Dishwasher Running Time Today/Yesterday/Last 24h/This Week/Last 30 Days
- Fridge Opened Count (Today/Yesterday)
- Fridge Freezer Running Time Today/Yesterday/Last 24h/This Week/Last 30 Days

### Environment Monitoring
- Kitchen Mould Indicator (calculated from temp/humidity + outdoor temp)

### Template Binary Sensors
- Kettle Powered On (power >10W)
- Dishwasher Powered On (power >4W)
- Fridge Freezer Powered On (10-100W range)
- Oven Powered On (power >16W)
- Low Water Softener Salt
- No Water Softener Salt

---

## Status Indicators

### Light Scenes for Status
- **Main Lights On:** Cooker and table lights full brightness
- **Main Lights Dim:** Cooker and table at 10% brightness
- **Ambient On:** Cabinets, down lights, draws at 255 brightness
- **Ambient Dim:** Accent lights at 26% brightness
- **RGB Status Lights:**
  - Pink: Grid power usage
  - Blue: Available for temperature display
  - Red: Alert state

---

## Key Features

✅ **Motion-Activated Lighting** - Automatic on/off with progressive dimming
✅ **Appliance Integration** - Oven/dishwasher/kettle status monitoring
✅ **Food Safety** - Fridge door timeout alerts, smoke detection
✅ **Energy Awareness** - Visual grid power indicator (pink lights)
✅ **Consumables Tracking** - Dishwasher tablet inventory
✅ **Water Quality** - Salt level monitoring with alerts
✅ **Timer-Based Control** - Progressive dimming prevents abrupt darkness
✅ **Manual Overrides** - Physical switch inputs override automation
✅ **Presence-Aware** - Notification routing based on occupancy
✅ **Safety Features** - Smoke alarm snapshot, appliance timeout alerts
✅ **Usage Statistics** - Appliance running time tracking for efficiency

---

## File Structure

```
packages/rooms/kitchen/
├── kitchen.yaml          # Main automation configuration (21 automations)
├── KITCHEN-SETUP.md      # This file - Room documentation
└── [future sub-files if consolidation needed]
```

---

**Last Updated:** 2026-01-24
**Documentation Version:** 1.0
**Automation Count:** 21
**Device Count:** 35+
**Configuration Files:** 1 main + reference docs
