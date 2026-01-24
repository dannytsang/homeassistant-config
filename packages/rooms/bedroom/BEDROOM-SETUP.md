# Bedroom Setup Documentation

**Created:** 2026-01-24
**Room:** Bedroom (Master Bedroom)
**Focus:** Sleep Tracking, Smart Wake, Climate Control, Adaptive Lighting, Awtrix Integration
**Special Features:** Sleep as Android Integration, Bed Occupancy Detection, Pixel Clock Notifications

---

## Device Inventory

| Category | Device | Type | Function |
|----------|--------|------|----------|
| **Sleep Tracking** | binary_sensor.bed_occupied | Template Binary Sensor | Bed occupancy detection from 4 pressure sensors |
| | sensor.bed_top_left | Pressure Sensor | Top left bed corner pressure (threshold: 0.15) |
| | sensor.bed_top_right | Pressure Sensor | Top right bed corner pressure (threshold: 0.15) |
| | sensor.bed_bottom_left | Pressure Sensor | Bottom left bed corner pressure (threshold: 0.15) |
| | sensor.bed_bottom_right | Pressure Sensor | Bottom right bed corner pressure (threshold: 0.1) |
| | input_text.sleep_as_android | Sleep Tracker State | Current sleep state from Sleep as Android app |
| | binary_sensor.danny_asleep | Template Binary Sensor | Derived sleep state indicator |
| | timer.sleep | Sleep Timer | Tracks remaining sleep time with pause/resume |
| **Lighting - Lamps** | light.bedroom_lamp_left, light.bedroom_lamp_right | Color Temperature Lamps | Desk lamps with color and brightness control |
| | light.bedroom_lamps | Group/Light | Both desk lamps as single entity |
| **Lighting - Ceiling** | light.bedroom_main_light, light.bedroom_main_light_2 | Ceiling Lights | Main bedroom ceiling lights |
| **Lighting - Ambient** | light.under_bed_left, light.under_bed_right | RGB LED Strips | Under-bed ambient lighting (Hue strips) |
| **Lighting - Clock** | light.bedroom_clock_matrix | Awtrix Pixel Clock | 8x32 RGB LED matrix display with notifications |
| **Motion** | binary_sensor.bedroom_area_motion | Motion Group | Aggregated motion detection for bedroom area |
| | binary_sensor.bedroom_motion_occupancy | Occupancy Sensor | Primary occupancy tracking |
| | binary_sensor.bedroom_motion_3_presence | Presence Sensor | Advanced presence detection |
| **Environment** | sensor.bedroom_door_temperature | Temperature Sensor | Room temperature monitoring |
| | sensor.bedroom_humidity_2 | Humidity Sensor | Room humidity monitoring |
| | sensor.bedroom_area_mean_temperature | Average Temperature | Mean temperature across bedroom sensors |
| | sensor.bedroom_mould_indicator | Mold Risk Sensor | Calculated mold risk (calibration: 1.38) |
| **Window Covers** | cover.bedroom_blinds | Motorized Blind | Main bedroom window blind |
| | binary_sensor.bedroom_window_contact | Window Contact Sensor | Detects if window is open |
| **Door Sensors** | binary_sensor.bedroom_door_contact | Contact Sensor | Master bedroom door state |
| | binary_sensor.leos_bedroom_door_contact | Contact Sensor | Leo's bedroom door (for notifications) |
| | binary_sensor.ashlees_bedroom_door_contact | Contact Sensor | Ashlee's bedroom door (for notifications) |
| **Entertainment** | binary_sensor.bedroom_tv_powered_on | Power Monitor | TV power state detection (>40W) |
| | sensor.bedroom_tv_plug_power | Smart Plug Power Monitor | TV power consumption tracking |
| | media_player.bedroom_tv | Chromecast/TV | Bedroom TV media player |
| **Climate Control** | switch.bedroom_fan | Smart Fan | Bedroom cooling fan with runtime limit |
| **Remote Control** | Device ID: 61ab87aac9c81fe8687771074e560f48 | MQTT Remote | 4-button + dial remote (Zigbee/MQTT) |
| | sensor.bedroom_dial_remote_action_time | Action Time Sensor | Dial rotation time for brightness control |
| **Awtrix Clock** | sensor.bedroom_clock_device_topic | MQTT Topic Sensor | Device topic for MQTT notifications |
| **Uptime Tracking** | sensor.bedroom_tv_uptime_today | History Stats | Today's TV runtime |
| | sensor.bedroom_tv_uptime_yesterday | History Stats | Yesterday's TV runtime |
| | sensor.bedroom_tv_uptime_this_week | History Stats | This week's TV runtime |
| | sensor.bedroom_tv_uptime_last_30_days | History Stats | Last 30 days TV runtime |
| **Presence Detection** | binary_sensor.upstairs_area_motion | Motion Group | Upstairs hallway motion detection |
| | light.stairs, light.stairs_ambient, light.stairs_2 | Stairway Lights | Stairway lighting (controlled by bedroom door) |

---

## Automation Functions

### 🛏️ Bed Occupancy & Sleep Management

**Triggers:** Bed occupancy sensor, sleep tracking state changes

**Logic:**
- **Someone Gets In Bed (After Sunset):**
  - Bed occupied for 30+ seconds
  - After sunset
  - Window is closed
  - Blinds are open (above threshold)
  - Bed sensor enabled
  - **Action:** Close bedroom blinds automatically
  - **Safety:** Only if window closed, prevents blind/window conflict

- **No One In Bed (After Sunrise):**
  - Bed empty for 30+ seconds
  - After sunrise (with -1 hour offset) and before sunset
  - Blinds are closed (below threshold)
  - Bed sensor enabled
  - **Action:** Wait 1 minute, then open blinds
  - **Purpose:** Natural wake-up light

**Safety Features:**
- Window contact sensor prevents blind movement if window open
- Bed sensor can be disabled via input_boolean.enable_bed_sensor
- Time-of-day constraints prevent inappropriate actions

**Related Automations:**
- `ID 1601641236163` - Close Blinds When Someone Is In Bed After Sunset
- `ID 1601641292576` - Open Blind When No One Is In Bed

---

### 😴 Sleep As Android Integration

**Sleep Tracking States:**
- `sleep_tracking_started` - Tracking begins
- `sleep_tracking_stopped` - Tracking ends
- `awake` - User detected awake
- `alarm_alert_start` - Alarm triggered
- And 20+ other states (snooze, smart wake, REM, deep sleep, etc.)

**Logic:**

- **Sleep Tracking Started:**
  - Receives webhook from Sleep as Android app
  - If Danny is home:
    - Starts sleep timer (configurable duration via input_number.sleep_timer_duration)
    - Default: 60 minutes
    - Logs to home log
  - If bedroom is warm (>22.5°C):
    - Turns on bedroom fan automatically
    - Prevents overheating during sleep

- **Awake Detection (Pause Timer):**
  - When state changes to 'awake'
  - If timer is active:
    - Pauses sleep timer
    - Preserves remaining time
    - Logs pause event

- **Fall Back Asleep (Resume Timer):**
  - When state changes FROM 'awake'
  - If timer is paused:
    - Resumes timer
    - Adds configurable time (input_number.sleep_as_android_time_to_add, default: minutes)
    - Caps at original duration
    - Logs resume with new time

- **Asleep For 15 Minutes (Reward):**
  - If Danny asleep for 15+ minutes continuously
  - Timer is active
  - **Action:** Subtract time from timer (input_number.sleep_as_android_time_to_subtract)
  - **Purpose:** Reward sustained sleep by reducing remaining timer
  - **Safety:** Doesn't allow negative time

- **Sleep Timer Finished:**
  - Timer reaches zero
  - **Actions:**
    - Executes script.bedroom_sleep (turns off clock)
    - Turns off bedroom fan if it's on
    - Logs completion

- **Alarm Triggered:**
  - State: 'alarm_alert_start'
  - If Danny home and blinds closed:
    - Wait 5 minutes
    - Open bedroom blinds for natural wake-up
  - Turn on clock if it's off
  - Logs alarm event

- **Daily Reset (5:00 AM):**
  - Cancels sleep timer if still active/paused
  - Prevents timer running into next day

**Notification Levels:**
- `input_select.sleep_as_android_notification_level`:
  - "Start/Stop" - Only log tracking start/stop
  - "Start/Stop/Alarms" - Add alarm events
  - "All" - Log every state change

**Related Automations:**
- `ID 1614285576722` - Sleep As Android: Event (webhook receiver)
- `ID 1658438667856` - Started Tracking
- `ID 1658843567854` - Awake
- `ID 1658843828191` - Fall Asleep
- `ID 1659861914053` - Danny Asleep For A Period Of Time
- `ID 1658842750488` - Timer: Sleep Timer Complete
- `ID 1644769166837` - Danny's Alarm
- `ID 1667424349110` - Stop Sleep Timer (5 AM reset)

---

### 🚪 Door Sensors & Child Monitoring

**Bedroom Door Closed:**
- **Trigger:** Bedroom door closed for 10+ seconds
- **Conditions:** All children's doors closed + no upstairs motion
- **Actions:**
  - Turn off stairs lighting (all 3 lights with 1s transition)
  - Logs door closure
- **Purpose:** Energy saving when upstairs unoccupied

**Children's Door Opens Warning:**
- **Trigger:** Leo's or Ashlee's door opens after children's bedtime
- **Conditions:**
  - After input_datetime.childrens_bed_time
  - Bedroom lights are on (lamps or ceiling)
  - NOT in "Guest" or "No Children" home mode
- **Actions (if bed occupied OR after sunset):**
  - Visual notification via bedroom lamps
  - Leo's door: Flash blue twice, restore lamp state
  - Ashlee's door: Flash pink twice, restore lamp state
  - Pauses bedroom TV if playing (except BBC iPlayer)
  - Logs event to home log
- **Purpose:** Alert parents to children out of bed at night

**Children's Door Closes Warning:**
- **Trigger:** Leo's or Ashlee's door closes after children's bedtime
- **Conditions:** Bedroom lamps on + after bedtime + not guest mode
- **Actions:**
  - Visual notification via bedroom lamps
  - Leo: Flash blue → green → off, restore state
  - Ashlee: Flash pink → green → off, restore state
  - Resumes TV if it was paused
  - Logs event
- **Purpose:** Confirm child back in bed

**Door Opens At Night (TV Pause):**
- **Trigger:** Bedroom door opens
- **Conditions:**
  - Between 22:00 and 02:00
  - TV is playing
  - NOT watching BBC iPlayer (live TV exception)
- **Actions:**
  - Pause bedroom TV
  - Logs event
- **Purpose:** Privacy when someone enters room

**Related Automations:**
- `ID 1715955339483` - Bedroom: Door Closed
- `ID 1615209552353` - Other Bedroom Door Opens Warning
- `ID 1615209552354` - Other Bedroom Door Closes Warning
- `ID 1724001157269` - Pause TV When Door Opens At Night

---

### 🔆 Motion-Based Lighting

**Motion Detected:**
- **Triggers:** Motion detected from bedroom_motion_occupancy
- **Conditions:**
  - Motion trigger enabled (input_boolean.enable_bedroom_motion_trigger)
  - Under-bed lights are off OR dim (brightness < 100)
- **Logic (context-aware):**

  **Blinds Down (Dark Room):**
  - Blind position < 31%
  - **Action:** Dim ambient lights (scene.bedroom_dim_ambient_light)
  - **Purpose:** Night-time navigation without being too bright

  **After Sunrise (Daytime):**
  - After 8:00 AM and before sunset
  - **Action:** Turn on ambient lights (scene.bedroom_turn_on_ambient_light)
  - **Purpose:** Normal daytime lighting

  **After Sunset or Before 8 AM (Night):**
  - After sunset OR before 8:00 AM
  - **Action:** Dim ambient lights (scene.bedroom_dim_ambient_light)
  - **Purpose:** Low-light navigation at night

  **Always:** Turn on clock matrix if it's off

**No Motion (2 Minutes):**
- **Trigger:** No motion for 2 minutes
- **Conditions:**
  - Either under-bed light is on
  - Motion trigger enabled
- **Actions:**
  - Turn off ambient lights (scene.bedroom_turn_off_ambient_light)
  - Logs event

**No Motion For Long Time (30 Minutes):**
- **Trigger:** No bedroom area motion for 30 minutes
- **Conditions:**
  - Bedroom lamps are OFF
  - Motion trigger enabled
- **Actions:**
  - Turn off bedroom clock matrix
  - Logs event
- **Purpose:** Deep energy saving when room truly vacant

**No Motion And Fan Is On (5 Minutes):**
- **Trigger:** No presence detection for 5 minutes
- **Conditions:** Bedroom fan is on
- **Actions:** Turn off bedroom fan
- **Purpose:** Prevent fan running in empty room

**Related Automations:**
- `ID 1621713217274` - Motion Detected
- `ID 1621713867762` - No Motion
- `ID 1621713867763` - No Motion For Long Time
- `ID 1725207477313` - No Motion And Fan Is On

---

### 💨 Climate Control - Fan Management

**Turn Off Fan After 2 Hours:**
- **Trigger:** Fan has been on for 2 hours
- **Actions:**
  - Turn off bedroom fan
  - Logs event with reason
- **Purpose:** Prevent excessive runtime, save energy

**Fan On When Sleep Tracking Starts:**
- **Trigger:** Sleep tracking started
- **Conditions:**
  - Danny is home
  - Bedroom mean temperature > 22.5°C
  - Fan is currently off
- **Actions:**
  - Turn on bedroom fan
  - Logs temperature and action
- **Purpose:** Comfort during sleep in warm conditions

**Fan Off When Sleep Timer Completes:**
- **Trigger:** Sleep timer finishes
- **Conditions:** Fan is on
- **Actions:**
  - Turn off fan
  - Logs event
- **Purpose:** Don't run fan all night after sleep achieved

**Fan Off When No Presence (5 Minutes):**
- **Trigger:** No presence for 5 minutes
- **Conditions:** Fan is on
- **Actions:** Turn off fan
- **Purpose:** Energy saving in vacant room

**Related Automations:**
- `ID 1690844451011` - Turn Off Fan (2 hour limit)
- `ID 1725207477313` - No Motion And Fan Is On
- Part of sleep tracking automations

---

### 🪟 Window & Blind Management

**Window Closed At Night:**
- **Trigger:** Window closes
- **Conditions:**
  - After sunset and before sunrise
  - Blind automation enabled
  - Blinds NOT already closed
- **Actions:**
  - Close bedroom blinds
  - Logs event
- **Purpose:** Privacy and thermal insulation at night

**Window Closed And Someone In Bed At Night:**
- **Trigger:** Window closes for 30+ seconds
- **Conditions:**
  - After sunset
  - Blinds are open (above threshold)
  - Blind automation enabled
- **Logic (conditional):**
  - **If bed sensor enabled AND bed occupied:**
    - Close blinds (someone in bed, window now closed)
  - **If bed sensor disabled:**
    - Close blinds (it's after sunset, window closed)
- **Purpose:** Automatic privacy when conditions met

**Morning Timed Open Blinds:**
- **Triggers:** 8:00 AM, 9:00 AM, or 10:00 AM
- **Conditions:**
  - Blinds closed (below threshold)
  - Blind automation enabled
  - TV is off (not watching in dark)
- **Logic (calendar-aware):**

  **8:00 AM (Workday):**
  - Binary workday sensor = ON
  - No annual leave in calendar
  - OR children have scheduled activities (excluding holidays)
  - **Action:** Open blinds

  **9:00 AM (Weekend with Activities):**
  - NOT a workday
  - NOT in "No Children" mode
  - Children have scheduled activities (excluding holidays)
  - **Action:** Open blinds

  **10:00 AM (Fallback):**
  - Any day, any conditions
  - **Action:** Open blinds
  - **Purpose:** Ensure blinds open by 10 AM latest

- **Calendar Integration:**
  - Checks calendar.work for annual leave
  - Checks calendar.tsang_children for activities
  - Filters out "half term" and "holidays" keywords
  - Uses 2-hour lookahead window

**Evening Timed Close Blinds:**
- **Trigger:** 22:00 (10 PM)
- **Conditions:**
  - Blind automation enabled
  - Blinds are open (above threshold)
- **Actions:**
  - If window is open: Log warning, skip closure
  - If window closed: Close blinds
  - Logs with clock emoji timestamp
- **Purpose:** Privacy before bedtime

**Related Automations:**
- `ID 1622667464880` - Window Closed At Night
- `ID 1615689096351` - Window Closed And Someone Is In Bed At Night
- `ID 1621875409014` - Morning Timed Open Blinds
- `ID 1621875567853` - Evening Timed Close Blinds

---

### 📺 TV & Entertainment Integration

**TV Turned On During Bright Day:**
- **Trigger:** TV powers on (>40W)
- **Conditions:**
  - After sunrise, before sunset
  - Blind automation enabled
  - Blinds are open (above threshold)
- **Logic:**
  - **If window is OPEN:**
    - Send actionable notification to Danny (if direct notifications enabled)
    - "Do you want to close the blinds?"
    - Options: Yes (set to 30%) or No (ignore)
  - **If window is CLOSED:**
    - Automatically set blinds to 20% position
    - Logs event
- **Purpose:** Reduce glare on TV screen during daytime viewing

**TV Turned Off:**
- **Trigger:** TV off for 1+ minute
- **Conditions:**
  - Blinds are closed (below threshold)
  - Blind automation enabled
  - After sunrise, before sunset, after 8:30 AM
- **Logic (weather-aware):**
  - Get hourly weather forecast
  - **If current temp OR next hour temp > high threshold:**
    - Keep blinds closed (too hot outside)
    - Logs temperature and decision
  - **If temperature acceptable:**
    - Open blinds (restore natural light)
    - Logs event
- **Purpose:** Restore natural light when TV off, unless too hot

**Related Automations:**
- `ID 1624194131454` - TV Turned On During Bright Day
- `ID 1624194439043` - TV Turned Off

---

### 🎛️ Remote Control Integration

**4-Button + Dial Remote (Zigbee MQTT)**

**Button 1 (Main Light Toggle):**
- **Trigger:** Button 1 press/release
- **Actions:**
  - If main lights on: Turn off both ceiling lights
  - If main lights off: Turn on both ceiling lights
- **Purpose:** Quick toggle of main bedroom lighting

**Button 2 (Desk Lamps Toggle):**
- **Trigger:** Button 2 press/release
- **Actions:**
  - If lamps off: Turn on desk lamps (scene.bedroom_desk_lamps_on with 1s transition)
  - If lamps on: Turn off lamps AND under-bed lights
- **Purpose:** Toggle work/reading lighting

**Button 3 (Open Blinds):**
- **Trigger:** Button 3 press/release
- **Actions:** Open bedroom blinds
- **Purpose:** Quick manual blind control

**Button 4 (Close Blinds):**
- **Trigger:** Button 4 press/release
- **Actions:** Close bedroom blinds
- **Purpose:** Quick manual blind control

**Dial Rotate Right (Brighten Lamps):**
- **Triggers:**
  - dial_rotate_right_slow
  - dial_rotate_right_step
  - brightness_step_up
- **Conditions:** Action time sensor value > 0
- **Actions:**
  - Increase lamp brightness by (action_time * 2)
  - Max: 255
  - 1 second transition
  - Queued mode (max 10)
- **Purpose:** Smooth brightness increase via dial

**Dial Rotate Left (Dim Lamps):**
- **Triggers:**
  - dial_rotate_left_slow
  - dial_rotate_left_step
  - brightness_step_down
- **Conditions:** Action time sensor value > 0
- **Actions:**
  - Decrease lamp brightness by (action_time * 2)
  - Min: 0
  - 1 second transition
  - Queued mode (max 10)
- **Purpose:** Smooth brightness decrease via dial

**Related Automations:**
- `ID 1699308571385` - Remote Button 1
- `ID 1699308571386` - Remote Button 2
- `ID 1699308571387` - Remote Button 3
- `ID 1699308571388` - Remote Button 4
- `ID 1710079376648` - Remote Dial Action Right
- `ID 1710079376649` - Remote Dial Action Left

---

### 🕐 Awtrix Pixel Clock Integration

**MQTT Notification System:**
- Device: 8x32 RGB LED matrix clock
- Protocol: MQTT
- Topic: sensor.bedroom_clock_device_topic/notify

**Script: send_bedroom_clock_notification**
- **Parameters:**
  - `message` (required) - Text to display (multiline supported)
  - `icon` (optional) - Icon number (1-100)
  - `duration` (optional) - Display time in seconds (1-120, default: 10)
- **Logic:**
  - If icon provided: Send message + icon + duration
  - If no icon: Send message + duration only
  - Uses MQTT publish to device topic
- **Payload Format:** JSON with text, icon, duration fields

**Clock Auto-Control:**
- **Motion Detected:** Turn on clock if it's off
- **No Motion 30 Min:** Turn off clock if lamps are off
- **Sleep Timer Complete:** Turn off clock
- **Alarm Triggered:** Turn on clock if it's off

**Use Cases:**
- Child door notifications (via scripts)
- System status messages
- Sleep tracking events
- Custom alerts

**Related Script:**
- `script.send_bedroom_clock_notification`

---

## Room Layout & Device Placement

```
                    NORTH (Window Wall)
    ╔════════════════════════════════════════════════════════╗
    ║                                                        ║
    ║  🪟 Bedroom Window                                     ║
    ║  ├─ 🚪 Contact Sensor (binary_sensor.bedroom_window)  ║
    ║  └─ 🎚️ Motorized Blind (cover.bedroom_blinds)        ║
    ║                                                        ║
    ║                  Environmental Sensors                 ║
    ║  🌡️ Temperature: sensor.bedroom_door_temperature      ║
    ║  💧 Humidity: sensor.bedroom_humidity_2               ║
    ║  🦠 Mold Indicator: sensor.bedroom_mould_indicator    ║
    ║                                                        ║
    ║                   Motion Detection                     ║
    ║  📏 Occupancy: bedroom_motion_occupancy               ║
    ║  👤 Presence: bedroom_motion_3_presence               ║
    ║  📍 Area Motion: bedroom_area_motion (group)          ║
    ║                                                        ║
    ║  ┌────────────────────────────────────────────────┐   ║
    ║  │  🕐 Awtrix Pixel Clock (8x32 matrix)          │   ║
    ║  │  light.bedroom_clock_matrix                    │   ║
    ║  │  MQTT notifications via bedroom_clock_topic    │   ║
    ║  └────────────────────────────────────────────────┘   ║
    ║                                                        ║
    ║                Ceiling Lighting                        ║
    ║  💡 bedroom_main_light + bedroom_main_light_2         ║
    ║                                                        ║
    ║  Desk Area                                             ║
    ║  ┌───────────────────┐  ┌──────────────────────┐     ║
    ║  │ 💡 Lamp Left      │  │ 💡 Lamp Right        │     ║
    ║  │ (Desk Lamp)       │  │ (Desk Lamp)          │     ║
    ║  └───────────────────┘  └──────────────────────┘     ║
    ║                                                        ║
    ║  🎛️ 4-Button + Dial Remote (Zigbee MQTT)              ║
    ║  ├─ Button 1: Toggle ceiling lights                   ║
    ║  ├─ Button 2: Toggle desk lamps                       ║
    ║  ├─ Button 3: Open blinds                             ║
    ║  ├─ Button 4: Close blinds                            ║
    ║  └─ Dial: Brightness control                          ║
    ║                                                        ║
    ║                    Bed Area                            ║
    ║  ┌──────────────────────────────────────────────┐     ║
    ║  │  🛏️ Bed (4 Pressure Sensors)                │     ║
    ║  │  ┌──────────────────────────────────┐       │     ║
    ║  │  │ TL: 0.15  │        │  TR: 0.15   │       │     ║
    ║  │  │ threshold │        │  threshold  │       │     ║
    ║  │  ├───────────┼────────┼─────────────┤       │     ║
    ║  │  │ BL: 0.15  │        │  BR: 0.1    │       │     ║
    ║  │  │ threshold │        │  threshold  │       │     ║
    ║  │  └───────────┴────────┴─────────────┘       │     ║
    ║  │                                              │     ║
    ║  │  binary_sensor.bed_occupied (template)      │     ║
    ║  │  Attributes: top_left, top_right,           │     ║
    ║  │             bottom_left, bottom_right        │     ║
    ║  └──────────────────────────────────────────────┘     ║
    ║                                                        ║
    ║  💡 Under-bed Lighting                                ║
    ║  ├─ light.under_bed_left (RGB LED strip)             ║
    ║  └─ light.under_bed_right (RGB LED strip)            ║
    ║                                                        ║
    ║                Entertainment Center                    ║
    ║  ┌────────────────────────────────────────────┐       ║
    ║  │  📺 Bedroom TV (media_player.bedroom_tv)  │       ║
    ║  │  🔌 Power Monitor (>40W threshold)         │       ║
    ║  │  sensor.bedroom_tv_plug_power              │       ║
    ║  │  binary_sensor.bedroom_tv_powered_on       │       ║
    ║  └────────────────────────────────────────────┘       ║
    ║                                                        ║
    ║  💨 Climate Control                                    ║
    ║  switch.bedroom_fan (2 hour max runtime)              ║
    ║  Auto-on if temp > 22.5°C during sleep tracking       ║
    ║                                                        ║
    ║  🚪 Door (SOUTH WALL)                                 ║
    ║  binary_sensor.bedroom_door_contact                   ║
    ║  └─ Controls stairs lighting when closed              ║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝

  External Integrations:
  📱 Sleep as Android (webhook integration)
     └─ States: sleep_tracking_started/stopped, awake, alarm_alert_start, etc.
     └─ Timer: timer.sleep (pause/resume capable)

  👦 Leo's Room: binary_sensor.leos_bedroom_door_contact
     └─ Triggers blue lamp flash notifications

  👧 Ashlee's Room: binary_sensor.ashlees_bedroom_door_contact
     └─ Triggers pink lamp flash notifications

  🌄 Upstairs Area: binary_sensor.upstairs_area_motion
     └─ Used for stairway light control

  💡 Stairs Lighting (controlled by bedroom door):
     ├─ light.stairs
     ├─ light.stairs_ambient
     └─ light.stairs_2
```

---

## Key Automation Workflows

### Sleep Tracking Complete Workflow

```
Sleep as Android: "sleep_tracking_started"
   ↓
Webhook → input_text.sleep_as_android
   ↓
Check: Is Danny home?
   ├─ No → Skip
   └─ Yes → Continue
       ↓
    Start Sleep Timer
    └─ Duration: input_number.sleep_timer_duration (default 60 min)
       ↓
    Check Bedroom Temperature
    ├─ > 22.5°C → Turn on bedroom fan
    └─ ≤ 22.5°C → Skip fan
       ↓
    Log: "Sleep timer started, XX:XX:XX remaining"
       ↓
    ┌───────────────────────────────────────────┐
    │  Sleep Cycle Monitoring                   │
    │  ┌─────────────────────────────────────┐  │
    │  │  State: Asleep (not "awake")        │  │
    │  │  ↓                                   │  │
    │  │  After 15 min continuously          │  │
    │  │  ↓                                   │  │
    │  │  Reward: Subtract time from timer   │  │
    │  │  (input_number...time_to_subtract)  │  │
    │  └─────────────────────────────────────┘  │
    │         OR                                 │
    │  ┌─────────────────────────────────────┐  │
    │  │  State Change: "awake"              │  │
    │  │  ↓                                   │  │
    │  │  Pause Timer                         │  │
    │  │  ↓                                   │  │
    │  │  State Change: FROM "awake"         │  │
    │  │  ↓                                   │  │
    │  │  Resume Timer                        │  │
    │  │  Add time (time_to_add)             │  │
    │  │  Cap at original duration           │  │
    │  └─────────────────────────────────────┘  │
    └───────────────────────────────────────────┘
       ↓
    Timer Reaches Zero OR 5:00 AM Reset
       ↓
    Execute bedroom_sleep script
    ├─ Turn off bedroom clock matrix
    └─ Log completion
       ↓
    If fan is on:
    └─ Turn off bedroom fan
       ↓
    Log: "Sleep timer finished. Turning everything off."
```

**Parallel Monitoring:**
- Temperature > 22.5°C → Fan on at start
- Motion detected → Clock turns on if off
- No motion 30 min → Clock turns off if lamps off

---

### Morning Alarm & Wake-Up Sequence

```
Sleep as Android: "alarm_alert_start"
   ↓
Check: Is Danny home?
   ├─ No → Log only, skip actions
   └─ Yes → Continue
       ↓
    Check Blind State
    ├─ Blinds open (above threshold) → Log only
    └─ Blinds closed (below threshold) → Continue
        ↓
     Check Blind Automation
     ├─ Disabled → Log only
     └─ Enabled → Continue
         ↓
      Log: "Alarm triggered. Opening bedroom blinds in 5 minutes."
         ↓
      Wait 5 Minutes
         ↓
      Open Bedroom Blinds
      └─ Natural light wake-up
         ↓
      Parallel Actions:
      ├─ Turn on clock if off
      └─ Log alarm event

Separate Time-Based Opening (if alarm doesn't trigger):
   ↓
8:00 AM (Workday) OR 9:00 AM (Weekend) OR 10:00 AM (Fallback)
   ↓
Check Calendar Integration
├─ Work Calendar: Check for annual leave
└─ Children Calendar: Check for activities (exclude holidays)
   ↓
Evaluate Triggers:
├─ 8 AM: Workday + no leave OR children activities scheduled
├─ 9 AM: Weekend + NOT "No Children" mode + activities scheduled
└─ 10 AM: Any day (fallback)
   ↓
Open Blinds
└─ Log with clock emoji
```

---

### Bed Occupancy → Blind Control

```
Evening Scenario (After Sunset):
   ↓
Someone Gets In Bed
└─ binary_sensor.bed_occupied: ON for 30 sec
   ↓
Check Conditions:
├─ Blind automation enabled?
├─ Bed sensor enabled?
├─ After sunset?
├─ Window closed?
└─ Blinds currently open (above threshold)?
   ↓
All YES → Close Blinds
   ├─ Action: cover.close_cover
   └─ Log: "Someone is in bed, window closed, late. Closing blinds."

Morning Scenario (After Sunrise):
   ↓
Everyone Gets Out Of Bed
└─ binary_sensor.bed_occupied: OFF for 30 sec
   ↓
Check Conditions:
├─ Blind automation enabled?
├─ Bed sensor enabled?
├─ After sunrise (-1hr offset) and before sunset?
└─ Blinds currently closed (below threshold)?
   ↓
All YES → Wait 1 Minute → Open Blinds
   ├─ Action: cover.open_cover
   └─ Log: "No one in bed. Opening the blinds."

Bed Occupancy Detection Logic:
   ↓
Four Pressure Sensors:
├─ Top Left: >= 0.15 → Occupied
├─ Top Right: >= 0.15 → Occupied
├─ Bottom Left: >= 0.15 → Occupied
└─ Bottom Right: >= 0.1 → Occupied (lower threshold)
   ↓
ANY sensor above threshold → binary_sensor.bed_occupied = ON
ALL sensors below threshold → binary_sensor.bed_occupied = OFF
```

---

### Children's Door Monitoring (Night Alerts)

```
After Children's Bedtime (input_datetime.childrens_bed_time):
   ↓
Child's Door Opens
├─ Leo's door (binary_sensor.leos_bedroom_door_contact)
└─ Ashlee's door (binary_sensor.ashlees_bedroom_door_contact)
   ↓
Check Conditions:
├─ Bedroom lamps OR ceiling on?
├─ After bedtime?
└─ NOT in "Guest" or "No Children" home mode?
   ↓
All YES → Visual + Media Notification
   ↓
Save Current Lamp State
   ↓
Flash Lamp Notification:
├─ Leo's door → Blue flash (repeat 2x)
└─ Ashlee's door → Pink flash (repeat 2x)
   ↓
Restore Lamp State:
├─ If lamps were off → Turn off after flash
└─ If lamps were on → Restore to scene.bedroom_desk_lamps_on
   ↓
Parallel Media Action:
├─ Is bedroom TV playing?
├─ Is app "Web Video Caster"?
└─ YES to both → Pause TV
   ↓
Log Event:
├─ "Leo's door opened, bedroom light on. Sending warning."
└─ "Ashlee's door opened, bedroom light on. Sending warning."

Child's Door Closes (Same Conditions):
   ↓
Flash Confirmation:
├─ Leo → Blue → Green → Off (repeat 2x)
└─ Ashlee → Pink → Green → Off (repeat 2x)
   ↓
Restore Lamp State
   ↓
If TV was paused → Resume playback
   ↓
Log: "Child's door closed, sending warning."
```

**Color Codes:**
- Blue = Leo's activity
- Pink = Ashlee's activity
- Green = "Back in bed" confirmation

---

### Motion-Based Ambient Lighting

```
Motion Detected (bedroom_motion_occupancy)
   ↓
Check Enable Flag
├─ input_boolean.enable_bedroom_motion_trigger OFF → Skip
└─ ON → Continue
   ↓
Check Under-Bed Light State
├─ Both lights off OR brightness < 100 → Continue
└─ Already bright enough → Skip
   ↓
Evaluate Context (Time + Blind State):
   ↓
┌─────────────────────────────────────────────────┐
│ Scenario 1: Blinds Down (Dark/Night)           │
│ ├─ Blind position < 31%                        │
│ └─ Action: scene.bedroom_dim_ambient_light     │
│    ├─ Under-bed left: brightness 15, 2732K     │
│    └─ Under-bed right: brightness 10, warm     │
├─────────────────────────────────────────────────┤
│ Scenario 2: Daytime (After 8 AM, Before Sunset)│
│ ├─ After 8:00 AM AND before sunset             │
│ └─ Action: scene.bedroom_turn_on_ambient_light │
│    ├─ Under-bed left: brightness 128, 366 mireds│
│    └─ Under-bed right: brightness 128, 366 mireds│
├─────────────────────────────────────────────────┤
│ Scenario 3: Night (After Sunset OR Before 8 AM)│
│ ├─ After sunset OR before 8:00 AM              │
│ └─ Action: scene.bedroom_dim_ambient_light     │
│    └─ Same as Scenario 1                        │
└─────────────────────────────────────────────────┘
   ↓
Turn On Clock Matrix (if off)
   ↓
Log Event (scenario-specific message)

No Motion Detected (2 min):
   ↓
Check Conditions:
├─ Either under-bed light is on?
└─ Motion trigger enabled?
   ↓
Both YES → Turn Off Ambient Lights
   ├─ scene.bedroom_turn_off_ambient_light
   └─ Log: "No motion for 2 minutes. Turning ambient lights off."

No Motion For Long Time (30 min):
   ↓
Check Conditions:
├─ No bedroom area motion for 30 min
├─ Bedroom lamps are OFF
└─ Motion trigger enabled
   ↓
All YES → Turn Off Clock
   ├─ light.bedroom_clock_matrix off
   └─ Log: "No motion for 30 minutes. Turning clock off."
```

---

### TV Watching During Day (Glare Management)

```
TV Turns On (>40W)
   ↓
Check Conditions:
├─ After sunrise, before sunset?
├─ Blind automation enabled?
└─ Blinds currently open (above threshold)?
   ↓
All YES → Evaluate Window State
   ↓
┌─────────────────────────────────────────────┐
│ Window OPEN:                                │
│ ├─ Direct notifications enabled?            │
│ │  └─ YES → Send Actionable Notification    │
│ │     ├─ Title: "TV On & Window Is Open"   │
│ │     ├─ Message: "Close the blinds?"      │
│ │     ├─ Button 1: "Yes" → set_bedroom_    │
│ │     │                    blinds_30        │
│ │     └─ Button 2: "No" → ignore           │
│ └─ NO → Do nothing                          │
├─────────────────────────────────────────────┤
│ Window CLOSED:                              │
│ └─ Automatic Action: Set blinds to 20%     │
│    ├─ cover.set_cover_position: 20         │
│    └─ Log: "TV on, bright. Lowering blinds"│
└─────────────────────────────────────────────┘

TV Turns Off (1 min delay):
   ↓
Check Conditions:
├─ Blinds closed (below threshold)?
├─ Blind automation enabled?
├─ After sunrise, before sunset, after 8:30 AM?
└─ All YES → Continue
   ↓
Get Weather Forecast (hourly)
   ↓
Evaluate Temperature:
├─ Current temp > input_number.forecast_high_temperature?
│  OR
├─ Next hour forecast > forecast_high_temperature?
   ↓
Temperature TOO HIGH:
└─ Keep blinds closed
   └─ Log: "TV off but weather above XX°C (YY°C). Keeping blinds closed."
   ↓
Temperature ACCEPTABLE:
└─ Open blinds (restore natural light)
   ├─ cover.open_cover
   └─ Log: "TV turned off. Opening blinds."
```

**Smart Features:**
- Window-aware: Different action if window open
- Weather-aware: Checks forecast before opening
- User control: Actionable notification for manual decision
- Glare reduction: Dims to 20% automatically when window closed

---

### Fan Auto-Management (Temperature + Timer)

```
Sleep Tracking Starts + Warm Room:
   ↓
Check Conditions:
├─ Danny is home?
├─ Bedroom mean temp > 22.5°C?
└─ Fan currently off?
   ↓
All YES → Turn On Fan
   ├─ switch.bedroom_fan ON
   └─ Log: "Bedroom warm (XX°C > 22.5). Turning on fan."
       ↓
    2-Hour Safety Timer Starts
       ├─ Automation: ID 1690844451011
       └─ Trigger: Fan on for 2 hours
           ↓
        After 2 Hours:
        ├─ Turn off fan
        └─ Log: "Fan on for 2 hours. Turning fan off."

Alternative Shutoff Triggers:
   ↓
┌────────────────────────────────────────┐
│ Sleep Timer Completes:                 │
│ ├─ Timer.sleep finished                │
│ └─ If fan on → Turn off fan            │
│    └─ Log: "Fan was on during sleep.   │
│             Turning off fan."          │
├────────────────────────────────────────┤
│ No Presence for 5 Minutes:             │
│ ├─ bedroom_motion_3_presence: OFF 5min │
│ └─ If fan on → Turn off fan            │
│    └─ Energy saving, room vacant       │
└────────────────────────────────────────┘

Result: Fan runs for:
- Maximum 2 hours continuous
- Until sleep timer completes
- Until room vacant for 5 min
(Whichever comes first)
```

---

### Remote Control Button Actions

```
4-Button + Dial Remote (Device ID: 61ab87aac9c81fe8687771074e560f48)

┌─────────────────────────────────────────────────┐
│ Button 1 (Ceiling Light Toggle)                │
│ ├─ Press/Release                                │
│ └─ If lights on → Turn off both ceiling lights │
│    If lights off → Turn on both ceiling lights │
├─────────────────────────────────────────────────┤
│ Button 2 (Desk Lamps Toggle)                    │
│ ├─ Press/Release                                │
│ └─ If lamps off → scene.bedroom_desk_lamps_on   │
│                   (1s transition)               │
│    If lamps on → Turn off lamps + under-bed     │
│                  (all ambient lighting)         │
├─────────────────────────────────────────────────┤
│ Button 3 (Open Blinds)                          │
│ ├─ Press/Release                                │
│ └─ cover.open_cover (bedroom_blinds)            │
├─────────────────────────────────────────────────┤
│ Button 4 (Close Blinds)                         │
│ ├─ Press/Release                                │
│ └─ cover.close_cover (bedroom_blinds)           │
└─────────────────────────────────────────────────┘

Dial Control (Lamp Brightness):
   ↓
Rotate Right (Brighten):
├─ Triggers: dial_rotate_right_slow/step, brightness_step_up
├─ Condition: action_time sensor > 0
└─ Action: Increase brightness
   ├─ Formula: current_brightness + (action_time * 2)
   ├─ Max: 255
   ├─ Transition: 1 second
   └─ Queue mode: max 10 (smooth continuous adjustment)
   ↓
Rotate Left (Dim):
├─ Triggers: dial_rotate_left_slow/step, brightness_step_down
├─ Condition: action_time sensor > 0
└─ Action: Decrease brightness
   ├─ Formula: current_brightness - (action_time * 2)
   ├─ Min: 0
   ├─ Transition: 1 second
   └─ Queue mode: max 10 (smooth continuous adjustment)

Action Time Calculation:
- sensor.bedroom_dial_remote_action_time
- Measures rotation speed/duration
- Multiplied by 2 for brightness delta
- Faster rotation = bigger steps
```

---

## Configuration Parameters

### Sleep Tracking Settings
- `input_number.sleep_timer_duration` - Total sleep timer duration (default: 60 minutes)
- `input_number.sleep_as_android_time_to_add` - Minutes to add when falling back asleep
- `input_number.sleep_as_android_time_to_subtract` - Minutes to subtract after 15 min continuous sleep (reward)
- `input_select.sleep_as_android_notification_level` - Notification verbosity
  - Options: "Start/Stop", "Start/Stop/Alarms", "All"

### Blind Control Settings
- `input_boolean.enable_bedroom_blind_automations` - Master enable for blind automations
- `input_number.blind_open_position_threshold` - Threshold for "open" state (e.g., 50)
- `input_number.blind_closed_position_threshold` - Threshold for "closed" state (e.g., 30)
- `input_number.bedroom_blind_closed_threshold` - Bedroom-specific closed threshold

### Motion & Lighting Settings
- `input_boolean.enable_bedroom_motion_trigger` - Master enable for motion-activated lighting
- `input_boolean.enable_bed_sensor` - Enable/disable bed occupancy sensor

### Temperature & Weather Settings
- `input_number.forecast_high_temperature` - High temperature threshold for blind decisions (°C)
- Bedroom fan auto-on threshold: 22.5°C (hardcoded in automation)

### Time Schedules
- `input_datetime.childrens_bed_time` - Bedtime for child monitoring automations
- Morning blind opening: 8:00 AM (workday), 9:00 AM (weekend), 10:00 AM (fallback)
- Evening blind closing: 22:00 (10 PM)
- Sleep timer reset: 5:00 AM daily
- Motion lighting: 2-minute off delay
- Clock auto-off: 30 minutes no motion
- Fan safety timeout: 2 hours
- Fan presence timeout: 5 minutes no presence

### Calendar Integration
- `calendar.work` - Danny's work calendar (checks for annual leave)
- `calendar.tsang_children` - Children's activity calendar (excludes "half term", "holidays")

---

## Helper Entities

### Input Booleans
- `input_boolean.enable_bedroom_blind_automations` - Master blind automation control
- `input_boolean.enable_bedroom_motion_trigger` - Motion-activated lighting enable
- `input_boolean.enable_bed_sensor` - Bed occupancy sensor enable/disable
- `input_boolean.enable_direct_notifications` - Actionable notifications (TV/window prompt)

### Input Numbers
- `input_number.sleep_timer_duration` - Sleep timer total duration (minutes)
- `input_number.sleep_as_android_time_to_add` - Awake penalty (minutes to add)
- `input_number.sleep_as_android_time_to_subtract` - Sleep reward (minutes to subtract)
- `input_number.blind_open_position_threshold` - Blind "open" detection threshold
- `input_number.blind_closed_position_threshold` - Blind "closed" detection threshold
- `input_number.bedroom_blind_closed_threshold` - Bedroom-specific blind threshold
- `input_number.forecast_high_temperature` - Weather threshold for blind control (°C)

### Input Text
- `input_text.sleep_as_android` - Current sleep tracking state from app
  - States: sleep_tracking_started, sleep_tracking_stopped, awake, alarm_alert_start, etc.

### Input Datetime
- `input_datetime.childrens_bed_time` - Children's bedtime for door monitoring

### Input Select
- `input_select.sleep_as_android_notification_level` - Notification verbosity
  - Options: "Start/Stop", "Start/Stop/Alarms", "All"
- `input_select.home_mode` - House mode (affects child door notifications)
  - Checked values: "Guest", "No Children"

### Timers
- `timer.sleep` - Sleep duration timer (pause/resume capable)
  - Starts when sleep tracking begins
  - Pauses when awake
  - Resumes when fall back asleep
  - Finishes at zero or 5:00 AM reset

---

## Scripts

### Child Door Notification Scripts
- `script.bedroom_leos_door_opened_notification`
  - Flash lamps blue twice
  - Restore previous lamp state
  - Parameters: lamp_state (on/off)

- `script.bedroom_leos_door_closed_notification`
  - Flash lamps blue → green (2x)
  - Restore previous lamp state
  - Parameters: lamp_state (on/off)

- `script.bedroom_ashlees_door_opened_notification`
  - Flash lamps pink twice
  - Restore previous lamp state
  - Parameters: lamp_state (on/off)

- `script.bedroom_ashlees_door_closed_notification`
  - Flash lamps pink → green (2x)
  - Restore previous lamp state
  - Parameters: lamp_state (on/off)

### Orchestration Scripts
- `script.other_bedroom_door_opening_warning`
  - Determines which child's door opened (leo/ashlee)
  - Saves current lamp state
  - Calls appropriate notification script
  - Pauses bedroom TV if playing Web Video Caster
  - Logs event
  - Parameters: bedroom (text: "leo" or "ashlee")

- `script.other_bedroom_door_closes_warning`
  - Determines which child's door closed
  - Saves current lamp state
  - Calls appropriate notification script
  - Resumes bedroom TV if paused
  - Logs event
  - Parameters: bedroom (text: "leo" or "ashlee")

### Weather & Blind Scripts
- `script.bedroom_close_blinds_by_weather`
  - Weather-aware blind closing
  - Only during daytime (before sunset)
  - Checks window state
  - Parameters:
    - temperature (number: -20 to 50°C, step 0.1)
    - weather_condition (text: e.g., "sunny", "partlycloudy")
  - Logic:
    - If sunny/partlycloudy + window open → Log warning only
    - If sunny/partlycloudy + window closed → Close blinds
    - Other conditions → Do nothing

### Sleep Control Scripts
- `script.bedroom_sleep`
  - Executes sleep mode actions
  - Turns off bedroom clock matrix if on
  - Called by sleep timer completion

### Awtrix Clock Scripts
- `script.send_bedroom_clock_notification`
  - Send notification to Awtrix pixel clock
  - Parameters:
    - message (text, multiline, required)
    - icon (number: 1-100, optional)
    - duration (number: 1-120 seconds, default 10)
  - Uses MQTT publish to bedroom_clock_device_topic/notify
  - Payload format: JSON with text, icon, duration

---

## Sensors

### Template Binary Sensors
- `binary_sensor.bedroom_tv_powered_on`
  - Unique ID: 0dcba639-2e46-428e-bb7e-43307fa653b3
  - Device class: running
  - State: Power > 40W
  - Dynamic icon: mdi:television-classic / mdi:television-classic-off
  - Source: sensor.bedroom_tv_plug_power

- `binary_sensor.bed_occupied`
  - Device class: occupancy
  - State logic: ANY of the 4 sensors above threshold
    - Top left: >= 0.15
    - Top right: >= 0.15
    - Bottom left: >= 0.15
    - Bottom right: >= 0.1
  - Dynamic icon: mdi:bed-double-outline (occupied) / mdi:bed-double (empty)
  - Attributes:
    - top_left: sensor.bed_top_left value
    - top_right: sensor.bed_top_right value
    - bottom_left: sensor.bed_bottom_left value
    - bottom_right: sensor.bed_bottom_right value

- `binary_sensor.danny_asleep`
  - Unique ID: 94b3d4d4-f5d9-4f9c-ae32-c98c40df72dc
  - State: NOT in ['awake', 'sleep_tracking_stopped']
  - Dynamic icon: mdi:sleep / mdi:sleep-off
  - Source: input_text.sleep_as_android

### History Stats Sensors (TV Uptime)
- `sensor.bedroom_tv_uptime_today`
  - Platform: history_stats
  - Entity: binary_sensor.bedroom_tv_powered_on
  - State: "on"
  - Type: time
  - Start: Today at midnight
  - End: Now

- `sensor.bedroom_tv_uptime_yesterday`
  - Platform: history_stats
  - Entity: binary_sensor.bedroom_tv_powered_on
  - State: "on"
  - Type: time
  - End: Today at midnight
  - Duration: 24 hours

- `sensor.bedroom_tv_uptime_this_week`
  - Platform: history_stats
  - Entity: binary_sensor.bedroom_tv_powered_on
  - State: "on"
  - Type: time
  - Start: Monday midnight (this week)
  - End: Now

- `sensor.bedroom_tv_uptime_last_30_days`
  - Platform: history_stats
  - Entity: binary_sensor.bedroom_tv_powered_on
  - State: "on"
  - Type: time
  - End: Today at midnight
  - Duration: 30 days

### Mold Indicator Sensor
- `sensor.bedroom_mould_indicator`
  - Platform: mold_indicator
  - Indoor temp: sensor.bedroom_door_temperature
  - Indoor humidity: sensor.bedroom_humidity_2
  - Outdoor temp: sensor.gw2000a_outdoor_temperature
  - Calibration factor: 1.38
  - Calculates mold risk based on temperature differential and humidity

---

## Status Indicators

### Light Scenes

**Ambient Lighting (Under-Bed):**

- `scene.bedroom_turn_on_ambient_light` (ID: 1621715555428)
  - Under-bed left: brightness 128, color_temp 366 mireds (2732K)
  - Under-bed right: brightness 128, color_temp 366 mireds
  - Icon: mdi:led-strip-variant
  - Purpose: Normal ambient lighting for motion detection

- `scene.bedroom_dim_ambient_light` (ID: 1621715588909)
  - Under-bed left: brightness 15, color_temp 366 mireds (2732K), warm white
  - Under-bed right: brightness 10, warm white XY color
  - Icon: mdi:led-strip-variant
  - Purpose: Low-light navigation at night, blinds down, or late evening

- `scene.bedroom_turn_off_ambient_light` (ID: 1621715612398)
  - Under-bed left: OFF
  - Under-bed right: OFF
  - Icon: mdi:led-strip-variant
  - Purpose: No motion detected, energy saving

**Desk Lamps:**

- `scene.bedroom_desk_lamps_on` (ID: 1615211281868)
  - Bedroom lamp left: brightness 200, warm color (38.667° hue, 52.941% sat)
  - Bedroom lamp right: brightness 200, warm color (matching)
  - RGB: (255, 207, 120)
  - XY: (0.457, 0.41)
  - Icon: mdi:lightbulb
  - Purpose: Work/reading lighting

- `scene.bedroom_desk_lamps_off` (ID: 1615211309175)
  - Bedroom lamp left: OFF
  - Bedroom lamp right: OFF
  - Icon: mdi:lightbulb
  - Purpose: Lamps off state

**Notification Colors:**
- Blue (Leo's door): RGB via lamp flash, temporary
- Pink (Ashlee's door): RGB via lamp flash, temporary
- Green (confirmation): RGB via lamp flash, temporary

---

## Key Features

✅ **Sleep as Android Integration** - Full webhook support with 20+ states
✅ **Intelligent Sleep Timer** - Pause/resume with awake detection, time rewards/penalties
✅ **Bed Occupancy Detection** - 4-sensor pressure mat with configurable thresholds
✅ **Smart Wake Alarm** - Gradual blind opening 5 min after alarm
✅ **Child Door Monitoring** - Visual lamp notifications (blue/pink) for parent awareness
✅ **TV Privacy Protection** - Auto-pause when door opens at night
✅ **Climate-Aware Fan Control** - Auto-on when warm (>22.5°C), 2-hour safety limit
✅ **Motion-Adaptive Lighting** - Context-aware brightness (blinds, time, ambient)
✅ **Calendar Integration** - Work/activity-aware blind scheduling
✅ **Weather-Aware Blind Control** - Temperature-based decisions for comfort
✅ **Awtrix Pixel Clock** - MQTT notification system with icons
✅ **4-Button + Dial Remote** - Complete room control via Zigbee
✅ **Window Safety Logic** - Prevents blind movement when window open
✅ **Automatic Stairway Control** - Turns off stairs lights when bedroom door closed
✅ **Progressive Lighting** - Gradual dim/off sequences (2 min motion timeout)
✅ **TV Glare Management** - Auto-adjusts blinds during daytime TV viewing
✅ **Multi-Sensor Redundancy** - Motion, occupancy, presence sensors
✅ **Usage Analytics** - TV runtime tracking (today, yesterday, week, 30 days)
✅ **Mold Prevention** - Environmental monitoring with calibrated risk calculation
✅ **Energy Monitoring** - Power consumption tracking for TV
✅ **Dual Blind Automations** - Both occupancy-based and time-based
✅ **Smart Scene Selection** - Context-aware lighting based on blind position and time
✅ **Manual Override Support** - Physical remote for all automated functions

---

## File Structure

```
packages/rooms/bedroom/
├── bedroom.yaml                    # Main automation configuration (1776 lines)
│   ├── Automations (35 total)
│   │   ├── Bed occupancy (2)
│   │   ├── Door sensors (4)
│   │   ├── Motion triggers (4)
│   │   ├── Fan control (1)
│   │   ├── Time-based blinds (2)
│   │   ├── TV integration (2)
│   │   └── Remote control (6)
│   ├── Scenes (5)
│   │   ├── Ambient lighting (3)
│   │   └── Desk lamps (2)
│   ├── Scripts (6)
│   │   ├── Child notifications (4)
│   │   ├── Door warning orchestration (2)
│   │   ├── Weather-based blind control (1)
│   │   └── Sleep mode (1)
│   ├── Sensors (5)
│   │   ├── History stats (4 TV uptime)
│   │   └── Mold indicator (1)
│   └── Template Sensors (2)
│       ├── TV powered on
│       └── Bed occupied
│
├── sleep_as_android.yaml           # Sleep tracking integration (363 lines)
│   ├── Automations (7)
│   │   ├── Webhook receiver (1)
│   │   ├── Sleep timer management (3)
│   │   ├── Awake/asleep transitions (2)
│   │   └── Alarm handling (1)
│   └── Template Sensors (1)
│       └── Danny asleep
│
├── awtrix_light.yaml               # Pixel clock notifications (53 lines)
│   └── Scripts (1)
│       └── Send clock notification
│
└── BEDROOM-SETUP.md                # This file - Room documentation
```

---

## Automation Summary by Category

### Sleep Tracking & Management (7 automations)
- Sleep As Android: Event (ID 1614285576722) - Webhook receiver
- Started Tracking (ID 1658438667856) - Timer start + fan
- Awake (ID 1658843567854) - Pause timer
- Fall Asleep (ID 1658843828191) - Resume timer + add time
- Danny Asleep For A Period Of Time (ID 1659861914053) - Subtract time reward
- Timer: Sleep Timer Complete (ID 1658842750488) - Execute sleep script
- Danny's Alarm (ID 1644769166837) - Blind opening + clock
- Stop Sleep Timer (ID 1667424349110) - 5 AM reset

### Bed Occupancy (2 automations)
- Close Blinds When Someone Is In Bed After Sunset (ID 1601641236163)
- Open Blind When No One Is In Bed (ID 1601641292576)

### Door Sensors (4 automations)
- Bedroom: Door Closed (ID 1715955339483) - Stairs light control
- Other Bedroom Door Opens Warning (ID 1615209552353) - Child monitoring
- Other Bedroom Door Closes Warning (ID 1615209552354) - Child monitoring
- Pause TV When Door Opens At Night (ID 1724001157269) - Privacy

### Motion & Lighting (4 automations)
- Motion Detected (ID 1621713217274) - Context-aware lighting
- No Motion (ID 1621713867762) - 2-min timeout
- No Motion For Long Time (ID 1621713867763) - 30-min clock off
- No Motion And Fan Is On (ID 1725207477313) - 5-min fan off

### Climate Control (1 automation)
- Turn Off Fan (ID 1690844451011) - 2-hour safety limit

### Time-Based Blinds (2 automations)
- Morning Timed Open Blinds (ID 1621875409014) - 8/9/10 AM calendar-aware
- Evening Timed Close Blinds (ID 1621875567853) - 22:00 (10 PM)

### Window & Blind (2 automations)
- Window Closed At Night (ID 1622667464880)
- Window Closed And Someone Is In Bed At Night (ID 1615689096351)

### TV Integration (2 automations)
- TV Turned On During Bright Day (ID 1624194131454) - Glare management
- TV Turned Off (ID 1624194439043) - Weather-aware blind opening

### Remote Control (6 automations)
- Remote Button 1 (ID 1699308571385) - Ceiling toggle
- Remote Button 2 (ID 1699308571386) - Lamp toggle
- Remote Button 3 (ID 1699308571387) - Open blinds
- Remote Button 4 (ID 1699308571388) - Close blinds
- Remote Dial Action Right (ID 1710079376648) - Brighten
- Remote Dial Action Left (ID 1710079376649) - Dim

**Total Automation Count:** 30 automations across 3 files
**Total Script Count:** 7 scripts
**Total Scene Count:** 5 scenes
**Total Sensor Count:** 7 sensors (5 history stats + 2 template)

---

## Advanced Features Explained

### Sleep Tracking Timer Logic

The sleep timer system implements sophisticated pause/resume with time adjustments:

**Initial Duration:**
- Configurable via input_number.sleep_timer_duration (default 60 min)
- Starts when sleep_tracking_started

**Awake Detection:**
- State changes to "awake" → Timer pauses
- Preserves remaining time
- No actions taken, just pause

**Fall Back Asleep:**
- State changes FROM "awake" (to any other state)
- Resumes timer from paused state
- Adds penalty time (input_number.sleep_as_android_time_to_add)
- Caps at original duration (prevents infinite extension)

**Sleep Reward (15 min continuous):**
- If asleep continuously for 15+ minutes
- Subtracts time from timer (input_number.sleep_as_android_time_to_subtract)
- Only if remaining time would still be positive
- Encourages sustained sleep

**Completion:**
- Timer reaches zero → Execute bedroom_sleep script + turn off fan
- 5:00 AM daily reset → Cancel timer if still active/paused
- Prevents timer running into next day

**Example Timeline:**
```
23:00 - Sleep tracking starts, 60 min timer begins
23:15 - Asleep 15 min → Subtract 5 min → 40 min remaining
23:30 - Wake up → Timer pauses at 40 min
23:45 - Fall back asleep → Add 10 min penalty → 50 min, timer resumes
00:35 - Timer reaches zero → Turn off clock, turn off fan
```

### Bed Occupancy Pressure Sensor Array

Four independent pressure sensors with individual thresholds:

**Sensor Layout:**
```
┌──────────────────────┐
│  TL (0.15)  TR (0.15) │  Top sensors: Higher threshold
│                       │  (head/shoulders area)
│                       │
│  BL (0.15)  BR (0.10) │  Bottom sensors: BR lower threshold
└──────────────────────┘  (foot area, less pressure)
```

**Detection Logic:**
- ANY sensor >= threshold → Bed occupied = ON
- ALL sensors < threshold → Bed occupied = OFF
- Bottom right has lower threshold (0.1 vs 0.15)
- Accommodates different body positions and weights

**Automation Impact:**
- Occupied + After sunset + Window closed → Close blinds (30 sec delay)
- Unoccupied + After sunrise + Before sunset → Open blinds (30 sec + 1 min delay)
- Child door warnings require bed occupied (parent alert logic)
- Can be disabled via input_boolean.enable_bed_sensor

### Child Door Monitoring Color System

**Visual Language:**
- **Blue** = Leo's room activity
- **Pink** = Ashlee's room activity
- **Green** = "Back in bed" confirmation

**Open Sequence:**
1. Save current lamp state (on/off)
2. Flash color twice (blue for Leo, pink for Ashlee)
3. Turn lamps off between flashes
4. Restore original state (off or scene.bedroom_desk_lamps_on)

**Close Sequence:**
1. Save current lamp state
2. Flash child's color (blue/pink)
3. Flash green (confirmation)
4. Turn lamps off
5. Repeat sequence twice
6. Restore original state

**Media Integration:**
- If TV playing Web Video Caster → Pause when door opens
- If TV paused → Resume when door closes
- BBC iPlayer excluded (live TV exception)

**Conditions:**
- Only after input_datetime.childrens_bed_time
- Only if bedroom lights are on (parent is awake)
- NOT in "Guest" or "No Children" home mode
- Queued mode (max 10) handles multiple door events

### Motion-Based Lighting Context Awareness

The system adapts lighting based on THREE contexts:

**Context 1: Blinds Down (Dark Room)**
- Blind position < 31%
- Result: Dim ambient (brightness 15/10)
- Purpose: Night navigation, minimal disturbance

**Context 2: Daytime (After 8 AM, Before Sunset)**
- After 8:00 AM AND before sunset
- Result: Full ambient (brightness 128)
- Purpose: Normal room lighting

**Context 3: Night/Early Morning**
- After sunset OR before 8:00 AM
- Result: Dim ambient (brightness 15/10)
- Purpose: Late evening or pre-dawn minimal lighting

**Additional Logic:**
- Only activates if under-bed lights off OR brightness < 100
- Always turns on clock matrix if off
- 2-minute timeout to turn off (no motion)
- 30-minute timeout to turn off clock (no area motion + lamps off)

### Weather-Aware TV Blind Control

When TV turns off during the day:

**Weather Check:**
1. Get hourly weather forecast (next 2 hours)
2. Compare current temperature to forecast_high_temperature
3. Compare next hour forecast to forecast_high_temperature

**Decision Logic:**
- **Current OR next hour > threshold:**
  - Keep blinds closed (prevent heat entry)
  - Log: "TV off but weather above XX°C. Keeping blinds closed."

- **Both below threshold:**
  - Open blinds (restore natural light)
  - Log: "TV turned off. Opening blinds."

**Conditions:**
- Only runs after sunrise, before sunset, after 8:30 AM
- Only if blinds currently closed
- Blind automation must be enabled

**Purpose:** Balance natural light with thermal comfort

### Calendar-Aware Morning Blind Opening

Three trigger times with intelligent calendar checks:

**8:00 AM (Workday):**
- Check binary_sensor.workday_sensor = ON
- Check calendar.work for "Danny" (annual leave)
- If workday AND no leave → Open blinds
- OR if calendar.tsang_children has activities (excluding "half term"/"holidays")

**9:00 AM (Weekend with Activities):**
- Check NOT a workday
- Check NOT in "No Children" home mode
- Check calendar.tsang_children for activities (excluding keywords)
- If activities scheduled → Open blinds

**10:00 AM (Fallback):**
- Any day, any conditions
- Always open blinds

**Calendar Integration:**
- 2-hour lookahead window (now + 2 hours)
- Filters activities by summary keywords
- Distinguishes work vs school holidays
- Prevents inappropriate wake-ups on vacation days

**Additional Conditions:**
- Blinds must be closed (below threshold)
- Blind automation enabled
- TV must be off (not watching in dark)

### Remote Dial Brightness Control

**Dynamic Brightness Adjustment:**
- Uses sensor.bedroom_dial_remote_action_time
- Measures rotation speed/duration
- Faster rotation = bigger brightness steps

**Calculation:**
```
Right rotation (brighten):
new_brightness = min(255, current_brightness + (action_time * 2))

Left rotation (dim):
new_brightness = max(0, current_brightness - (action_time * 2))
```

**Smooth Operation:**
- 1-second transition per adjustment
- Queued mode (max 10) allows continuous rotation
- Multiple events processed sequentially
- No jarring jumps, smooth ramping

**Triggers:**
- Slow rotation (dial_rotate_right/left_slow)
- Step rotation (dial_rotate_right/left_step)
- Brightness buttons (brightness_step_up/down)

**Condition:** Action time must be > 0 (prevents division by zero)

---

**Last Updated:** 2026-01-24
**Documentation Version:** 1.0
**Automation Count:** 30 (across 3 files)
**Device Count:** 50+ entities
**Scene Count:** 5
**Script Count:** 7
**Sensor Count:** 7 (+ 3 template binary sensors)
**Configuration Files:** 3 (bedroom.yaml, sleep_as_android.yaml, awtrix_light.yaml)
**Special Integrations:** Sleep as Android (webhook), Awtrix Light (MQTT), Calendar (Work + Children)
