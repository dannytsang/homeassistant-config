# Conservatory Setup Documentation

**Last Updated:** 2026-01-25
**Package:** packages/rooms/conservatory/ (3 files)
**Maintainer:** Danny Tsang
**Status:** ✅ Operational

---

## 1. Device Inventory

### Lighting Systems

**Main Lights**
- `light.conservatory` - Main conservatory light (dimmable, motion-triggered)
- `light.prusa` - 3D printer work light (triggered by print detection)

**Scenes**
- `scene.conservatory_turn_on_light` - Conservatory full brightness (motion activation)
- `scene.conservatory_turn_off_light` - Conservatory lights off
- `scene.3d_printer_light_on` - 3D printer work light (high brightness for detail work)
- `scene.3d_printer_light_off` - 3D printer light off

---

### Climate Control

**Heating Systems**
- `climate.conservatory_under_floor_heating` - Underfloor heating with thermostat
  - Configurable target temperature: input_number.conservatory_default_under_floor_temperature
  - Cost-aware scheduling via input_boolean helpers
- `climate.hive_receiver_heat` - Hive heating receiver (boiler controller)
  - Integrated with Home Assistant Hive integration

---

### Motion & Presence Detection

**Motion Sensors**
- `binary_sensor.conservatory_area_motion` - PIR motion detection (primary trigger)
- `binary_sensor.conservatory_motion_occupancy` - Multi-sensor occupancy fusion
- `binary_sensor.everything_presence_one_26eb54_occupancy` - Everything Presence One mmWave occupancy
- `binary_sensor.everything_presence_one_26eb54_mmwave` - Direct mmWave sensor output

**Associated Sensors**
- `sensor.conservatory_motion_illuminance` - Ambient light level from motion sensor
- `sensor.everything_presence_one_26eb54_illuminance` - Ambient light from Presence sensor
- `sensor.conservatory_area_mean_temperature` - Room temperature average
- `sensor.conservatory_temperature_over_12_hours` - Temperature trend tracking

---

### Door & Access Control

**Contact Sensors**
- `binary_sensor.conservatory_door` - Conservatory door contact (open/closed detection)
- `binary_sensor.back_garden_gate_contact` - Back garden gate (for multi-room automation)
- `binary_sensor.shed_door` - Shed door (for security/awareness)

---

### 3D Printing System (OctoPrint Integration)

**Printer Control**
- `switch.prusa_fan` - Prusa 3D printer fan control (on/off)

**OctoPrint Status Sensors**
- `binary_sensor.octoprint_printing` - Printer active state (on = printing, off = idle)
- `sensor.octoprint_current_state` - State text (Printing, Paused, Error, etc.)
- `sensor.octoprint_job_percentage` - Print progress percentage (0-100%)
- `sensor.octoprint_estimated_finish_time` - ETA for completion

---

### Airer / Clothes Drying System

**Airer Control**
- `switch.airer` - Motorized clothes airer (raise/lower control)
- `binary_sensor.conservatory_airer_schedule_1` - Schedule 1 activation status

**Airer Automations**
- Cost-aware scheduling (runs when energy cost is low/free)
- Temperature threshold control (only when warm enough)
- Manual enable/disable via input_boolean helpers

---

### Power & Auxiliary Control

**Additional Switches**
- `switch.conservatory_extension_2` - Power outlet extension (for appliances/devices)

---

### Timers & Scheduling

**Active Timers**
- `timer.conservatory_lights_off` - Countdown for lights off after motion stops
- `timer.restart_conservatory_motion_sensor` - Restart sequence timer for motion sensor recovery
- `timer.sleep` - General sleep/delay timer (multi-purpose)

---

## 2. Automation Functions

### 2.1 Motion-Triggered Lighting (4 automations)

#### Motion Detected And It's Dark
- **ID:** 1610234394136
- **Trigger:** Motion detected from any sensor (4 sensors: PIR, occupancy, Presence occupancy, mmWave)
- **Conditions:**
  - Light level below threshold (conservatory_light_level_threshold) OR
  - Light sensor unavailable
  - Motion trigger automation enabled
- **Actions:**
  - Log motion event with current light level
  - Turn on conservatory light via scene (2-second transition)
  - Cancel any pending lights-off timer
- **Mode:** Single
- **Purpose:** Automatic lighting when motion detected in darkness

---

#### No Motion Detected
- **ID:** 1610234794461
- **Trigger:** Motion stops (state off)
- **Conditions:**
  - Conservatory light is on
  - Motion trigger automation enabled
- **Actions:**
  - Log no-motion event
  - Start 1-minute countdown timer
- **Mode:** Single
- **Purpose:** Initiate gradual shutdown sequence

---

#### No Motion Turn Lights Off
- **ID:** 1610238960657
- **Trigger:** Timer finished (timer.conservatory_lights_off)
- **Conditions:**
  - Conservatory light is on
  - Motion trigger automation enabled
- **Actions:**
  - Log lights-off event
  - Turn off lights via scene
- **Mode:** Single
- **Purpose:** Final lights-off after motion inactivity timeout

---

#### Motion Sensor Goes Offline
- **ID:** 1610238960658
- **Trigger:** Motion sensor state becomes unavailable
- **Conditions:**
  - Motion trigger automation enabled
- **Actions:**
  - Log sensor offline event
  - Start 10-minute restart timer
  - Disable motion automations (prevent false states)
- **Mode:** Single
- **Purpose:** Detect and respond to sensor disconnection

---

### 2.2 Motion Sensor Recovery (2 automations)

#### Motion Sensor Comes Online
- **ID:** 1610238960659
- **Trigger:** Motion sensor becomes available
- **Conditions:**
  - Motion trigger automation enabled
- **Actions:**
  - Log sensor online event
  - Cancel restart timer
- **Mode:** Single
- **Purpose:** Confirm sensor reconnection

---

#### Restart Motion Sensor Finished
- **ID:** 1610238960660
- **Trigger:** Restart timer finished
- **Conditions:**
  - Motion sensor still unavailable
- **Actions:**
  - Restart motion sensor integration/device
  - Log restart attempt
- **Mode:** Single
- **Purpose:** Force sensor recovery if still offline

---

### 2.3 Door Monitoring (2 automations)

#### Door Open
- **ID:** 1610238960661
- **Trigger:** Conservatory door opens
- **Conditions:**
  - Motion trigger automation enabled
- **Actions:**
  - Log door open event
- **Mode:** Single
- **Purpose:** Track door activity (security awareness)

---

#### Door Closed
- **ID:** 1610238960662
- **Trigger:** Conservatory door closes
- **Conditions:**
  - Motion trigger automation enabled
- **Actions:**
  - Log door closed event
- **Mode:** Single
- **Purpose:** Track door activity

---

### 2.4 Airer Automation (2 automations)

#### Turn On Airer
- **ID:** [varies by schedule]
- **Trigger:** Time-based (specific times defined) OR cost-aware
- **Conditions:**
  - Airer schedule enabled (input_boolean.enable_conservatory_airer_schedule)
  - Temperature above minimum (input_number.airer_minimum_temperature)
  - Cost conditions met (if cost-aware mode enabled)
  - Home mode is not Away
- **Actions:**
  - Raise motorized airer (switch.airer on)
  - Log airer activation
- **Mode:** Single
- **Purpose:** Automatic clothes drying with cost optimization

---

#### Turn Off Airer
- **ID:** [varies by schedule]
- **Trigger:** Time-based (end of drying window) OR temperature drop
- **Conditions:**
  - Airer schedule enabled
  - Airer is currently raised (on)
- **Actions:**
  - Lower motorized airer (switch.airer off)
  - Log airer shutdown
- **Mode:** Single
- **Purpose:** Automatic shutdown of drying cycle

---

### 2.5 3D Printer Monitoring (9 automations)

#### Print Started
- **ID:** 1608655560832
- **Trigger:** OctoPrint printing state = on
- **Conditions:**
  - 3D printer automations enabled
- **Actions:**
  - Log print start
  - If after sunset: Turn on printer light for visibility
  - If before sunrise: Turn on printer light
- **Mode:** Single
- **Purpose:** Ensure adequate lighting for print monitoring

---

#### 50% Complete
- **ID:** [in octoprint.yaml]
- **Trigger:** Print progress reaches 50%
- **Conditions:**
  - 3D printer automations enabled
  - Progress transitions through 50% mark
- **Actions:**
  - Log print halfway event
  - Optional: Send notification (if configured)
- **Mode:** Single
- **Purpose:** Checkpoint notification (print is progressing)

---

#### Check If Printing Light
- **ID:** [in octoprint.yaml]
- **Trigger:** Printer light state changes
- **Conditions:**
  - OctoPrint currently printing
- **Actions:**
  - Monitor and maintain light state based on print status
- **Mode:** Single
- **Purpose:** Ensure light stays on during active printing

---

#### Finished Printing
- **ID:** [in octoprint.yaml]
- **Trigger:** OctoPrint printing state = off AND print completed
- **Conditions:**
  - Print completion detected (not pause, not error)
  - 3D printer automations enabled
- **Actions:**
  - Log print finished event
  - Turn off printer light
  - Optional: Send notification with completion time
  - Optional: Camera snapshot for print inspection
- **Mode:** Single
- **Purpose:** Celebration moment + light management

---

#### Light Turned On
- **ID:** [in octoprint.yaml]
- **Trigger:** Printer light turns on
- **Conditions:**
  - OctoPrint not printing
- **Actions:**
  - Log manual light activation
  - Track light-on duration
- **Mode:** Single
- **Purpose:** Manual light usage tracking

---

#### Paused Mid Print
- **ID:** [in octoprint.yaml]
- **Trigger:** OctoPrint state = paused
- **Conditions:**
  - 3D printer automations enabled
- **Actions:**
  - Log pause event
  - Keep light on (user may resume)
  - Optional: Send notification
- **Mode:** Single
- **Purpose:** Maintain work environment during pause

---

## 3. Room Layout & Device Placement

```
                    CONSERVATORY LAYOUT

    ╔════════════════════════════════════════════╗
    ║                                            ║
    ║   🚪 DOOR (contact sensor)                ║
    ║   [Motion Sensors - ceiling mounted]      ║
    ║   ├─ PIR motion detector                  ║
    ║   ├─ Everything Presence One (mmWave)     ║
    ║   ├─ Light sensors (2)                    ║
    ║   └─ Temperature sensors                  ║
    ║                                            ║
    ║   💡 MAIN LIGHT                           ║
    ║   ├─ Motion-triggered                     ║
    ║   ├─ Dimmable RGB                         ║
    ║   └─ 2-second transition on/off           ║
    ║                                            ║
    ║   🌡️ CLIMATE CONTROL                      ║
    ║   ├─ Underfloor heating thermostat        ║
    ║   ├─ Temperature setpoint control         ║
    ║   ├─ Cost-aware scheduling                ║
    ║   └─ 12-hour temperature tracking         ║
    ║                                            ║
    ║   🛠️ CLOTHES AIRER (motorized)            ║
    ║   ├─ Raise/lower control                  ║
    ║   ├─ Temperature-gated automation         ║
    ║   ├─ Cost-optimized scheduling            ║
    ║   └─ Schedule 1 activation binary         ║
    ║                                            ║
    ║   🖨️ 3D PRINTER WORKSTATION               ║
    ║   ├─ Prusa printer (OctoPrint control)    ║
    ║   ├─ Dedicated printer light (bright)     ║
    ║   ├─ Fan control (on/off)                 ║
    ║   ├─ Workbench lighting                   ║
    ║   └─ Print progress monitoring (7 states) ║
    ║                                            ║
    ║   🔌 POWER MANAGEMENT                      ║
    ║   ├─ Extension outlet 2 (smart switch)    ║
    ║   └─ For temporary device connections     ║
    ║                                            ║
    ║   🔗 EXTERNAL INTEGRATIONS                ║
    ║   ├─ Hive heating receiver                ║
    ║   ├─ OctoPrint network integration        ║
    ║   └─ Multi-room sensor fusion             ║
    ║                                            ║
    ╚════════════════════════════════════════════╝
```

---

## 4. Key Automation Workflows

### 4.1 Daily Motion-Triggered Lighting

**Daytime (Bright)**
1. Motion detected
2. Light level check: Already bright
3. Action: Lights remain off (natural light sufficient)
4. Purpose: Energy saving in daytime

**Evening (Dark)**
1. Motion detected
2. Light level check: Below threshold
3. Action: Lights activate with 2-second transition
4. Timer: 1-minute no-motion countdown starts
5. If motion returns: Timer cancels, lights stay on
6. If no motion for 1 minute: Lights fade off

---

### 4.2 3D Printer Monitoring Workflow

**Print Lifecycle**

```
User starts print on Prusa
        ↓
OctoPrint "printing" state = on
        ↓
"Print Started" automation triggers
        ↓
Check time of day
    ├─ After sunset → Turn on printer light (for visibility)
    └─ Before sunrise → Turn on printer light
        ↓
Monitor print progress (sent to sensors)
        ↓
At 50% completion
    ├─ Log checkpoint event
    └─ Optional: Send notification "Print halfway"
        ↓
Print continues to completion
        ↓
OctoPrint state = off (print finished)
        ↓
"Finished Printing" automation triggers
        ↓
Actions:
  ├─ Log completion event
  ├─ Turn off printer light
  ├─ Optional: Camera snapshot
  ├─ Optional: Notification with total time
  └─ Optional: Fire event for downstream automations
        ↓
Print removed from printer
        ↓
Ready for next print
```

**Print Pause Flow**

```
Print running normally
        ↓
User pauses via Prusa/OctoPrint
        ↓
OctoPrint state = paused
        ↓
"Paused Mid Print" automation triggers
        ↓
Actions:
  ├─ Log pause event
  ├─ Keep printer light ON (user may resume)
  ├─ Temperature check (if long pause)
  └─ Optional: Notification with pause duration
        ↓
Wait for user action:
  ├─ Resume → Continue printing workflow
  └─ Cancel → Trigger "Finished" cleanup
```

---

### 4.3 Airer Optimization Workflow

**Cost-Aware Drying Schedule**

```
Schedule time arrives (e.g., 2 PM)
        ↓
Check conditions:
  ├─ Airer automations enabled? ✓
  ├─ Temperature > threshold? ✓
  ├─ Cost conditions met? ✓
  ├─ Home mode ≠ Away? ✓
  └─ All conditions pass
        ↓
Action: Raise airer (motor up)
        ↓
Log: "Airer raised for drying"
        ↓
Time passes (clothes drying)
        ↓
End of window time OR
Temperature drops below threshold
        ↓
Check state:
  ├─ Is airer still raised? ✓
  └─ Is automation still enabled? ✓
        ↓
Action: Lower airer (motor down)
        ↓
Log: "Airer lowered after drying"
        ↓
Status: Clothes dried, ready to fold
```

---

### 4.4 Motion Sensor Recovery Workflow

**Sensor Failure Detection**

```
Motion sensor operating normally
        ↓
Network disconnection or device failure
        ↓
Sensor state becomes "unavailable"
        ↓
"Motion Sensor Goes Offline" automation triggers
        ↓
Actions:
  ├─ Log: "Motion sensor offline"
  ├─ Start 10-minute restart timer
  └─ Disable motion automations (prevent false triggers)
        ↓
Wait 10 minutes
        ↓
Two possible outcomes:

  A) Sensor reconnects (state ≠ unavailable)
     ├─ "Comes Online" automation triggers
     ├─ Log: "Motion sensor back online"
     ├─ Cancel restart timer
     └─ Re-enable motion automations ✓

  B) Sensor still offline after 10 minutes
     ├─ Timer expires
     ├─ "Restart Finished" automation triggers
     ├─ Attempt device restart (integration or WiFi)
     ├─ Log: "Restart sequence initiated"
     └─ Wait for sensor to recover
```

---

## 5. Configuration Parameters

### Input Booleans (Toggles)

| Entity | Purpose | Default | Used In |
|--------|---------|---------|---------|
| `input_boolean.enable_conservatory_motion_trigger` | Enable/disable all motion lighting automations | On | All motion automations |
| `input_boolean.enable_conservatory_airer_schedule` | Enable/disable airer automations | On | Airer automation |
| `input_boolean.enable_conservatory_airer_when_cost_nothing` | Run airer only when energy is free | On | Airer (advanced) |
| `input_boolean.enable_conservatory_airer_when_cost_below_nothing` | Run airer when energy cost below threshold | Off | Airer (advanced) |
| `input_boolean.enable_3d_printer_automations` | Enable/disable printer light automations | On | All printer automations |
| `input_boolean.conservatory_under_floor_heating_cost_below_nothing` | Cost threshold for heating | Off | Climate automation |

**Usage Notes:**
- Disable motion trigger during maintenance work
- Disable airer schedule when not in use (rainy season)
- Disable printer automations during testing/debug

---

### Input Numbers (Numeric Parameters)

| Entity | Purpose | Range | Default | Unit |
|--------|---------|-------|---------|------|
| `input_number.conservatory_light_level_threshold` | Lux level to trigger lights | 0-1000 | 250 | lux |
| `input_number.airer_minimum_temperature` | Don't dry if temp below this | 5-30 | 15 | °C |
| `input_number.conservatory_default_under_floor_temperature` | Target heating temperature | 15-25 | 20 | °C |

**Configuration Notes:**
- Light threshold: Adjust based on natural light (lower = more sensitive)
- Airer temp: Prevents damp clothes (set to room dew point estimate)
- Heat target: Comfort vs. cost trade-off (lower saves energy)

---

### Input Selects

| Entity | Purpose | Options |
|--------|---------|---------|
| `input_select.home_mode` | Global home/away mode | Away, Home, Sleep, Guest |

---

## 6. Helper Entities & Timers

### Automation Control Flags

| Timer/Flag | Purpose | Set By | Duration |
|------------|---------|--------|----------|
| `timer.conservatory_lights_off` | Countdown for lights off | No Motion automation | 1 minute |
| `timer.restart_conservatory_motion_sensor` | Recovery retry countdown | Sensor Offline automation | 10 minutes |
| `timer.sleep` | General-purpose timer | Various automations | Configurable |

---

## 7. Scripts

**Scripts Not Defined in conservatory.yaml** - Uses shared scripts:

- `script.send_to_home_log` - Logging automation events
  - Parameters: message, title, log_level
  - Used in: All automations for event tracking

---

## 8. Sensors & Tracking

### Computed States (from automations)

- **Conservatory Light Status**: Determined by:
  - Motion detection + light level
  - Scene activation (on/off)
  - Manual control (app/voice)

- **3D Printer Status**: From OctoPrint:
  - Printing: True/False
  - Progress: 0-100%
  - State: Idle, Printing, Paused, Error, etc.
  - ETA: Time remaining to completion

- **Airer Position**: From smart switch:
  - Raised: switch.airer = on
  - Lowered: switch.airer = off
  - Motor state: Active/Inactive

- **Temperature Tracking**:
  - Current: sensor.conservatory_area_mean_temperature
  - 12-hour trend: sensor.conservatory_temperature_over_12_hours

---

## 9. Status Indicators

### Light Status Summary

- **On** → Motion detected or manual activation
- **Off** → No motion for >1 minute after detection
- **Dimming** → Transition active (2 seconds)

### Airer Status

- **Raised** → Drying cycle active
- **Lowered** → Not drying or cycle complete
- **Scheduled** → Awaiting optimal conditions

### 3D Printer Status

- **Printing** → Active print in progress
- **Paused** → Print suspended, waiting for resume
- **Idle** → Not printing (light off)
- **Error** → Print failed or device issue

### Climate Status

- **Heating** → Underfloor heating active (temp below target)
- **Idle** → Room at target temperature
- **Cost-Aware** → Delayed heating (waiting for low-cost period)

---

## 10. Key Features & Automations Highlights

### Smart Motion-Based Lighting
- **Multi-sensor Fusion**: PIR + mmWave occupancy + visual sensors
- **Light-Level Adaptive**: Only activates when dark (energy efficient)
- **Graceful Fade**: 2-second transition prevents jarring on/off
- **Auto-Shutdown**: 1-minute inactivity timer (configurable)
- **Sensor Resilience**: Detects and recovers from sensor failures

### Cost-Optimized Airer Control
- **Time-Based Scheduling**: Fixed drying windows
- **Temperature-Gated**: Won't dry in cold/damp conditions
- **Cost-Aware**: Optional: Only raise when energy is free/cheap
- **Multi-Condition Logic**: All factors must align before activation
- **Manual Override**: Enable/disable via input_boolean

### Intelligent 3D Printer Monitoring
- **Work Lighting**: Automatic light when printing (day or night)
- **Progress Tracking**: Checkpoint at 50% completion
- **Completion Detection**: Distinguishes finish vs. pause vs. error
- **Print State Preservation**: Keeps light on during pause (user may resume)
- **Event Logging**: Every state transition logged
- **Optional Notifications**: Setup-dependent alerting

### Environmental Awareness
- **Underfloor Heating Control**: Cost and comfort optimization
- **Temperature Monitoring**: 12-hour trend tracking
- **Climate Integration**: Hive boiler control integration
- **Dual Feedback**: Both local and external climate sensors

### Robust Sensor Management
- **Offline Detection**: Immediate notification of sensor failures
- **Auto-Recovery**: 10-minute restart sequence for stuck sensors
- **State Validation**: Checks sensor status before automation triggers
- **Graceful Fallback**: Disables automations if sensors unavailable

---

## Implementation Notes

### Motion Sensor Calibration

1. **Light Threshold Selection**
   - Default: 250 lux (well-lit room)
   - Reduce for: North-facing conservatory
   - Increase for: South-facing, strong sunlight
   - Test at different times of day

2. **Sensor Coverage**
   - Mount motion sensors on ceiling for best coverage
   - Test movement patterns in typical use
   - Verify light sensor accuracy (outdoor sources)

3. **Multi-Sensor Redundancy**
   - PIR for budget power savings
   - mmWave for better activity detection
   - Fusion improves false-negative rate

---

### 3D Printer Setup

1. **OctoPrint Integration**
   - Requires OctoPrint with Moonraker/Klippy (Prusa Link)
   - Network connectivity to OctoPrint instance
   - Sensor entities properly configured

2. **Light Automation**
   - Printer light must be controllable via Home Assistant
   - Scene activation provides consistent on/off behavior
   - Test with actual print (automation triggers correctly)

3. **Print Monitoring**
   - ETA requires OctoPrint with file info enabled
   - Progress updates depend on Marlin firmware feedback
   - Completion detection needs state transition logging

---

### Airer Motorization

1. **Motor Control**
   - Smart switch must control airer motor reliably
   - Test raise/lower cycles for proper timing
   - Verify safety cutoffs (end-of-travel)

2. **Temperature Sensing**
   - Use local conservatory temperature (not external)
   - Account for humidity (damp air inhibits drying)
   - Seasonal adjustments may be needed

3. **Schedule Planning**
   - Align with solar weather patterns
   - Consider laundry frequency
   - Test cost conditions if using energy pricing

---

### Climate Control Integration

1. **Underfloor Heating**
   - Requires climate entity from Hive integration
   - Setpoint changes apply immediately
   - Monitor actual temperature vs. target

2. **Energy Management**
   - Heating is most power-hungry system
   - Cost-aware scheduling saves significantly
   - Consider time-of-use tariffs (TOU)

3. **Comfort vs. Efficiency**
   - Lower setpoint (18°C) saves ~10% per degree
   - Consider occupancy patterns
   - Unoccupied periods: Drop temperature 2-3°C

---

## Testing Checklist

- [ ] Motion detected → Lights activate after sunset
- [ ] Light level high → Lights don't activate (natural light)
- [ ] No motion 1 minute → Lights fade off
- [ ] Motion returns → Timer cancels, lights stay on
- [ ] Airer schedule time → Airer raises (if conditions met)
- [ ] Temperature too low → Airer won't raise (safety)
- [ ] 3D print starts → Printer light activates
- [ ] Print 50% → Log entry created (notification optional)
- [ ] Print finishes → Light turns off, completion logged
- [ ] Print paused → Light stays on, pause logged
- [ ] Motion sensor offline → Automations disabled
- [ ] Motion sensor recovery → Automations re-enabled
- [ ] Door open/close → Door events logged

---

## Troubleshooting Guide

### Lights Won't Turn On on Motion

**Symptoms:** Motion detected but lights remain off

**Diagnosis:**
1. Check `input_boolean.enable_conservatory_motion_trigger` is ON
2. Check light level: Is it below threshold? (sensor.conservatory_motion_illuminance)
3. Verify light entity exists and responds to manual on/off
4. Check motion sensor state is actually "on"

**Solutions:**
- Adjust `input_number.conservatory_light_level_threshold` lower
- Verify motion sensor is properly installed and powered
- Test light scene manually: `scene.conservatory_turn_on_light`
- Check automation logs for error messages

---

### Airer Not Raising on Schedule

**Symptoms:** Scheduled time passes but airer doesn't raise

**Diagnosis:**
1. Is `input_boolean.enable_conservatory_airer_schedule` ON?
2. Check room temperature vs. `input_number.airer_minimum_temperature`
3. Check home mode: Is it "Away"? (automations may skip)
4. Check cost conditions if enabled

**Solutions:**
- Verify motor switch can control airer manually
- Raise minimum temperature threshold if room is cool
- Check time zone is set correctly
- Review automation conditions in airer.yaml

---

### 3D Printer Light Not Activating

**Symptoms:** Printer starts but light doesn't turn on

**Diagnosis:**
1. Is `input_boolean.enable_3d_printer_automations` ON?
2. Verify OctoPrint integration is connected
3. Check if scene exists: `scene.3d_printer_light_on`
4. Check time of day: Is it night?

**Solutions:**
- Test scene manually: `scene.3d_printer_light_on`
- Verify OctoPrint WebSocket connection
- Check automation logs for print state transitions
- Confirm printer light switch is controllable

---

### Motion Sensor Offline/Unavailable

**Symptoms:** Motion sensor state shows "unavailable" or "unknown"

**Diagnosis:**
1. Check WiFi/Zigbee connection to sensor
2. Verify sensor power/battery level
3. Check Home Assistant integration is configured
4. Look for connection timeouts in logs

**Solutions:**
- Power cycle the motion sensor (wait 30 seconds)
- Check router/gateway for sensor connectivity
- Move sensor closer to access point if signal weak
- Restart Home Assistant integration if stuck
- Replace batteries if battery-powered

---

## Related Documentation

- **Main package files:**
  - `packages/rooms/conservatory/conservatory.yaml` (10 automations)
  - `packages/rooms/conservatory/airer.yaml` (2 automations)
  - `packages/rooms/conservatory/octoprint.yaml` (9 automations)

- **Related setups:**
  - KITCHEN-SETUP.md (for appliance monitoring patterns)
  - BEDROOM-SETUP.md (for occupancy-based automation patterns)

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-25 | Initial documentation generation | Claude Code |
| TBD | System calibration post-deployment | Danny Tsang |
| TBD | Airer motor integration | Danny Tsang |
| TBD | OctoPrint web hooks setup | Danny Tsang |

---

**Documentation Status:** ✅ Complete
**Last Review:** 2026-01-25
**Next Review:** 2026-02-25
