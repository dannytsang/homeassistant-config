# Bedroom Setup Documentation

**Last Updated:** 2026-01-24
**Package:** packages/rooms/bedroom/bedroom.yaml
**Maintainer:** Danny Tsang
**Status:** ✅ Operational

---

## 1. Device Inventory

### Lighting Systems

**Main Lights**
- `light.bedroom_main_light` - Primary ceiling light (dimmable RGB capable)
- `light.bedroom_main_light_2` - Secondary ceiling light (coordinated with main)
- `light.bedroom_lamps` - Bedside lamps (paired control)
- `light.bedroom_clock_matrix` - Decorative clock display with RGB capability
- `light.under_bed_left` - Ambient under-bed lighting (left side)
- `light.under_bed_right` - Ambient under-bed lighting (right side)

**Stairwell Lights** (accessible from bedroom)
- `light.stairs` - Main stairwell light
- `light.stairs_2` - Secondary stairwell light
- `light.stairs_ambient` - Ambient stairwell lighting

**Scenes**
- `scene.bedroom_turn_on_ambient_light` - Full ambient mode (relaxation)
- `scene.bedroom_turn_off_ambient_light` - All ambient off
- `scene.bedroom_dim_ambient_light` - Dimmed ambient mode
- `scene.bedroom_desk_lamps_on` - Desk workspace lighting

---

### Window & Shade Control

- `cover.bedroom_blinds` - Motorized roller blinds with position tracking (0-100%)
  - Closed position threshold: input_number.blind_closed_position_threshold
  - Open position threshold: input_number.blind_open_position_threshold

---

### Environmental Sensors

**Binary Sensors**
- `binary_sensor.bed_occupied` - Occupancy detection (bed sensor, active high)
- `binary_sensor.bedroom_window_contact` - Window contact sensor (open: on, closed: off)
- `binary_sensor.bedroom_area_motion` - Motion detection (primary bedroom area)
- `binary_sensor.upstairs_area_motion` - Motion detection (upstairs general area)
- `binary_sensor.ashlees_bedroom_door_contact` - Ashlee's bedroom door contact
- `binary_sensor.leos_bedroom_door_contact` - Leo's bedroom door contact

**Other Sensors**
- `binary_sensor.bedroom_tv_powered_on` - TV power state detection
- `binary_sensor.workday_sensor` - Workday indicator (for automation logic)

---

### Climate & Ventilation

- `switch.bedroom_fan` - Ceiling fan (on/off control)

---

### Entertainment

- `media_player.bedroom_tv` - TV control and status
  - Integration: Home Assistant media_player
  - Actions: On/Off, Volume, Input selection

---

### External Data

- `weather.home` - Local weather forecast
  - Used for: Daytime brightness determination, temperature forecasting

---

## 2. Automation Functions

### 2.1 Blind Control Automations (5 automations)

#### Close Blinds When Someone Is In Bed After Sunset
- **ID:** 1601641236163
- **Trigger:** Bed occupied (state: off → on, 30s delay)
- **Conditions:**
  - Blinds currently open (position > threshold)
  - Blind automations enabled
  - After sunset (sun condition)
  - Window is closed
  - Bed sensor enabled
- **Action:** Close bedroom blinds
- **Mode:** Single
- **Purpose:** Privacy during sleeping hours

---

#### Window Closed At Night
- **ID:** 1622667464880
- **Trigger:** Window contact changes (open → closed)
- **Conditions:**
  - Blind automations enabled
  - After sunset
  - Before sunrise
  - Blinds not already closed
- **Action:** Close blinds
- **Mode:** Single
- **Purpose:** Automatic nighttime privacy when window closes

---

#### Window Closed And Someone Is In Bed At Night
- **ID:** 1615689096351
- **Trigger:** Window contact (open → closed, 30s delay)
- **Conditions:**
  - Blinds currently open
  - Blind automations enabled
  - After sunset
- **Actions:**
  - If bed sensor enabled: Close blinds
  - If bed sensor disabled: Turn on under-bed lights for 5 minutes
- **Mode:** Single
- **Purpose:** Privacy when in bed, light guidance when empty

---

#### Morning Timed Open Blinds
- **ID:** 1650650651310
- **Trigger:** Time-based at 7:00 AM
- **Conditions:**
  - Blind automations enabled
  - It's a workday
  - Blinds not already open
- **Action:** Open blinds to 100%
- **Mode:** Single
- **Purpose:** Morning light exposure for circadian rhythm

---

#### Evening Timed Close Blinds
- **ID:** 1735567472487
- **Trigger:** Time-based at sunset + 15 minutes
- **Conditions:**
  - Blind automations enabled
  - Blinds currently open
- **Action:** Close blinds
- **Mode:** Single
- **Purpose:** Consistent evening privacy schedule

---

### 2.2 Door & Entry Automations (3 automations)

#### Door Closed
- **ID:** 1622667464880
- **Trigger:** Bedroom door contact (any state change)
- **Conditions:**
  - Motion trigger enabled
- **Action:** Log door closure event
- **Mode:** Single

---

#### Other Bedroom Door Opens Warning
- **ID:** 1715955339483
- **Trigger:** Other bedroom door (Ashlee's) opens
- **Conditions:**
  - Bedroom motion trigger enabled
  - After sunset
  - Before sunrise
- **Action:** Send notification to primary user
- **Mode:** Single
- **Purpose:** Alert to door activity during sleep hours

---

#### Other Bedroom Door Closes Warning
- **ID:** 1601641292576
- **Trigger:** Other bedroom door closes
- **Conditions:**
  - Bedroom motion trigger enabled
- **Action:** Send notification
- **Mode:** Single

---

### 2.3 TV & Entertainment Automations (3 automations)

#### TV Turned On During Bright Day
- **ID:** 1715955339483
- **Trigger:** TV power (off → on)
- **Conditions:**
  - During daylight hours
  - Forecast high temp above threshold
- **Action:** Turn on bedroom main light
- **Mode:** Single
- **Purpose:** Automatic lighting when TV used during day

---

#### TV Turned Off
- **ID:** 1601641292576
- **Trigger:** TV power (on → off)
- **Conditions:**
  - After sunset
- **Actions:**
  - Dim lights to 20%
  - Set to ambient scene
  - Log action
- **Mode:** Single
- **Purpose:** Mood lighting when TV turned off at night

---

#### Pause TV When Door Opens At Night
- **ID:** 1708895092115
- **Trigger:** Bedroom door opens at night
- **Conditions:**
  - After sunset
  - TV is on
- **Action:** Pause media playback
- **Mode:** Single
- **Purpose:** Courtesy pause when entering/leaving room

---

### 2.4 Motion & Occupancy Automations (3 automations)

#### Motion Detected
- **ID:** 1622667464880
- **Trigger:** Motion detected in bedroom area
- **Conditions:**
  - Motion trigger enabled
  - After sunset
  - Before sunrise
- **Actions:**
  - Turn on main lights to 75%
  - Turn on ambient lights
  - Cancel any pending off timers
- **Mode:** Single
- **Purpose:** Automatic lighting when motion detected at night

---

#### No Motion
- **ID:** 1735567472487
- **Trigger:** Motion stops (no motion for 10 minutes)
- **Conditions:**
  - Motion trigger enabled
- **Actions:**
  - Start 5-minute lights-off timer
  - Set ambient to dim mode
- **Mode:** Single
- **Purpose:** Gradual transition to sleep state

---

#### No Motion For Long Time
- **ID:** 1735567472488
- **Trigger:** No motion for 30 minutes
- **Conditions:**
  - Motion trigger enabled
  - Bed not occupied
- **Action:** Turn off all lights
- **Mode:** Single
- **Purpose:** Energy saving when room not in use

---

#### No Motion And Fan Is On
- **ID:** 1735567472489
- **Trigger:** No motion detected (3 minutes) AND fan is on
- **Conditions:**
  - Motion trigger enabled
  - Fan currently on
- **Action:** Turn off ceiling fan
- **Mode:** Single
- **Purpose:** Energy saving - auto-fan shutdown

---

### 2.5 Fan Control Automations (1 automation)

#### Turn Off Fan
- **ID:** 1735567472490
- **Trigger:** Time-based (variable, controlled by helper)
- **Conditions:**
  - Fan currently on
  - Bedroom not occupied
- **Action:** Turn off fan
- **Mode:** Single

---

### 2.6 Remote Control Automations (6 automations)

#### Remote Button 1 (All Lights On)
- **ID:** 1735567472491
- **Trigger:** Remote button press (button 1)
- **Action:** Turn on all bedroom lights to full brightness
- **Mode:** Single

---

#### Remote Button 2 (Ambient Only)
- **ID:** 1735567472492
- **Trigger:** Remote button press (button 2)
- **Actions:**
  - Turn off main lights
  - Activate ambient scene
- **Mode:** Single

---

#### Remote Button 3 (All Off)
- **ID:** 1735567472493
- **Trigger:** Remote button press (button 3)
- **Action:** Turn off all lights
- **Mode:** Single

---

#### Remote Button 4 (Dim)
- **ID:** 1735567472494
- **Trigger:** Remote button press (button 4)
- **Action:** Dim all lights to 50%
- **Mode:** Single

---

#### Remote Dial Right (Brightness Up)
- **ID:** 1735567472495
- **Trigger:** Remote dial rotated right
- **Action:** Increase all lights brightness by 10%
- **Mode:** Single

---

#### Remote Dial Left (Brightness Down)
- **ID:** 1735567472496
- **Trigger:** Remote dial rotated left
- **Action:** Decrease all lights brightness by 10%
- **Mode:** Single

---

## 3. Room Layout & Device Placement

```
                    BEDROOM LAYOUT

    ╔════════════════════════════════════════╗
    ║                                        ║
    ║   🪟 WINDOW (contact sensor)          ║
    ║   [Motorized Blinds - cover]          ║
    ║                                        ║
    ║   👁️ Motion Sensor (ceiling)          ║
    ║                                        ║
    ║   💡 Ceiling Lights                   ║
    ║   ├─ Main Light (RGB dimmable)        ║
    ║   ├─ Secondary Light                  ║
    ║   └─ Clock Matrix Display             ║
    ║                                        ║
    ║   🛏️ BED (center)                     ║
    ║   ├─ Bed Occupancy Sensor             ║
    ║   ├─ Under-bed Left Light (RGB)       ║
    ║   ├─ Under-bed Right Light (RGB)      ║
    ║   ├─ Bedside Lamps (paired)           ║
    ║   └─ Remote Control                   ║
    ║                                        ║
    ║   📺 TV AREA                          ║
    ║   ├─ Media Player (TV)                ║
    ║   ├─ Power Sensor                     ║
    ║   └─ Ambient Lighting Scenes          ║
    ║                                        ║
    ║   🌀 FAN (ceiling)                    ║
    ║   └─ Motion-controlled shutdown       ║
    ║                                        ║
    ║   🚪 DOORS                            ║
    ║   ├─ Ashlee's Room Door               ║
    ║   ├─ Leo's Room Door                  ║
    ║   └─ Contact sensors on each          ║
    ║                                        ║
    ╚════════════════════════════════════════╝
```

---

## 4. Workflows

### 4.1 Morning Workflow (7:00 AM)

1. **Blinds Open** (if workday)
   - Time trigger: 7:00 AM
   - Action: Open blinds to 100%
   - Purpose: Circadian rhythm alignment, natural light

2. **Motion Detection Active**
   - Condition: After 7:00 AM
   - Lights automatically activate on motion
   - Purpose: Responsive lighting during morning routine

---

### 4.2 Evening Workflow (Sunset onwards)

1. **Motion Detected at Night**
   - Trigger: Any motion after sunset
   - Lights: Main lights 75%, Ambient on
   - Purpose: Safe navigation, comfortable lighting

2. **No Motion for 10 Minutes**
   - Lights: Dim to ambient mode
   - Timer: Schedule 5-minute lights-off
   - Purpose: Transition toward sleep state

3. **No Motion for 30 Minutes**
   - All lights: Off
   - Purpose: Sleep preservation, energy saving

4. **Blinds Close at Sunset + 15min**
   - Automatic privacy
   - Purpose: Consistent evening routine

---

### 4.3 TV Entertainment Workflow

**Daytime TV Usage**
1. TV turns on
2. Automatic: Main light activates
3. Purpose: Combat screen glare during day

**Nighttime TV Usage**
1. TV turns on
2. Motion detected → lights activate to 75%
3. Door opens → pause TV (courtesy)
4. TV turns off → lights dim to 20%, ambient scene
5. Purpose: Immersive viewing with comfort transitions

---

### 4.4 Sleep Preparation Workflow

**User Enters Bed at Night**
1. Bed occupancy detected (30s delay)
2. If window closed: Blinds auto-close
3. If any lights on: Dim to low ambient
4. Motion: Won't trigger lights (bed sensor prevents)
5. Purpose: Undisturbed sleep, privacy

**Other Bedroom Activity**
1. Ashlee's door opens → notification sent
2. Leo's door opens → notification sent
3. Purpose: Parental awareness during sleep hours

---

### 4.5 Fan Control Workflow

**Fan Auto-Off After Inactivity**
1. Motion detected → fan may be on
2. No motion for 3+ minutes AND fan is on
3. Action: Fan turns off automatically
4. Purpose: Energy saving, prevent unnecessary cooling

---

### 4.6 Remote Control Quick Actions

| Button | Action | Use Case |
|--------|--------|----------|
| **Button 1** | All lights full | Movie off, need full brightness |
| **Button 2** | Ambient only | Evening mood, dim lighting |
| **Button 3** | All off | Sleep time, instant off |
| **Button 4** | 50% dim | Comfortable reading/relaxation |
| **Dial Right** | +10% brightness | Fine-tune lighting up |
| **Dial Left** | -10% brightness | Fine-tune lighting down |

---

## 5. Configuration Parameters

### Input Booleans (Toggles)

| Entity | Purpose | Default |
|--------|---------|---------|
| `input_boolean.enable_bed_sensor` | Activate bed occupancy automations | On |
| `input_boolean.enable_bedroom_blind_automations` | Activate blind control automations | On |
| `input_boolean.enable_bedroom_motion_trigger` | Activate motion-based lighting | On |
| `input_boolean.enable_direct_notifications` | Alert on door activity | On |

**Usage Notes:**
- Disable bed sensor when unoccupied to prevent false triggers
- Disable blind automations for manual control periods
- Disable motion trigger during daytime if desired

---

### Input Numbers (Numeric Parameters)

| Entity | Purpose | Range | Default |
|--------|---------|-------|---------|
| `input_number.blind_open_position_threshold` | Minimum position for "open" detection | 0-100 | 80 |
| `input_number.blind_closed_position_threshold` | Maximum position for "closed" detection | 0-100 | 20 |
| `input_number.bedroom_blind_closed_threshold` | Threshold for blind position | 0-100 | 15 |
| `input_number.forecast_high_temperature` | Max temp for daytime TV lighting | 0-50°C | 28 |

**Configuration Notes:**
- Adjust thresholds based on actual blind positions
- Temperature threshold determines when TV lighting triggers

---

### Input Datetimes

| Entity | Purpose | Type |
|--------|---------|------|
| `input_datetime.childrens_bed_time` | Set bedtime for children room automations | Time picker |

---

### Input Selects

| Entity | Purpose | Options |
|--------|---------|---------|
| `input_select.home_mode` | Global mode selector | Away, Home, Sleep, Guest |

---

## 6. Helper Entities & Timers

### Automation Control Flags

| Flag | Purpose | Set By |
|------|---------|--------|
| Lights-off timer pending | Queued lights off after motion stops | Motion automation (5 min) |
| Long motion timer active | Extended inactivity tracking | No-motion automation (30 min) |

---

## 7. Scripts

**Scripts Not Defined in bedroom.yaml** - Uses shared scripts:

- `script.send_to_home_log` - Logging automation events
  - Parameters: message, title, log_level
  - Example: "Motion Detected - Turning on lights"

---

## 8. Sensors & Tracking

### Computed States (from automations)

- **Lights Status**: Determined by combination of:
  - Motion detection state
  - Time of day (sunset/sunrise)
  - Bed occupancy
  - TV power state

- **Blind Position Tracking**:
  - Current position: 0-100%
  - Automated to: 100% (morning), 0% (evening/occupied)

- **Fan Runtime**:
  - Controlled by: Motion state
  - Auto-off: After 3+ minutes inactivity

---

## 9. Status Indicators

### Light Status Summary

- **All On** → Full brightness lighting active
- **Ambient Only** → Dim mood lighting, TV mode
- **Dim** → 50% brightness, reading mode
- **Off** → All lights extinguished

### Blind Status Summary

- **Open** → Position 80-100%, daytime mode
- **Partial** → Position 20-80%, transitional
- **Closed** → Position 0-20%, nighttime privacy

### Room Occupancy

- **Occupied** → Bed sensor active, person present
- **Empty** → All motion/bed sensors inactive
- **Sleeping** → After 11 PM with occupancy active

---

## 10. Key Features & Automations Highlights

### Smart Blind Control
- **Sunset Auto-Close**: Blinds automatically close at sunset + 15 minutes
- **Occupancy-Based**: If someone in bed + window closed, blinds auto-close
- **Morning Routine**: Blinds open at 7:00 AM on workdays for natural light
- **Manual Override**: Always controllable via remote/app

### Motion-Adaptive Lighting
- **Night Detection**: After sunset, motion triggers lights to 75%
- **Fade-Out**: 10 min no motion → dim, 30 min no motion → off
- **Sleep Protection**: Bed occupancy prevents motion triggers to preserve sleep
- **Remote Quick-Access**: 6-button/dial remote for instant control

### Privacy & Security
- **Auto Close on Occupancy**: When in bed, blinds close for privacy
- **Entry Alerts**: Notifications when other bedroom doors open (parental monitoring)
- **Window Safety**: Blind close triggers if window closed at night
- **Access Control**: Independent door sensors for Ashlee's and Leo's rooms

### Entertainment Integration
- **TV-Responsive**: Main light activates automatically when TV on during day
- **Pause Courtesy**: Door opening pauses TV at night (distraction prevention)
- **Mood Lighting**: TV-off triggers dim ambient lighting (transition to sleep)

### Energy Efficiency
- **Motion-Based Shutdown**: Fan auto-off after 3+ min inactivity
- **Long Inactivity**: All lights off after 30 min no motion
- **Occupancy Awareness**: No automation actions when room empty

### User Control
- **Remote Control**: 6-button control for manual light management
- **Time-Based Automation**: Blind open/close follows sunrise/sunset schedule
- **Conditional Logic**: All automations respect enable/disable toggles
- **Multi-Floor Support**: Stair lights controllable from bedroom

---

## Implementation Notes

### Blind Automation Recommendations

1. **Calibrate Position Thresholds**
   - Test actual blind positions when fully open/closed
   - Adjust `blind_open_position_threshold` and `blind_closed_position_threshold`
   - Default 80/20 may need adjustment for your specific blinds

2. **Bed Sensor Configuration**
   - Requires bed occupancy sensor (pressure/weight based)
   - Should have minimal false positives (<1% daily)
   - Test triggering with 30-second delay

3. **Motion Sensor Placement**
   - Mount ceiling-center for optimal coverage
   - Test at night to ensure reliable detection
   - Avoid direct heat sources (fan, AC) affecting readings

### Remote Control Setup

1. Pair remote to Home Assistant Zigbee/Z-Wave network
2. Configure button mappings to bedroom light entities
3. Test each button in low-light conditions

### Testing Checklist

- [ ] Blinds close automatically at sunset + 15 min
- [ ] Blinds open at 7:00 AM on workdays
- [ ] Motion detected → lights activate after sunset
- [ ] 10 min no motion → lights dim
- [ ] 30 min no motion → all lights off
- [ ] Bed occupancy → blinds close if window closed
- [ ] Other bedroom door → notification sent
- [ ] TV on during day → main light activates
- [ ] All remote buttons → lights respond correctly
- [ ] Fan → turns off after 3+ min inactivity

---

## Troubleshooting Guide

### Blinds Not Closing on Schedule

**Symptoms:** Blinds remain open at sunset + 15 min

**Diagnosis:**
1. Check `input_boolean.enable_bedroom_blind_automations` is ON
2. Verify `cover.bedroom_blinds` entity status (not offline)
3. Check sunset time calculation (Home Assistant sun integration)

**Solutions:**
- Re-calibrate blind position thresholds
- Increase motor timeout if slow response
- Force-close blinds via UI, then re-enable automation

---

### Motion Lights Not Triggering

**Symptoms:** No lights on when motion detected at night

**Diagnosis:**
1. Verify `input_boolean.enable_bedroom_motion_trigger` is ON
2. Check `binary_sensor.bedroom_area_motion` is reporting state correctly
3. Confirm current time is after sunset

**Solutions:**
- Test motion sensor in dark room
- Adjust motion sensor sensitivity
- Check for obstruction (dust, cobwebs)
- Verify light entities respond to manual on/off

---

### Blinds Closing Multiple Times

**Symptoms:** Blinds close repeatedly (every 15 minutes)

**Diagnosis:**
1. Window contact sensor may be flaky (open/close bouncing)
2. Multiple automations may be queued

**Solutions:**
- Test window contact sensor for proper state
- Check contact sensor magnet alignment
- Review automation logs for duplicate triggers

---

## Related Documentation

- Main package: `packages/rooms/bedroom/bedroom.yaml`
- Related automations: `packages/rooms/bedroom/sleep_as_android.yaml`, `packages/rooms/bedroom/awtrix_light.yaml`
- Kitchen setup: `KITCHEN-SETUP.md`

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-24 | Initial documentation generation | Claude Code |
| TBD | System calibration post-deployment | Danny Tsang |

---

**Documentation Status:** ✅ Complete
**Last Review:** 2026-01-24
**Next Review:** 2026-02-24
