# Stairs Setup Documentation

**Created:** 2026-01-24
**Room:** Stairs (Connecting Ground Floor and First Floor)
**Focus:** Motion-Activated Multi-Zone Lighting, Time-Based Brightness Control, Safety Lighting, Blind Automation
**Special Features:** Multi-Level Motion Detection, Progressive Lighting, Children's Door Integration, Magic Mirror Control, Person Detection

---

## Device Inventory

| Category | Device | Type | Function |
|----------|--------|------|----------|
| **Motion Detection** | binary_sensor.stairs_motion_occupancy | Occupancy Sensor | Bottom of stairs motion detection (primary) |
| | binary_sensor.upstairs_area_motion | Motion Group | Top of stairs/landing motion detection |
| | binary_sensor.upstairs_motion_occupancy | Occupancy Sensor | Top of stairs motion (fallback if Ring disconnects) |
| | binary_sensor.living_room_area_motion | Motion Group | Living room motion (for Magic Mirror) |
| | sensor.stairs_motion_illuminance | Light Level Sensor | Ambient light measurement for automation triggers |
| **Lighting - Main** | light.stairs | Main Stairway Light | Primary stairwell lighting (color temperature, dimmable) |
| **Lighting - Ambient** | light.stairs_2 | Secondary Ambient Light | Lower stairs ambient/accent lighting (LED strip) |
| | light.stairs_ambient | Landing Ambient Light | Top landing ambient status light (RGB capable) |
| **Environment** | sensor.stairs_motion_illuminance | Illuminance Sensor | Light level detection (threshold: input_number) |
| **Window Covers** | cover.stairs_blinds | Motorized Blind | Stairway window blind |
| **Door Sensors** | binary_sensor.leos_bedroom_door_contact | Contact Sensor | Leo's bedroom door (affects stair lighting) |
| | binary_sensor.ashlees_bedroom_door_contact | Contact Sensor | Ashlee's bedroom door (affects stair lighting) |
| | binary_sensor.childrens_bedroom_doors | Binary Group | Both children's doors combined state |
| | binary_sensor.front_door | Contact Sensor | Front door state (for ambient light timeout) |
| **Switches** | binary_sensor.stairs_light_input_0_input | Physical Light Switch | Manual toggle switch for main stairs light |
| **Entertainment** | switch.magic_mirror_plug | Smart Plug | Magic Mirror display power control |
| **Security** | camera.stairs_high_resolution_channel | Camera | Frigate camera for person detection |
| | binary_sensor.stairs_person_detected | Person Detection | AI person detection from Frigate |
| | alarm_control_panel.house_alarm | Alarm Panel | House alarm state (triggers camera snapshot) |

---

## Automation Functions

### Motion Detection & Multi-Zone Lighting

**Triggers:** Motion sensors at different stair levels (top, bottom, living room)

**Logic:**

- **Motion Detected For Ambient Lights (ID: 1624918278463):**
  - Bottom stairs motion detected (stairs_motion_occupancy)
  - Two time-based scenarios:
    - **After sunrise:** Turn on stairs_2 ambient light at dim level
    - **Between midnight and sunrise:** Turn on stairs_2 at very dim level
  - Requires motion triggers enabled
  - 0.5 second transition for smooth activation
  - Mode: Single (prevents overlapping)

- **Motion Detected Before Kids Bed Time (Dark, Upstairs - ID: 1598726353326):**
  - Triggers: upstairs_area_motion OR upstairs_motion_occupancy
  - Time window: 07:00 - children's bedtime
  - Conditions:
    - Illuminance < threshold (input_number.stairs_light_level_threshold)
    - Motion triggers enabled
    - Main stairs light is off OR very dim (brightness < 5)
  - **Action:** Turn on main stairs light at full brightness (scene.stairs_light_on)
  - Mode: Queued (max 10) for multiple motion events

- **Upstairs Dark, After Bed Time, Motion Detected Before Midnight (ID: 1587595659605):**
  - Triggers: upstairs_area_motion OR upstairs_motion_occupancy (fallback)
  - Time window: After children's bedtime until midnight
  - Conditions:
    - Illuminance < threshold
    - Motion triggers enabled
    - Main light off OR dim (brightness < 5)
  - **Complex Decision Tree:**
    - **"No Children" Mode:** Full brightness (scene.stairs_light_on)
    - **Both children's doors closed + door automations enabled:** Full brightness
    - **Both children's doors open + door automations enabled:** Dim light (scene.stairs_light_dim)
    - **Only Leo's door closed:** Dim light
    - **Only Ashlee's door closed:** Full brightness
  - Mode: Queued (max 10)
  - **Purpose:** Respect children's sleep by dimming when doors open

- **Dark, After Bed Time, Motion Detected After Midnight (ID: 1587595659606):**
  - Triggers: upstairs_area_motion OR upstairs_motion_occupancy
  - Time window: After midnight AND (before sunrise OR before 07:00)
  - Conditions:
    - Illuminance < threshold
    - Motion triggers enabled
    - Main light off OR dim
  - **Smart Decision Logic:**
    - **Bedroom light is on:** Full brightness (someone awake)
    - **Night light enabled:** Ultra-dim red night light (scene.stairs_night_light)
    - **Night light disabled:** Full brightness (safer default)
  - Mode: Single
  - **Safety Feature:** Defaults to full brightness if night mode disabled

**Safety Features:**
- Multiple motion sensors for redundancy (Ring integration + Zigbee fallback)
- Light level threshold prevents triggering in bright conditions
- Can be globally disabled via input_boolean.enable_stairs_motion_triggers
- Night mode prevents full brightness disruption after midnight
- Children's door state integration for appropriate brightness

**Related Automations:**
- ID 1624918278463 - Motion Detected For Ambient Lights
- ID 1598726353326 - Motion Detected Before Kids Bed Time
- ID 1587595659605 - Upstairs Dark, After Bed Time, Before Midnight
- ID 1587595659606 - Dark, After Bed Time, After Midnight

---

### No Motion Detection & Light Timeout

**Triggers:** Motion sensors returning to "off" state for 1 minute

**Logic:**

- **No Motion Detected (Lights Off - ID: 1587595847618):**
  - Three trigger points:
    - Upstairs motion off for 1 minute
    - Bottom stairs motion off for 1 minute (primary)
    - Bottom stairs motion off for 1 minute (fallback)
  - Requires motion triggers enabled
  - **Actions by trigger:**
    - **Upstairs motion off:**
      - Turn off main stairs light (1 second transition)
      - If stairs_2 ambient is on: Turn off after 2 second transition
    - **Bottom motion off (fallback):**
      - Turn off stairs_2 ambient light only (2 second transition)
  - Mode: Queued (max 10)
  - **Progressive Shutdown:** Main light first, then ambient after delay

**Safety Features:**
- 1-minute timeout prevents lights turning off too quickly
- Separate timeouts for top and bottom lights
- Gradual transitions (1-2 seconds) for smooth shutdown
- Can be disabled globally

**Related Automations:**
- ID 1587595847618 - No Motion Detected (Lights Off)

---

### Magic Mirror Control

**Triggers:** Motion detection in living room or stairs area, scheduled time, no motion timeout

**Logic:**

- **Magic Mirror Control (Motion/Night - ID: 1592062695452):**
  - Four trigger scenarios:
    - Living room motion detected
    - Stairs motion detected
    - Stairs motion cleared for 3 minutes
    - Scheduled time: 23:30 (11:30 PM)
  - Requires Magic Mirror automations enabled
  - **Turn On Conditions:**
    - Motion detected (living room OR stairs)
    - Magic Mirror plug is off
    - Stairs motion triggers enabled
    - **Action:** Turn on Magic Mirror plug + log event
  - **Turn Off Conditions:**
    - No stairs motion for 3 minutes OR 23:30 time trigger
    - Between 23:00 and 05:00
    - Magic Mirror plug is on
    - **Action:** Turn off Magic Mirror plug + log event
  - Mode: Queued (max 10)

- **Turn Off Based On Time During Weekday (ID: 1588856667889):**
  - Trigger: No stairs motion for 5 minutes
  - Time window: 09:00 - 17:30 (Monday-Friday only)
  - Requires both Magic Mirror + stairs motion triggers enabled
  - **Action:** Turn off Magic Mirror + log event
  - **Purpose:** Energy saving during typical work hours

**Purpose:**
- Activate Magic Mirror when people use stairs or living room
- Auto-shutdown at night (23:30) or after extended inactivity
- Weekday energy saving during typical away hours

**Related Automations:**
- ID 1592062695452 - Magic Mirror Control (Motion/Night)
- ID 1588856667889 - MagicMirror: Turn Off Based On Time During Weekday

---

### Physical Light Switch Integration

**Trigger:** Physical wall switch state change

**Logic:**

- **Light Switch (ID: 1714869692076):**
  - Trigger: stairs_light_input_0_input state change
  - Excludes unknown/unavailable states
  - **Action:** Toggle main stairs light
    - Transition: 1 second
    - Brightness: 255 (full)
  - Mode: Single
  - **Purpose:** Manual override capability

**Safety Features:**
- State filtering prevents spurious triggers
- Always full brightness for manual control
- Works independently of motion automation enable state

**Related Automations:**
- ID 1714869692076 - Stairs: Light Switch

---

### Children's Door Integration

**Triggers:** Children's bedroom doors opening/closing after bedtime

**Logic:**

- **Light On And Children's Door Open After Bedtime (ID: 1615849889104):**
  - Triggers: Leo's OR Ashlee's door opens
  - Time window: After children's bedtime, before midnight
  - Conditions:
    - Main stairs light is on
    - NOT in "No Children" home mode
  - **Actions (conditional by door):**
    - **Leo's door opens + automation enabled:**
      - Dim main light (scene.stairs_light_dim)
      - Turn on ambient light_2 (scene.stairs_light_2_on)
      - 0.5 second transition
    - **Ashlee's door opens + automation enabled:**
      - Full brightness main light (scene.stairs_light_on)
      - Turn on ambient light_2
      - 0.5 second transition
  - Mode: Queued (max 10)
  - **Purpose:** Provide safe lighting when child leaves room at night

- **Light On And Children's Door Closed Before Midnight (ID: 1615850302527):**
  - Triggers: Leo's OR Ashlee's door closes
  - Time window: After children's bedtime, before midnight
  - Conditions:
    - Main stairs light is on
    - In "Normal" home mode
  - **Actions (conditional by door state):**
    - **Both children's doors closed:**
      - Full brightness all lights (scene.stairs_light_on + stairs_light_2_on)
    - **Only Leo's door closed:**
      - Full brightness all lights
    - **Only Ashlee's door closed:**
      - Full brightness all lights
  - Mode: Single
  - **Purpose:** Restore full lighting when children back in rooms

**Safety Features:**
- Different brightness levels based on which child's door
- Always provides lighting for safety
- Home mode aware (respects "No Children" mode)
- Works in conjunction with motion detection

**Related Automations:**
- ID 1615849889104 - Light On And Children's Door Open After Bedtime
- ID 1615850302527 - Light On And Children's Door Closed Before Midnight

---

### Time-Based Blind Automation

**Triggers:** Scheduled times and solar events

**Logic:**

- **Close Blinds At Night (ID: 1630760046947):**
  - Trigger: Sunset + 1 hour offset
  - Conditions:
    - Blinds currently open
    - Blind automation enabled
  - **Action:** Close stairs blinds + log event
  - Mode: Single
  - **Purpose:** Privacy and thermal insulation

- **Open Blinds In The Morning (ID: 1630760149356):**
  - Trigger: 08:00 (8:00 AM)
  - Conditions:
    - Blinds currently closed
    - Blind automation enabled
  - **Action:** Open stairs blinds + log event
  - Mode: Single
  - **Purpose:** Natural morning light

**Safety Features:**
- State checks prevent unnecessary actions
- Can be disabled globally
- Offset from sunset for natural timing

**Related Automations:**
- ID 1630760046947 - Close Blinds At Night
- ID 1630760149356 - Open Blinds In The Morning

---

### Person Detection & Security

**Trigger:** Frigate AI person detection on stairs camera

**Logic:**

- **Person Detected (ID: 1630015410190):**
  - Trigger: stairs_person_detected changes to "on"
  - Condition: House alarm is in "armed_away" state
  - **Actions:**
    - Capture snapshot from stairs_high_resolution_channel
    - Save to path from input_text.latest_frigate_upstairs_person_file_path
    - Send notification with attachment via script.send_home_log_with_local_attachments
    - Title: "Person detected on stairs"
    - Message: "Frigate detected a person on the stairs."
  - Mode: Queued (max 10) for multiple detections
  - **Purpose:** Security monitoring when house is unoccupied

**Safety Features:**
- Only active when alarm armed away
- Saves evidence (snapshot)
- Immediate notification with image
- Queued mode handles multiple detections

**Related Automations:**
- ID 1630015410190 - Person Detected

---

### Ambient Light Status & Timeout

**Trigger:** Ambient light on for extended period

**Logic:**

- **Front Door Status On For Long Time (ID: 1743186662872):**
  - Triggers:
    - stairs_ambient on for 3 minutes
    - stairs_ambient on for 5 minutes
  - Condition: Front door is closed
  - **Action:** Turn off stairs_ambient light
  - Mode: Single
  - **Purpose:** Energy saving when ambient light left on accidentally

**Safety Features:**
- Front door check prevents turning off during entry/exit
- Dual timeouts (3 min and 5 min) for flexibility

**Related Automations:**
- ID 1743186662872 - Front Door Status On For Long Time

---

## Room Layout & Device Placement

```
                          NORTH (Window Wall)
         ╔══════════════════════════════════════════════════╗
         ║                                                  ║
         ║  🪟 Stairway Window                              ║
         ║  └─ 🎚️ Motorized Blind (cover.stairs_blinds)    ║
         ║     └─ Opens: 08:00, Closes: Sunset + 1hr       ║
         ║                                                  ║
         ╠══════════════════════════════════════════════════╣
         ║                  FIRST FLOOR LANDING             ║
         ║                                                  ║
         ║  💡 Landing Ambient Light (light.stairs_ambient) ║
         ║  └─ RGB capable, status indicator               ║
         ║                                                  ║
         ║  📏 Upstairs Motion Sensors (TOP OF STAIRS)      ║
         ║  ├─ binary_sensor.upstairs_area_motion (group)  ║
         ║  └─ binary_sensor.upstairs_motion_occupancy     ║
         ║                                                  ║
         ║  👦 Leo's Room: binary_sensor.leos_bedroom_door ║
         ║  └─ Door open → Dim stairs                      ║
         ║                                                  ║
         ║  👧 Ashlee's Room: binary_sensor.ashlees_door   ║
         ║  └─ Door open → Full brightness stairs          ║
         ║                                                  ║
         ║  ═══════════════════════════════════════════     ║
         ║              STAIRWAY (Vertical)                 ║
         ║                                                  ║
         ║    💡 Main Stairs Light (light.stairs)           ║
         ║    ├─ Color temperature adjustable              ║
         ║    ├─ Dimmable (brightness 5-255)               ║
         ║    └─ Scenes:                                    ║
         ║       ├─ scene.stairs_light_on (bright 155)     ║
         ║       ├─ scene.stairs_light_dim (dim 20)        ║
         ║       ├─ scene.stairs_night_light (red 5)       ║
         ║       └─ scene.stairs_light_off                  ║
         ║                                                  ║
         ║    🔆 Physical Light Switch                      ║
         ║    └─ binary_sensor.stairs_light_input_0_input  ║
         ║       └─ Manual toggle, always full brightness  ║
         ║                                                  ║
         ║  ═══════════════════════════════════════════     ║
         ║                                                  ║
         ║                  GROUND FLOOR LEVEL              ║
         ║                                                  ║
         ║  📏 Bottom Motion Sensor                         ║
         ║  └─ binary_sensor.stairs_motion_occupancy       ║
         ║     └─ Controls ambient light stairs_2          ║
         ║                                                  ║
         ║  🌡️ Environmental Sensing                        ║
         ║  └─ sensor.stairs_motion_illuminance            ║
         ║     └─ Threshold: input_number.stairs_light_    ║
         ║                   level_threshold               ║
         ║                                                  ║
         ║  💡 Lower Ambient Light (light.stairs_2)         ║
         ║  ├─ LED strip, dimmable                         ║
         ║  └─ Scenes:                                      ║
         ║     ├─ scene.stairs_light_2_on (bright 255)     ║
         ║     ├─ scene.stairs_light_2_dim (dim 38)        ║
         ║     └─ scene.stairs_light_2_off                  ║
         ║                                                  ║
         ║  🪞 Magic Mirror Display                         ║
         ║  └─ switch.magic_mirror_plug                    ║
         ║     ├─ On: Motion detected (stairs or lounge)   ║
         ║     ├─ Off: 23:30 or no motion 3-5 min         ║
         ║     └─ Weekday off: 09:00-17:30 + 5 min idle   ║
         ║                                                  ║
         ║  📹 Security Camera                              ║
         ║  └─ camera.stairs_high_resolution_channel       ║
         ║     └─ binary_sensor.stairs_person_detected     ║
         ║        └─ Triggers when alarm armed_away        ║
         ║                                                  ║
         ╚══════════════════════════════════════════════════╝
                          SOUTH (Entrance)

External Integrations:
  📏 Living Room Motion: binary_sensor.living_room_area_motion
     └─ Triggers Magic Mirror activation

  🚨 House Alarm: alarm_control_panel.house_alarm
     └─ "armed_away" enables person detection snapshots

  🚪 Front Door: binary_sensor.front_door
     └─ Prevents ambient light timeout during entry/exit

  🕐 Time-Based Controls:
     ├─ Children's bedtime: input_datetime.childrens_bed_time
     ├─ Night mode threshold: Midnight
     ├─ Day mode start: 07:00
     └─ Magic Mirror shutdown: 23:30

Multi-Zone Lighting Behavior:
  TOP (Upstairs Motion):
  ├─ Before bedtime + dark → Full brightness
  ├─ After bedtime + dark + children doors closed → Full brightness
  ├─ After bedtime + dark + children doors open → Dim
  └─ After midnight + dark → Night light OR full (depends on settings)

  BOTTOM (Lower Stairs Motion):
  ├─ After sunrise → Ambient light dim
  └─ Midnight to sunrise → Ambient light very dim

Progressive Lighting Shutdown:
  1. Motion stops (both top and bottom)
  2. Wait 1 minute
  3. Turn off main light (1s transition)
  4. If ambient on: wait, then turn off ambient (2s transition)
```

---

## Key Automation Workflows

### Morning Routine (After Sunrise)

```
07:00 AM - Day Mode Begins
   ↓
Check Conditions:
├─ Blind automation enabled?
└─ Motion detection enabled?
   ↓
Bottom Stairs Motion Detected
   ↓
Check Illuminance
├─ sensor.stairs_motion_illuminance < threshold?
│  ├─ YES → Check time + light state
│  │  ├─ Before bedtime + dark → Turn on MAIN light (full)
│  │  └─ After sunrise → Turn on AMBIENT stairs_2 (dim)
│  └─ NO → Skip (bright enough)
   ↓
08:00 AM - Morning Blind Opening
   ↓
Check Conditions:
├─ Blinds currently closed?
└─ Blind automation enabled?
   ↓
All YES → Open Stairs Blinds
   └─ Log: "Opening blinds."
```

**Key Points:**
- Daytime motion prioritizes ambient lighting (stairs_2)
- Main light requires dark conditions (illuminance check)
- Blinds open at fixed 08:00 time
- Two-zone lighting (main + ambient) for energy efficiency

---

### Evening Routine (After Sunset)

```
Sunset + 1 Hour
   ↓
Check Conditions:
├─ Blinds currently open?
└─ Blind automation enabled?
   ↓
All YES → Close Stairs Blinds
   └─ Log: "Closing blinds."
   ↓
Motion Detected (Upstairs)
   ↓
Check Time + Illuminance
├─ After children's bedtime?
├─ Illuminance < threshold?
└─ Main light off OR dim?
   ↓
Evaluate Home Mode + Door States
   ↓
┌─────────────────────────────────────────────────┐
│ Scenario 1: "No Children" Mode                 │
│ └─ Action: Full brightness (scene.stairs_light_│
│            on)                                  │
├─────────────────────────────────────────────────┤
│ Scenario 2: Both children's doors closed       │
│ ├─ Automations for both enabled                │
│ └─ Action: Full brightness (safe for adults)   │
├─────────────────────────────────────────────────┤
│ Scenario 3: Both children's doors open         │
│ ├─ Automations for both enabled                │
│ └─ Action: Dim light (scene.stairs_light_dim)  │
│    └─ Prevents waking children                 │
├─────────────────────────────────────────────────┤
│ Scenario 4: Only Leo's door closed             │
│ └─ Action: Dim light                            │
├─────────────────────────────────────────────────┤
│ Scenario 5: Only Ashlee's door closed          │
│ └─ Action: Full brightness                      │
└─────────────────────────────────────────────────┘
```

**Safety Logic:**
- Children's door states determine brightness
- Defaults to safe lighting (full brightness)
- Respects sleep patterns (dim when doors open)

---

### Night Mode (After Midnight, Before Sunrise)

```
After Midnight AND Before Sunrise
   ↓
Motion Detected (Upstairs)
   ↓
Check Conditions:
├─ Illuminance < threshold?
├─ Motion triggers enabled?
└─ Main light off OR dim (brightness < 5)?
   ↓
All YES → Evaluate Night Settings
   ↓
┌─────────────────────────────────────────────────┐
│ Check 1: Is bedroom light on?                  │
│ ├─ YES → Someone awake, full brightness        │
│ │  └─ Action: scene.stairs_light_on            │
│ │     └─ Log with illuminance values           │
│ └─ NO → Continue to next check                 │
├─────────────────────────────────────────────────┤
│ Check 2: Night light enabled?                  │
│ └─ input_boolean.enable_stairs_night_light     │
│    ├─ ON → Ultra-dim red night light           │
│    │  └─ Action: scene.stairs_night_light      │
│    │     ├─ Brightness: 5                       │
│    │     ├─ Color: Red (358° hue, 100% sat)    │
│    │     └─ Safest for night vision            │
│    └─ OFF → Default to full brightness         │
│       └─ Action: scene.stairs_light_on         │
│          └─ Safety override (prevent falls)    │
└─────────────────────────────────────────────────┘
   ↓
Log Event with Context
   └─ Includes illuminance reading and action taken
```

**Night Mode Features:**
- Bedroom light awareness (someone already awake)
- Optional ultra-dim red night light mode
- Safety default: full brightness if night mode disabled
- Prevents accidental falls in complete darkness

---

### Children's Door Event Workflow

```
After Children's Bedtime (input_datetime.childrens_bed_time)
   ↓
Child's Door Opens (Leo OR Ashlee)
   ↓
Check Preconditions:
├─ Main stairs light is on?
├─ NOT in "No Children" home mode?
└─ Time before midnight?
   ↓
All YES → Determine Which Door
   ↓
┌─────────────────────────────────────────────────┐
│ Leo's Door Opens                                │
│ ├─ Automation enabled?                          │
│ └─ YES → Actions:                               │
│    ├─ Dim main light (scene.stairs_light_dim)  │
│    │  └─ Brightness: 20                         │
│    ├─ Turn on ambient stairs_2 (on scene)      │
│    │  └─ Brightness: 255                        │
│    ├─ Transition: 0.5 seconds                   │
│    └─ Log: "Leo's door opened after bed time"  │
├─────────────────────────────────────────────────┤
│ Ashlee's Door Opens                             │
│ ├─ Automation enabled?                          │
│ └─ YES → Actions:                               │
│    ├─ Full main light (scene.stairs_light_on)  │
│    │  └─ Brightness: 155                        │
│    ├─ Turn on ambient stairs_2 (on scene)      │
│    ├─ Transition: 0.5 seconds                   │
│    └─ Log: "Ashlee's door opened after bed"    │
└─────────────────────────────────────────────────┘
   ↓
Child Returns to Room (Door Closes)
   ↓
Check Preconditions:
├─ Main stairs light is on?
├─ In "Normal" home mode?
└─ Time before midnight?
   ↓
All YES → Evaluate All Door States
   ↓
┌─────────────────────────────────────────────────┐
│ Both Children's Doors Now Closed               │
│ ├─ Both automations enabled                     │
│ └─ Actions:                                     │
│    ├─ Full brightness main (stairs_light_on)   │
│    ├─ Full brightness ambient (stairs_light_2_ │
│    │                            on)             │
│    ├─ Transition: 0.5 seconds                   │
│    └─ Log: "Doors closed, turn up all lights"  │
├─────────────────────────────────────────────────┤
│ Individual Door Closed                          │
│ └─ Same action: Full brightness all lights     │
│    └─ Restore normal adult lighting            │
└─────────────────────────────────────────────────┘
```

**Child-Specific Behavior:**
- Leo's door: Dims (he may be more sensitive to light)
- Ashlee's door: Full brightness (different sleep pattern)
- Both provide safe navigation lighting
- Restores full brightness when back in rooms

---

### Magic Mirror Control Workflow

```
Motion Detected (Stairs OR Living Room)
   ↓
Check Conditions:
├─ Magic Mirror automations enabled?
├─ Stairs motion triggers enabled?
└─ Mirror currently off?
   ↓
All YES → Turn On Magic Mirror
   ├─ Action: switch.magic_mirror_plug ON
   └─ Log: "Turning on Magic Mirror."
   ↓
┌─────────────────────────────────────────────────┐
│ Monitor for Shutdown Conditions                 │
│                                                  │
│ Condition 1: No Motion (Night)                  │
│ ├─ Trigger: No stairs motion for 3 minutes     │
│ ├─ Time: Between 23:00 and 05:00               │
│ └─ Action: Turn off mirror                      │
│    └─ Log: "No motion detected, turning off"   │
│                                                  │
│ Condition 2: Scheduled Shutdown                 │
│ ├─ Trigger: Time is 23:30 (11:30 PM)           │
│ ├─ Time: Between 23:00 and 05:00               │
│ └─ Action: Turn off mirror                      │
│    └─ Log: "Turning off (scheduled)"           │
│                                                  │
│ Condition 3: Weekday Daytime Idle              │
│ ├─ Trigger: No stairs motion for 5 minutes     │
│ ├─ Time: 09:00-17:30 (Mon-Fri only)            │
│ ├─ Both automations enabled                     │
│ └─ Action: Turn off mirror                      │
│    └─ Log: "No motion, turning off (time)"     │
└─────────────────────────────────────────────────┘
```

**Energy Saving Logic:**
- 3 different timeout scenarios based on time and day
- Longer timeout during work hours (5 min vs 3 min)
- Forced shutdown at 23:30 regardless of motion
- Living room motion also activates (shared display)

---

### Progressive Light Shutdown Sequence

```
Motion Stops (No Detection)
   ↓
Start 1-Minute Countdown
   ├─ Separate timers for top and bottom sensors
   └─ Motion triggers must be enabled
   ↓
1 Minute Elapsed - No Motion Detected
   ↓
Identify Which Motion Sensor(s) Triggered Off
   ↓
┌─────────────────────────────────────────────────┐
│ Upstairs Motion Stopped                         │
│ └─ Actions (parallel):                          │
│    ├─ Turn off main stairs light                │
│    │  └─ Transition: 1 second                   │
│    │     └─ scene.stairs_light_off              │
│    ├─ Check if stairs_2 ambient is on           │
│    │  └─ YES → Turn off stairs_2                │
│    │     ├─ Transition: 2 seconds               │
│    │     ├─ scene.stairs_light_2_off            │
│    │     ├─ Delay: 1 second                     │
│    │     └─ Forced off: light.turn_off          │
│    └─ Log: "No motion for 1 minute, off"       │
├─────────────────────────────────────────────────┤
│ Bottom Stairs Motion Stopped (Fallback)        │
│ ├─ Check: Is stairs_2 ambient on?              │
│ └─ YES → Actions:                               │
│    ├─ Turn off stairs_2 only                    │
│    ├─ Transition: 2 seconds                     │
│    ├─ scene.stairs_light_2_off                  │
│    └─ Log: "No motion bottom, turning off"     │
└─────────────────────────────────────────────────┘
```

**Progressive Shutdown Features:**
- Main light (stairs) turns off first (1s transition)
- Ambient light (stairs_2) turns off second (2s transition)
- Delay between shutdowns for gradual dimming
- Forced off command ensures complete shutdown
- Different transitions create smooth fade-out

---

### Person Detection & Security Alert

```
Frigate AI Person Detection
   ↓
binary_sensor.stairs_person_detected: ON
   ↓
Check Alarm State
└─ alarm_control_panel.house_alarm
   ├─ State: "armed_away"?
   │  ├─ YES → SECURITY EVENT
   │  └─ NO → Ignore (normal occupancy)
   ↓
Execute Security Actions (Parallel)
   ↓
┌─────────────────────────────────────────────────┐
│ Action 1: Capture Snapshot                     │
│ ├─ Camera: stairs_high_resolution_channel      │
│ ├─ Filename: From input_text.latest_frigate_   │
│ │             upstairs_person_file_path        │
│ └─ Template: Dynamic path with timestamp       │
├─────────────────────────────────────────────────┤
│ Action 2: Send Notification with Attachment    │
│ ├─ Script: send_home_log_with_local_attachments│
│ ├─ Title: "Person detected on stairs"          │
│ ├─ Message: "Frigate detected a person on the  │
│ │            stairs."                           │
│ ├─ Attachment: Snapshot file path              │
│ └─ Delivery: Immediate push notification       │
└─────────────────────────────────────────────────┘
   ↓
Queue Management
└─ Mode: Queued (max 10)
   └─ Handles multiple detections without losing events
```

**Security Features:**
- Only active when house unoccupied (armed_away)
- High-resolution snapshot for evidence
- Immediate notification with image attachment
- Queued processing ensures no missed events
- AI-powered detection reduces false positives

---

## Configuration Parameters

### Motion & Light Detection Settings
- `input_boolean.enable_stairs_motion_triggers` - Master enable for all motion-based lighting
- `input_number.stairs_light_level_threshold` - Illuminance threshold for motion triggers (lux)
  - Motion detection only activates below this threshold (dark conditions)

### Night Mode Settings
- `input_boolean.enable_stairs_night_light` - Enable ultra-dim red night light after midnight
  - ON: Use dim red light (brightness 5, red hue)
  - OFF: Default to full brightness (safety override)

### Blind Control Settings
- `input_boolean.enable_stairs_blind_automations` - Master enable for blind automations
  - Controls both morning opening (08:00) and evening closing (sunset+1hr)

### Children's Door Settings
- `input_boolean.enable_leos_door_automations` - Enable Leo's door → stairs light integration
- `input_boolean.enable_ashlees_door_automations` - Enable Ashlee's door → stairs light integration
- `input_datetime.childrens_bed_time` - Time when door-based lighting changes activate

### Magic Mirror Settings
- `input_boolean.enable_magic_mirror_automations` - Master enable for Magic Mirror control

### Home Mode Settings
- `input_select.home_mode` - Current house occupancy mode
  - Checked values: "No Children", "Normal"
  - Affects lighting decisions and door automation behavior

### Time Schedules
- Morning blind opening: 08:00 (8:00 AM)
- Evening blind closing: Sunset + 1 hour offset
- Day mode start: 07:00 (7:00 AM)
- Children's bedtime: input_datetime.childrens_bed_time
- Midnight threshold: 00:00 (transitions to ultra-night mode)
- Night mode end: 07:00 OR sunrise (whichever first)
- Magic Mirror night shutdown: 23:30 (11:30 PM)
- Magic Mirror weekday shutdown window: 09:00-17:30 (Monday-Friday)
- Motion timeout (lights off): 1 minute no motion
- Magic Mirror timeout (night): 3 minutes no motion
- Magic Mirror timeout (weekday): 5 minutes no motion
- Ambient light timeout (front door closed): 3-5 minutes

### Security Settings
- Person detection only active when: alarm_control_panel.house_alarm = "armed_away"
- Snapshot storage path: input_text.latest_frigate_upstairs_person_file_path

---

## Helper Entities

### Input Booleans
- `input_boolean.enable_stairs_motion_triggers` - Master motion detection enable/disable
- `input_boolean.enable_stairs_night_light` - Night light mode (ultra-dim red after midnight)
- `input_boolean.enable_stairs_blind_automations` - Blind automation enable/disable
- `input_boolean.enable_magic_mirror_automations` - Magic Mirror control enable/disable
- `input_boolean.enable_leos_door_automations` - Leo's bedroom door integration enable
- `input_boolean.enable_ashlees_door_automations` - Ashlee's bedroom door integration enable

### Input Numbers
- `input_number.stairs_light_level_threshold` - Illuminance threshold for motion triggers (lux)
  - Motion detection only activates when illuminance below this value
  - Prevents triggering in bright daylight conditions

### Input Datetime
- `input_datetime.childrens_bed_time` - Time when bedtime lighting logic activates
  - Affects door-based brightness decisions
  - Triggers different motion detection behavior

### Input Select
- `input_select.home_mode` - Current house mode
  - Values checked: "No Children", "Normal"
  - Affects lighting decisions and automation behavior

### Input Text
- `input_text.latest_frigate_upstairs_person_file_path` - Dynamic file path for camera snapshots
  - Used by person detection automation
  - Template-based for timestamp organization

---

## Scripts

### Logging Scripts
All automations use centralized logging scripts:

- `script.send_to_home_log`
  - Standard logging with title, message, log_level
  - Used by most automations for event tracking
  - Parameters:
    - title: Room/area identifier
    - message: Event description (supports templates)
    - log_level: "Debug", "Info", "Warning", "Error"

- `script.log_with_clock`
  - Logging with clock emoji timestamp
  - Used by Magic Mirror shutdown automation
  - Parameters: Same as send_to_home_log

- `script.send_home_log_with_local_attachments`
  - Logging with file attachment capability
  - Used by person detection for snapshot notifications
  - Parameters:
    - title: Notification title
    - message: Notification message
    - filePath: Local file path to attach (snapshot image)

**Note:** No room-specific scripts defined in stairs.yaml. All use global scripts.

---

## Sensors

### Environmental Sensors
- `sensor.stairs_motion_illuminance`
  - Platform: Integrated with motion sensor
  - Unit: Lux (light level)
  - Purpose: Determine if lighting needed (compare to threshold)
  - Used by all motion detection automations

### Binary Sensors (Groups)
- `binary_sensor.upstairs_area_motion`
  - Platform: Group
  - Purpose: Aggregated motion detection for top of stairs
  - Includes multiple motion sensors
  - Used for redundancy (Ring + Zigbee fallback)

- `binary_sensor.living_room_area_motion`
  - Platform: Group
  - Purpose: Living room motion detection
  - Used for Magic Mirror activation

- `binary_sensor.childrens_bedroom_doors`
  - Platform: Binary sensor group
  - Purpose: Combined state of both children's doors
  - Values: "on" (any door open), "off" (all closed)
  - Used for stair lighting decisions after bedtime

### Person Detection Sensors
- `binary_sensor.stairs_person_detected`
  - Platform: Frigate AI integration
  - Purpose: AI-powered person detection on stairs camera
  - Triggers security snapshots when alarm armed

### Input Sensors (Physical)
- `binary_sensor.stairs_light_input_0_input`
  - Platform: Physical wall switch
  - Purpose: Manual light toggle input
  - Excludes: unknown, unavailable states

---

## Status Indicators

### Light Scenes

**Main Stairs Light (light.stairs):**

- `scene.stairs_light_on` (ID: 1609512133205)
  - Name: "Stairs: Turn Light On"
  - Icon: mdi:lightbulb
  - Brightness: 155 (60% of max)
  - Color temperature: 3921K (warm white)
  - Color temp value: 255 mireds
  - RGB equivalent: (255, 203, 162)
  - Purpose: Normal full brightness for active use

- `scene.stairs_light_dim` (ID: 1612221653166)
  - Name: "Stairs: Dim Light"
  - Icon: mdi:lightbulb
  - Brightness: 20 (8% of max)
  - Color temperature: 3921K (warm white)
  - Color temp value: 255 mireds
  - RGB equivalent: (255, 203, 162)
  - Purpose: Low-light navigation when children's doors open

- `scene.stairs_night_light` (ID: 1631754396696)
  - Name: "Stairs Night Light"
  - Brightness: 5 (2% of max, ultra-dim)
  - Color mode: HS (hue/saturation)
  - Hue: 358.599° (deep red)
  - Saturation: 100% (pure color)
  - RGB equivalent: (255, 0, 5)
  - Purpose: Ultra-dim red night vision preservation after midnight
  - When used: After midnight + night light enabled

- `scene.stairs_light_off` (ID: stairs_light_off)
  - Name: "Stairs: Turn Light Off"
  - Icon: mdi:lightbulb
  - State: off
  - Purpose: Complete light shutdown

**Secondary Ambient Light (light.stairs_2):**

- `scene.stairs_light_2_on` (ID: 1623880439954)
  - Name: "Stairs Light 2 On"
  - Icon: mdi:led-strip-variant
  - Brightness: 255 (100%, full brightness)
  - Color temperature: 430 mireds (warm)
  - Effect: none
  - Purpose: Full ambient lighting at bottom of stairs

- `scene.stairs_light_2_dim` (ID: 1623970390049)
  - Name: "Stairs 2 Light Dim"
  - Icon: mdi:led-strip-variant
  - Brightness: 38 (15% of max)
  - Color temperature: 430 mireds (warm)
  - Effect: none
  - Purpose: Low-level ambient lighting (after sunrise)

- `scene.stairs_light_2_off` (ID: stairs_light_2_off)
  - Name: "Stairs Light 2 Off"
  - Icon: mdi:led-strip-variant
  - Brightness: 0
  - State: on (with brightness 0)
  - Purpose: Ambient light shutdown

**Landing Ambient Light (light.stairs_ambient):**

- `scene.landing_set_light_to_blue` (ID: 1612220515925)
  - Name: "Landing: Set Light To Blue"
  - Brightness: 255 (100%)
  - Color mode: XY
  - Hue: 237.073° (blue)
  - Saturation: 96.471%
  - RGB: (9, 21, 255)
  - XY: (0.136, 0.042)
  - Purpose: Status indicator (blue)

- `scene.landing_set_light_to_red` (ID: 1612220555547)
  - Name: "Landing Set Light To Red"
  - Brightness: 255 (100%)
  - Color mode: XY
  - Hue: 9.231° (red)
  - Saturation: 66.275%
  - RGB: (255, 112, 86)
  - XY: (0.589, 0.329)
  - Purpose: Status indicator (red)

**Note:** Landing ambient scenes not actively used in automations (legacy/manual control)

---

## Key Features

✅ **Multi-Level Motion Detection** - Separate sensors for top and bottom of stairs with independent control
✅ **Time-Based Adaptive Lighting** - Different brightness levels based on time of day (day/evening/night/after-midnight)
✅ **Children's Door Integration** - Smart brightness adjustment based on which child's door is open
✅ **Progressive Lighting Zones** - Two-zone lighting (main + ambient) with independent control
✅ **Safety-First Night Mode** - Optional ultra-dim red night light OR full brightness safety default
✅ **Illuminance-Aware Triggers** - Only activates lighting when actually dark (threshold-based)
✅ **Physical Switch Override** - Manual wall switch always available (full brightness)
✅ **Magic Mirror Automation** - Context-aware display control (motion + time + day of week)
✅ **Blind Schedule Automation** - Solar-based closing (sunset+1hr) and fixed morning opening (08:00)
✅ **Person Detection Security** - AI-powered detection with snapshot when alarm armed
✅ **Home Mode Awareness** - Different behavior for "No Children" vs "Normal" modes
✅ **Progressive Light Shutdown** - Gradual fade-out with transitions (main first, then ambient)
✅ **Redundant Motion Sensors** - Ring integration with Zigbee fallback for reliability
✅ **Weekday Energy Saving** - Extended Magic Mirror timeout during typical work hours (09:00-17:30)
✅ **Bedroom Light Awareness** - Detects if someone already awake (bedroom light on)
✅ **Multiple Timeout Strategies** - Different timeouts for night (3 min), weekday (5 min), general (1 min)
✅ **Child-Specific Behavior** - Different brightness for Leo vs Ashlee (personalized sleep patterns)
✅ **Front Door Integration** - Prevents ambient light timeout during entry/exit
✅ **Queued Event Processing** - Handles multiple rapid motion/door events without loss
✅ **Scene-Based Control** - Consistent lighting states via predefined scenes
✅ **Comprehensive Logging** - All automation actions logged with context and illuminance values

---

## File Structure

```
packages/rooms/
├── stairs.yaml                     # Main stairs configuration (1117 lines)
│   ├── Automations (14 total)
│   │   ├── Motion Detection (5)
│   │   │   ├── ID 1624918278463 - Motion Detected For Ambient Lights
│   │   │   ├── ID 1598726353326 - Motion Before Kids Bed Time
│   │   │   ├── ID 1587595659605 - After Bed Time Before Midnight
│   │   │   ├── ID 1587595659606 - After Midnight Motion
│   │   │   └── ID 1587595847618 - No Motion Detected (Lights Off)
│   │   ├── Magic Mirror Control (2)
│   │   │   ├── ID 1592062695452 - Magic Mirror Control (Motion/Night)
│   │   │   └── ID 1588856667889 - Turn Off Based On Time (Weekday)
│   │   ├── Light Switch (1)
│   │   │   └── ID 1714869692076 - Physical Light Switch
│   │   ├── Children's Door Integration (2)
│   │   │   ├── ID 1615849889104 - Door Open After Bedtime
│   │   │   └── ID 1615850302527 - Door Closed Before Midnight
│   │   ├── Blind Automation (2)
│   │   │   ├── ID 1630760046947 - Close Blinds At Night
│   │   │   └── ID 1630760149356 - Open Blinds In Morning
│   │   ├── Security (1)
│   │   │   └── ID 1630015410190 - Person Detected
│   │   └── Ambient Light Timeout (1)
│   │       └── ID 1743186662872 - Front Door Status On For Long Time
│   ├── Scenes (9 total)
│   │   ├── Main Stairs Light (4)
│   │   │   ├── stairs_light_on (bright 155)
│   │   │   ├── stairs_light_dim (dim 20)
│   │   │   ├── stairs_night_light (red 5)
│   │   │   └── stairs_light_off
│   │   ├── Ambient Light stairs_2 (3)
│   │   │   ├── stairs_light_2_on (bright 255)
│   │   │   ├── stairs_light_2_dim (dim 38)
│   │   │   └── stairs_light_2_off
│   │   └── Landing Ambient (2)
│   │       ├── landing_set_light_to_blue
│   │       └── landing_set_light_to_red
│   └── Scripts (0)
│       └─ Uses global logging scripts only
│
└── STAIRS-SETUP.md                 # This file - Room documentation
```

---

## Automation Summary by Category

### Motion Detection & Lighting (5 automations)
- **ID 1624918278463** - Motion Detected For Ambient Lights (bottom stairs, time-based)
- **ID 1598726353326** - Motion Detected Before Kids Bed Time (upstairs, dark, daytime)
- **ID 1587595659605** - Upstairs Dark, After Bed Time, Before Midnight (children's doors aware)
- **ID 1587595659606** - Dark, After Bed Time, After Midnight (night light + bedroom awareness)
- **ID 1587595847618** - No Motion Detected (progressive shutdown, 1-min timeout)

### Magic Mirror Control (2 automations)
- **ID 1592062695452** - Magic Mirror Control (Motion/Night) - Multi-trigger on/off logic
- **ID 1588856667889** - MagicMirror: Turn Off Based On Time During Weekday (09:00-17:30)

### Physical Control (1 automation)
- **ID 1714869692076** - Light Switch (manual wall switch toggle)

### Children's Door Integration (2 automations)
- **ID 1615849889104** - Light On And Children's Door Open After Bedtime (dim/bright by child)
- **ID 1615850302527** - Light On And Children's Door Closed Before Midnight (restore brightness)

### Time-Based Automation (2 automations)
- **ID 1630760046947** - Close Blinds At Night (sunset + 1hr)
- **ID 1630760149356** - Open Blinds In The Morning (08:00)

### Security (1 automation)
- **ID 1630015410190** - Person Detected (Frigate AI + snapshot when alarm armed)

### Light Timeout (1 automation)
- **ID 1743186662872** - Front Door Status On For Long Time (3-5 min ambient timeout)

**Total Automation Count:** 14 automations
**Total Scene Count:** 9 scenes
**Total Script Count:** 0 (uses global scripts)
**Total Sensor Count:** 4+ (motion, illuminance, person detection, door contacts)

---

## Advanced Features Explained

### Multi-Zone Progressive Lighting Strategy

The stairs implement a sophisticated two-zone lighting system with progressive activation and shutdown:

**Zone 1: Main Stairs Light (light.stairs)**
- Primary stairwell illumination
- Color temperature adjustable (2702-6535K)
- Brightness range: 5-255
- Controlled by upstairs motion detection
- Three brightness modes: Full (155), Dim (20), Night (5)

**Zone 2: Ambient Light (light.stairs_2)**
- Bottom stairs accent lighting
- LED strip with color temperature control
- Brightness range: 0-255
- Controlled by bottom stairs motion detection
- Two brightness modes: Full (255), Dim (38)

**Progressive Activation Logic:**
```
Daytime (After Sunrise):
├─ Bottom motion → Ambient light only (stairs_2 dim)
└─ Top motion + dark → Main light full

Evening (After Bedtime, Before Midnight):
├─ Top motion + dark → Main light (brightness depends on doors)
└─ Bottom motion → Ambient light dim

Night (After Midnight):
├─ Top motion + dark → Main light (night mode OR full)
└─ Bottom motion → Ambient light very dim
```

**Progressive Shutdown Sequence:**
```
1. Both motion sensors: "off" for 1 minute
2. Turn off main light (stairs) with 1s transition
3. Check if ambient (stairs_2) is on
4. If yes: Delay 1 second, then turn off with 2s transition
5. Force off command to ensure complete shutdown
```

**Benefits:**
- Energy efficient (only lights needed zones)
- Gradual transitions prevent jarring changes
- Redundant shutdown ensures lights don't stay on
- Separate timeouts allow zone-independent control

---

### Children's Door State Machine

The system implements a sophisticated state machine for children's door events:

**State Variables:**
- Leo's door: binary_sensor.leos_bedroom_door_contact
- Ashlee's door: binary_sensor.ashlees_bedroom_door_contact
- Combined: binary_sensor.childrens_bedroom_doors
- Automation enables: input_boolean.enable_leos_door_automations, enable_ashlees_door_automations

**Decision Matrix (After Bedtime, Before Midnight):**

```
Door Open Event (Light Already On):
├─ Leo's Door Opens + Automation Enabled
│  └─ Action: Dim main (20) + Full ambient (255)
│     └─ Reason: Leo sensitive to bright light
├─ Ashlee's Door Opens + Automation Enabled
│  └─ Action: Full main (155) + Full ambient (255)
│     └─ Reason: Ashlee needs more light for safety
└─ Home Mode: "No Children" → Skip automation

Door Close Event (Light Already On):
├─ Both Doors Now Closed
│  └─ Action: Full all lights (155 + 255)
│     └─ Reason: Adults can use normal brightness
├─ Only Leo's Door Closed
│  └─ Action: Full all lights
├─ Only Ashlee's Door Closed
│  └─ Action: Full all lights
└─ Home Mode: NOT "Normal" → Skip automation
```

**Integration with Motion Detection:**

After bedtime motion also checks door states:
```
Motion + Dark + After Bedtime:
├─ "No Children" Mode → Full brightness
├─ Both doors closed + both automations on → Full brightness
├─ Both doors open + both automations on → Dim brightness
├─ Only Leo automation on + Leo's door closed → Dim
└─ Only Ashlee automation on + Ashlee's door closed → Full
```

**Personalization Rationale:**
- Different children have different light sensitivities
- Leo: Prefers dimmer light (less disruptive to sleep)
- Ashlee: Needs brighter light (safety/confidence)
- System respects individual needs while maintaining safety

---

### Illuminance-Based Smart Triggering

**Threshold System:**
- Sensor: sensor.stairs_motion_illuminance (lux)
- Threshold: input_number.stairs_light_level_threshold
- Comparison: illuminance < threshold → dark enough for lights

**Smart Logic:**
```
Motion Detected:
   ↓
Check Illuminance
├─ Current reading: {{ states('sensor.stairs_motion_illuminance') }} lux
├─ Threshold: {{ states('input_number.stairs_light_level_threshold') }} lux
└─ Comparison: < threshold?
   ├─ YES → Proceed with lighting automation
   └─ NO → Skip (already bright enough)
```

**Benefits:**
- Prevents lights turning on during bright daylight
- Saves energy (no unnecessary activations)
- User-configurable threshold (input_number)
- Logged in messages for troubleshooting

**Example Log Messages:**
```
"Motion on the upstairs, before bed time and it's dark
(3.2 lux < 5.0 lux). Turning light on."

"Motion upstairs and it's dark (2.1 lux < 5.0 lux) and
bedroom light is on. Turning light on."
```

---

### Night Light Mode Safety Override

**Three Night Mode States:**

```
After Midnight + Motion + Dark:
   ↓
Check 1: Bedroom Light State
├─ light.bedroom_lamps: "on"
│  └─ Action: Full brightness (someone awake)
│     └─ Reason: If bedroom light on, adults active
└─ Bedroom light: "off" → Continue
   ↓
Check 2: Night Light Setting
├─ input_boolean.enable_stairs_night_light: "on"
│  └─ Action: Ultra-dim red night light
│     ├─ Brightness: 5 (2% of max)
│     ├─ Hue: 358° (deep red)
│     └─ Reason: Preserve night vision
└─ Night light setting: "off"
   └─ Action: Full brightness (safety override)
      └─ Reason: Prevent falls in darkness
```

**Safety Philosophy:**
- Default to FULL BRIGHTNESS if night mode disabled
- Rationale: Falls in darkness more dangerous than sleep disruption
- Red light option for those who want minimal disruption
- Bedroom light awareness detects if someone already awake

**Night Light Color Choice:**
- Red wavelength (358° hue) preserves night vision
- 100% saturation for pure color
- Brightness 5 (minimum visible level)
- Less disruptive to sleep than white light

---

### Magic Mirror Multi-Trigger Energy Management

**Four Trigger Types:**

```
1. Living Room Motion (ID: motion_on_living_room)
   └─ Shared display, activate from either room

2. Stairs Motion (ID: motion_on_stairs)
   └─ Direct proximity, activate when present

3. No Stairs Motion for 3 Minutes (ID: motion_off_stairs)
   └─ Time: 23:00-05:00 only (night shutdown)

4. Scheduled Time 23:30 (ID: night_shutdown)
   └─ Time: 23:00-05:00 only (forced shutdown)
```

**Decision Tree:**
```
Trigger → Check Conditions → Action
   ↓
┌─────────────────────────────────────────────────┐
│ Motion Triggers (living_room OR stairs)        │
│ ├─ Mirror currently: off                        │
│ ├─ Stairs motion enabled: on                    │
│ ├─ Magic Mirror automation: on                  │
│ └─ Action: Turn on switch.magic_mirror_plug     │
├─────────────────────────────────────────────────┤
│ No Motion Trigger (stairs 3 min) OR Time 23:30 │
│ ├─ Current time: 23:00-05:00                    │
│ ├─ Mirror currently: on                         │
│ └─ Action: Turn off switch.magic_mirror_plug    │
├─────────────────────────────────────────────────┤
│ Weekday Daytime Idle (separate automation)     │
│ ├─ No stairs motion: 5 minutes                  │
│ ├─ Time: 09:00-17:30                            │
│ ├─ Day: Monday-Friday                           │
│ └─ Action: Turn off switch.magic_mirror_plug    │
└─────────────────────────────────────────────────┘
```

**Timeout Strategy:**
- Night: 3 minutes (quick shutdown, save energy)
- Weekday: 5 minutes (allow longer viewing)
- Forced: 23:30 (regardless of motion)

**Energy Savings:**
- Typical work hours (09:00-17:30): Auto-off when idle
- Night hours (23:00-05:00): Aggressive shutdown
- Only on when actively used

---

### Person Detection Security Integration

**Frigate AI Integration:**
```
Camera: camera.stairs_high_resolution_channel
   ↓
Frigate AI Processing
   ↓
Person Detected → binary_sensor.stairs_person_detected: ON
   ↓
Check Alarm State
└─ alarm_control_panel.house_alarm
   ├─ State: "armed_away"
   │  └─ SECURITY EVENT (continue)
   └─ Any other state
      └─ NORMAL OCCUPANCY (ignore)
```

**Security Actions (Parallel Execution):**
```
1. Snapshot Capture:
   ├─ Camera: stairs_high_resolution_channel
   ├─ Filename: Template from input_text
   │  └─ input_text.latest_frigate_upstairs_person_file_path
   └─ Quality: High resolution for evidence

2. Notification with Attachment:
   ├─ Script: send_home_log_with_local_attachments
   ├─ Title: "Person detected on stairs"
   ├─ Message: "Frigate detected a person on the stairs."
   ├─ Attachment: Snapshot file path
   └─ Delivery: Immediate push notification
```

**Queue Management:**
- Mode: Queued (max 10)
- Handles rapid successive detections
- No events lost during processing
- Each detection gets snapshot + notification

**Security Benefits:**
- Only active when house unoccupied
- High-resolution evidence capture
- Immediate notification with image
- AI reduces false positives (vs motion-only)
- Template file path allows organization/archiving

---

### Physical Switch Manual Override

**Always-Available Control:**
```
Physical Wall Switch (binary_sensor.stairs_light_input_0_input)
   ↓
State Change (any transition)
   ├─ Exclude: unknown states
   ├─ Exclude: unavailable states
   └─ Valid state change → Continue
   ↓
Action: Toggle light.stairs
├─ Transition: 1 second (smooth)
├─ Brightness: 255 (always full)
└─ Mode: Single (prevent multiple toggles)
```

**Override Philosophy:**
- Works REGARDLESS of automation enable states
- Always full brightness (no dim mode)
- Simple toggle (on→off, off→on)
- 1-second transition for smooth activation
- No dependency on motion/time/doors

**Coexistence with Automation:**
- Physical switch and motion automation independent
- Manual on → stays on until manually off or motion timeout
- Motion automation can still trigger
- No conflicts (separate control paths)

---

**Last Updated:** 2026-01-24
**Documentation Version:** 1.0
**Automation Count:** 14
**Device Count:** 20+ entities
**Scene Count:** 9
**Script Count:** 0 (uses global scripts)
**Configuration Files:** 1 (stairs.yaml)
**Special Integrations:** Frigate AI (person detection), Magic Mirror (MQTT plug), Children's bedroom doors, House alarm
