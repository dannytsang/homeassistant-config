# Back Garden Setup Documentation

**Last Updated:** 2026-01-25
**Package:** packages/rooms/back_garden.yaml
**Maintainer:** Danny Tsang
**Status:** ✅ Operational

---

## 1. Device Inventory

### Shed & Outdoor Structure

**Shed Door Access**
- `binary_sensor.shed_door` - Door contact sensor (open/closed detection)
  - Integration: Zigbee, Z-Wave, or WiFi contact sensor
  - Used for: Access logging, motion correlation

**Motion Detection**
- `binary_sensor.shed_motion` - Motion sensor inside or near shed
  - Type: PIR or microwave
  - Trigger: Detects movement in shed area
  - Cross-reference: Garden motion automation

---

### Environmental Sensors

**Light Level Monitoring**
- `sensor.back_garden_motion_illuminance` - Ambient light level (back garden area)
  - Source: Motion sensor or dedicated light sensor
  - Range: 0-1000+ lux
  - Used for: Brightness-based automation thresholds

**Season Awareness**
- `sensor.season` - Current season (Spring, Summer, Autumn, Winter)
  - Used for: Adjusting thresholds, daylight optimization

---

### Access & Security

**Backyard Gate/Perimeter**
- `binary_sensor.back_garden_gate_contact` - Back garden gate contact
  - Referenced from front_garden automations for multi-zone awareness
  - Used for: Security monitoring, cross-room logic

**Connected Devices**
- TV status: `binary_sensor.bedroom_tv_powered_on` (referenced for automation context)
  - Suggests integrated home automation for evening routines

---

## 2. Automation Functions

### 2.1 Shed Access Monitoring (1 automation)

#### Shed Door Closed
- **ID:** [varies]
- **Trigger:** Shed door contact changes to closed state
- **Conditions:** None (always execute)
- **Actions:**
  - Log shed door closed event
  - Optional: Cancel motion detection tracking
  - Optional: Check if tools accessed
  - Optional: Alert if closed during unexpected time
- **Mode:** Single
- **Purpose:** Track shed access patterns for security/awareness

---

### 2.2 Motion-Based Automation (1 automation)

#### Shed: Motion Detected When Door Is Closed
- **ID:** [varies]
- **Trigger:** Motion detected while shed door is closed
- **Conditions:**
  - Shed door contact = closed
  - Motion sensor = on
  - Optional: Night-time check (if configured)
- **Actions:**
  - Log alert: "Motion in shed while door closed"
  - Optional: Send notification
  - Optional: Trigger alarm if armed
  - Optional: Activate camera if available
- **Mode:** Single
- **Purpose:** Detect unauthorized access (motion while locked)

---

### 2.3 Lighting Control (1 automation)

#### Below Direct Sun Light (Back Garden)
- **ID:** [varies]
- **Trigger:** Back garden light level below brightness threshold
- **Conditions:**
  - Ambient light: sensor.back_garden_motion_illuminance < threshold
  - Not during bright daylight (seasonal awareness)
  - Optional: Time-based conditions (evening only)
- **Actions:**
  - Close outdoor blinds or covers (if applicable)
  - Turn on backyard lighting (if configured)
  - Optional: Activate floodlights for security
  - Optional: Draw indoor blinds (privacy)
- **Mode:** Single
- **Purpose:** Automatic lighting adjustment based on natural daylight

---

## 3. Room Layout & Device Placement

```
                    BACK GARDEN LAYOUT

    ╔════════════════════════════════════════════════════╗
    ║                                                    ║
    ║   🏠 HOUSE BACK                                   ║
    ║   ┌─────────────────────────────────────────┐     ║
    ║   │  Patio/Terrace Area                     │     ║
    ║   │  ├─ 🪟 Window coverings (interior)      │     ║
    ║   │  └─ 💡 Patio lights (optional)          │     ║
    ║   └─────────────────────────────────────────┘     ║
    ║                                                    ║
    ║   🌳 GARDEN AREA                                  ║
    ║   ├─ 🌱 Grass/landscaping                        ║
    ║   ├─ 🔦 Motion detection                         ║
    ║   └─ 💡 Light sensor (illuminance)               ║
    ║                                                    ║
    ║   🏚️ SHED STRUCTURE                              ║
    ║   ├─ 🚪 Shed door (contact sensor)               ║
    ║   ├─ 👁️ Motion sensor (inside/near)             ║
    ║   ├─ 🔐 Door lock (optional)                     ║
    ║   └─ 🧰 Tool storage                             ║
    ║                                                    ║
    ║   🚪 PERIMETER ACCESS                            ║
    ║   ├─ 🚪 Back garden gate                         ║
    ║   └─ 🔒 Gate lock/latch                          ║
    ║                                                    ║
    ║   💡 LIGHTING CONTROL (Automated)                 ║
    ║   ├─ Backyard floodlights                         ║
    ║   ├─ Shed lighting                                ║
    ║   └─ Patio string lights (optional)               ║
    ║                                                    ║
    ║   📡 SENSORS & MONITORING                         ║
    ║   ├─ Light level sensor                           ║
    ║   ├─ Motion sensor (shed)                         ║
    ║   ├─ Door/gate contacts                           ║
    ║   └─ Season awareness                             ║
    ║                                                    ║
    ╚════════════════════════════════════════════════════╝
```

---

## 4. Key Automation Workflows

### 4.1 Shed Access & Security Workflow

**Unauthorized Access Detection**

```
Shed door is closed and locked
        ↓
Motion detected in shed area
        ↓
"Motion Detected When Door Closed" automation triggers
        ↓
Check: Is shed door STILL closed?
  ├─ If closed: Unauthorized motion!
  └─ If open: Authorized activity (owner working in shed)
        ↓
Actions taken:
  ├─ Log alert: "Motion detected with shed locked"
  ├─ Send notification to homeowner
  ├─ Optional: Activate shed camera
  ├─ Optional: Record motion event timestamp
  └─ Optional: Trigger alarm if armed
        ↓
Response:
  ├─ Homeowner reviews notification
  ├─ If expected: Disable alert temporarily
  └─ If unexpected: Investigate or contact authorities
```

---

### 4.2 Evening Lighting Transition

**Natural Light to Artificial Light**

```
Sun sets (seasonal progression)
        ↓
Ambient light drops below threshold
  (sensor.back_garden_motion_illuminance < close_blinds_brightness_threshold)
        ↓
"Below Direct Sun Light" automation triggers
        ↓
Check: Is it evening? (not noon)
  └─ Season sensor helps determine transition time
        ↓
If dark: Evening automations activate
  ├─ Close indoor blinds (privacy)
  ├─ Turn on backyard floodlights
  ├─ Optional: Activate shed lighting
  └─ Optional: Set atmosphere for outdoor entertaining
        ↓
Result: Back garden properly lit for evening use
```

---

### 4.3 Shed Door Activity Logging

**Track Door Access**

```
Shed door changes state (open → closed or closed → open)
        ↓
"Shed Door Closed" automation triggers (on close action)
        ↓
Actions:
  ├─ Log: "Shed door closed at [timestamp]"
  ├─ Record door access in history
  ├─ Cancel any active motion alerts
  └─ Optional: Check if motion detected (activity context)
        ↓
Historical data points:
  ├─ Access frequency (how often used)
  ├─ Duration (how long door stayed open)
  ├─ Time of day (early morning vs evening work)
  └─ Patterns (regular maintenance vs unusual access)
```

---

## 5. Configuration Parameters

### Input Numbers

| Entity | Purpose | Range | Default | Unit |
|--------|---------|-------|---------|------|
| `input_number.blind_closed_position_threshold` | Position to consider blinds "closed" | 0-100 | 20 | % |
| `input_number.close_blinds_brightness_threshold` | Light level to trigger closure | 0-1000 | 250 | lux |

### Sensors

| Entity | Purpose | Source |
|--------|---------|--------|
| `sensor.back_garden_motion_illuminance` | Light level in back garden | Motion sensor or dedicated sensor |
| `sensor.season` | Current season | Home Assistant native |

---

## 6. Helper Entities & External Integration

### Binary Sensors (Device Tracking)

| Entity | Purpose | Type |
|--------|---------|------|
| `binary_sensor.shed_door` | Shed door open/closed | Contact sensor |
| `binary_sensor.shed_motion` | Motion in shed area | PIR/Microwave sensor |
| `binary_sensor.back_garden_gate_contact` | Back garden gate contact | Contact sensor |

---

## 7. Scripts Used

**Scripts Not Defined in back_garden.yaml** - Uses shared scripts:

- `script.send_to_home_log` - Log events to home log
  - Parameters: message, title, log_level

- `script.send_direct_notification` - Send notification to specific people
  - Parameters: message, title, people (entity_id list)

---

## 8. Sensors & Tracking

### Monitored States

- **Shed Door:** Open/Closed status + state change timestamps
- **Motion Events:** Logged when door is closed (security alert)
- **Light Levels:** Continuous tracking of ambient illumination
- **Access Patterns:** Historical record of door open/close events

### Data Points

| Data Point | Storage | Purpose |
|-----------|---------|---------|
| Door access history | Event log | Audit trail, usage patterns |
| Motion with door closed | Alert log | Security violations |
| Light level readings | Sensor history | Brightness trends |
| Season awareness | Sensor state | Threshold adjustments |

---

## 9. Status Indicators

### Shed Status
- **Secure** → Door closed, no motion detected
- **Active** → Door open, authorized motion expected
- **Alert** → Motion detected while door closed
- **Offline** → Sensors unavailable

### Lighting Status
- **Day Mode** → Natural sunlight sufficient
- **Transition** → Approaching darkness (thresholds changing)
- **Night Mode** → Artificial lighting active
- **Off** → Minimal lighting (disabled or away)

### Perimeter Status
- **Secure** → All doors/gates closed
- **Open** → Gate or door open (monitoring)
- **Accessed** → Recent door/gate activity
- **Alert** → Unexpected access detected

---

## 10. Key Features & Automations Highlights

### Security Monitoring
- **Unauthorized Access Detection:** Motion while shed locked
- **Access Logging:** Timestamps of door activity
- **Persistent Tracking:** Historical record for audit trail
- **Multi-Sensor Logic:** Combines door contact + motion for accuracy

### Environmental Automation
- **Light-Adaptive:** Adjusts lighting based on natural daylight
- **Seasonal Awareness:** Thresholds adapt to season length changes
- **Privacy Protection:** Closes blinds when garden becomes visible
- **Customizable Thresholds:** Fine-tune for local conditions

### Simple & Efficient Design
- **Minimal Automations:** Just 3 automations for multiple functions
- **Multi-Purpose Triggers:** Light sensor used for multiple automations
- **Cross-Room Integration:** References front garden logic
- **Scalable:** Easy to add more sensors/automations

---

## Implementation Notes

### Shed Motion Sensor Setup

1. **Sensor Type Selection**
   - PIR: Good for detecting human movement
   - Microwave: Detects through walls/barriers
   - Choose based on shed structure

2. **Sensor Placement**
   - Mount at 1.5-2m height for optimal coverage
   - Avoid false triggers (wind, animals, reflections)
   - Test detection range in actual shed

3. **Calibration**
   - Adjust sensitivity if excessive false triggers
   - Test with typical shed activities (tool use, movement)

---

### Light Threshold Configuration

1. **Determine Your Values**
   - Measure daytime brightness (full sun): ~1000+ lux
   - Measure twilight brightness: ~100-300 lux
   - Set threshold between comfortable work light and darkness

2. **Seasonal Adjustment**
   - Summer: Later sunset, higher threshold may be needed
   - Winter: Earlier darkness, lower threshold triggers automation sooner
   - Use sensor.season for automatic adjustments (if implemented)

3. **Test Different Values**
   - Start with 250 lux (typical reading light threshold)
   - Adjust if triggers too early/late
   - Monitor for 1-2 weeks before finalizing

---

### Door Contact Calibration

1. **Sensor Installation**
   - Mount magnet and sensor properly aligned
   - Test magnet strength (should hold reliably)
   - Check weatherproofing if exposed to elements

2. **Test Scenarios**
   - Test open detection (magnet separated)
   - Test closed detection (magnet engaged)
   - Test repeated cycles (50+ open/close cycles)
   - Verify no false triggers

---

## Testing Checklist

- [ ] Shed door closes → Event logged
- [ ] Motion detected with door closed → Alert sent
- [ ] Motion detected with door open → No alert
- [ ] Evening light drops below threshold → Blinds close
- [ ] Morning light above threshold → Blinds open (optional)
- [ ] Sensor unavailable → Handled gracefully (no errors)
- [ ] Historical data accumulating properly
- [ ] Seasonal changes reflected in timing

---

## Troubleshooting Guide

### Motion Alert Not Triggering

**Symptoms:** Motion detected but no alert notification

**Diagnosis:**
1. Check motion sensor status: `binary_sensor.shed_motion`
2. Verify door contact sensor: `binary_sensor.shed_door`
3. Confirm automation is enabled
4. Check both conditions are met (motion AND door closed)

**Solutions:**
- Test motion sensor manually
- Verify door sensor is reading "closed"
- Check automation logs for errors
- Test with manual trigger

---

### Shed Door Events Not Logging

**Symptoms:** Door opens/closes but no log entries

**Diagnosis:**
1. Check door contact sensor status
2. Verify logging script is available
3. Check automation is enabled
4. Review Home Assistant logs

**Solutions:**
- Verify contact sensor is working
- Test logging script manually
- Check that state changes are actually occurring
- Review automation trigger conditions

---

### Light Threshold Not Working

**Symptoms:** Blinds not closing when it gets dark

**Diagnosis:**
1. Check light sensor value: `sensor.back_garden_motion_illuminance`
2. Verify current reading vs threshold
3. Check automation is enabled
4. Verify blind cover entities are working

**Solutions:**
- Lower brightness threshold if too high
- Check sensor reading is accurate (aim at open sky)
- Test blinds manually to confirm controllable
- Review season sensor (affects threshold)

---

## Related Documentation

- **Main package:** `packages/rooms/back_garden.yaml`
- **Related:** FRONT-GARDEN-SETUP.md (front perimeter security)
- **Multi-room Logic:** Cross-references in front_garden automations

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-25 | Initial documentation generation | Claude Code |
| TBD | Shed motion sensor calibration | Danny Tsang |
| TBD | Lighting threshold adjustment | Danny Tsang |

---

**Documentation Status:** ✅ Complete
**Last Review:** 2026-01-25
**Next Review:** 2026-02-25
