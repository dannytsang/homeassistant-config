# Bathroom Setup Documentation

**Last Updated:** 2026-01-25
**Package:** packages/rooms/bathroom.yaml
**Maintainer:** Danny Tsang
**Status:** ✅ Operational

---

## 1. Device Inventory

### Lighting Systems

**Bathroom Lights**
- `light.bathroom` - Primary bathroom light (ceiling)
- `light.bathroom_lights` - Coordinated bathroom lighting suite

**Features:**
- Dimmable brightness control
- Motion-triggered automation
- Manual switch override
- Timer-based auto-off

---

### Environmental Sensors

**Humidity Monitoring**
- `sensor.bathroom_motion_humidity` - Humidity level from motion sensor
  - Trigger: High humidity detection (>70-80%)
  - Purpose: Ventilation/exhaust fan trigger

**Light Level Sensing**
- `sensor.bathroom_area_mean_light_level` - Ambient light level
  - Used for: Determining if lights needed (day vs night)
  - Prevents unnecessary light activation during day

---

### Access & Safety

**Door & Window Monitoring**
- `binary_sensor.bathroom_door_contact` - Door open/closed detection
  - Used for: Privacy, occupancy awareness

- `binary_sensor.bathroom_window_contact` - Window open/closed
  - Used for: Ventilation coordination
  - Can prevent exhaust fan if window open

---

### Special Integrations

**Toothbrush Tracking**
- Integration: Electric toothbrush (Bluetooth or app-based)
  - "Danny's Toothbrush" automation
  - Triggers: Toothbrush on/off events
  - Purpose: Track personal health routines (brushing reminders/tracking)

---

### Control & Scheduling

**Timer Management**
- `timer.bathroom_light_off` - Auto-shutoff timer for lights
  - Duration: Configurable (typically 20-30 minutes)
  - Purpose: Prevent lights left on accidentally

---

## 2. Automation Functions

### 2.1 Motion-Based Lighting (2 automations)

#### Motion Detected
- **ID:** \[varies]
- **Trigger:** Motion detected in bathroom area
- **Conditions:**
  - Bathroom automation enabled
  - Optional: Time range (only certain hours)
  - Optional: Light level check (only at night)
- **Actions:**
  - Turn on lights to 100%
  - Set warm color temperature (if color-capable)
  - Cancel any pending light-off timer
  - Log motion event
- **Mode:** Single
- **Purpose:** Automatic lighting on occupancy

---

#### No Motion Detected
- **ID:** \[varies]
- **Trigger:** Motion stops (no motion for 5-10 minutes)
- **Conditions:**
  - Lights are currently on
  - Bathroom automation enabled
- **Actions:**
  - Start light-off timer (10-20 minute countdown)
  - Log no-motion event
  - Optional: Dim lights to 50% as warning
- **Mode:** Single
- **Purpose:** Initiate auto-off sequence after vacancy

---

### 2.2 Light Control (3 automations)

#### Light Turned Off
- **ID:** \[varies]
- **Trigger:** Lights turn off (any method: automation, manual, or timer finish)
- **Conditions:**
  - Lights transitioned from on → off
- **Actions:**
  - Cancel light-off timer
  - Log light-off event
  - Optional: Trigger humidity check if high
- **Mode:** Single
- **Purpose:** Cleanup when lights manually turned off

---

#### Light Switch Toggled
- **ID:** \[varies]
- **Trigger:** Physical light switch pressed (or smart switch entity changed)
- **Conditions:** None
- **Actions:**
  - Toggle lights on/off based on current state
  - Cancel any active timers
  - Log manual control action
- **Mode:** Single
- **Purpose:** Allow manual override of automation

---

#### Light Timer Finished
- **ID:** \[varies]
- **Trigger:** timer.bathroom_light_off expires
- **Conditions:**
  - No motion detected recently (double-check)
  - Lights are still on
- **Actions:**
  - Turn off lights
  - Log: "Auto-shutoff after X minutes"
  - Optional: Turn on night light (low brightness)
- **Mode:** Single
- **Purpose:** Final auto-off after inactivity timer expires

---

### 2.3 Environmental Control (1 automation)

#### High Humidity
- **ID:** \[varies]
- **Trigger:** Humidity rises above threshold (>75-80%)
- **Conditions:**
  - Humidity automation enabled
  - Window not already open (redundant ventilation check)
- **Actions:**
  - Turn on exhaust fan (switch.bathroom_exhaust_fan)
  - Log humidity event
  - Optional: Notification if humidity critical (>90%)
  - Optional: Set reminder to open window
- **Mode:** Single
- **Purpose:** Automatic ventilation to prevent mold/moisture

---

### 2.4 Personal Routine Tracking (1 automation)

#### Danny's Toothbrush
- **ID:** \[varies]
- **Trigger:** Electric toothbrush turns on/off
- **Conditions:** None
- **Actions:**
  - Log toothbrush usage (time, duration)
  - Optional: Notification if brushing time too short (<2 min)
  - Optional: Daily reminder if not used by certain time
  - Optional: Store metrics for health insights
- **Mode:** Single
- **Purpose:** Health routine tracking and reminder

---

## 3. Room Layout & Device Placement

```
                    BATHROOM LAYOUT

    ╔════════════════════════════════════════════╗
    ║                                            ║
    ║   🚪 DOOR (contact sensor)                ║
    ║   [Privacy monitoring + occupancy]         ║
    ║                                            ║
    ║   💡 LIGHTS                               ║
    ║   ├─ Ceiling light (motion-triggered)     ║
    ║   ├─ Motion auto-on                       ║
    ║   ├─ Timer auto-off (10-20 min)           ║
    ║   └─ Manual switch override               ║
    ║                                            ║
    ║   👁️ MOTION SENSOR                        ║
    ║   ├─ Ceiling mounted                      ║
    ║   ├─ Detects presence                     ║
    ║   ├─ Measures humidity                    ║
    ║   └─ Measures light level                 ║
    ║                                            ║
    ║   🪟 WINDOW (contact sensor)              ║
    ║   ├─ Open/closed detection                ║
    ║   └─ Ventilation coordination             ║
    ║                                            ║
    ║   💨 EXHAUST FAN                          ║
    ║   ├─ Humidity-triggered                   ║
    ║   ├─ Motion deactivated                   ║
    ║   └─ Window sensor coordination           ║
    ║                                            ║
    ║   🪥 ELECTRIC TOOTHBRUSH                  ║
    ║   ├─ Usage tracking                       ║
    ║   ├─ Duration monitoring                  ║
    ║   └─ Health routine logging               ║
    ║                                            ║
    ║   ⏱️ TIMERS                                ║
    ║   ├─ Light auto-off (10-20 min)           ║
    ║   └─ Humidity clearing timer              ║
    ║                                            ║
    ╚════════════════════════════════════════════╝
```

---

## 4. Key Automation Workflows

### 4.1 Daily Bathroom Usage (Typical Morning)

```
Danny wakes up and enters bathroom
        ↓
Motion detected
        ↓
"Motion Detected" automation triggers
        ├─ Lights turn on to 100%
        ├─ Warm color temp applied
        └─ Light-off timer cancelled
        ↓
Danny uses facilities/showers
        ↓
Motion continuously detected (stays on)
        ↓
Danny uses toothbrush
        ↓
"Danny's Toothbrush" automation triggers
        ├─ Logs toothbrush session
        ├─ Records duration
        └─ Optional: Notification if < 2 min (poor brushing)
        ↓
Shower creates high humidity
        ↓
"High Humidity" automation triggers
        ├─ Exhaust fan turns on
        ├─ Humidity monitoring continues
        └─ Optional: Window open reminder
        ↓
Danny exits bathroom, motion stops
        ↓
"No Motion Detected" automation triggers
        ├─ Start 15-minute light-off timer
        ├─ Optional: Dim lights to 50% as warning
        └─ Exhaust fan continues (humidity clearing)
        ↓
After 15 minutes with no motion
        ↓
"Light Timer Finished" automation triggers
        ├─ Lights turn off automatically
        ├─ Log: "Auto-shutoff after 15 min"
        └─ Optional: Night light activates (low 10% warm)
        ↓
Exhaust fan continues until humidity drops
```

---

### 4.2 Manual Light Control

**When Guest Uses Bathroom**

```
Guest enters bathroom
        ↓
Motion triggers lights on (automatically)
        ↓
Guest prefers lights off (too bright)
        ↓
Guest toggles physical switch
        ↓
"Light Switch Toggled" automation triggers
        ├─ Lights turn off immediately
        ├─ Cancel light-off timer
        └─ Log manual override
        ↓
Guest uses bathroom with preference respected
```

---

### 4.3 Humidity & Ventilation Workflow

**After Hot Shower**

```
Shower running
        ↓
Moisture accumulates
        ↓
Humidity sensor reading rises: 65% → 75%
        ↓
"High Humidity" automation triggers
        ├─ Exhaust fan: OFF → ON
        ├─ Noise: Fan running
        └─ Logging humidity event
        ↓
Window still closed (cool day, don't want AC loss)
        ├─ Exhaust fan is primary ventilation
        └─ Optional: Reminder "Consider opening window"
        ↓
Fan runs continuously
        ↓
Humidity drops: 75% → 60%
        ↓
Automation condition no longer met
        ├─ Fan turns off
        └─ Damp air cleared
```

---

## 5. Configuration Parameters

### Input Numbers (Configurable Thresholds)

| Entity | Purpose | Range | Default |
|--------|---------|-------|---------|
| `input_number.bathroom_humidity_threshold` | % to trigger exhaust fan | 60-90 | 75 |

---

## 6. Helper Entities & Integrations

### Timers

| Entity | Purpose | Duration |
|--------|---------|----------|
| `timer.bathroom_light_off` | Auto-off countdown | 10-20 minutes |

### External Integrations

| System | Purpose | Details |
|--------|---------|---------|
| Electric Toothbrush App/BLE | Usage tracking | Health routine logging |
| Exhaust Fan Switch | Ventilation control | Humidity-triggered |

---

## 7. Scripts Used

**Scripts Not Defined in bathroom.yaml** - Uses shared scripts:

- `script.send_to_home_log` - Log automation events
- `script.send_direct_notification` - Alert on high humidity
- `script.toothbrush_reminder` - Daily brushing reminder (if implemented)

---

## 8. Sensors & Tracking

### Monitored States

- **Lights:** On/Off status
- **Motion:** Presence detected or not
- **Humidity:** Current % and trending up/down
- **Light Level:** Ambient brightness
- **Door:** Open/Closed for privacy
- **Window:** Open/Closed for ventilation
- **Toothbrush:** On/Off, duration of sessions

### Health Data Collected

| Metric | Storage | Purpose |
|--------|---------|---------|
| Toothbrush sessions | History | Daily routine tracking |
| Session duration | History | Health awareness |
| Missed sessions | Alert log | Reminder notifications |
| Peak humidity levels | Statistics | Ventilation effectiveness |

---

## 9. Status Indicators

### Light Status

- **Off** → Lights extinguished
- **On** → Full brightness active
- **Dimmed** → 50% warning (motion stopping)
- **Night Light** → 10% warm (low-visibility mode)

### Humidity Status

- **Normal** → <60% (dry, safe)
- **Elevated** → 60-75% (slightly damp)
- **High** → 75-85% (exhaust active)
- **Critical** → >85% (potential mold risk)

### Motion Status

- **Active** → Movement detected, lights stay on
- **Inactive** → No motion, timer started
- **Timeout** → Timer expired, lights off

### Ventilation Status

- **Off** → Humidity below threshold
- **Running** → Exhaust fan clearing moisture
- **Long Run** → Critical humidity or window-closed mode

---

## 10. Key Features & Automations Highlights

### Smart Motion-Based Lighting
- **Automatic On:** No switches to flip when entering
- **Graceful Off:** Timer prevents lights left on accidentally
- **Manual Override:** Switch always works independently
- **Daylight Aware:** Doesn't activate if already bright

### Humidity Management
- **Automatic Ventilation:** Fan runs when needed
- **Mold Prevention:** Keeps moisture under control
- **Window Coordination:** Respects open/closed status
- **Customizable Threshold:** Adjust for your climate

### Health Routine Tracking
- **Toothbrush Logging:** Automatic usage tracking
- **Reminders:** Alerts if brushing too short
- **Historical Data:** See patterns over time
- **Privacy-First:** Data stays local, not cloud-synced

### User-Friendly Design
- **Minimal Intervention:** Motion does most work
- **Manual Control:** Always respected (switch overrides)
- **Logical Defaults:** Warm light, 10-20 min timeout
- **Accessible:** Works for family members of all ages

---

## Implementation Notes

### Motion Sensor Setup

1. **Sensor Placement**
   - Mount on ceiling, angled toward main entry/mirror
   - Avoid mounting directly above heat source (shower)
   - Clear line-of-sight to bathroom area

2. **Sensitivity Calibration**
   - Adjust to detect person entering
   - Avoid false triggers from shower steam
   - Test with typical movements (standing, sitting)

3. **Detection Range**
   - Small bathroom: Usually 6-8 feet detection OK
   - Set timer for 5-10 minutes (adjust based on usage)

---

### Humidity Sensor Setup

1. **Calibration**
   - Baseline reading with door open (outdoor humidity%)
   - Test threshold during/after shower (peak humidity)
   - Typical bathroom peak: 75-85% (varies by ventilation)

2. **Threshold Selection**
   - Conservative: 70% (fan runs often, but safe)
   - Moderate: 75% (standard recommendation)
   - Aggressive: 80% (saves fan runtime)

3. **Placement**
   - Often integrated in motion sensor
   - Avoid direct water spray
   - Keep sensor dry

---

### Timer Configuration

1. **Timeout Duration**
   - 10 minutes: Quick auto-off (save energy)
   - 15-20 minutes: Standard (typical bathroom use)
   - 30 minutes: Extended (large family)

2. **Warning System**
   - Optional: Dim to 50% at 5-min mark (user warning)
   - Optional: Notification before cutoff
   - Manual switch always works (no timeout affects it)

---

## Testing Checklist

- [ ] Motion detected → Lights on within 2 seconds
- [ ] No motion 10 min → Timer starts countdown
- [ ] Timer expires → Lights off automatically
- [ ] Manual switch press → Override works anytime
- [ ] High humidity (>75%) → Exhaust fan turns on
- [ ] Humidity drops (<70%) → Exhaust fan turns off
- [ ] Window open → Exhaust fan operates normally
- [ ] Toothbrush on → Usage event logged
- [ ] Toothbrush off → Duration recorded
- [ ] Light-off timer → Can be cancelled by motion
- [ ] Motion → All timers reset

---

## Troubleshooting Guide

### Lights Won't Turn On on Motion

**Symptoms:** Motion detected but lights stay off

**Diagnosis:**
1. Check motion sensor is powered/connected
2. Verify automation is enabled
3. Check light entity responds to manual commands
4. Check time/conditions (maybe disabled during day?)

**Solutions:**
- Power cycle motion sensor
- Test automation manually in UI
- Verify light is controlled by correct entity
- Check if daylight-only mode is active

---

### Lights Stay On Too Long

**Symptoms:** Lights stay on hours after leaving bathroom

**Diagnosis:**
1. Check motion sensor (may be detecting water movement)
2. Verify light-off timer is configured
3. Check timer automation is enabled

**Solutions:**
- Move motion sensor away from shower area
- Reduce timer duration (15 min → 10 min)
- Test manual light-off to verify it works
- Check for continuous motion triggers

---

### Exhaust Fan Won't Turn On

**Symptoms:** Humidity high but fan doesn't activate

**Diagnosis:**
1. Check humidity reading is actually high (sensor reading)
2. Verify exhaust fan switch exists and is controllable
3. Check humidity automation is enabled
4. Verify humidity threshold setting

**Solutions:**
- Calibrate humidity threshold (lower if needed)
- Test fan manual control in UI
- Verify exhaust fan switch entity is correct
- Check automation logs for errors

---

## Related Documentation

- **Main package:** `packages/rooms/bathroom.yaml`
- **Related:** Other room setups for motion/automation patterns
- **Humidity Control:** Home Assistant docs for sensor calibration

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-25 | Initial documentation generation | Claude Code |
| TBD | Motion sensor calibration | Danny Tsang |
| TBD | Humidity threshold tuning | Danny Tsang |

---

**Documentation Status:** ✅ Complete
**Last Review:** 2026-01-25
**Next Review:** 2026-02-25
