# Living Room Setup Documentation

**Created:** 2026-01-24
**Room:** Living Room (Primary Entertainment & Relaxation Space)
**Focus:** Smart Automation, Entertainment Integration, Adaptive Lighting, Climate Control

---

## Device Inventory

| Category | Device | Type | Function |
|----------|--------|------|----------|
| **Lighting - Lamps** | light.living_room_lamp_left, light.living_room_lamp_right | Color Temperature Lamps | Main ambient floor lamps with color and brightness control |
| **Lighting - Ceiling** | light.living_room_left, light.living_room_left_2, light.living_room_left_3 | RGB/Color Temperature Lights | Left side ceiling lights (3 bulbs) |
| | light.living_room_right, light.living_room_right_2, light.living_room_right_3 | RGB/Color Temperature Lights | Right side ceiling lights (3 bulbs) |
| | light.lounge_ceiling | Group/Light | Ceiling light group |
| | light.living_room_lamps | Group/Light | Lamps group |
| | light.living_room_ceiling | Group/Light | All ceiling lights group |
| **Lighting - Ambient** | light.tv_backlight | WLED RGB Light | TV backlight for ambient viewing |
| **Motion** | binary_sensor.living_room_area_motion | Motion Group | Aggregated motion detection |
| | binary_sensor.lounge_motion | Motion Detector | Primary lounge motion sensor |
| | binary_sensor.living_room_motion_occupancy | Occupancy Sensor | Secondary occupancy tracking |
| | binary_sensor.apollo_r_pro_1_w_ef755c_ld2412_presence | Presence Sensor | Advanced presence detection (LD2412) |
| **Environment** | sensor.apollo_r_pro_1_w_ef755c_ltr390_light | Light Sensor | Primary illuminance measurement (LTR390) |
| | sensor.living_room_motion_illuminance | Light Sensor | Secondary illuminance measurement |
| | sensor.living_room_motion_temperature | Temperature Sensor | Room temperature monitoring |
| | sensor.living_room_motion_humidity | Humidity Sensor | Room humidity monitoring |
| | sensor.front_garden_motion_illuminance | Light Sensor | Outdoor brightness for blind control |
| **Window Covers** | cover.living_room_blinds_left | Motorized Blind | Left window blind with tilt control (0-50) |
| | cover.living_room_blinds_middle | Motorized Blind | Middle window blind with tilt control (0-50) |
| | cover.living_room_blinds_right | Motorized Blind | Right window blind with tilt control (0-50) |
| | binary_sensor.living_room_windows | Window Sensor Group | Detects if any windows are open |
| **Entertainment** | binary_sensor.tv_powered_on | Power Monitor | TV power state detection (>10W) |
| | sensor.tv_plug_power | Smart Plug Power Monitor | TV power consumption tracking |
| | binary_sensor.playstation_powered_on | Power Monitor | PlayStation power state (>15W) |
| | sensor.playstation_plug_power | Smart Plug Power Monitor | PlayStation power consumption |
| | remote.living_room | Harmony Hub | Universal remote control (Logitech Harmony) |
| | switch.harmony_hub_plug | Smart Plug | Harmony Hub power control |
| **Computers** | group.family_computer | Device Tracker Group | Family PC presence tracking |
| | group.terinas_work_computer | Device Tracker Group | Terina's work laptop tracking |
| | device_tracker.doug | Device Tracker | Family PC (Doug) tracking device |
| **Control** | binary_sensor.living_room_ceiling_lights_input_0 | Physical Switch | Manual ceiling light toggle input |
| | switch.server_fan | Smart Fan | Server/equipment cooling fan |
| **Other** | sensor.sun.sun | Sun Tracker | Sun position (azimuth/elevation) for blind control |
| | alarm_control_panel.house_alarm | Alarm Panel | House security system integration |
| | binary_sensor.stairs_motion_occupancy | Motion Detector | Stairs motion (for morning routine) |

---

## Automation Functions

### 🔆 Motion-Based Lighting

**Triggers:** Motion detected from any motion sensor (area, lounge, occupancy, presence)

**Logic:**
- Detects motion → checks room illuminance levels
- **Dark Room (primary logic):**
  - Light levels below thresholds (LTR390 < threshold OR motion illuminance < threshold)
  - Lamps are OFF or dim (brightness < 190)
  - If ceiling light already on: Turn on full scene (lamps + ceiling)
  - If ceiling light off: Turn on lamps only
  - Smooth transition: 1 second fade
- **Bright Room (visual signal):**
  - Light levels below threshold BUT lamps are OFF
  - Flash yellow signal (1 second pulse, then off)
  - Visual acknowledgment without turning lights on permanently
- **Brightness-aware:** Skips activation if room already bright enough
- Cancels any pending dim/off timers when motion detected

**Safety Features:**
- Enable/disable boolean (input_boolean.enable_living_room_motion_triggers)
- Dual illuminance sensors for redundancy
- Progressive dimming prevents abrupt darkness
- Queue mode (max 10) handles rapid motion changes

**Related Automations:**
- `ID 1583956425622` - Motion Detected
- `ID 1606170045632` - No Motion
- `ID 1606170045630` - No Motion After Short Time Dim Lights
- `ID 1605567425876` - No Motion For Long Time

---

### ⏱️ Progressive Dimming Timer Sequence

**Triggers:** Motion sensor clears or timer events

**Logic:**
- **Motion stops:** Start 2-minute dim timer
- **After 2 min (dim timer):**
  - Dims lights via scenes
  - Starts 5-minute off timer
  - Scene selection based on what's currently on:
    - Both lamps + ceiling: scene.living_room_dim_lights
    - Lamps only: scene.living_room_dim_lamps
    - Ceiling only: scene.living_room_dim_ceiling_lights
- **After 5 min (off timer):**
  - Turns off lights completely
  - Same scene logic applies for targeted shutdown
- **Total no-motion time:** 7 minutes (2 min + 5 min)

**Features:**
- Timer-based gradual reduction (not abrupt)
- Re-detection cancels entire sequence
- Conditional scene selection for intelligent control
- Separate timers for each zone

**Related Automations:**
- `ID 1606170045632` - No Motion (starts 2-min timer)
- `ID 1606170045630` - Dim Lights After Short Time
- `ID 1605567425876` - Turn Off After Long Time

---

### 🪟 Intelligent Blind Management

**Schedule-Based Control:**
- **7:30 AM:** Partial open to 25% tilt
- **8:00 AM:** Full open to 50% tilt
- **Sunset or 20:00:** Partial close to 25% tilt
- **Sunset +1hr or 21:00:** Full close to 0% tilt (privacy mode)

**Sun Position Tracking:**
- **Morning Sun Avoidance:** When azimuth below morning threshold, opens blinds (sun moved away)
- **Afternoon Sun Avoidance:** When azimuth AND elevation above afternoon thresholds, opens blinds
- **Sun in Position:** Automatically adjusts based on sun's path through the day
- Uses both azimuth and elevation angles for precision

**Brightness-Based Control:**
- **Bright Outside (medium):** Closes middle & right blinds to 25% when:
  - Illuminance between low and high thresholds
  - Computer(s) are on (prevents glare on screens)
  - Sun in specific position window
  - After 8:00:30 AM
- **Really Bright Outside (high):** Closes middle & right blinds to 0% when:
  - Illuminance above high threshold
  - Computer(s) are on
  - Sun in position window
- **Outside Went Darker:** Opens all blinds to 50% when:
  - Illuminance below low threshold for 5 minutes
  - ALL computers are OFF (no glare concern)
  - During daylight hours

**Computer Integration:**
- Tracks family_computer and terinas_work_computer groups
- Closes blinds when computers on + bright outside
- Opens blinds 5 minutes after ALL computers turn off (daytime only)
- Weekday logic: Only considers work laptop Mon-Fri

**Safety Features:**
- **Window Open Detection:** Blocks all blind movements if windows open
- **Time Constraints:** Only operates during daylight (after sunrise, before sunset)
- **Position Validation:** Checks current position before moving

**Related Automations:**
- `ID 1677711735249` - Open Blinds In The Morning (7:30 AM)
- `ID 1677711735250` - Open Blinds In The Morning 2 (8:00 AM)
- `ID 1677969986112` - Close Blinds In The Evening (sunset)
- `ID 1677969986113` - Close Blinds In The Evening 2 (sunset +1hr)
- `ID 1680528200298` - No Direct Sun Light In The Morning
- `ID 1680528200296` - No Direct Sun Light In The Afternoon
- `ID 1678300398735` - Bright Outside
- `ID 1678300398734` - Really Bright Outside
- `ID 1678637987423` - Outside Went Darker
- `ID 1678741966793` - Computer Turned Off

---

### 📺 Entertainment System Integration

**TV Power Monitoring:**
- **TV Turned On:** Detects when TV power >10W
  - Logs event
  - If PlayStation already on: Auto-select game input on AV receiver
- **TV Turned Off:** Detects when TV off for 30+ seconds
  - Logs event
  - Turns off TV backlight (WLED) if it's on
  - Prevents wasted power on ambient lighting

**PlayStation Integration:**
- Power detection (>15W threshold)
- Triggers automatic input switching on AV receiver
- Seamless gaming experience

**Harmony Hub Management:**
- **Weekly Restart:** Every Monday at 3:00 AM (if TV off)
  - Powers off Harmony hub plug
  - Waits 1 minute
  - Powers back on
  - Prevents hub from becoming unresponsive
- Controls Onkyo AV Receiver and Samsung TV

**AV Receiver Control:**
- Script: living_room_select_game_input (BD/DVD input)
- Script: living_room_select_vcr_dvr_input (HDMI2 input)
- Handles timing delays for device sync
- Accounts for HDMI-CEC quirks

**Related Automations:**
- `ID 1610388192224` - TV Turned On
- `ID 1610388192225` - TV Turned Off
- `ID 1610918759041` - Restart Harmony Hub

---

### 💻 Computer & Work Integration

**Laptop Tracking:**
- Monitors Terina's work laptop status
- Family PC (Doug) tracking
- Presence-based automation triggers

**Work Laptop Events:**
- **Turned On:** Logs event, runs status check script
- **Turned Off:** Logs event, runs status check script

**Computer Off After 5 Minutes:**
- Opens blinds when ALL computers off (daytime only)
- Conditions:
  - Both family_computer and terinas_work_computer groups = not_home
  - After sunrise, before sunset
  - After 8:00:30 AM
  - Blind automation enabled
  - At least one blind is currently closed (<50% tilt)
- Purpose: Maximize natural light when screens not in use

**Uptime Tracking:**
- Family PC uptime statistics (today, yesterday, last 24h, this week, last 30 days)
- Uses device_tracker.doug as source
- History stats platform for time-based analytics

**Related Automations:**
- `ID 1654005357582` - Terina's Work Laptop Turned Off
- `ID 1654005357583` - Terina's Work Laptop Turned On
- `ID 1678741966793` - Computer Turned Off

---

### 🌅 Morning Routine Integration

**Triggers:**
- Motion detected in lounge OR on stairs
- Between 5:00 AM and 11:00 PM

**Conditions:**
- Morning routine enabled (input_boolean.enable_morning_routine)
- Someone home (group.tracked_people)
- House alarm in "armed_home" state (night mode)

**Actions:**
- Executes script.morning_script
- Coordinates with whole-house morning routine
- Disarms alarm, adjusts climate, opens blinds, etc.

**Purpose:** First-motion-of-the-day automation triggers household wake-up sequence

**Related Automations:**
- `ID 1588859622571` - Motion Detected In The Morning

---

### 🔌 Device Management

**Server Fan Control:**
- Monitors runtime of switch.server_fan
- **Alert after 1 hour:** Suggests turning off fan
  - Sends log message
  - If direct notifications enabled: Actionable notification
  - Options: "Yes" (turn off) or "No" (ignore)
- Purpose: Prevent unnecessary fan runtime, save energy

**Ceiling Light Manual Control:**
- Physical switch toggle detection
- **Switch Flipped:** Toggles ceiling light state
  - If lights off → Turn on (scene.living_room_ceiling_lights_on)
  - If lights on → Turn off (scene.living_room_ceiling_lights_off)
- Allows manual override of automation

**Deprecated Automation:**
- `ID 1714512650107` - Lamps On And No Motion (10 min)
  - Backup automation for restart scenarios
  - Turns off lights if on for 10+ min with no motion

**Related Automations:**
- `ID 1611063957341` - Server Fan Running Longer Than 1 Hour
- `ID 1754839043037` - Ceiling Light Switch Flipped
- `ID 1714512650107` - Lamps On And No Motion (DEPRECATED)

---

## Room Layout & Device Placement

```
                    NORTH (Bay Window Area)
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║  🪟 Bay Windows (3 sections)                         ║
    ║  ┌─────────┬──────────┬──────────┐                   ║
    ║  │ Left    │  Middle  │  Right   │                   ║
    ║  │ Blind   │  Blind   │  Blind   │                   ║
    ║  │ 🎚️      │  🎚️      │  🎚️      │                   ║
    ║  │ (Tilt   │ (Tilt    │ (Tilt    │                   ║
    ║  │  0-50)  │  0-50)   │  0-50)   │                   ║
    ║  └─────────┴──────────┴──────────┘                   ║
    ║                                                       ║
    ║  🌡️ Temperature & Humidity Sensors                   ║
    ║  💡 Illuminance Sensors (LTR390 + Motion)            ║
    ║  📏 Motion Detectors (Area + Lounge + Occupancy)     ║
    ║  👤 Presence Sensor (Apollo LD2412)                  ║
    ║                                                       ║
    ║  Ceiling Lighting System                             ║
    ║  💡 Left Side: living_room_left (+ _2, _3)           ║
    ║  💡 Right Side: living_room_right (+ _2, _3)         ║
    ║  💡 Group: lounge_ceiling                            ║
    ║  🔲 Manual Switch: ceiling_lights_input_0            ║
    ║                                                       ║
    ║                    Seating Area                       ║
    ║  ┌──────────────────────────────────────┐            ║
    ║  │  🛋️ Sofa                              │            ║
    ║  │                                       │            ║
    ║  │  💡 Lamp Left      💡 Lamp Right     │            ║
    ║  │  (Floor Lamp)     (Floor Lamp)       │            ║
    ║  └──────────────────────────────────────┘            ║
    ║                                                       ║
    ║                Entertainment Center                   ║
    ║  ┌───────────────────────────────────────────┐       ║
    ║  │  📺 Samsung TV (power monitored)          │       ║
    ║  │  💡 WLED Backlight (ambient lighting)     │       ║
    ║  ├───────────────────────────────────────────┤       ║
    ║  │  🎮 PlayStation (power monitored)         │       ║
    ║  │  🔊 Onkyo AV Receiver (Harmony control)   │       ║
    ║  │  📡 Harmony Hub (universal remote)        │       ║
    ║  │  🔌 Harmony Hub Plug (weekly restart)     │       ║
    ║  └───────────────────────────────────────────┘       ║
    ║                                                       ║
    ║  Server/Equipment Area                                ║
    ║  💨 Server Fan (runtime monitored)                    ║
    ║  💻 Family PC (Doug - device tracker)                 ║
    ║  💻 Terina's Work Laptop (device tracker)             ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
                 SOUTH (Interior Wall/Doorway)
```

---

## Key Automation Workflows

### Morning Routine (7:30-8:00 AM)

```
7:30 AM - Partial Blind Opening
   ↓
Check Enable Flag (input_boolean.enable_living_room_blind_automations)
   ├─ Disabled → Skip
   └─ Enabled → Continue
       ↓
    Check Windows (binary_sensor.living_room_windows)
    ├─ Open → Skip (safety)
    └─ Closed → Open blinds to 25% tilt
        ↓
     8:00 AM - Full Blind Opening
        ↓
     Check same conditions
        ↓
     Open blinds to 50% tilt (full open)
```

**Decision Tree:**
1. Is automation enabled?
2. Are windows closed? (safety check)
3. Execute timed opening sequence
4. Log with clock emoji timestamp

---

### Motion Detection During Day/Evening

```
Motion Sensor: TRIGGERED
   ↓
Check Enable Switch (input_boolean.enable_living_room_motion_triggers)
   ├─ Disabled → Skip all actions
   └─ Enabled → Continue
       ↓
    Check Illuminance Levels
    ├─ LTR390 sensor < threshold OR
    ├─ Motion illuminance < threshold OR
    └─ Motion sensor unavailable
         ↓
      Evaluate Lamp Brightness
      ├─ Lamp brightness < 190 OR lamps off
      │  ├─ Ceiling light already on?
      │  │  └─ Yes → Turn on full scene (lamps + ceiling)
      │  └─ No → Turn on lamps only
      │
      └─ Lamps off but room bright enough
         └─ Flash yellow signal (visual acknowledgment)
              ↓
           Cancel All Timers
           (timer.living_room_lamps_dim + timer.living_room_lamps_off)
```

---

### Motion Stops (Progressive Shutdown)

```
Motion Sensor: CLEARED
   ↓
Start 2-Minute Dim Timer
   ├─ If motion detected during timer: Cancel
   └─ If timer completes → Dim Phase
       ↓
    Evaluate Current Light State
    ├─ Both lamps + ceiling on → scene.living_room_dim_lights
    ├─ Lamps only on → scene.living_room_dim_lamps
    └─ Ceiling only on → scene.living_room_dim_ceiling_lights
         ↓
      Lights Dimmed
         ↓
      Start 5-Minute Off Timer
         ├─ If motion detected: Cancel
         └─ If timer completes → Off Phase
             ↓
          Turn Off Lights (same scene logic)
          ├─ Both on → scene.living_room_lights_off
          ├─ Lamps → scene.living_room_lamps_off
          └─ Ceiling → scene.living_room_ceiling_lights_off
```

**Total Timeline:** 7 minutes of no motion before lights fully off

---

### Bright Day - Blind Adjustment

```
Check Outdoor Brightness (sensor.front_garden_motion_illuminance)
   ↓
Medium Bright (above low threshold, below high threshold)
   ├─ After sunrise + after 8:00:30 AM + before sunset
   ├─ Windows closed
   ├─ Sun in specific position window
   │  ├─ Azimuth > morning threshold
   │  ├─ Azimuth < afternoon threshold
   │  └─ Elevation < afternoon threshold
   ├─ Current blind position not already at 25%
   └─ Computer(s) are on (family OR work laptop on weekdays)
       ↓
    Close middle & right blinds to 25% (prevent glare)
       ↓
Really Bright (above high threshold)
   ├─ Same conditions as above
   └─ Current blind position > 0%
       ↓
    Close middle & right blinds to 0% (full closure)
       ↓
Outside Went Darker (below low threshold for 5 min)
   ├─ ALL computers are OFF
   ├─ During daylight hours
   └─ At least one blind currently < 50%
       ↓
    Open all blinds to 50% (maximize light)
```

---

### Sun Position Tracking

```
Morning Sun Tracking:
├─ Monitor sun azimuth
├─ When azimuth drops below morning threshold
│  ├─ Sun moved away from window angle
│  └─ Open blinds to 50%
│
Afternoon Sun Tracking:
├─ Monitor sun azimuth AND elevation
├─ When both exceed afternoon thresholds
│  ├─ Sun moved to different position
│  └─ Open blinds to 50%
│
Purpose: Avoid direct sunlight glare while maximizing natural light
```

---

### Evening Routine (Sunset)

```
Sunset OR 20:00 (whichever first)
   ↓
Check Conditions
   ├─ Enable flag on
   ├─ Windows closed
   └─ At least one blind currently > 25%
       ↓
    Partial Close to 25%
       ↓
    Wait 1 Hour
       ↓
Sunset +1hr OR 21:00
   ↓
Same condition checks
   ↓
Full Close to 0% (privacy mode)
```

---

### TV Watching Session

```
TV Powered On (>10W)
   ↓
Log: TV turned on
   ↓
Check PlayStation Status
   ├─ PlayStation on (>15W)?
   │  └─ Yes → Auto-select game input
   │      ├─ Wait 13 seconds
   │      ├─ Send InputBd/Dvd command to Onkyo
   │      └─ Log: Changed to game input
   └─ No → Do nothing
       ↓
    [Watching/Gaming Session]
       ↓
TV Powered Off (30 sec delay)
   ↓
Log: TV turned off
   ↓
Check TV Backlight Status
   ├─ Backlight on?
   │  └─ Yes → Turn off backlight
   │      └─ Log: Turning off backlight
   └─ No → Do nothing
```

---

### Computer Work Session End

```
Computer(s) Turned Off (5 min delay)
   ↓
Check Conditions
   ├─ Both family_computer AND terinas_work_computer = not_home
   ├─ Blind automation enabled
   ├─ After sunrise, before sunset, after 8:00:30
   └─ At least one blind currently < 50%
       ↓
    Open All Blinds to 50%
       ↓
    Log: All computers off, opening blinds
```

**Purpose:** Maximize natural light when no one needs glare protection

---

### Weekly Harmony Hub Restart

```
Every Monday at 3:00 AM
   ↓
Check Conditions
   ├─ Is it Monday?
   └─ Is TV off?
       ↓
    Turn Off Harmony Hub Plug
       ↓
    Wait 1 Minute
       ↓
    Turn On Harmony Hub Plug
       ↓
    Log: Restarted Harmony Hub
```

**Purpose:** Prevent hub from becoming unresponsive over time

---

## Configuration Parameters

### Light Level Thresholds
- `input_number.living_room_light_level_2_threshold` - Primary LTR390 sensor threshold (lux)
- `input_number.living_room_light_level_4_threshold` - Secondary motion sensor threshold (lux)

### Blind Brightness Thresholds
- `input_number.blind_low_brightness_threshold` - Threshold for "Bright Outside" (partial close)
- `input_number.blind_high_brightness_threshold` - Threshold for "Really Bright Outside" (full close)

### Sun Position Thresholds
- `input_number.living_room_blinds_morning_sun_azimuth_threshold` - Morning sun avoidance angle
- `input_number.living_room_blinds_afternoon_sun_azimuth_threshold` - Afternoon sun avoidance angle
- `input_number.living_room_blinds_afternoon_sun_elevation_threshold` - Sun elevation angle threshold

### Time Schedules
- Morning blind opening: 7:30 AM (partial), 8:00 AM (full)
- Evening blind closing: Sunset or 20:00 (partial), Sunset+1hr or 21:00 (full)
- Motion lighting: 2-min dim delay, 5-min off delay (7 min total)
- Harmony hub restart: Monday 3:00 AM
- Computer off blind opening: 5 minutes after all computers off
- Server fan alert: 1 hour runtime
- TV off backlight: 30 second delay

---

## Helper Entities

### Input Booleans
- `input_boolean.enable_living_room_motion_triggers` - Master enable for motion-activated lighting
- `input_boolean.enable_living_room_blind_automations` - Master enable for blind automations
- `input_boolean.enable_morning_routine` - Enable morning wake-up automation
- `input_boolean.enable_direct_notifications` - Enable actionable notifications (server fan)

### Timers
- `timer.living_room_lamps_dim` - 2-minute dim timer (after motion stops)
- `timer.living_room_lamps_off` - 5-minute off timer (after dim phase)

### Groups
- `group.tracked_people` - All tracked people in household
- `group.family_computer` - Family PC device tracker group
- `group.terinas_work_computer` - Work laptop device tracker group

### Input Numbers
- `input_number.living_room_light_level_2_threshold` - LTR390 light threshold
- `input_number.living_room_light_level_4_threshold` - Motion sensor light threshold
- `input_number.blind_low_brightness_threshold` - Medium brightness level
- `input_number.blind_high_brightness_threshold` - High brightness level
- `input_number.living_room_blinds_morning_sun_azimuth_threshold` - Morning sun angle
- `input_number.living_room_blinds_afternoon_sun_azimuth_threshold` - Afternoon sun angle
- `input_number.living_room_blinds_afternoon_sun_elevation_threshold` - Sun elevation angle

---

## Scripts

### Entertainment Control Scripts
- `script.living_room_select_game_input` - Switch AV receiver to game input (BD/DVD)
- `script.living_room_select_vcr_dvr_input` - Switch to VCR/DVR input with TV HDMI2
- `script.living_room_flash_lounge_lights_green` - Flash lamps green (notification)
- `script.lounge_flash_lounge_lights_red` - Flash lamps red (alert)

### System Scripts
- `script.check_terinas_work_laptop_status` - Check and respond to laptop status changes
- `script.morning_script` - Coordinated morning routine (house-wide)
- `script.turn_everything_off` - Emergency shutdown (via NFC)
- `script.nfc_bedroom_right` - NFC tag handler for shutdown

### Utility Scripts
- `script.send_to_home_log` - Centralized logging system
- `script.send_actionable_notification_with_2_buttons` - Two-option notifications
- `script.get_clock_emoji` - Generate time emoji for log messages

---

## Sensors

### TV & Entertainment Usage Tracking
- `sensor.tv_running_time_today` - Today's TV runtime
- `sensor.tv_running_time_last_24_hours` - Last 24 hours TV runtime
- `sensor.tv_running_time_yesterday` - Yesterday's TV runtime
- `sensor.tv_running_time_this_week` - This week's TV runtime
- `sensor.tv_running_time_last_30_days` - Last 30 days TV runtime

### Computer Uptime Tracking
- `sensor.family_pc_uptime_today` - Today's PC uptime
- `sensor.family_pc_uptime_last_24_hours` - Last 24 hours PC uptime
- `sensor.pc_uptime_yesterday` - Yesterday's PC uptime
- `sensor.family_pc_uptime_this_week` - This week's PC uptime
- `sensor.family_pc_uptime_last_30_days` - Last 30 days PC uptime

### Environment Monitoring
- `sensor.living_room_mould_indicator` - Mold risk calculation (temp + humidity + outdoor temp)
  - Uses calibration factor: 1.5
  - Indoor temp: sensor.living_room_motion_temperature
  - Indoor humidity: sensor.living_room_motion_humidity
  - Outdoor temp: sensor.gw2000a_outdoor_temperature

### Template Binary Sensors
- `binary_sensor.playstation_powered_on` - PlayStation power state (>15W threshold)
  - Device class: running
  - Dynamic icon: mdi:controller / mdi:controller-off
- `binary_sensor.tv_powered_on` - TV power state (>10W threshold)
  - Device class: running
  - Dynamic icon: mdi:television-classic / mdi:television-classic-off

---

## Status Indicators

### Light Scenes for Status

**Main Scenes:**
- `scene.living_room_lights_on` - All lights on (lamps + ceiling at 240 brightness, 310 mireds)
- `scene.living_room_lamps_on` - Lamps only (240 brightness, 310 mireds)
- `scene.living_room_ceiling_lights_on` - Ceiling lights only (241 brightness, 366 mireds)

**Dim Scenes:**
- `scene.living_room_dim_lights` - All lights dimmed
- `scene.living_room_dim_lamps` - Lamps dimmed
- `scene.living_room_dim_ceiling_lights` - Ceiling dimmed

**Off Scenes:**
- `scene.living_room_lights_off` - All lights off
- `scene.living_room_lamps_off` - Lamps off
- `scene.living_room_ceiling_lights_off` - Ceiling lights off

**Notification Scenes:**
- `scene.living_room_lamps_yellow` - Yellow flash (motion acknowledgment when bright)
- `scene.living_room_lights_green` - Green flash (success/positive notification)
- `scene.lounge_lights_red` - Red flash (alert/warning)

**Color Specifications:**
- Yellow: RGB (255, 245, 2), XY (0.455, 0.507), 100% brightness
- Green: RGB (1, 255, 0), XY (0.173, 0.747), 100% brightness
- Warm White: 2732K color temp (366 mireds)
- Lamp Default: 310 mireds color temp

---

## Key Features

✅ **Adaptive Motion Lighting** - Dual illuminance sensors with brightness-aware activation
✅ **Progressive Dimming** - 7-minute gradual shutdown (2 min dim → 5 min off)
✅ **Intelligent Blind Control** - Sun tracking + brightness + computer-aware adjustments
✅ **Entertainment Integration** - TV/PlayStation power monitoring, auto-input switching
✅ **Computer-Aware Automation** - Glare protection when working, opens blinds when done
✅ **Harmony Hub Management** - Weekly restart prevents connectivity issues
✅ **Multi-Sensor Redundancy** - Dual motion sensors, dual illuminance sensors
✅ **Visual Acknowledgment** - Yellow flash when motion detected but room bright enough
✅ **Window Safety** - Blocks all blind movements when windows open
✅ **Manual Override** - Physical switch control with automation integration
✅ **Usage Analytics** - TV runtime, PC uptime, environmental monitoring
✅ **Morning Routine Integration** - First motion triggers house-wide wake sequence
✅ **Presence Detection** - Multiple motion/occupancy sensors for reliable detection
✅ **Scene-Based Control** - Conditional scene selection based on current state
✅ **Mold Prevention** - Environmental monitoring with calibrated thresholds
✅ **Energy Monitoring** - Power consumption tracking for all entertainment devices

---

## File Structure

```
packages/rooms/
├── living_room.yaml          # Main automation configuration (3307 lines)
├── LIVING-ROOM-SETUP.md      # This file - Room documentation
└── [future sub-files if consolidation needed]
```

---

## Automation Summary by Category

### Motion & Lighting (5 automations)
- Motion Detected (ID 1583956425622)
- No Motion (ID 1606170045632)
- No Motion After Short Time Dim Lights (ID 1606170045630)
- No Motion For Long Time (ID 1605567425876)
- Lamps On And No Motion - DEPRECATED (ID 1714512650107)

### Blind Control (9 automations)
- Open Blinds In The Morning (ID 1677711735249) - 7:30 AM
- Open Blinds In The Morning 2 (ID 1677711735250) - 8:00 AM
- Close Blinds In The Evening (ID 1677969986112) - Sunset
- Close Blinds In The Evening 2 (ID 1677969986113) - Sunset +1hr
- No Direct Sun Light In The Morning (ID 1680528200298)
- No Direct Sun Light In The Afternoon (ID 1680528200296)
- Bright Outside (ID 1678300398735)
- Really Bright Outside (ID 1678300398734)
- Outside Went Darker (ID 1678637987423)

### Entertainment (3 automations)
- TV Turned On (ID 1610388192224)
- TV Turned Off (ID 1610388192225)
- Restart Harmony Hub (ID 1610918759041) - Weekly Monday 3 AM

### Computer Integration (3 automations)
- Terina's Work Laptop Turned Off (ID 1654005357582)
- Terina's Work Laptop Turned On (ID 1654005357583)
- Computer Turned Off (ID 1678741966793) - Opens blinds after 5 min

### Device Management (2 automations)
- Server Fan Running Longer Than 1 Hour (ID 1611063957341)
- Ceiling Light Switch Flipped (ID 1754839043037)

### Morning Routine (1 automation)
- Motion Detected In The Morning (ID 1588859622571)

**Total Automation Count:** 23 active automations (1 deprecated)

---

## Advanced Features Explained

### Dual Illuminance Sensor Logic
The system uses TWO illuminance sensors for redundancy and accuracy:
1. **LTR390 sensor** (sensor.apollo_r_pro_1_w_ef755c_ltr390_light) - Primary, high-quality sensor
2. **Motion sensor illuminance** (sensor.living_room_motion_illuminance) - Backup sensor

**Logic:** Lights activate if EITHER sensor reads below threshold OR if motion sensor is unavailable. This ensures lights work even if one sensor fails.

### Computer-Aware Blind Control
Blinds intelligently respond to computer usage:
- **Weekday 9-5:** Considers both family PC and work laptop
- **Evenings/Weekends:** Only considers family PC (work laptop ignored)
- **5-min delay:** Opens blinds 5 minutes after ALL computers turn off (prevents frequent open/close)
- **Brightness check:** Only closes blinds if actually bright outside + computers on

### Sun Position Mathematics
The system calculates sun position using:
- **Azimuth:** Compass direction (0-360°)
  - Morning threshold: Sun moving away from east-facing windows
  - Afternoon threshold: Sun moving away from west-facing windows
- **Elevation:** Angle above horizon (0-90°)
  - Afternoon threshold: Sun high enough to cause direct glare

**Window Logic:** Middle and right blinds close when sun in "danger zone", left blind unaffected (different window angle).

### Progressive Dimming Prevents Shock
Instead of abrupt off, the system uses a gentle 3-stage approach:
1. **Full brightness** (normal operation)
2. **2-min delay** → **Dim** (visual warning)
3. **5-min delay** → **Off** (final shutdown)

**Total:** 7 minutes from last motion to lights off. Re-detection at ANY stage cancels entire sequence.

### Scene-Based Conditional Control
The automation dynamically selects scenes based on what's currently on:
- If both lamps AND ceiling on → Use combined scene
- If only lamps on → Use lamp-only scene
- If only ceiling on → Use ceiling-only scene

This prevents turning off lights that user manually turned off earlier.

### TV Backlight Auto-Off
When TV powers off, system waits 30 seconds then checks if WLED backlight is still on. If yes, turns it off. This prevents accidentally leaving ambient lighting running all night.

### Harmony Hub Weekly Restart
Many users report Harmony hubs becoming unresponsive over time. Weekly restart (Monday 3 AM) prevents this issue. Only runs if TV is off to avoid interrupting viewing.

---

**Last Updated:** 2026-01-24
**Documentation Version:** 1.0
**Automation Count:** 23 (1 deprecated)
**Device Count:** 45+ entities
**Scene Count:** 13
**Script Count:** 11
**Sensor Count:** 16
**Configuration Files:** 1 main (3307 lines)
