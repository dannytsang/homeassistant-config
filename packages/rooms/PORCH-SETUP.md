# Porch Setup Documentation

**Created:** 2026-01-24
**Room:** Porch (Front Entrance)
**Focus:** Entry/Exit Management, Motion-Activated Lighting, Front Door Monitoring, Security Integration
**Special Features:** Ring Doorbell Integration, Nuki Smart Lock, Entry Direction Detection, Package Detection, Door Open/Close Tracking

---

## Device Inventory

| Category | Device | Type | Function |
|----------|--------|------|----------|
| **Motion Detection** | binary_sensor.porch_motion_occupancy | Occupancy Sensor | Porch motion detection for lighting and entry direction |
| | sensor.porch_motion_illuminance | Light Level Sensor | Ambient light measurement for lighting triggers |
| **Lighting** | light.porch | Color LED Light | Main porch exterior light (color capable, dimmable) |
| **Door Sensors** | binary_sensor.front_door | Contact Sensor | Front door open/close state detection |
| **Physical Controls** | binary_sensor.porch_main_light_input | Physical Switch | Manual wall switch for porch light |
| **Timers** | timer.porch_light | Timer | Light timeout timer (1 minute default) |
| **Counters** | counter.front_door_opened_closed | Counter | Tracks door open/close events for entry/exit detection |
| **Templates** | sensor.door_entry_direction | Template Sensor | Determines if entry or exit based on motion and door state |
| **Security Integration** | camera.porch (Ring) | Doorbell Camera | Security camera with person detection |
| | lock.nuki_front_door | Smart Lock | Nuki smart lock integration |
| | alarm_control_panel.house_alarm | Alarm Panel | House alarm state integration |

---

## Automation Functions

### Motion Detection & Lighting Control

**Triggers:** Porch motion sensor occupancy changes

**Logic:**

- **Motion Detected (On/Off) - ID: 1737283018710:**
  - Consolidated automation handling both motion detection and clearing
  - Two trigger branches:
    - **Motion ON:** Detected for 2 minutes
      - Turn on porch light at 100% brightness
      - Cancel any active light timer
    - **Motion OFF:** Cleared for 1 minute
      - Start 1-minute light timer
      - Log event to home log
  - Mode: Single (prevents overlapping triggers)
  - Purpose: Automatic lighting when approaching porch

- **Light Timer Finished - ID: 1737283018709:**
  - Trigger: timer.porch_light finishes
  - Actions:
    - Turn off porch light
    - Log event
  - Mode: Single
  - Purpose: Automatic light shutdown after motion clears

**Safety Features:**
- 2-minute motion detection delay (prevents false triggers)
- 1-minute no-motion delay (safe exit time)
- 1-minute timer after motion clears (total 2 minutes on after motion stops)
- Timer cancellation on new motion (extends lighting)

**Related Automations:**
- ID 1737283018710 - Motion Detected (On/Off)
- ID 1737283018709 - Light Timer Finished

---

### Front Door Entry/Exit Management

**Triggers:** Front door opening and closing events

**Logic:**

- **Front Door Opened - ID: 1606157753577:**
  - Trigger: binary_sensor.front_door changes to "on"
  - Conditional lighting:
    - If illuminance < 100 lux (dark):
      - Turn on porch light via scene.porch_light_on
      - Cancel any active light timer
      - Log event with illuminance value
  - Always increments counter.front_door_opened_closed
  - 2-second delay for camera capture timing
  - Mode: Single

- **Front Door Opened Once For More than 20 seconds - ID: 1614033445487:**
  - Trigger: Front door open for 20 seconds
  - Condition: Counter < 2 (single opening)
  - Action: Reset counter to 0
  - Purpose: Differentiate single open from entry/exit
  - Mode: Single

- **Front Door Open Indicator - ID: 1611931052908:**
  - Trigger: Front door opens
  - Condition: group.tracked_people is "home"
  - Actions:
    - Log event
    - Execute script.front_door_open_notification
  - Mode: Single
  - Purpose: Visual notification when door open and someone home

- **Front Door Closed For More than 20 seconds - ID: 1615224190495:**
  - Trigger: Front door closed for 20 seconds
  - Action: Reset counter to 0
  - Purpose: Reset entry/exit tracking
  - Mode: Single

- **Front Door Closed - ID: 1611931640441:**
  - Trigger: Front door closes
  - Actions:
    - Log event
    - Execute script.front_door_closed_notification
  - Mode: Single

- **Front Door Closed And Start Timer - ID: 1606157835544:**
  - Trigger: Front door closes
  - Actions:
    - Start 1-minute porch light timer
    - Log event
    - If stairs light is on: Turn stairs light off (fallback)
  - Mode: Single
  - Purpose: Coordinate porch and stairs lighting

**Counter Logic:**
- Counter increments on door open
- If door stays open 20+ seconds: Reset (not entry/exit)
- If door closes after 20+ seconds: Reset
- Counter used to detect rapid open/close (entry/exit pattern)

**Safety Features:**
- Always turns on light if dark when door opens
- Provides exit lighting for 1 minute after door closes
- Counter prevents false entry/exit detection
- Coordinates with stairs lighting

**Related Automations:**
- ID 1606157753577 - Front Door Opened
- ID 1614033445487 - Front Door Opened Once For More than 20 seconds
- ID 1611931052908 - Front Door Open Indicator
- ID 1615224190495 - Front Door Closed For More than 20 seconds
- ID 1611931640441 - Front Door Closed
- ID 1606157835544 - Front Door Closed And Start Timer

---

### Light Timeout & Safety Shutdown

**Trigger:** Porch light on for extended period with door closed

**Logic:**

- **Light On And Door Is Shut - ID: 1708895092115:**
  - Trigger: light.porch on for 5 minutes
  - Conditions:
    - binary_sensor.front_door is "off" (closed)
    - timer.porch_light is NOT "active"
  - Actions:
    - Turn off porch light (2 second transition)
    - Log event
  - Mode: Single
  - Purpose: Energy saving, prevent light left on accidentally

**Safety Features:**
- Only triggers if door closed (not during entry/exit)
- Only triggers if timer not active (not during motion period)
- 5-minute delay prevents premature shutdown
- Gradual 2-second transition

**Related Automations:**
- ID 1708895092115 - Light On And Door Is Shut

---

### Physical Light Switch Control

**Trigger:** Physical wall switch state change

**Logic:**

- **Light Switch - ID: 1700940016581:**
  - Trigger: binary_sensor.porch_main_light_input state change
  - Excludes: unknown/unavailable states
  - Actions:
    - If light is off: Turn on via scene.porch_light_on
    - If light is on: Turn off with 2-second transition
    - Cancel any active light timer
    - Log event
  - Mode: Queued (max 10)
  - Purpose: Manual override control

**Override Features:**
- Works independently of motion automation
- Always cancels timer (manual control priority)
- Toggle behavior (on→off, off→on)
- Smooth transitions (2 seconds)
- Queued mode handles multiple rapid switches

**Related Automations:**
- ID 1700940016581 - Porch: Light Switch

---

## Room Layout & Device Placement

```
                          NORTH (Street Side)
         ╔══════════════════════════════════════════════════╗
         ║                                                  ║
         ║  🏠 HOUSE FRONT WALL                             ║
         ║                                                  ║
         ║  💡 Porch Light (light.porch)                    ║
         ║  ├─ Color capable (RGB + CT)                    ║
         ║  ├─ Dimmable (brightness 0-255)                 ║
         ║  ├─ Main entry lighting                         ║
         ║  └─ Scenes:                                      ║
         ║     ├─ scene.porch_light_on (178 brightness)    ║
         ║     ├─ scene.porch_light_off                     ║
         ║     ├─ scene.porch_green_light (RGB green)      ║
         ║     ├─ scene.porch_red_light (RGB red)          ║
         ║     └─ scene.porch_blue_light (RGB blue)        ║
         ║                                                  ║
         ║  🔔 Ring Doorbell (camera.porch)                 ║
         ║  ├─ Video doorbell camera                       ║
         ║  ├─ Motion detection                            ║
         ║  ├─ Person detection                            ║
         ║  └─ Package detection capability                ║
         ║                                                  ║
         ║  🔒 Nuki Smart Lock (lock.nuki_front_door)       ║
         ║  ├─ Smart door lock                             ║
         ║  └─ Integration with alarm system               ║
         ║                                                  ║
         ║  🚪 Front Door (binary_sensor.front_door)        ║
         ║  ├─ Contact sensor (open/close detection)       ║
         ║  ├─ Entry/exit tracking                         ║
         ║  └─ Counter: counter.front_door_opened_closed   ║
         ║     └─ Tracks rapid open/close patterns         ║
         ║                                                  ║
         ║  🔆 Physical Light Switch                        ║
         ║  └─ binary_sensor.porch_main_light_input        ║
         ║     └─ Manual toggle, cancels timers            ║
         ║                                                  ║
         ╠══════════════════════════════════════════════════╣
         ║                                                  ║
         ║                  PORCH AREA                      ║
         ║                                                  ║
         ║  📏 Motion Sensor                                ║
         ║  └─ binary_sensor.porch_motion_occupancy        ║
         ║     ├─ 2 min delay for ON trigger               ║
         ║     ├─ 1 min delay for OFF trigger              ║
         ║     └─ Entry/exit direction detection           ║
         ║                                                  ║
         ║  🌡️ Environmental Sensing                        ║
         ║  └─ sensor.porch_motion_illuminance             ║
         ║     └─ Threshold: 100 lux (door open trigger)   ║
         ║                                                  ║
         ║  🧭 Entry Direction Sensor (Template)            ║
         ║  └─ sensor.door_entry_direction                 ║
         ║     ├─ States: "entering", "leaving", "unknown" ║
         ║     ├─ Logic: Motion ON → leaving               ║
         ║     │         Motion OFF → entering             ║
         ║     └─ Icon changes based on direction          ║
         ║                                                  ║
         ║  ⏲️ Light Timer                                  ║
         ║  └─ timer.porch_light                           ║
         ║     ├─ Duration: 1 minute                       ║
         ║     ├─ Started: Motion off OR door closed       ║
         ║     ├─ Cancelled: Motion on OR door opened      ║
         ║     └─ Finished: Turns off light                ║
         ║                                                  ║
         ║  🧮 Door Event Counter                           ║
         ║  └─ counter.front_door_opened_closed            ║
         ║     ├─ Increments: Door opens                   ║
         ║     ├─ Resets: Door open/closed > 20 seconds    ║
         ║     └─ Purpose: Detect entry/exit patterns      ║
         ║                                                  ║
         ╚══════════════════════════════════════════════════╝
                          SOUTH (Driveway/Path)

External Integrations:
  🏠 House Alarm: alarm_control_panel.house_alarm
     └─ Triggers security responses

  👥 People Tracking: group.tracked_people
     └─ Enables "door open" notifications when home

  🪜 Stairs Integration: light.stairs
     └─ Turns off stairs when porch door closes (fallback)

  🖥️ Office Notification: light.office_light
     └─ Front door open notification (purple light)
     └─ Scene: scene.front_door_open_notification

  🍳 Kitchen Notification Lights:
     ├─ light.kitchen_cooker_rgb → Blue when door open
     ├─ light.kitchen_table_rgb → Blue when door open
     └─ Scenes:
        ├─ scene.kitchen_cooker_ambient_light_to_blue
        └─ scene.kitchen_table_ambient_light_to_blue

  🪜 Stairs Ambient Notification:
     └─ light.stairs_ambient → Blue when door open

Lighting Behavior:
  Motion Detected:
  ├─ Motion ON for 2 minutes → Light ON (100%)
  ├─ Cancel any active timer
  └─ Light stays on until motion clears

  Motion Cleared:
  ├─ Motion OFF for 1 minute → Start timer
  ├─ Timer runs for 1 minute
  └─ Timer finishes → Light OFF

  Front Door Opens:
  ├─ Check illuminance < 100 lux
  ├─ YES → Light ON (scene brightness)
  ├─ NO → No light action
  ├─ Increment counter
  └─ Delay 2 seconds (camera capture)

  Front Door Closes:
  ├─ Start 1-minute timer
  ├─ Execute notification script (turn off indicators)
  └─ If stairs on → Turn stairs off (fallback)

  Door Open 20+ Seconds:
  └─ Reset counter (not entry/exit pattern)

  Light On 5+ Minutes (Door Closed):
  ├─ Timer not active
  └─ Turn off light (safety)

Entry Direction Detection:
  Motion ON + Door Opens:
  └─ Direction: "leaving" (exiting house)

  Motion OFF + Door Opens:
  └─ Direction: "entering" (arriving at house)
```

---

## Key Automation Workflows

### Arrival Sequence (Entering Home)

```
Person Approaches Porch
   ↓
Motion Detected (porch_motion_occupancy: OFF)
   ↓
2-Minute Motion Confirmation
   ↓
Check Conditions:
├─ Motion stable for 2 minutes?
└─ Motion triggers enabled?
   ↓
All YES → Turn On Porch Light
   ├─ Brightness: 100%
   ├─ Cancel any active timer
   └─ Log: "Motion detected, turning on light"
   ↓
Person Opens Front Door
   ↓
Check Illuminance:
├─ sensor.porch_motion_illuminance < 100 lux?
│  ├─ YES → Turn on porch light (scene)
│  │  └─ Cancel timer
│  └─ NO → Skip (already bright)
   ↓
Increment Door Counter
├─ counter.front_door_opened_closed += 1
└─ Purpose: Track entry pattern
   ↓
Delay 2 Seconds
└─ Allow camera to capture person
   ↓
If Tracked People Home:
└─ Execute Front Door Open Notification
   ├─ Office light → Purple
   ├─ Kitchen cooker RGB → Blue
   ├─ Kitchen table RGB → Blue
   └─ Stairs ambient → Blue
   ↓
Entry Direction Sensor Updates:
├─ Motion: OFF when door opened
└─ sensor.door_entry_direction: "entering"
```

**Key Points:**
- Motion detection has 2-minute confirmation (prevents false triggers)
- Light turns on during approach if motion confirmed
- Door opening turns on light if dark (< 100 lux)
- Visual notifications in office/kitchen when home
- Entry direction detected based on motion timing

---

### Departure Sequence (Leaving Home)

```
Person Walks to Door from Inside
   ↓
Motion Detected on Porch
   ↓
Check Motion State:
└─ binary_sensor.porch_motion_occupancy: ON
   ↓
2-Minute Motion Confirmation
   ↓
Motion Confirmed → Turn On Porch Light
├─ Brightness: 100%
├─ Cancel any active timer
└─ Preparation for exit
   ↓
Person Opens Front Door
   ↓
Check Illuminance:
├─ sensor.porch_motion_illuminance < 100 lux?
│  ├─ YES → Ensure light on (scene)
│  └─ NO → Light already on or bright
   ↓
Increment Door Counter
└─ counter.front_door_opened_closed += 1
   ↓
Entry Direction Sensor Updates:
├─ Motion: ON when door opened
└─ sensor.door_entry_direction: "leaving"
   ↓
Person Exits, Door Closes
   ↓
Front Door Closed Actions (Parallel):
   ↓
┌─────────────────────────────────────────────────┐
│ Action 1: Start Light Timer                    │
│ ├─ timer.porch_light starts (1 minute)         │
│ └─ Log: "Front door closed. Starting timer."   │
├─────────────────────────────────────────────────┤
│ Action 2: Turn Off Notification Lights         │
│ └─ script.front_door_closed_notification       │
│    ├─ Stairs ambient → OFF                     │
│    ├─ Kitchen cooker RGB → OFF                 │
│    ├─ Kitchen table RGB → OFF                  │
│    └─ Office light → OFF                       │
├─────────────────────────────────────────────────┤
│ Action 3: Stairs Fallback (if on)              │
│ └─ If light.stairs is on:                      │
│    └─ Turn off stairs light                    │
│       └─ scene.stairs_light_off                │
└─────────────────────────────────────────────────┘
   ↓
Wait for Motion to Clear
   ↓
Motion Clears for 1 Minute
   ↓
(Timer already running from door close)
   ↓
Timer Finishes (1 minute elapsed)
   ↓
Turn Off Porch Light
└─ Log: "Timer finished. Turning light off."
   ↓
Door Open 20+ Seconds Check:
├─ If door was open > 20 seconds (single action)
└─ Reset counter to 0
```

**Key Points:**
- Motion ON before door opens = leaving
- Light stays on during exit
- Door close starts 1-minute timer
- Notification lights turn off
- Stairs light turns off (fallback)
- Total light-on time: ~2 minutes after departure

---

### Entry/Exit Pattern Detection

```
Front Door Event Counter Logic:

Initial State:
└─ counter.front_door_opened_closed = 0

Scenario 1: Taking Out Trash (Single Door Open)
   ↓
Door Opens:
├─ Counter: 0 → 1
└─ Wait...
   ↓
Door Stays Open 20+ Seconds:
├─ Trigger: "Front Door Opened Once For More than 20 seconds"
├─ Condition: Counter < 2 (YES, counter = 1)
└─ Action: Reset counter to 0
   ↓
Door Closes:
├─ Start light timer
└─ After 20+ seconds: Reset counter (already 0)

Result: Single open event detected, not entry/exit

---

Scenario 2: Quick Entry/Exit (Grabbing Package)
   ↓
Door Opens (First Time):
├─ Counter: 0 → 1
└─ Delay 2 seconds (camera)
   ↓
Door Closes (Within 20 Seconds):
├─ Counter still: 1
├─ Start light timer
└─ No reset yet (< 20 seconds)
   ↓
Door Opens Again (Second Time):
├─ Counter: 1 → 2
└─ Quick pattern detected
   ↓
Door Closes Final:
└─ After 20+ seconds: Reset counter to 0

Result: Entry/exit pattern tracked via counter

---

Scenario 3: Normal Entry
   ↓
Door Opens:
├─ Counter: 0 → 1
└─ Person enters
   ↓
Door Closes:
├─ Start light timer
└─ Counter still: 1
   ↓
20 Seconds Elapse:
├─ Trigger: "Front Door Closed For More than 20 seconds"
└─ Action: Reset counter to 0

Result: Normal single entry, counter reset
```

**Purpose:**
- Counter < 2 with 20+ second open = single action
- Counter ≥ 2 = multiple open/close events
- Reset after 20 seconds closed = pattern complete
- Used for detecting rapid entry/exit vs single use

---

### Motion-Based Lighting Control

```
Motion Detected on Porch
   ↓
binary_sensor.porch_motion_occupancy: "on"
   ↓
Wait for Stability (2 Minutes)
   ↓
2 Minutes Elapsed, Motion Still ON
   ↓
Trigger: Motion ON (ID: motion_on)
   ↓
Actions (Parallel):
   ↓
┌─────────────────────────────────────────────────┐
│ Action 1: Turn On Light                        │
│ ├─ Target: light.porch                         │
│ ├─ Brightness: 100%                            │
│ └─ Immediate activation                        │
├─────────────────────────────────────────────────┤
│ Action 2: Cancel Timer                         │
│ └─ timer.porch_light → cancelled               │
│    └─ Prevents light turning off during motion│
└─────────────────────────────────────────────────┘
   ↓
Light Stays On While Motion Continues
   ↓
Person Leaves Porch Area
   ↓
binary_sensor.porch_motion_occupancy: "off"
   ↓
Wait for Stability (1 Minute)
   ↓
1 Minute Elapsed, Motion Still OFF
   ↓
Trigger: Motion OFF (ID: motion_off)
   ↓
Actions (Parallel):
   ↓
┌─────────────────────────────────────────────────┐
│ Action 1: Log Event                            │
│ ├─ Message: "No motion. Starting light timer." │
│ ├─ Title: "Porch"                              │
│ └─ Log Level: "Debug"                          │
├─────────────────────────────────────────────────┤
│ Action 2: Start Timer                          │
│ ├─ Target: timer.porch_light                   │
│ ├─ Duration: 1 minute                          │
│ └─ Countdown begins                            │
└─────────────────────────────────────────────────┘
   ↓
Timer Countdown (1 Minute)
   ↓
Timer Finished Event
   ↓
Trigger: timer.finished (timer.porch_light)
   ↓
Actions (Parallel):
   ↓
┌─────────────────────────────────────────────────┐
│ Action 1: Log Event                            │
│ ├─ Message: "Timer finished. Turning light off"│
│ └─ Title: "Porch"                              │
├─────────────────────────────────────────────────┤
│ Action 2: Turn Off Light                       │
│ └─ Target: light.porch                         │
│    └─ State: OFF                               │
└─────────────────────────────────────────────────┘
```

**Timing Summary:**
- Motion ON → Wait 2 minutes → Light ON
- Motion OFF → Wait 1 minute → Start timer (1 minute)
- Total time from motion cleared to light off: 2 minutes
- New motion during timer → Cancel timer, keep light on

**Safety Features:**
- Long motion confirmation (2 min) prevents false triggers
- Extended light timeout (2 min total) ensures safe exit
- Timer cancellation on new motion prevents darkness
- Single mode prevents overlapping triggers

---

### Manual Light Switch Override

```
Physical Wall Switch Pressed
   ↓
binary_sensor.porch_main_light_input: State Change
   ↓
Filter Invalid States:
├─ Exclude: "unknown"
├─ Exclude: "unavailable"
└─ Valid state change → Continue
   ↓
Check Current Light State:
└─ light.porch current state?
   ↓
┌─────────────────────────────────────────────────┐
│ Branch 1: Light Currently OFF                  │
│ └─ Action: Turn ON via scene                   │
│    ├─ scene.porch_light_on                     │
│    ├─ Brightness: 178                          │
│    └─ Color temp: 285 mireds (warm white)      │
├─────────────────────────────────────────────────┤
│ Branch 2: Light Currently ON                   │
│ └─ Action: Turn OFF                            │
│    ├─ Target: light.porch                      │
│    └─ Transition: 2 seconds (smooth)           │
└─────────────────────────────────────────────────┘
   ↓
Cancel Active Timer (Always):
├─ Target: timer.porch_light
└─ Purpose: Manual control overrides automation
   ↓
Log Event:
├─ Title: "Porch"
└─ Message: "Light switch changed"
```

**Override Features:**
- Works regardless of motion state
- Works regardless of door state
- Always cancels timer (manual priority)
- Toggle behavior (ON↔OFF)
- Smooth 2-second transition on OFF
- Queued mode (max 10) handles rapid toggles

**Coexistence with Automation:**
- Manual ON → Stays on until manual OFF or 5-min safety timeout
- Motion can still trigger while manually controlled
- Timer always cancelled on manual action
- No conflicts between manual and automatic control

---

### Light Safety Timeout (5 Minutes)

```
Porch Light Turns ON
   ↓
Start Monitoring (5-Minute Window)
   ↓
5 Minutes Elapsed
   ↓
Trigger: light.porch ON for 5 minutes
   ↓
Check Safety Conditions:
   ↓
┌─────────────────────────────────────────────────┐
│ Condition 1: Front Door Closed                 │
│ └─ binary_sensor.front_door: "off"             │
│    ├─ YES → Safe to turn off (not in use)     │
│    └─ NO → Skip (door open, light needed)     │
├─────────────────────────────────────────────────┤
│ Condition 2: Timer Not Active                  │
│ └─ timer.porch_light: NOT "active"             │
│    ├─ YES → Not in motion timeout period       │
│    └─ NO → Skip (motion automation handling)   │
└─────────────────────────────────────────────────┘
   ↓
All Conditions Met → Safety Shutdown
   ↓
Actions (Parallel):
   ↓
┌─────────────────────────────────────────────────┐
│ Action 1: Log Event                            │
│ └─ Message: "Light on 5 min and door closed.   │
│              Turning light off."               │
├─────────────────────────────────────────────────┤
│ Action 2: Turn Off Light                       │
│ ├─ Target: light.porch                         │
│ └─ Transition: 2 seconds (smooth)              │
└─────────────────────────────────────────────────┘
```

**Purpose:**
- Prevent light left on accidentally
- Energy saving
- Only triggers when safe (door closed, no active automation)

**Safety Logic:**
- Does NOT turn off if door open (may be in use)
- Does NOT turn off if timer active (motion automation running)
- Only triggers after 5 full minutes (not premature)
- Smooth transition prevents jarring off

---

## Configuration Parameters

### Motion Detection Settings
- **Motion ON Delay:** 2 minutes (binary_sensor.porch_motion_occupancy stable)
  - Prevents false triggers from passing pedestrians
  - Ensures person approaching porch (not just walking by)

- **Motion OFF Delay:** 1 minute (binary_sensor.porch_motion_occupancy cleared)
  - Allows person time to enter/exit
  - Prevents light turning off during door interaction

### Light Timer Settings
- **timer.porch_light Duration:** 1 minute
  - Started when motion clears OR door closes
  - Can be cancelled by new motion or door opening
  - Total light-on time after motion: 2 minutes (1 min clear + 1 min timer)

### Illuminance Thresholds
- **Door Opening Threshold:** 100 lux
  - Below 100 lux → Turn on light when door opens
  - Above 100 lux → Skip light (daylight sufficient)
  - Purpose: Energy saving during bright conditions

### Safety Timeout
- **Light On Duration:** 5 minutes
  - Triggers safety shutdown if door closed and timer not active
  - Prevents accidentally leaving light on
  - Transition: 2 seconds (smooth)

### Counter Settings
- **counter.front_door_opened_closed:**
  - Increments: On door open
  - Resets: Door open/closed > 20 seconds
  - Threshold: < 2 for single action detection
  - Purpose: Entry/exit pattern tracking

### Time Delays
- Door open → Camera capture delay: 2 seconds
- Door open > 20 seconds → Reset counter (single action)
- Door closed > 20 seconds → Reset counter (pattern complete)
- Motion confirmed → Light on: 2 minutes
- Motion cleared → Timer start: 1 minute
- Timer start → Light off: 1 minute
- Light on (safe) → Auto off: 5 minutes

---

## Helper Entities

### Timers
- **timer.porch_light**
  - Duration: 1 minute (configurable via automation)
  - Purpose: Delayed light shutdown after motion/door close
  - Started by: Motion OFF trigger, door close
  - Cancelled by: Motion ON trigger, door open, manual switch
  - Finished event: Triggers light shutdown

### Counters
- **counter.front_door_opened_closed**
  - Initial value: 0
  - Step: 1 (increments)
  - Increments when: Door opens
  - Resets when: Door open/closed > 20 seconds
  - Purpose: Track door usage patterns (entry/exit vs single action)
  - Used by: "Front Door Opened Once For More than 20 seconds" automation

### Template Sensors
- **sensor.door_entry_direction (Template Trigger Sensor)**
  - Unique ID: 97c1df2b-dcde-4aba-884c-acfc59c140aa
  - States:
    - "leaving" - Motion ON when door opens (exiting)
    - "entering" - Motion OFF when door opens (arriving)
    - "unknown" - Indeterminate state
  - Icon (dynamic):
    - mdi:location-exit - When leaving
    - mdi:location-enter - When entering
    - mdi:alert-circle-outline - When unknown
  - Trigger: binary_sensor.front_door state change
  - Purpose: Visual indication of entry/exit direction
  - Logic: Based on porch motion at moment of door opening

---

## Scripts

### Door Notification Scripts

**script.front_door_open_notification**
- **Alias:** "Front Door Open Notification"
- **Icon:** mdi:door-open
- **Purpose:** Visual notification when front door opens and someone home
- **Sequence:**
  1. Create snapshot of current office light state
     - Scene ID: current_office_light_1
     - Snapshot: light.office_light
  2. Activate notification scenes:
     - scene.front_door_open_notification (Office purple)
     - scene.kitchen_cooker_ambient_light_to_blue
     - scene.kitchen_table_ambient_light_to_blue
- **Mode:** Single
- **Triggered by:** "Front Door Open Indicator" automation (ID: 1611931052908)

**script.front_door_closed_notification**
- **Alias:** "Front Door Closed Notification"
- **Icon:** mdi:door
- **Purpose:** Turn off notification lights when door closes
- **Sequence:**
  - Turn off multiple notification lights:
    - light.stairs_ambient
    - light.kitchen_cooker_rgb
    - light.kitchen_table_rgb
    - light.office_light
- **Mode:** Single
- **Triggered by:** "Front Door Closed" automation (ID: 1611931640441)

### NFC & Alarm Scripts

**script.nfc_front_door**
- **Alias:** "NFC Front Door"
- **Icon:** mdi:nfc
- **Purpose:** NFC tag action at front door (alarm disarm)
- **Sequence:**
  - Check if alarm is armed (not "disarmed"):
    - If armed:
      - Log: "Turning off alarm"
      - Execute: script.set_alarm_to_disarmed_mode
      - Flash living room lights green (success)
    - If already disarmed:
      - Log: "Alarm is not on so nothing to do"
      - Flash living room lights red (already off)
- **Mode:** Single
- **Use Case:** NFC tag on door frame for easy alarm disarm

### Porch Override Scripts

**script.porch_override_notification**
- **Alias:** "Porch Override Notification"
- **Purpose:** Visual feedback notification (flash blue/white)
- **Sequence:**
  - Repeat 2 times:
    - Turn light blue (255 brightness, blue color)
    - Turn light white (178 brightness, white color)
  - Restore to normal: scene.porch_light_on
- **Mode:** Single
- **Use Case:** Manual notification or confirmation

**script.stop_lock_status_light**
- **Alias:** "Stop Lock Status Light"
- **Icon:** mdi:lock-off
- **Purpose:** Stop lock status display and turn off light
- **Sequence:**
  1. Turn off script.front_door_lock_status (if running)
  2. Turn off light.porch
- **Mode:** Single
- **Use Case:** Cancel lock status indication

---

## Sensors

### Binary Sensors

**binary_sensor.porch_motion_occupancy**
- **Platform:** Motion sensor (likely Ring or Zigbee)
- **Type:** Occupancy detection
- **Purpose:** Primary motion detection for porch area
- **Used in:**
  - Motion lighting automation (2-min ON delay, 1-min OFF delay)
  - Entry direction detection (template sensor)
- **Triggers:**
  - Light ON when motion detected for 2 minutes
  - Timer start when motion cleared for 1 minute

**binary_sensor.front_door**
- **Platform:** Contact sensor
- **Type:** Door open/close detection
- **Purpose:** Front door state monitoring
- **States:**
  - "on" - Door open
  - "off" - Door closed
- **Used in:**
  - 6 door-related automations
  - Entry/exit tracking
  - Light control (turn on if dark)
  - Notification triggers
  - Safety timeout conditions

**binary_sensor.porch_main_light_input**
- **Platform:** Physical switch input
- **Type:** Wall switch state
- **Purpose:** Manual light control
- **Used in:**
  - Light Switch automation (ID: 1700940016581)
  - Toggle behavior (ON↔OFF)
  - Timer cancellation

### Numeric Sensors

**sensor.porch_motion_illuminance**
- **Platform:** Integrated with motion sensor
- **Type:** Light level sensor
- **Unit:** Lux
- **Purpose:** Ambient light measurement
- **Threshold:** 100 lux (for door open lighting trigger)
- **Used in:**
  - "Front Door Opened" automation
  - Determines if porch light needed when door opens
- **Logic:**
  - < 100 lux → Dark, turn on light
  - ≥ 100 lux → Bright enough, skip light

### Template Sensors

**sensor.door_entry_direction**
- **Platform:** Template trigger sensor
- **Unique ID:** 97c1df2b-dcde-4aba-884c-acfc59c140aa
- **Trigger:** binary_sensor.front_door state change
- **States:**
  - "leaving" - Motion detected ON when door opens
  - "entering" - Motion detected OFF when door opens
  - "unknown" - Indeterminate or error state
- **Icon (dynamic):**
  - mdi:location-exit (leaving)
  - mdi:location-enter (entering)
  - mdi:alert-circle-outline (unknown)
- **Purpose:** Visual direction indication on dashboard
- **Logic:**
  ```yaml
  State: Motion ON → "leaving", Motion OFF → "entering"
  Icon: Based on current state
  ```
- **Use Cases:**
  - Dashboard display
  - Entry/exit tracking
  - Future automation potential (welcome vs goodbye messages)

---

## Status Indicators

### Light Scenes

**Main Porch Light Scenes:**

**scene.porch_light_on (ID: 1606157646144)**
- **Name:** "Porch Light On"
- **State:** ON
- **Brightness:** 178 (70% of max)
- **Color Temperature:** 285 mireds (warm white, ~3509K)
- **Min Color Temp:** 111 mireds (9009K, cool white)
- **Max Color Temp:** 400 mireds (2500K, warm white)
- **Effects Available:**
  - effect_colorloop
  - effect_pulse
  - effect_stop
- **Supported Features:** 55 (color temp, brightness, effects)
- **Purpose:** Standard porch lighting (entry/exit, motion, manual)

**scene.porch_light_off (ID: 1606157607021)**
- **Name:** "Porch Lights Off"
- **State:** OFF
- **Purpose:** Complete light shutdown

**Color Status Scenes:**

**scene.porch_green_light (ID: 1696367037290)**
- **Name:** "Porch Green Light"
- **State:** ON
- **Brightness:** 255 (100%)
- **Color Mode:** XY
- **Hue:** 127.895° (green)
- **Saturation:** 89.412%
- **RGB:** (27, 255, 57)
- **XY Color:** (0.176, 0.707)
- **Effects Available:** blink, breathe, okay, channel_change, candle, fireplace, colorloop
- **Purpose:** Status indicator (success, alarm disarmed, etc.)
- **Use Case:** NFC alarm disarm confirmation

**scene.porch_red_light (ID: 1701031703306)**
- **Name:** "Porch Red Light"
- **State:** ON
- **Brightness:** 255 (100%)
- **Color Mode:** XY
- **Hue:** 358.745° (red)
- **Saturation:** 93.725%
- **RGB:** (255, 16, 21)
- **XY Color:** (0.695, 0.299)
- **Purpose:** Status indicator (error, alarm already off, alert)
- **Use Case:** NFC alarm already disarmed notification

**scene.porch_blue_light (ID: 1701032346965)**
- **Name:** "Porch Blue Light"
- **State:** ON
- **Brightness:** 255 (100%)
- **Color Mode:** XY
- **Hue:** 242.683° (blue)
- **Saturation:** 96.471%
- **RGB:** (20, 9, 255)
- **XY Color:** (0.137, 0.041)
- **Purpose:** Status indicator (information, notification)

### Notification Scenes (External Lights)

**scene.front_door_open_notification (ID: 1611931150080)**
- **Name:** "Front Door Open Notification"
- **Purpose:** Multi-room visual notification when door opens (people home)
- **Included Lights:**
  1. **light.office_light**
     - Brightness: 255 (100%)
     - Color: Purple (Hue: 254.997°, Sat: 100%)
     - RGB: (63, 0, 255)
     - XY: (0.157, 0.05)
  2. **light.stairs_ambient**
     - Brightness: 255 (100%)
     - Color: Blue (Hue: 237.073°, Sat: 96.471%)
     - RGB: (9, 21, 255)
     - XY: (0.136, 0.042)
- **Triggered by:** script.front_door_open_notification
- **Use Case:** Visual alert when door opens and someone home

**Kitchen Notification Scenes:**
- **scene.kitchen_cooker_ambient_light_to_blue**
  - Target: light.kitchen_cooker_rgb → Blue
- **scene.kitchen_table_ambient_light_to_blue**
  - Target: light.kitchen_table_rgb → Blue

---

## Key Features

✅ **Consolidated Motion Detection** - Single automation handles both motion ON and OFF with appropriate delays
✅ **Entry/Exit Direction Detection** - Template sensor determines direction based on motion timing
✅ **Smart Illuminance Awareness** - Only turns on light when dark (< 100 lux threshold)
✅ **Multi-Room Notification System** - Office, kitchen, and stairs lights indicate door state
✅ **Door Event Pattern Tracking** - Counter distinguishes single actions from entry/exit patterns
✅ **Dual Light Triggers** - Motion (2-min delay) AND door open (if dark) both trigger lighting
✅ **Extended Exit Lighting** - 2-minute total light-on time after motion clears (safe exit)
✅ **Manual Override Control** - Physical switch with timer cancellation and toggle behavior
✅ **Safety Timeout** - Automatic shutdown after 5 minutes if door closed and no automation active
✅ **Color Status Indication** - RGB scenes for visual feedback (green/red/blue)
✅ **NFC Tag Integration** - Front door NFC for alarm control with visual feedback
✅ **Smart Lock Integration** - Nuki lock with status indication capability
✅ **Camera Capture Timing** - 2-second delay after door opens for Ring snapshot
✅ **Stairs Coordination** - Automatically turns off stairs light when porch door closes
✅ **Timer Management** - Sophisticated timer cancellation on motion or door events
✅ **Event Logging** - Comprehensive debug logging for all automation actions
✅ **Queued Switch Handling** - Handles rapid switch toggles (max 10 queued)
✅ **Smooth Transitions** - 2-second transitions on manual/safety light shutdowns
✅ **People Awareness** - Only shows notifications when tracked people home
✅ **Parallel Action Execution** - Efficient simultaneous execution of related actions
✅ **Scene-Based Control** - Consistent lighting via predefined scenes

---

## File Structure

```
packages/rooms/
├── porch.yaml                      # Main porch configuration (647 lines)
│   ├── Automations (11 total)
│   │   ├── Motion Detection (2)
│   │   │   ├── ID 1737283018710 - Motion Detected (On/Off)
│   │   │   └── ID 1737283018709 - Light Timer Finished
│   │   ├── Front Door Management (6)
│   │   │   ├── ID 1606157753577 - Front Door Opened
│   │   │   ├── ID 1614033445487 - Front Door Opened Once > 20s
│   │   │   ├── ID 1611931052908 - Front Door Open Indicator
│   │   │   ├── ID 1615224190495 - Front Door Closed > 20s
│   │   │   ├── ID 1611931640441 - Front Door Closed
│   │   │   └── ID 1606157835544 - Front Door Closed And Start Timer
│   │   ├── Light Safety (1)
│   │   │   └── ID 1708895092115 - Light On And Door Is Shut
│   │   └── Physical Control (1)
│   │       └── ID 1700940016581 - Light Switch
│   │
│   ├── Scenes (9 total)
│   │   ├── Porch Light Scenes (4)
│   │   │   ├── scene.porch_light_off
│   │   │   ├── scene.porch_light_on (warm white, 178 brightness)
│   │   │   ├── scene.porch_green_light (RGB green status)
│   │   │   ├── scene.porch_red_light (RGB red status)
│   │   │   └── scene.porch_blue_light (RGB blue status)
│   │   └── Notification Scenes (4)
│   │       ├── scene.front_door_open_notification (office + stairs)
│   │       └── Kitchen scenes (cooker + table blue)
│   │
│   ├── Scripts (4 total)
│   │   ├── script.front_door_closed_notification
│   │   ├── script.front_door_open_notification
│   │   ├── script.nfc_front_door
│   │   ├── script.porch_override_notification
│   │   └── script.stop_lock_status_light
│   │
│   └── Template Sensors (1 total)
│       └── sensor.door_entry_direction (entering/leaving detection)
│
└── PORCH-SETUP.md                  # This file - Room documentation

External Dependencies (referenced but defined elsewhere):
├── Timers: timer.porch_light
├── Counters: counter.front_door_opened_closed
├── Groups: group.tracked_people
├── Alarm: alarm_control_panel.house_alarm
├── Lock: lock.nuki_front_door
├── Camera: camera.porch (Ring doorbell)
├── Global Scripts:
│   ├── script.send_to_home_log
│   ├── script.set_alarm_to_disarmed_mode
│   └── script.living_room_flash_lounge_lights_* (green/red)
└── External Lights:
    ├── light.office_light
    ├── light.stairs
    ├── light.stairs_ambient
    ├── light.kitchen_cooker_rgb
    └── light.kitchen_table_rgb
```

---

## Automation Summary by Category

### Motion Detection & Lighting (2 automations)
- **ID 1737283018710** - Motion Detected (On/Off) - Consolidated motion handling with 2-min ON, 1-min OFF delays
- **ID 1737283018709** - Light Timer Finished - Turns off light when 1-minute timer expires

### Front Door Management (6 automations)
- **ID 1606157753577** - Front Door Opened - Light control (if dark), counter increment, camera delay
- **ID 1614033445487** - Front Door Opened Once For More than 20 seconds - Single action detection, reset counter
- **ID 1611931052908** - Front Door Open Indicator - Multi-room notification when people home
- **ID 1615224190495** - Front Door Closed For More than 20 seconds - Reset counter after closure
- **ID 1611931640441** - Front Door Closed - Execute close notification script
- **ID 1606157835544** - Front Door Closed And Start Timer - Start light timer, stairs fallback

### Light Safety & Timeout (1 automation)
- **ID 1708895092115** - Light On And Door Is Shut - 5-minute safety timeout (door closed, timer not active)

### Physical Control (1 automation)
- **ID 1700940016581** - Light Switch - Manual toggle with timer cancellation

### Template Sensors (1 sensor)
- **sensor.door_entry_direction** - Entry/exit direction based on motion timing

**Total Automation Count:** 11 automations
**Total Scene Count:** 9 scenes (4 porch light + 5 notification)
**Total Script Count:** 5 scripts (4 porch-specific + references to global)
**Total Sensor Count:** 4 sensors (motion occupancy, illuminance, door contact, direction template)
**Total Helper Count:** 2 (timer, counter)

---

## Advanced Features Explained

### Entry/Exit Direction Detection Logic

The porch implements a sophisticated direction detection system using motion timing:

**Principle:**
- Motion detected BEFORE door opens → Person leaving (inside → outside)
- No motion detected when door opens → Person entering (outside → inside)

**Implementation:**
```yaml
Template Trigger Sensor: sensor.door_entry_direction
Trigger: binary_sensor.front_door state change
Logic:
  State Calculation:
    IF binary_sensor.porch_motion_occupancy == 'on':
      RETURN "leaving"
    ELIF binary_sensor.porch_motion_occupancy == 'off':
      RETURN "entering"
    ELSE:
      RETURN "unknown"

  Icon Calculation:
    IF state == "leaving":
      RETURN "mdi:location-exit"
    ELIF state == "entering":
      RETURN "mdi:location-enter"
    ELSE:
      RETURN "mdi:alert-circle-outline"
```

**Scenarios:**

**Scenario 1: Leaving Home**
```
1. Person walks to door from inside
2. Porch motion sensor detects motion: ON
3. Wait 2 minutes (motion confirmation)
4. Person opens door (motion still: ON)
5. sensor.door_entry_direction updates: "leaving"
6. Icon: mdi:location-exit
7. Use cases:
   - Goodbye message automation
   - Arm alarm automation
   - Turn off interior lights
```

**Scenario 2: Arriving Home**
```
1. Person approaches from outside (no porch motion yet)
2. Porch motion sensor: OFF (inside sensor, outside approach)
3. Person opens door (motion still: OFF)
4. sensor.door_entry_direction updates: "entering"
5. Icon: mdi:location-enter
6. Motion then detects after door opens
7. Use cases:
   - Welcome message automation
   - Disarm alarm reminder
   - Turn on interior lights
```

**Benefits:**
- No additional sensors required
- Uses existing motion + door sensors
- Instant direction determination
- Visual dashboard indication
- Foundation for welcome/goodbye automations

---

### Door Event Counter Pattern Detection

The counter system differentiates between single door actions and entry/exit patterns:

**Counter Lifecycle:**

```
Initial State: counter.front_door_opened_closed = 0

Event 1: Door Opens
├─ Counter: 0 → 1
├─ Delay: 2 seconds (camera capture)
└─ Start 20-second timer (implicit)

Decision Point A (20 seconds elapsed):
├─ Door STILL open?
│  ├─ YES → Single action (taking out trash, letting cat out)
│  │  └─ Action: Reset counter to 0
│  │     └─ Automation: "Front Door Opened Once For More than 20 seconds"
│  └─ NO → Door closed, continue to Decision Point B

Decision Point B (Door closes):
├─ Start light timer (1 minute)
├─ Start 20-second timer (implicit)
└─ Counter still: 1

Decision Point C (20 seconds after close):
├─ Door STILL closed?
│  └─ YES → Normal entry/exit complete
│     └─ Action: Reset counter to 0
│        └─ Automation: "Front Door Closed For More than 20 seconds"

Event 2: Door Opens Again (within 20 seconds of close)
├─ Counter: 1 → 2
├─ Pattern detected: Quick entry/exit (grabbing package, brief exit)
└─ Continue tracking...
```

**Pattern Examples:**

**Pattern A: Taking Out Trash**
```
Time 0:00 - Door opens (counter = 1)
Time 0:02 - Person steps outside
Time 0:25 - Door still open (> 20 seconds)
         → TRIGGER: Reset counter to 0
         → REASON: Single prolonged action, not entry/exit
Time 1:30 - Door closes
Time 1:50 - Counter reset confirmed (> 20 seconds closed)
```

**Pattern B: Quick Package Grab**
```
Time 0:00 - Door opens (counter = 1)
Time 0:02 - Person exits
Time 0:10 - Door closes (< 20 seconds, counter still 1)
Time 0:15 - Door opens again (counter = 2)
         → Pattern: Multiple actions detected
Time 0:25 - Door closes
Time 0:45 - Counter reset (> 20 seconds closed)
```

**Pattern C: Normal Entry**
```
Time 0:00 - Door opens (counter = 1)
Time 0:03 - Person enters
Time 0:05 - Door closes (< 20 seconds)
Time 0:25 - Counter reset (> 20 seconds closed)
         → Normal single entry pattern
```

**Purpose:**
- Distinguish prolonged single actions (trash, letting pet out)
- Detect rapid entry/exit patterns (forgot something, package grab)
- Future automation potential (different responses based on pattern)
- Prevent false triggers for single-action events

---

### Multi-Room Notification System

When the front door opens and people are home, a visual notification system activates:

**Notification Flow:**

```
Front Door Opens
   ↓
Check: group.tracked_people == "home"?
├─ NO → Skip notification (no one home to notify)
└─ YES → Execute Notification
   ↓
script.front_door_open_notification executes:
   ↓
Step 1: Preserve Current State
├─ Create scene snapshot: "current_office_light_1"
├─ Snapshot entity: light.office_light
└─ Purpose: Restore original state later (future enhancement)
   ↓
Step 2: Activate Notification Scenes (Parallel)
   ↓
┌─────────────────────────────────────────────────┐
│ Scene 1: Front Door Open Notification          │
│ ├─ light.office_light                          │
│ │  ├─ Brightness: 255 (100%)                   │
│ │  ├─ Color: Purple (Hue 254.997°)             │
│ │  └─ RGB: (63, 0, 255)                        │
│ ├─ light.stairs_ambient                        │
│ │  ├─ Brightness: 255 (100%)                   │
│ │  ├─ Color: Blue (Hue 237.073°)               │
│ │  └─ RGB: (9, 21, 255)                        │
├─────────────────────────────────────────────────┤
│ Scene 2: Kitchen Cooker Ambient Light To Blue  │
│ └─ light.kitchen_cooker_rgb → Blue             │
├─────────────────────────────────────────────────┤
│ Scene 3: Kitchen Table Ambient Light To Blue   │
│ └─ light.kitchen_table_rgb → Blue              │
└─────────────────────────────────────────────────┘
   ↓
Notification Active (Visual Indication)
   ↓
Front Door Closes
   ↓
script.front_door_closed_notification executes:
   ↓
Turn Off All Notification Lights:
├─ light.stairs_ambient → OFF
├─ light.kitchen_cooker_rgb → OFF
├─ light.kitchen_table_rgb → OFF
└─ light.office_light → OFF
```

**Notification Color Meanings:**

```
Office Light: PURPLE (RGB: 63, 0, 255)
└─ Meaning: Door state change
└─ Location: Upstairs office
└─ Purpose: Alert while working

Stairs Ambient: BLUE (RGB: 9, 21, 255)
└─ Meaning: Door open
└─ Location: Stairway landing
└─ Purpose: Visible from multiple rooms

Kitchen Lights: BLUE
├─ Cooker RGB
└─ Table RGB
└─ Meaning: Door open
└─ Location: Kitchen area
└─ Purpose: Alert while cooking/eating
```

**Benefits:**
- No audible notifications needed
- Visual indication in multiple rooms
- Non-intrusive (color change only)
- Automatic cleanup on door close
- People-aware (only when home)
- Room-specific positioning (office, kitchen, stairs)

**Future Enhancements:**
- Restore scene from snapshot (currently just turns off)
- Different colors for entry vs exit
- Timeout for prolonged door open (escalation)
- Integration with alarm state (different color if armed)

---

### NFC Tag Alarm Control Integration

Front door NFC tag provides quick alarm disarm with visual feedback:

**NFC Tag Workflow:**

```
NFC Tag Scanned at Front Door
   ↓
Trigger: script.nfc_front_door
   ↓
Check Alarm State:
└─ alarm_control_panel.house_alarm state?
   ↓
┌─────────────────────────────────────────────────┐
│ Scenario 1: Alarm Armed (any armed state)      │
│ ├─ Condition: State NOT "disarmed"             │
│ └─ Actions:                                     │
│    ├─ Log: "Turning off alarm"                 │
│    │  └─ Title: "Alarm", Level: "Debug"        │
│    ├─ Execute: script.set_alarm_to_disarmed_   │
│    │           mode                             │
│    └─ Execute: script.living_room_flash_       │
│    │           lounge_lights_green              │
│       └─ Visual feedback: GREEN (success)      │
├─────────────────────────────────────────────────┤
│ Scenario 2: Alarm Already Disarmed             │
│ ├─ Condition: State == "disarmed"              │
│ └─ Actions:                                     │
│    ├─ Log: "Alarm is not on so nothing to do" │
│    │  └─ Title: "Alarm", Level: "Debug"        │
│    └─ Execute: script.living_room_flash_       │
│               lounge_lights_red                 │
│       └─ Visual feedback: RED (already off)    │
└─────────────────────────────────────────────────┘
```

**Visual Feedback Colors:**

```
GREEN Flash (Alarm Was Armed):
├─ Meaning: Alarm successfully disarmed
├─ Location: Living room lounge lights
├─ Pattern: Flash green (script-defined)
└─ Use Case: Confirmation entering home

RED Flash (Alarm Already Off):
├─ Meaning: Alarm already disarmed, no action needed
├─ Location: Living room lounge lights
├─ Pattern: Flash red (script-defined)
└─ Use Case: Prevent confusion, show tag detected
```

**Benefits:**
- Quick alarm disarm (no phone needed)
- Visual confirmation (green/red feedback)
- Works from outside door (NFC on frame)
- Prevents double-disarm attempts (red feedback)
- Logging for audit trail
- Integration with existing alarm system

**Typical Usage:**
1. Arrive home with bags
2. Tap phone/NFC tag to door frame
3. Alarm disarms automatically
4. Green flash confirms success
5. Open door and enter
6. No need to find phone or keypad

---

### Lock Status Indication System

Porch light can display smart lock status visually:

**script.stop_lock_status_light:**

```
Purpose: Cancel lock status display mode

Sequence:
├─ Step 1: Stop Status Script
│  └─ script.turn_off
│     └─ Target: script.front_door_lock_status
│        └─ Stops any running lock status animation
├─ Step 2: Turn Off Light
│  └─ light.turn_off
│     └─ Target: light.porch
│        └─ Returns to normal lighting mode
```

**Use Cases:**

```
Lock Status Indication (Implied from stop script):
├─ script.front_door_lock_status (running)
├─ Porch light shows lock state via color/pattern
└─ Stop script cancels indication and turns off light

Potential Status Colors:
├─ Green: Locked (secure)
├─ Red: Unlocked (warning)
├─ Blue: Locking/unlocking in progress
└─ Flash: State change

Integration Points:
└─ lock.nuki_front_door state changes
   ├─ locked → Green indication
   ├─ unlocked → Red indication
   └─ locking/unlocking → Blue flash
```

**Benefits:**
- Visual lock status from outside
- No need to check phone
- Security awareness (red if unlocked)
- Nuki smart lock integration
- Cancellable indication (stop script)

---

### Porch Override Notification Flash

Visual notification/confirmation via light color flash:

**script.porch_override_notification:**

```
Purpose: Visual feedback for manual actions or confirmations

Sequence:
├─ Repeat: 2 times
│  ├─ Iteration 1:
│  │  ├─ Turn on: Blue (brightness 255)
│  │  └─ Turn on: White (brightness 178)
│  └─ Iteration 2:
│     ├─ Turn on: Blue (brightness 255)
│     └─ Turn on: White (brightness 178)
├─ Final State:
│  └─ scene.porch_light_on (restore normal)
│     ├─ Brightness: 178
│     └─ Color temp: 285 mireds (warm white)
```

**Visual Pattern:**
```
Time 0.0s: Blue (full brightness)
Time 0.5s: White (normal brightness)
Time 1.0s: Blue (full brightness)
Time 1.5s: White (normal brightness)
Time 2.0s: Restore to scene (warm white normal)
```

**Use Cases:**
- Manual override confirmed
- Automation disabled notification
- Special mode activation
- Custom button action feedback
- Integration with external services

**Benefits:**
- Clear visual feedback
- Non-intrusive (no sound)
- Visible from street
- Automatic restoration to normal
- Distinct blue/white flash pattern

---

### Illuminance-Based Smart Lighting

Porch implements intelligent light triggering based on ambient brightness:

**Illuminance Logic:**

```
Front Door Opens
   ↓
Check Ambient Light Level:
└─ sensor.porch_motion_illuminance current value?
   ↓
┌─────────────────────────────────────────────────┐
│ Scenario 1: Dark Conditions (< 100 lux)        │
│ ├─ Current reading: e.g., 35 lux               │
│ ├─ Threshold: 100 lux                          │
│ ├─ Comparison: 35 < 100 (TRUE)                 │
│ └─ Actions:                                     │
│    ├─ Log: "Front door opened it's dark (35    │
│    │        < 100). Turning on light."          │
│    ├─ scene.porch_light_on (activate)          │
│    └─ timer.porch_light (cancel if active)     │
├─────────────────────────────────────────────────┤
│ Scenario 2: Bright Conditions (≥ 100 lux)      │
│ ├─ Current reading: e.g., 450 lux              │
│ ├─ Threshold: 100 lux                          │
│ ├─ Comparison: 450 < 100 (FALSE)               │
│ └─ Actions:                                     │
│    └─ Skip light activation (daylight          │
│       sufficient)                               │
└─────────────────────────────────────────────────┘
```

**Illuminance Threshold: 100 lux**

Reference values:
```
Illuminance Levels:
├─     0-50 lux: Dark / Night (light needed)
├─   50-100 lux: Dim / Twilight (light helpful)
├─  100-300 lux: Overcast day (light optional)
├─  300-500 lux: Office lighting (no light needed)
└─ 500+ lux: Bright daylight (definitely no light)

Threshold: 100 lux
├─ Below: Activate porch light
└─ Above: Skip activation (natural light sufficient)
```

**Benefits:**
- Energy saving (no daytime lighting)
- Smart triggering (only when needed)
- Sensor-based (not just time-based)
- Logged values (debugging/optimization)
- Adjustable threshold (future tuning)

**Example Log Messages:**
```
DEBUG: "Front door opened it's dark (35 < 100). Turning on light."
DEBUG: "Front door opened it's bright (450 > 100). Skipping light."
```

---

### Timer Management & Cancellation Strategy

Sophisticated timer system prevents premature light shutdown:

**Timer Lifecycle:**

```
Timer: timer.porch_light (1 minute duration)

Start Triggers:
├─ Motion OFF for 1 minute (automation ID: 1737283018710)
└─ Front door closes (automation ID: 1606157835544)

Cancel Triggers:
├─ Motion ON detected (automation ID: 1737283018710)
├─ Front door opens (automation ID: 1606157753577)
└─ Physical switch toggle (automation ID: 1700940016581)

Finish Action:
└─ Turn off porch light (automation ID: 1737283018709)
```

**Scenario Analysis:**

**Scenario 1: Normal Motion Timeout**
```
Time 0:00 - Motion detected (2-min confirmation)
Time 2:00 - Light turns ON
Time 3:30 - Motion clears
Time 4:30 - Motion cleared for 1 minute
         → Start timer (1 minute)
Time 5:30 - Timer finishes
         → Turn off light
Total light-on time: 3.5 minutes
```

**Scenario 2: Door Opens During Timer**
```
Time 0:00 - Motion cleared, timer started
Time 0:30 - Front door opens (timer still running)
         → Cancel timer
         → Light stays on (door in use)
Time 1:00 - Door closes
         → Start new timer (1 minute)
Time 2:00 - Timer finishes
         → Turn off light
```

**Scenario 3: New Motion During Timer**
```
Time 0:00 - Motion cleared, timer started (1 min)
Time 0:40 - Motion detected again (before timer finishes)
         → Cancel timer immediately
         → Light stays on
Time 2:40 - Motion confirmed (2 min stability)
         → Ensure light still on (already on)
Time 3:00 - Motion clears
Time 4:00 - Start timer again (1 min)
Time 5:00 - Timer finishes
         → Turn off light
```

**Scenario 4: Manual Switch During Timer**
```
Time 0:00 - Motion cleared, timer started
Time 0:30 - Physical switch pressed
         → Cancel timer (manual control priority)
         → Toggle light (OFF in this case)
Manual control overrides automation
```

**Timer Cancellation Priority:**
1. Manual switch (highest priority)
2. Door opens (safety priority)
3. Motion detected (activity priority)

**Benefits:**
- No premature shutdowns
- Activity-aware (cancels on new motion/door)
- Manual override respected
- Safe exit time guaranteed (1 min + door close)
- Multiple trigger sources (motion + door)

---

### Stairs Coordination Fallback

Porch automations include coordination with stairs lighting:

**Coordination Logic:**

```
Front Door Closes
   ↓
automation ID: 1606157835544 executes
   ↓
Action 3 (Conditional):
└─ Check: light.stairs state?
   ├─ State: "on"
   │  └─ Actions:
   │     ├─ Log: "Front door closed. Turning stairs
   │     │        light off as fall back."
   │     └─ scene.turn_on
   │        └─ Target: scene.stairs_light_off
   │           └─ Turns off stairs light
   └─ State: "off"
      └─ Skip (already off)
```

**Why This Coordination?**

```
Problem Scenario (Without Coordination):
1. Person opens front door
2. Stairs light turns on (stairs automation)
3. Person exits via porch
4. Front door closes
5. Porch light starts timer
6. Stairs light STAYS ON (no one upstairs)
7. Result: Wasted energy, lights left on

Solution (With Coordination):
1. Person opens front door
2. Stairs light turns on (stairs automation)
3. Person exits via porch
4. Front door closes
5. Porch automation checks stairs light
6. Stairs light turned off (fallback)
7. Porch light starts timer
8. Result: Both lights managed, no waste
```

**Coordination Scenarios:**

**Scenario 1: Entry from Porch to Stairs**
```
Front door opens → Porch light on
Person enters → Stairs motion detects
Stairs light turns on → Normal stairs automation
Front door closes → Porch checks stairs (on)
Porch turns off stairs → Fallback triggers
Result: Porch manages both lights during entry
```

**Scenario 2: Exit from Stairs to Porch**
```
Stairs light on (person descending)
Front door opens → Porch light on
Person exits
Front door closes → Porch checks stairs (on)
Porch turns off stairs → Fallback ensures cleanup
Result: Coordinated shutdown
```

**Scenario 3: Stairs Already Off**
```
Front door opens → Porch light on
Person enters (no stairs approach)
Front door closes → Porch checks stairs (off)
Porch skips stairs action → No unnecessary command
Result: No redundant commands
```

**Benefits:**
- Prevents stairs light left on after exit
- Catches edge cases (stairs automation doesn't catch)
- Conditional (only if stairs actually on)
- Logged for debugging
- Energy saving
- Cross-room coordination

**Note:**
- This is a "fallback" safety mechanism
- Primary stairs control via stairs.yaml automations
- Porch acts as backup coordinator for exit scenarios

---

**Last Updated:** 2026-01-24
**Documentation Version:** 1.0
**Automation Count:** 11
**Device Count:** 10+ entities
**Scene Count:** 9
**Script Count:** 5
**Configuration Files:** 1 (porch.yaml)
**Special Integrations:** Ring Doorbell, Nuki Smart Lock, Entry Direction Detection, Multi-Room Notifications, NFC Alarm Control, Stairs Coordination
