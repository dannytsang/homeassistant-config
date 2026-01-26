# Bedroom 2 (Leo's Bedroom) Setup Documentation

**Last Updated:** 2026-01-25
**Package:** packages/rooms/bedroom2.yaml
**Maintainer:** Danny Tsang
**Status:** ✅ Operational

---

## 1. Device Inventory

### Lighting Systems

**Main Lights**
- `light.leos_bedroom_main_light` - Primary ceiling light (dimmable, RGB capable)
- `light.leo_s_bedroom_lights` - Coordinated bedroom lighting suite

**Features:**
- Circadian rhythm color temperature (cool in morning, warm at night)
- Scheduled transitions throughout day
- Remote control integration
- Manual override capability

---

### Window & Blind Control

**Motorized Blinds**
- `cover.leos_bedroom_blinds` - Motorized roller blinds
  - Position tracking (0-100%)
  - Timed open/close automation
  - Wake-up triggered opening
  - Sunrise/sunset awareness

---

### Occupancy & Environmental Sensing

**Occupancy Detection**
- `binary_sensor.leos_bed_occupied` - Bed occupancy sensor (pressure mat)
  - Used for: Wake-up detection, bedtime routines
  - Trigger: Automation when Leo gets in/out of bed

**Window & Security**
- `binary_sensor.leos_bedroom_window_contact` - Window contact sensor
  - Open/closed detection
  - Night-time security (close blinds if window open)

**Time Awareness**
- `binary_sensor.workday_sensor` - Workday indicator
  - Monday-Friday: Working day
  - Saturday-Sunday: Weekend
  - Used for: Different blind open times (school vs no school)

---

### Control Interfaces

**Remote Control**
- 4-button RF remote or similar
  - Button functions: On, Off, Up (brighten), Down (dim)
  - Direct light control independent of automations
  - Wake-up scene trigger capability

---

## 2. Automation Functions

### 2.1 Lighting Control (2 automations)

#### Light Switch Toggle
- **Trigger:** Manual light switch press (physical or smart switch)
- **Conditions:** None
- **Actions:**
  - Toggle lights on/off based on current state
  - Log action to home log
- **Mode:** Single
- **Purpose:** Basic on/off control for manual use

---

#### Apply Circadian Color Temperature
- **Trigger:** Light turns on (any method: automation, manual, remote)
- **Conditions:**
  - Light is now on
  - Circadian automation enabled
- **Actions:**
  - Apply color temperature based on current time of day
  - Cool (5000K+) in morning (alertness)
  - Neutral (4000K) midday
  - Warm (2700K) evening (sleep prep)
- **Mode:** Single
- **Purpose:** Health-aware lighting matching circadian rhythm

---

### 2.2 Scheduled Lighting (1 automation)

#### Scheduled Circadian Transitions
- **Trigger:** Time-based at specific hours throughout day
- **Conditions:**
  - Lights are on
  - Circadian automation enabled
- **Actions:**
  - Smoothly transition color temperature (no jarring changes)
  - Timeline:
    - 6 AM: Cool white (wake-up brightness)
    - 9 AM: Neutral white
    - 3 PM: Bright neutral
    - 6 PM: Warm white transition begins
    - 8 PM: Warm white (sleep prep)
- **Mode:** Single
- **Purpose:** Automatic daily circadian lighting routine

---

### 2.3 Blind Control - Timed (3 automations)

#### Timed Open Blinds Weekday
- **Trigger:** Time 7:00 AM on weekdays
- **Conditions:**
  - It's a workday (school day)
  - Blind automation enabled
  - Blinds not already open
- **Actions:**
  - Open blinds to 100% (with transition)
  - Purpose: Morning natural light for school prep
- **Mode:** Single
- **Purpose:** Weekday morning routine (school mornings)

---

#### Timed Open Blinds Weekend No Children Mode
- **Trigger:** Time 9:00 AM on weekends
- **Conditions:**
  - It's NOT a workday (weekend)
  - Blind automation enabled
  - Blinds not already open
- **Actions:**
  - Open blinds to 100% (slower transition)
  - Purpose: Gentle weekend wake-up
- **Mode:** Single
- **Purpose:** Weekend morning routine (no school rush)

---

#### Timed Close Blinds
- **Trigger:** Time at sunset or 7:00 PM (whichever later)
- **Conditions:**
  - After sunset (seasonal accuracy)
  - Blind automation enabled
- **Actions:**
  - Close blinds to 0% (full closure)
  - Purpose: Evening privacy + sleep prep
- **Mode:** Single
- **Purpose:** Evening privacy and darkness for sleep

---

### 2.4 Blind Control - Event-Based (4 automations)

#### Close Blinds Before Sun Rise
- **Trigger:** Time 30 minutes before sunrise
- **Conditions:**
  - Blind automation enabled
  - Winter (shorter days) - seasonal adaptation
- **Actions:**
  - Close blinds if still open
  - Purpose: Block early morning light in winter
- **Mode:** Single
- **Purpose:** Extended sleep in winter mornings

---

#### Open Blinds In The Morning
- **Trigger:** Time at sunrise
- **Conditions:**
  - Blind automation enabled
  - Blinds closed
  - Optional: If not a weekend
- **Actions:**
  - Open blinds (2-minute transition)
  - Natural light wakes Leo naturally
- **Mode:** Single
- **Purpose:** Natural light-based wake-up cue

---

#### Open Blinds When Leo Wakes Up
- **Trigger:** Bed occupancy changes from "on" to "off" (Leo gets out of bed)
- **Conditions:**
  - Morning time (6-9 AM window)
  - Blinds closed
  - Bed sensor enabled
- **Actions:**
  - Open blinds fully
  - Turn on lights to warm color
  - Optional: Alexa announcement "Good morning!"
- **Mode:** Single
- **Purpose:** Positive reinforcement when Leo wakes up naturally

---

#### Window Closed At Night
- **Trigger:** Window contact changes to closed
- **Conditions:**
  - After sunset
  - Before sunrise
  - Blind automation enabled
- **Actions:**
  - Close blinds for security/privacy
  - Log window closure
- **Mode:** Single
- **Purpose:** Safety and privacy when window closed at night

---

### 2.5 Remote Control (2 automations)

#### Remote Turn On
- **Trigger:** Remote button 1 pressed
- **Conditions:** None
- **Actions:**
  - Turn on lights to 100%
  - Set warm color temperature
  - Cancel any pending off timers
- **Mode:** Single
- **Purpose:** Quick light activation via remote

---

#### Remote Turn Off
- **Trigger:** Remote button 2 pressed
- **Conditions:** None
- **Actions:**
  - Turn off lights immediately
  - Log remote action
- **Mode:** Single
- **Purpose:** Quick light shutdown via remote

---

#### Remote Up (Brighten)
- **Trigger:** Remote button 3 pressed (or dial up)
- **Conditions:** None
- **Actions:**
  - Increase brightness by 10% (per press)
  - Cap at 100%
- **Mode:** Single
- **Purpose:** Fine-tune brightness upward

---

#### Remote Down (Dim)
- **Trigger:** Remote button 4 pressed (or dial down)
- **Conditions:** None
- **Actions:**
  - Decrease brightness by 10% (per press)
  - Floor at 10% (don't turn off)
- **Mode:** Single
- **Purpose:** Fine-tune brightness downward

---

## 3. Room Layout & Device Placement

```
                    LEO'S BEDROOM LAYOUT

    ╔════════════════════════════════════════════╗
    ║                                            ║
    ║   🪟 WINDOW (contact sensor)              ║
    ║   [Motorized Blinds]                      ║
    ║   ├─ Timed open/close                     ║
    ║   ├─ Wake-up triggered                    ║
    ║   └─ Manual remote control                ║
    ║                                            ║
    ║   💡 CEILING LIGHTS                       ║
    ║   ├─ Main light (RGB dimmable)            ║
    ║   ├─ Coordinated suite                    ║
    ║   ├─ Circadian color temp                 ║
    ║   └─ Remote + manual control              ║
    ║                                            ║
    ║   🛏️ BED (center)                         ║
    ║   ├─ Bed occupancy sensor                 ║
    ║   ├─ Wake-up detection                    ║
    ║   └─ Get-out-of-bed trigger               ║
    ║                                            ║
    ║   📱 REMOTE CONTROL                       ║
    ║   ├─ Button 1: On (warm white)            ║
    ║   ├─ Button 2: Off (immediate)            ║
    ║   ├─ Button 3: Brightness up (+10%)       ║
    ║   ├─ Button 4: Brightness down (-10%)     ║
    ║   └─ Direct light control                 ║
    ║                                            ║
    ║   🌡️ ENVIRONMENT                          ║
    ║   ├─ Temperature monitoring (if available) ║
    ║   └─ Workday detection (school schedule)  ║
    ║                                            ║
    ╚════════════════════════════════════════════╝
```

---

## 4. Key Automation Workflows

### 4.1 Weekday School Morning Routine

**7:00 AM on School Days**

```
Alarm time: 7:00 AM on weekday
        ↓
Multiple automations trigger simultaneously:
        ├─ Timed Open Blinds Weekday
        │  └─ Blinds open to 100% (signals wake-up time)
        │
        ├─ Lights ready to turn on (if Leo manually activates)
        │
        └─ System ready for day
        ↓
Leo sees morning light from open blinds
        ↓
Natural light cue helps Leo wake up
        ↓
When Leo gets out of bed (occupancy sensor detects):
        ├─ "Open Blinds When Leo Wakes Up" triggers
        ├─ Lights turn on with warm color
        ├─ Optional: Alexa announces "Good morning!"
        └─ Leo ready for school prep
```

---

### 4.2 Evening Wind-Down Routine

**6:00 PM onwards**

```
Approaching sunset
        ↓
Scheduled Circadian Transitions activate
        ├─ 6 PM: Warm white transition begins
        └─ 8 PM: Full warm white for sleep prep
        ↓
At sunset + 15 minutes → Timed Close Blinds triggers
        ├─ Blinds close to 0%
        ├─ Privacy established
        └─ Darkness prepares body for sleep
        ↓
Evening lighting supports melatonin production
        ↓
Bedtime routine can proceed
```

---

### 4.3 Wake-Up Light Alarm (Alternative)

**Using Bed Occupancy Sensor**

```
Leo in bed at night (occupancy on)
        ↓
Morning hours (6-9 AM)
        ↓
Leo gets out of bed (occupancy off)
        ↓
"Open Blinds When Leo Wakes Up" automation triggers
        ├─ Blinds open immediately
        ├─ Lights turn on with warm white
        ├─ Gentle wake-up without harsh alarm
        └─ Natural wake-up support
        ↓
Leo starts day gradually and naturally
```

---

### 4.4 Remote Control Scenarios

**Scenario 1: Quick Wake-Up (No Morning Routine)**

```
Leo still in bed, needs light NOW
        ↓
Press Remote Button 1
        ↓
Lights turn on to 100%
        ├─ Warm color temperature applied
        └─ Immediate brightness
        ↓
Leo can see without additional automation
```

**Scenario 2: Fine-Tuning Brightness**

```
Lights are on but not quite right brightness
        ↓
Press Remote Button 3 (Up) or 4 (Down)
        ↓
Brightness adjusts by 10% per press
        ├─ Up: +10% (max 100%)
        └─ Down: -10% (min 10%, won't turn off)
        ↓
Fine-tuned to perfect level
```

---

## 5. Configuration Parameters

### Input Booleans

| Entity | Purpose | Default |
|--------|---------|---------|
| `input_boolean.enable_circadian_lighting` | Enable/disable color temp automation | On |
| `input_boolean.enable_blind_automations` | Enable/disable blind control | On |
| `input_boolean.enable_bed_sensor` | Use bed occupancy for automations | On |

### Input Numbers

| Entity | Purpose | Range | Default |
|--------|---------|-------|---------|
| `input_number.leo_wake_up_brightness` | Light level for wake-up | 0-100 | 80 |
| `input_number.leo_sleep_prep_color_temp` | Evening color temp (mireds) | 2000-5000 | 3500 |

### Input Select

| Entity | Purpose | Options |
|--------|---------|---------|
| `input_select.leo_sleep_schedule` | School vs no-school mode | School, No School, Custom |

### Input Datetime

| Entity | Purpose | Type |
|--------|---------|------|
| `input_datetime.leo_school_time` | School start time (for wake-up) | Time picker |

---

## 6. Helper Entities

### Timers & State Tracking

| Entity | Purpose | Duration |
|--------|---------|----------|
| Light-off timer (optional) | Prevents lights on all night | 30-60 minutes |
| Blind-open timer | Gradual blind opening | 2-3 minutes |

---

## 7. Scripts Used

**Scripts Not Defined in bedroom2.yaml** - Uses shared scripts:

- `script.send_to_home_log` - Log automation events
- `script.circadian_light_on` - Apply circadian color based on time
- `script.alexa_announce` - Optional wake-up announcement

---

## 8. Sensors & Tracking

### Monitored States

- **Bed Occupancy:** On/Off status (Leo in/out of bed)
- **Light State:** On/Off + brightness + color temperature
- **Blind Position:** 0-100% (fully closed to fully open)
- **Window Status:** Open/Closed for night monitoring

### Circadian Tracking

| Time | Color Temp | Brightness | Purpose |
|------|-----------|-----------|---------|
| 6:00 AM | Cool (5000K) | 100% | Wake-up, alertness |
| 9:00 AM | Neutral (4000K) | 100% | Daylight |
| 3:00 PM | Bright (5000K) | 100% | Afternoon peak |
| 6:00 PM | Warm (3000K) | 80% | Evening transition |
| 8:00 PM | Very Warm (2700K) | 60% | Sleep prep |

---

## 9. Status Indicators

### Light Status

- **Off** → No lights active
- **Cool White** → Morning mode (alertness)
- **Neutral White** → Midday mode
- **Warm White** → Evening/night mode
- **Fully Dimmed** → Sleep mode ready

### Blind Status

- **Open (100%)** → Full natural light, day mode
- **Closed (0%)** → Full privacy, night mode
- **Transitioning** → Automatic opening/closing in progress

### Bed Status

- **Occupied** → Leo in bed (bedtime)
- **Unoccupied** → Leo out of bed (awake)
- **Offline** → Sensor unavailable (use manual control)

---

## 10. Key Features & Automations Highlights

### Circadian Rhythm Support
- **Color Temperature Optimization:** Cool morning → Warm evening
- **Gradual Transitions:** No jarring light changes
- **Health Focus:** Supports natural sleep-wake cycle
- **Customizable Schedule:** Adjust colors per family preference

### Blind Automation Sophistication
- **Multiple Triggers:** Time-based, bed occupancy, sunrise/sunset
- **School Awareness:** Different schedules weekday vs weekend
- **Natural Wake-Up:** Blinds open helps body wake naturally
- **Security:** Closes at night for privacy

### Remote Control Flexibility
- **Direct Activation:** Overrides automation anytime
- **Fine-Tuning:** 10% brightness adjustments
- **Quick Actions:** On/Off for rapid changes
- **Independent:** Works without internet/automation

### Child-Appropriate Design
- **Gentle Wake-Up:** Natural light + warm colors (not jarring)
- **School Support:** Encourages early morning rising
- **Positive Routine:** Rewards good sleep habits
- **Safety:** Bed sensor tracks occupancy for awareness

---

## Implementation Notes

### Circadian Lighting Setup

1. **Color Temperature Understanding**
   - Kelvin scale: 2700K (very warm/orange) to 5000K+ (cool/blue)
   - Morning (5000K+): Increases cortisol (wake-up hormone)
   - Evening (2700K): Increases melatonin (sleep hormone)

2. **Light Bulb Requirements**
   - Must support "color temperature" changes (not just brightness)
   - RGB bulbs work well (can dial any color)
   - "Color temp" bulbs (CCT) provide cool-to-warm range
   - Smart bulbs (Philips Hue, etc.) recommended

3. **Timing Calibration**
   - Adjust times based on school start
   - Consider natural sunrise/sunset (varies seasonally)
   - Test for first 1-2 weeks before finalizing

---

### Blind Motor Setup

1. **Motor Installation**
   - Ensure smooth operation (no binding)
   - Test open/close cycles (30+ cycles)
   - Verify end-of-travel stops work

2. **Position Calibration**
   - Fully open = 100%
   - Fully closed = 0%
   - Test intermediate positions (50% = half-open)

3. **Automation Safety**
   - Add manual override capability
   - Emergency stop button (if applicable)
   - Power-fail safe (defaults to open or closed?)

---

### Bed Occupancy Sensor

1. **Sensor Type**
   - Pressure mat under mattress (most reliable for kids)
   - Weight threshold: Set to Leo's weight (usually 20-40 lbs)
   - Sensitivity: Adjust to avoid false triggers

2. **Calibration**
   - Test with Leo in bed (should trigger "on")
   - Test empty bed (should trigger "off")
   - Verify no false positives (jumping on bed = not sleeping)

---

## Testing Checklist

- [ ] Weekday 7 AM → Blinds open automatically
- [ ] Weekend 9 AM → Blinds open automatically
- [ ] Sunset → Blinds close automatically
- [ ] Lights turn warm in evening (6 PM+)
- [ ] Color transitions smooth (no jarring changes)
- [ ] Remote button 1 → Lights on (warm)
- [ ] Remote button 2 → Lights off
- [ ] Remote button 3 (up) → Brightness increases
- [ ] Remote button 4 (down) → Brightness decreases
- [ ] Bed sensor: Leo gets in → sensor = "on"
- [ ] Bed sensor: Leo gets out → sensor = "off"
- [ ] Window closed at night → Blinds close
- [ ] Morning light helps Leo wake naturally
- [ ] Evening warmth helps Leo sleep

---

## Troubleshooting Guide

### Lights Won't Change Color Temperature

**Symptoms:** Lights stay same color all day

**Diagnosis:**
1. Check bulbs support color temperature (not just brightness)
2. Verify circadian automation is enabled
3. Check light entity is smart bulb, not dumb bulb

**Solutions:**
- Replace with RGB or color-temp bulbs
- Check automation logs for errors
- Verify light responds to manual color change in UI

---

### Blinds Not Opening/Closing on Schedule

**Symptoms:** Time passes but blinds don't move

**Diagnosis:**
1. Check blind motor is powered
2. Verify automation is enabled
3. Check blind entity responds to manual commands
4. Verify workday sensor is accurate

**Solutions:**
- Power cycle blind motor
- Test manual open/close in UI
- Check workday sensor for correct day
- Review automation logs for failures

---

### Remote Control Not Working

**Symptoms:** Remote buttons don't trigger lights

**Diagnosis:**
1. Check remote is paired with system
2. Verify remote batteries are fresh
3. Check automation is enabled
4. Verify light entity responds to commands

**Solutions:**
- Re-pair remote (follow integration instructions)
- Replace remote batteries
- Test light control manually in UI
- Check for signal interference

---

## Related Documentation

- **Main package:** `packages/rooms/bedroom2.yaml`
- **Related:** BEDROOM-SETUP.md (Master bedroom for comparison)
- **Circadian Light:** Reference HA automation docs for color temperature syntax

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-25 | Initial documentation generation | Claude Code |
| TBD | Circadian light tuning | Danny Tsang |
| TBD | Blind motor calibration | Danny Tsang |

---

**Documentation Status:** ✅ Complete
**Last Review:** 2026-01-25
**Next Review:** 2026-02-25
