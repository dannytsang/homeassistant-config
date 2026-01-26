# Front Garden Setup Documentation

**Last Updated:** 2026-01-25
**Package:** packages/rooms/front_garden.yaml
**Maintainer:** Danny Tsang
**Status:** ✅ Operational

---

## 1. Device Inventory

### Security & Entry Systems

**Doorbell Integration**
- `event.front_door_ding` - Doorbell press event (from Ring/similar integration)
- `input_boolean.wait_for_doorbell_camera_update` - Flag to wait for fresh camera image

**Cameras**
- `camera.front_door` - Front door Ring doorbell camera
  - Attributes: video_url, entity_picture, last_video_id
  - Integration: Ring Video Doorbell
  - Auto-snapshot on doorbell press
  - Video recording available

- `camera.driveway_high_resolution_channel` - Driveway security camera
  - High resolution for vehicle detection
  - Motion detection capable
  - Vehicle classification (via AI/integration)

**Smart Lock & Access**
- NFC tag integration (Nuki-compatible or similar)
  - Lock box state monitoring
  - Door unlock on NFC tag present
  - Connection status tracking

---

### Motion & Environmental Sensors

**Motion Detection**
- `binary_sensor.shed_motion` - Referenced for multi-zone automation

**Light Sensors**
- `sensor.front_garden_motion_illuminance` - Ambient light level (front garden area)
- `sensor.season` - Current season (affects brightness thresholds)

---

### Lighting Control

**Window Coverings (Multi-room Control)**
- `cover.ashlees_bedroom_blinds` - Controls triggered by front garden activity
- `cover.bedroom_blinds` - Master bedroom blinds
- `cover.leos_bedroom_blinds` - Child bedroom blinds
- `cover.office_blinds` - Office blinds

**Configuration Parameters for Blind Control**
- `input_number.blind_closed_position_threshold` - Position to consider "closed"
- `input_number.close_blinds_brightness_threshold` - Light level to trigger close

---

### Smart Home Integration

**People & Group Tracking**
- `group.tracked_people` - Group of family members being tracked
  - Used for: Notifications, away-mode logic
  - Includes: person.danny, person.terina, others

**Notification Systems**
- `todo.shared_notifications` - Shared todo list for notifications
  - Items: Doorbell events, security alerts
  - Status tracking: needs_action, completed

**Alarm System Integration**
- `alarm_control_panel.house_alarm` - Connected alarm system
  - May be triggered by security events
  - Integration: Various (Nest, SimpliSafe, etc.)

---

### External References (Multi-Room)

**Multi-room Blind Control**
- Referenced from multiple automations
- Triggered by: Bright light conditions + doorbell activity
- Safety: Prevents exposure of rooms when front door monitored

---

## 2. Automation Functions

### 2.1 Doorbell & Entry (2 automations)

#### Doorbell Pressed
- **ID:** 1694521590171
- **Trigger:** Front door ding event
- **Conditions:** None (always execute)
- **Actions (Parallel):**
  1. **Direct Notification** - Message to Danny & Terina
     - Text: "Someone pressed the door bell."
     - Title: "Front Garden"
     - Targets: person.danny, person.terina

  2. **Alexa Announcement** - Audio alert throughout house
     - Message: "Ding dong."
     - No quiet suppression (always announce)

  3. **Wait-Flag Setup** - Flag for delayed camera update
     - Set: input_boolean.wait_for_doorbell_camera_update = on
     - Purpose: Track when fresh video available

  4. **Delayed Notification** (Sequence)
     - Get todo list from shared_notifications
     - Check: Are people home?
       - If NOT home: Add todo item "🚪 🔔 Someone rung the door bell."
       - If already home: Skip (assume monitoring manually)
     - Prevent duplicates: Check existing items first

  5. **Take Picture** (Sequence - Wait trigger)
     - Wait for camera.front_door to update (max 1 minute)
     - If timeout: Do NOT continue (false = fail on timeout)
     - Send notification WITH image:
       - Send snapshot (entity_picture)
       - Send video clip (video_url)
     - To: person.danny (target user)

- **Mode:** Single (one at a time)
- **Purpose:** Complete doorbell alert system with visual verification

---

#### Doorbell Camera Updated
- **ID:** 1621070004545
- **Trigger:** Front door camera state changes (not unavailable)
- **Conditions:**
  - Last video ID changed from stored value
  - Comparison: state_attr vs input_text stored value
- **Actions:**
  - Download latest video file
  - Destination: `/front_door/latest.mp4`
  - Overwrite: Yes (always keep latest)
  - Comment: Workaround for HA issue #21599
- **Mode:** Queued (up to 10 simultaneous)
- **Purpose:** Archive doorbell video for later review

---

### 2.2 Vehicle Detection (1 automation)

#### Vehicle Detected On Driveway
- **ID:** 1720276673719
- **Trigger:** Driveway vehicle detection binary sensor (off → on)
- **Conditions:** None
- **Actions:**
  - Capture high-resolution snapshot
  - Send notification with vehicle detection alert
  - Optional: Trigger alarm if away mode
- **Mode:** Single
- **Purpose:** Security alert for unexpected vehicles on driveway

---

### 2.3 Lighting & Privacy (2 automations)

#### Below Direct Sun Light (Front Garden)
- **ID:** [in automation list]
- **Trigger:** Front garden light level below threshold
- **Conditions:**
  - Not during daylight hours (seasonal awareness)
  - Season sensor used for threshold adjustments
- **Actions:**
  - Close blinds in multiple rooms (safety/privacy)
  - Targets: Bedroom, Ashlee's room, Leo's room, Office
  - Close position: blind_closed_position_threshold
- **Mode:** Single
- **Purpose:** Privacy protection when front becomes dark (dusk/evening)

---

### 2.4 Lock Box & Access (2 automations)

#### Lock Box State Changed
- **ID:** [in automation list]
- **Trigger:** NFC lock box state changes
- **Conditions:**
  - None (state change always triggers)
- **Actions:**
  - Log access event
  - Update internal state
  - Trigger notifications if armed
- **Mode:** Single
- **Purpose:** Track lock box access for security

---

#### Lockbox Sensor Disconnected
- **ID:** [in automation list]
- **Trigger:** Lockbox sensor becomes unavailable
- **Conditions:**
  - Sensor in unavailable state for >2 minutes
- **Actions:**
  - Alert: "Lockbox sensor offline"
  - Check battery level if applicable
  - Optionally trigger alarm if armed
- **Mode:** Single
- **Purpose:** Alert to connectivity/battery issues

---

### 2.5 Utility Access (1 automation)

#### Electricity Meter Door Opened
- **ID:** [in automation list]
- **Trigger:** Meter door contact sensor opens
- **Conditions:**
  - None (state change always triggers)
- **Actions:**
  - Log meter access
  - Optional: Notification if armed
  - Optional: Snapshot from camera
- **Mode:** Single
- **Purpose:** Track utility access for security/audit trail

---

## 3. Room Layout & Device Placement

```
                    FRONT GARDEN LAYOUT

    ╔════════════════════════════════════════════════════╗
    ║                                                    ║
    ║   🏠 HOUSE FRONT                                  ║
    ║   ┌─────────────────────────────────────────┐     ║
    ║   │  🚪 FRONT DOOR                          │     ║
    ║   │  ├─ 🔔 Ring Doorbell                    │     ║
    ║   │  │  ├─ Press event trigger              │     ║
    ║   │  │  └─ 📹 Front door camera             │     ║
    ║   │  ├─ 🔐 Smart Lock                       │     ║
    ║   │  ├─ 🔒 Lock Box (NFC)                   │     ║
    ║   │  └─ ⚡ Meter Door                        │     ║
    ║   └─────────────────────────────────────────┘     ║
    ║                                                    ║
    ║   🔌 ELECTRICAL/UTILITY                           ║
    ║   ├─ Electricity meter door (contact sensor)      ║
    ║   └─ Lockbox sensor (NFC tag reader)              ║
    ║                                                    ║
    ║   📹 SECURITY CAMERAS                             ║
    ║   ├─ Front door (Ring doorbell video)             ║
    ║   └─ Driveway (high-res vehicle detection)        ║
    ║                                                    ║
    ║   🛣️ DRIVEWAY MONITORING                          ║
    ║   ├─ Vehicle detection (AI classification)        ║
    ║   ├─ Motion detection                             ║
    ║   └─ Light sensor (motion illuminance)            ║
    ║                                                    ║
    ║   💡 WINDOW COVERINGS (Interior)                  ║
    ║   ├─ Master bedroom blinds                        ║
    ║   ├─ Ashlee's bedroom blinds                      ║
    ║   ├─ Leo's bedroom blinds                         ║
    ║   └─ Office blinds                                ║
    ║                                                    ║
    ║   🔊 NOTIFICATION SYSTEMS                         ║
    ║   ├─ Direct notifications (app)                   ║
    ║   ├─ Alexa announcements                          ║
    ║   ├─ Todo/shared notifications                    ║
    ║   └─ Alarm system integration                     ║
    ║                                                    ║
    ╚════════════════════════════════════════════════════╝
```

---

## 4. Key Automation Workflows

### 4.1 Doorbell Complete Workflow

**When Doorbell is Pressed**

```
Ring/Doorbell hardware detects button press
        ↓
Event: front_door_ding triggered
        ↓
Automation starts (PARALLEL processing)
        ↓
        ├─ Immediate Alerts (simultaneous):
        │  ├─ Send notification to Danny & Terina
        │  │  └─ "Someone pressed the door bell."
        │  │
        │  ├─ Alexa announcement throughout house
        │  │  └─ "Ding dong."
        │  │
        │  └─ Set wait flag for camera image
        │     └─ input_boolean.wait_for_doorbell_camera_update = on
        │
        └─ Delayed Processing (queued sequences):
           │
           ├─ Away-mode todo notification:
           │  ├─ Check: Are people home?
           │  ├─ If away: Get current todo items
           │  ├─ Check: Doorbell item already exists?
           │  └─ If not: Add "🚪 🔔 Someone rung the door bell." to todo list
           │
           └─ Camera image capture & video:
              ├─ Wait for camera state update (max 60 seconds)
              ├─ On timeout: STOP (don't send unverified notification)
              ├─ When image ready: Send snapshot notification
              │  └─ Include: entity_picture (still image)
              └─ Send video notification
                 └─ Include: video_url (video clip)
```

**Why This Design?**
- **Immediate alerts:** People know someone is at door immediately
- **Parallel processing:** All actions happen simultaneously
- **Wait for camera:** Ensures fresh image (not old cached version)
- **Todo list:** Persistent record when away (not missed)
- **No duplicates:** Template check prevents repeated entries
- **Multiple notifications:** Image + video provide full context

---

### 4.2 Vehicle Detection Workflow

**When Vehicle Detected on Driveway**

```
Driveway camera AI detects vehicle
        ↓
binary_sensor.driveway_vehicle_detected = on
        ↓
Vehicle Detected automation triggers
        ↓
Actions:
  ├─ Capture high-resolution snapshot
  ├─ Send alert notification with image
  ├─ If away-mode: Trigger alarm system
  └─ Optional: Record event timestamp

Home dashboard updates:
  └─ "Vehicle on driveway at [time]"
```

---

### 4.3 Privacy-Based Blind Closure

**When Front Garden Becomes Dark**

```
Sun sets (seasonal change)
        ↓
Ambient light drops below threshold
  (sensor.front_garden_motion_illuminance < threshold)
        ↓
"Below Direct Sun Light" automation triggers
        ↓
Check: Is it evening? (not midday)
        ├─ Season check (sensor.season)
        └─ Light level vs threshold
        ↓
If dark: Close blinds in all bedrooms
  ├─ Master bedroom (cover.bedroom_blinds)
  ├─ Ashlee's room (cover.ashlees_bedroom_blinds)
  ├─ Leo's room (cover.leos_bedroom_blinds)
  └─ Office (cover.office_blinds)
        ↓
Position: blind_closed_position_threshold
        ↓
Status: All window coverings drawn for privacy
```

---

## 5. Configuration Parameters

### Input Booleans

| Entity | Purpose | Default | Used In |
|--------|---------|---------|---------|
| `input_boolean.wait_for_doorbell_camera_update` | Flag to wait for fresh doorbell image | Off | Doorbell automation |
| `input_boolean.turn_on` | Generic on/off flag | Off | Conditional logic |

---

### Input Numbers

| Entity | Purpose | Range | Default | Unit |
|--------|---------|-------|---------|------|
| `input_number.blind_closed_position_threshold` | Position to consider blinds "closed" | 0-100 | 20 | % |
| `input_number.close_blinds_brightness_threshold` | Light level to trigger closure | 0-1000 | 250 | lux |

---

### Input Datetimes

| Entity | Purpose | Type |
|--------|---------|------|
| `input_datetime.childrens_bed_time` | Bedtime for children (affects blind timing) | Time picker |

---

## 6. Helper Entities & External Systems

### Notification Systems

| System | Purpose | Integration |
|--------|---------|-------------|
| `todo.shared_notifications` | Persistent todo list for doorbell alerts | Home Assistant native |
| `group.tracked_people` | Family members group for away/home logic | Home Assistant group |

### External Integrations

| System | Purpose | Details |
|--------|---------|---------|
| Ring Doorbell | Video doorbell + button events | `event.front_door_ding` |
| NFC Lock Box | Access control via NFC tags | Contact sensor + access logging |
| Vehicle Detection AI | Driveway security camera | `binary_sensor.driveway_vehicle_detected` |
| Alarm System | Security integration | `alarm_control_panel.house_alarm` |

---

## 7. Scripts Used

**Scripts Not Defined in front_garden.yaml** - Uses shared scripts:

- `script.send_direct_notification` - Send notification to specific people
  - Parameters: message, title, people (entity_id list)

- `script.send_direct_notification_with_url` - Send notification with media attachment
  - Parameters: message, title, people, url, url_type (image/video)

- `script.alexa_announce` - Make Alexa announcement
  - Parameters: message, suppress_if_quiet (bool)

- `script.send_to_home_log` - Log event to home log (if implemented)
  - Parameters: message, title, log_level

---

## 8. Sensors & Tracking

### Monitored States

- **Doorbell Events:** Logged via todo items and notifications
- **Vehicle Detection:** Binary sensor state + timestamp
- **Lock Box Access:** NFC reads + timestamp
- **Meter Access:** Contact sensor changes
- **Camera Status:** Video URL and entity picture tracking

### Data Points Stored

| Data Point | Storage | Purpose |
|-----------|---------|---------|
| Doorbell press events | Todo list | Persistent history (when away) |
| Video URLs | input_text.doorbell_last_video_id | Track latest footage |
| Vehicle detections | Binary sensor history | Review driveway activity |
| Lock box access | Event log | Audit trail for security |

---

## 9. Status Indicators

### Doorbell Status
- **Idle** → No recent press
- **Pressed** → Notifications sent
- **Waiting** → Camera image capture in progress
- **Complete** → Image + video notifications sent

### Vehicle Detection
- **Clear** → No vehicles on driveway
- **Detected** → Vehicle present, alert sent
- **Recording** → Camera capturing video

### Privacy Status
- **Exposed** → Blinds open, front of house visible
- **Private** → Blinds closed, bedrooms not visible

### Lock Box Status
- **Secured** → Door closed, locked
- **Accessed** → NFC tag detected
- **Offline** → Sensor unavailable

---

## 10. Key Features & Automations Highlights

### Comprehensive Doorbell System
- **Multi-Channel Alerts:** App notification + voice announcement + todo list
- **Media Capture:** Snapshot + video automatically sent
- **Away-Mode Integration:** Persistent todo list when family away
- **Duplicate Prevention:** Checks existing items before adding
- **Timeout Handling:** Waits up to 1 minute for fresh image, fails gracefully

### Vehicle Security Monitoring
- **AI Detection:** Classifies vehicles on driveway
- **High Resolution:** Captures detail for identification
- **Automatic Alerts:** Immediate notification when detected
- **Integration:** Optional alarm trigger if armed

### Privacy Protection
- **Light-Adaptive:** Closes blinds when front becomes dark
- **Seasonal Awareness:** Adjusts thresholds by season
- **Multi-Room:** Controls all bedroom + office blinds
- **Customizable:** Threshold configuration for tuning

### Access Logging
- **Lock Box Tracking:** Records NFC tag access
- **Meter Monitoring:** Tracks utility access
- **Sensor Health:** Detects offline/battery issues
- **Audit Trail:** Historical record of all access events

---

## Implementation Notes

### Ring Doorbell Setup

1. **Integration Installation**
   - Ring integration must be configured in Home Assistant
   - Event entity: `event.front_door_ding`
   - Camera entity: `camera.front_door`

2. **Video URL Attributes**
   - Doorbell must support video clips
   - Check that video_url attribute is populated
   - Test with manual snapshot to confirm access

3. **Download Directory**
   - Configure `/front_door/` directory for video archival
   - Ensure proper permissions for file write
   - Monitor disk space if archiving frequently

---

### Vehicle Detection Setup

1. **Camera AI Integration**
   - Driveway camera must have AI/ML capabilities
   - Or use integration with vehicle detection service
   - Test detection accuracy (false positives expected)

2. **Binary Sensor Calibration**
   - Adjust sensitivity if too many false triggers
   - Consider: Parked cars, packages, people

3. **Notification Targeting**
   - Decide if notifications should only when away
   - Or always alert for security purposes

---

### NFC Lock Box

1. **Reader Installation**
   - NFC reader must be near lock box
   - Test tag reads before automation activation

2. **Access Control**
   - Verify NFC tags are assigned to authorized users
   - Consider timeout mechanism (auto-lock)

3. **Battery Monitoring**
   - If battery-powered: Add low-battery alerts
   - Check status regularly

---

## Testing Checklist

- [ ] Doorbell press → Notifications received within 2 seconds
- [ ] Alexa announcement plays when doorbell pressed
- [ ] Camera snapshot received in notification
- [ ] Video clip sent after camera image
- [ ] Away-mode: Todo item added to shared list
- [ ] Home-mode: No duplicate todo items added
- [ ] Camera update detected → Video file downloaded
- [ ] Vehicle detected → High-res snapshot captured
- [ ] Vehicle alert received with image
- [ ] Evening light threshold → Blinds close automatically
- [ ] Lock box access → Event logged
- [ ] Meter door open → Notification received (if configured)

---

## Troubleshooting Guide

### Doorbell Notification Not Received

**Symptoms:** Doorbell pressed but no notification

**Diagnosis:**
1. Check automation is enabled
2. Verify event entity exists: `event.front_door_ding`
3. Check notification script is working
4. Verify people entities exist (person.danny, person.terina)

**Solutions:**
- Test automation manually
- Check Home Assistant logs for errors
- Verify notification service is working
- Test with different people entity

---

### Camera Image Not Sending

**Symptoms:** Doorbell alert received but no image in notification

**Diagnosis:**
1. Check camera entity status: `camera.front_door`
2. Verify camera is online and responsive
3. Check video_url attribute is populated
4. Verify wait_for_trigger is working

**Solutions:**
- Power cycle Ring doorbell
- Check camera integration connection
- Verify camera has recent activity
- Review automation logs for timeout

---

### Blinds Not Closing on Schedule

**Symptoms:** Evening arrives but blinds remain open

**Diagnosis:**
1. Check light sensor: `sensor.front_garden_motion_illuminance`
2. Verify blind covers are controllable
3. Check threshold is set correctly
4. Verify season sensor is accurate

**Solutions:**
- Adjust brightness threshold lower
- Test blinds manually to confirm controllable
- Check light sensor readings
- Review automation logs

---

## Related Documentation

- **Main package:** `packages/rooms/front_garden.yaml`
- **Related:** BACK-GARDEN-SETUP.md (garden security integration)
- **Scripts:** Check shared scripts for notification system

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-25 | Initial documentation generation | Claude Code |
| TBD | Ring doorbell integration review | Danny Tsang |
| TBD | Vehicle detection tuning | Danny Tsang |

---

**Documentation Status:** ✅ Complete
**Last Review:** 2026-01-25
**Next Review:** 2026-02-25
