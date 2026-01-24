# Office Setup Documentation

**Created:** 2026-01-24
**Room:** Office (Danny's Work/Gaming Space)
**Focus:** Smart Automation, Streaming, Gaming Integration

---

## Device Inventory

| Category | Device | Type | Function |
|----------|--------|------|----------|
| **Lighting** | light.office_2, 3, 4 | Color Temperature Lights | Main ambient/desk lighting with brightness & color control |
| | light.office_light | RGB Light | Status indicator (notifications, PC off, door open) |
| | light.office_key_lights | Streaming Light | Illumination for video/streaming |
| **Motion** | binary_sensor.office_motion_2 | Motion Detector | Detects presence in room |
| | sensor.office_motion_2_target_distance | Proximity Sensor | Distance-based motion detection |
| **Environment** | sensor.office_motion_2_illuminance | Light Sensor | Measures ambient brightness |
| | sensor.office_area_mean_temperature | Thermometer | Room temperature monitoring |
| | binary_sensor.office_windows | Window Sensor | Detects open/closed state |
| **Climate** | switch.office_fan | Smart Fan | Temperature-controlled ventilation |
| **Window** | cover.office_blinds | Motorized Blinds | Tilt control (0-50 position) |
| **Computer** | group.jd_computer | PC Group | Tracks personal PC power state |
| | group.dannys_work_computer | PC Group | Tracks work PC power state |
| | switch.external_hdd | Storage Device | External backup drive |
| | sensor.steam_danny | Gaming Tracker | Game detection via Steam |
| **Other** | switch.fly_zapper | Pest Control | Auto-shuts off after 2 hours |
| | Remote Control | MQTT Device | Toggle key lights & fan |

---

## Automation Functions

### 🔆 Motion-Based Lighting

**Triggers:** Motion detected or proximity sensor activation

**Logic:**
- Detects motion → checks brightness level
- **Bright outside**: Skips turning on lights
- **Dark**: Turns on main lights (office_2, office_3 at full brightness)
- **Already on but not bright enough**: Increases brightness
- Cancels light-off timers on re-detection
- Turns off after 3 minutes no motion (1 min detection + 1 min timer + 1 min additional)

**Related Automations:**
- `ID 1606428361967` - Motion Detected
- `ID 1587044886896` - No Motion Detected
- `ID 1587044886897` - Office Light Off Timer Finished

---

### 🌡️ Temperature Control

**Triggers:** Temperature thresholds reached

**Priority Levels:**
1. **26°C+**: Auto-on if daytime (8:30-22:00) & people home
2. **29°C+**: Warning notification with manual toggle option
3. **31°C+**: Emergency override - forces fan on immediately

**Safety Features:**
- **3:00 AM Shutdown**: Force fan off (overnight safety)
- Prevents fan from running indefinitely
- Escalating notification strategy

**Related Automations:**
- `ID 1622584959878` - High Temperature
- `ID 1728046359271` - Fan Turns Off at 3am

---

### 🪟 Intelligent Blind Management

**Schedule-Based Control:**
- **8:00 AM**: Opens blinds (with brightness & computer state checks)
- **Sunset**: Partially closes to 25% tilt
- **Sunset +1 hour**: Fully closes (0% tilt)

**Brightness-Based Control:**
- **Very Bright**: Fully closes blinds
- **Medium Bright**: Tilt to 25%
- **Dark**: Opens to 50%

**Sun Position Tracking:**
- **Morning Sun (8:10+)**: Tracks azimuth to avoid direct glare
- **Afternoon Sun**: Closes if sun in view + room is dark
- Uses both azimuth and elevation angles

**Safety Features:**
- **Window Open**: Blocks blind closure (prevents damage)
- **Computer Offline**: Opens blinds
- Responsive to external conditions

**Related Automations:**
- `ID 1622374444832` - Open Blinds In The Morning
- `ID 1622374233312` - Partially Close Office Blinds At Sunset
- `ID 1622374233310` - Fully Close Office Blinds At Night
- `ID 1622666920056` - Window Closed At Night
- `ID 1680528200295` - No Direct Sun Light In The Morning
- `ID 1680528200297` - No Direct Sun Light In The Afternoon
- `ID 1678300398737` - Bright Outside
- `ID 1678300398736` - Really Bright Outside
- `ID 1678637987424` - Outside Went Darker

---

### 💻 Computer Integration

**PC Status Tracking:**
- Personal PC (JD Computer)
- Work PC (Danny's Work Computer)
- Steam game detection

**Computer ON (1 min):**
- Activates goXLR audio mixer
- Runs brightness check script
- Adjusts blinds if needed

**Computer OFF (1 min):**
- Turns off key lights

**Computer OFF (5 min):**
- Opens blinds (if daytime & sunny)

**Computer OFF (10 min):**
- Turns off external HDD backup drive
- Powers down EcoFlow plug

**Gaming Detection:**
- Monitors Steam for specific games (e.g., ARC Raiders)
- Automatically closes blinds when gaming
- Prevents screen glare during gameplay

**Uptime Tracking:**
- Daily uptime statistics
- Weekly uptime statistics
- Monthly (30-day) uptime statistics
- Yesterday's uptime

**Related Automations:**
- `ID 1619865008647` - Computer Turned On
- `ID 1606256309890` - Computer Turned Off For A Period Of Time
- `ID 1678741966796` - Computer Turned Off
- `ID 1678741966794` - Computer Turned Off After Sunrise
- `ID 1768737131768` - Playing Computer Games

---

### 🎮 Streaming & Gaming Features

**Remote Control:**
- MQTT-based remote with 2 buttons
- Button 1 (open): Toggle key lights
- Button 2 (close): Toggle fan

**Status Light Notifications (office_light RGB):**
- 🟢 Green: Door open
- 🔵 Blue: Front door open (secondary notification)
- 🟣 Purple: Front garden motion detected
- 🔴 Red: PC off notification

**Key Light Control:**
- Toggles via remote or automation
- Used for streaming/video recording
- Brightness and color adjustable

**Scene Integration:**
- PC turned off notification scenes
- Light notification scenes
- Doorbell notification scene

**Related Automations:**
- `ID 1722108194998` - Remote Keylight
- `ID 1722108194999` - Remote Fan

---

### 🔌 Smart Device Controls

**External Backup Drive:**
- Powers down when PC off for 10+ minutes
- Prevents unnecessary power consumption
- Extends drive lifespan

**EcoFlow Plug Management:**
- Controlled via script when PC off
- Smart power management

**Fly Zapper:**
- Auto-shutoff after 2 hours
- Prevents accidental extended operation
- Saves power and extends bulb life

**Light Status Monitor:**
- Front door status light turns off after 3 minutes
- Prevents notification spam
- Auto-reset after status changes

**Related Automations:**
- `ID 1721434316175` - Fly Zapper
- `ID 1743186662871` - Front Door Status On For Long Time
- Custom scripts for device management

---

## Room Layout & Device Placement

```
                         NORTH (Morning Sun)
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║  🪟 Window           🪟 Window (Sensor)              ║
    ║  (Cover Office      ┌─────────────┐                  ║
    ║   Blinds)           │  Motorized  │                  ║
    ║  ▼ ▼ ▼ ▼ ▼        │  Blinds     │                  ║
    ║                     │  (Tilt 0-50)│                  ║
    ║  ┌─────────────┐    └─────────────┘                  ║
    ║  │   Desk      │                                      ║
    ║  │  Setup      │    💡 office_2   💡 office_3        ║
    ║  │             │    (Main Lights - Color Temp)       ║
    ║  └──┬──────────┘                                      ║
    ║     │                                                  ║
    ║  ┌──┴─────────────────────┐                           ║
    ║  │  PC Monitors           │  🌡️ Temperature          ║
    ║  │  (JD's Computer)       │     Sensor               ║
    ║  │                        │                           ║
    ║  │ 💻 External HDD        │  📏 office_motion_2      ║
    ║  │    Backup Drive        │     (Proximity +          ║
    ║  │                        │      Illuminance)         ║
    ║  └────────────────────────┘                           ║
    ║                                                       ║
    ║  🎙️  GoXLR Audio Mixer                               ║
    ║  🖥️  Work Computer (Separate PC)                      ║
    ║  💡 office_key_lights (Streaming/RGB)                ║
    ║  🎮 Steam Game Detection                             ║
    ║  📡 Remote Control (MQTT)                            ║
    ║                                                       ║
    ║  💡 office_light (Status Light - RGB)                ║
    ║     Status Indicators:                               ║
    ║     - Green: Door Open                               ║
    ║     - Blue: Door Open (Different notification)       ║
    ║     - Purple: Motion Detected                        ║
    ║     - Red: PC Off Notification                       ║
    ║                                                       ║
    ║  💨 office_fan                                        ║
    ║     (Temp-controlled, >26°C auto-on)                 ║
    ║                                                       ║
    ║  🪰 Fly Zapper                                        ║
    ║     (Auto-off after 2 hours)                          ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
           SOUTH (Afternoon Sun - Higher Azimuth)
```

---

## Key Automation Workflows

### Morning Routine (8:00 AM)

```
Blind Opening Logic:
├─ Check brightness (front garden illuminance)
├─ Check if computers are on (work/personal)
├─ If VERY BRIGHT: Keep blinds closed (avoid glare)
├─ If MEDIUM BRIGHT: Open to 25% tilt
└─ If DARK: Fully open (50% tilt)
```

**Decision Tree:**
1. Is it sunrise? → Continue
2. Is it after 8:00 AM? → Continue
3. Are computers on? → Factor in
4. Check external brightness levels
5. Check sun position (azimuth/elevation)
6. Apply appropriate blind tilt

---

### During Work (Computer On)

```
Active Workflow:
├─ Lights auto-adjust with motion
│   ├─ Motion on: Brightness check
│   ├─ Motion off: 2 min wait → 1 min timer → Off
│   └─ Brightness-aware: Skip if room is bright
├─ Blinds respond to sun position & brightness
│   ├─ Morning sun (azimuth <X): Avoid glare
│   ├─ Afternoon sun (azimuth >X): Close if needed
│   └─ Responsive to brightness thresholds
├─ Temperature fan activates if >26°C
│   ├─ Daytime priority
│   ├─ Emergency override at 31°C
│   └─ Notification at 29°C
├─ If gaming detected: Close blinds (reduce glare)
├─ GoXLR audio mixer: Active
├─ Key lights: Available for streaming
└─ Status light: Shows current notifications
```

---

### After Work (Computer Off)

```
Shutdown Sequence:
├─ At 1 min: Turn off key lights
├─ At 5 min: Open blinds (if daytime & sunny)
├─ At 10 min:
│   ├─ Turn off external HDD
│   ├─ Turn off EcoFlow plug
│   └─ GoXLR mixer off
└─ Lights continue: Motion-based control
```

---

### Evening (Sunset)

```
Evening Routine:
├─ At Sunset: Partial close to 25% tilt
│   └─ Check: Window sensor (don't close if open)
├─ At Sunset +1 hour: Full close (0% tilt)
│   └─ Check: Window sensor (safety)
├─ Temperature management:
│   ├─ If >26°C: Keep fan on
│   └─ At 3:00 AM: Force fan off (sleep safety)
└─ Lights: Motion sensors still active
```

---

## Configuration Parameters

### Temperature Thresholds
- `sensor.office_area_mean_temperature`
- Warning: 26°C (auto-on if daytime)
- Alert: 29°C (notification)
- Emergency: 31°C (override)

### Brightness Thresholds
- `input_number.office_light_level_threshold` - Motion trigger level
- `input_number.blind_low_brightness_threshold` - Partial opening
- `input_number.blind_high_brightness_threshold` - Closing level

### Sun Position Thresholds
- `input_number.office_blinds_morning_sun_azimuth_threshold` - Morning sun angle
- `input_number.office_blinds_afternoon_sun_azimuth_threshold` - Afternoon sun angle
- `input_number.office_blinds_afternoon_sun_elevation_threshold` - Sun elevation

### Time Schedules
- Motion detection: 2 minutes no-motion delay
- Light-off timer: 1 minute
- Blind opening: 8:00 AM
- Partial close: At sunset
- Full close: Sunset +1 hour
- Fan shutdown: 3:00 AM
- PC off detection: 1, 5, 10 minutes

---

## Helper Entities

### Input Booleans
- `input_boolean.enable_office_motion_triggers` - Enable/disable motion lighting
- `input_boolean.enable_office_blind_automations` - Enable/disable blind automations

### Timers
- `timer.office_lights_off` - 1-minute light-off timer

### Groups
- `group.jd_computer` - Personal PC devices
- `group.dannys_work_computer` - Work PC devices

---

## Scripts

### Blind Control
- `office_open_blinds` - Opens blinds to 50% tilt
- `office_close_blinds` - Fully closes blinds (0% tilt)
- `office_check_brightness` - Checks brightness and adjusts blinds accordingly

### Device Management
- `office_turn_off_backup_drive` - Powers down external HDD
- `ecoflow_office_turn_off_plug` - Powers down EcoFlow outlet
- `office_pc_turned_off_notification` - Lights notification sequence

---

## Sensors

### PC Uptime Tracking
- PC Uptime Today (today's hours)
- PC Uptime Last 24 Hours
- PC Uptime Yesterday
- PC Uptime This Week
- PC Uptime Last 30 Days
- Work Computer Uptime Today
- Work Computer Uptime Yesterday
- Work Computer Uptime This Week
- Work Computer Uptime Last 30 Days

---

## Status Indicators

### RGB Status Light (light.office_light)

**Notification Scenes:**
- Doorbell notification: Green (Green RGB)
- PC off notification: Purple (Purple RGB)
- Front door open: Blue (Blue RGB)
- Front garden motion: Purple (Purple RGB)
- Door closed notification: Off
- Auto-timeout: 3 minutes

---

## Key Features

✅ **Adaptive Lighting** - Brightness-aware motion response
✅ **Climate Control** - Graduated temperature alerts (26°C warning → 31°C emergency)
✅ **Sun Tracking** - Avoids glare based on sun azimuth & elevation
✅ **PC Integration** - Game detection, uptime tracking, auto-shutdown helpers
✅ **Streaming Ready** - Key lights, audio mixer, remote controls
✅ **Status Notifications** - RGB indicator light for multiple events
✅ **Safety Features** - Window sensor blocks blind closure, emergency fan override
✅ **Gaming Optimized** - Auto-closes blinds when gaming, reduces glare
✅ **Remote Control** - MQTT-based buttons for key lights & fan
✅ **History Tracking** - PC uptime statistics (daily/weekly/monthly)

---

## File Structure

```
packages/rooms/office/
├── office.yaml          # Main automation configuration
├── OFFICE-SETUP.md      # This file - Room documentation
└── [future sub-files]
```

---

**Last Updated:** 2026-01-24
**Documentation Version:** 1.0
**Automation Count:** 24
**Device Count:** 18
**Configuration Files:** 1 main + reference docs
