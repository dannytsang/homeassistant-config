# Home Assistant Home Systems

**Last Updated:** 2026-01-22
**Scope:** Lighting, Climate, Security, Presence, Media, Blinds

---

## Lighting System

### Hardware
- **Philips Hue** (motion sensors, bulbs)
- **LIFX** (candles, color bulbs, mini white)
- **Innr Smart Bulbs** (E14)
- **Elgato Key Light** (studio lighting)
- **73 total lights** across multiple rooms

### Automation Features
- **Scene-based automation** with 75 pre-configured scenes
- **Motion-based triggering** with illuminance thresholds
- **Adaptive lighting** (color temp changes based on time)
- **Dynamic thresholds** - Living room changes from 81 to 30 lux based on Terina's work laptop status
- **Context-aware responses** - Different lighting based on room brightness and occupancy

### Motion-Based Patterns
- Living room motion → check light level + work laptop status → adjust thresholds
- Kitchen motion on different zones (table lights, cooker lights)
- Conservatory motion with door open detection
- Porch/front door occupancy detection

### Scene Usage
- Pre-configured scenes for each room state (on, off, dim, color presets)
- Transition times (0-2s depending on automation type)
- Parameterized scenes with brightness and color

---

## Climate Control (HVAC)

### Hardware
- **Hive Active Heating** (SLT3) - central heating hub
- **TRV radiators** across 6+ rooms (Tuya-based)
- **Eddi solar diverter** - intelligent hot water heating from excess solar
- **Temperature sensors** in fridge and freezers (TuYa)

### Automation Features
- **Dynamic heating scheduling** based on presence and weather
- Conservatory below 3°C → boost heating
- Radiators below target temperature (by room) → alert
- Heating turn-on checks (office window open, etc.)
- Set to home mode when people arrive
- Off when no one home
- Radiator TRV synchronization with thermostat

### Climate Entities
- `climate.thermostat` - Hive heating hub
- Modes: `heat`, `off`, `auto`
- TRV control via Tuya integration

---

## Security & Monitoring

### Security Hardware
- **Ring Doorbell 2** + **Ring Alarm System** (1st gen with 2nd gen sensors)
- **Reolink RLC-520A** camera
- **Ubiquiti Protect** cameras (G4 Instant, G5 Flex, G6 Instant, G6 Turret)
- **Nest Protect** smoke/CO detectors
- **Nuki smart lock** (front door)
- **NFC tag scanning** for automation triggers (bedroom, front door)
- **Contact sensors** on all doors/windows

### Alarm States
- `armed_away` - No one home, full perimeter protection
- `armed_home` - Everyone home, perimeter + interior checks
- `disarmed` - Normal operation

### Alarm Automations
- Motion detected in office/kitchen while armed_home (logs alert)
- Door armed (NFC tag triggers office door alarm)
- Overnight arm (midnight with various retry times 00:00, 01:00, 02:00)
- Checks all doors/windows are closed before arming
- Sets heating to home mode when disarmed
- Auto-disarm when approaching home
- Auto-lock house when everyone leaves

### NFC Integration
- **Front door tag** → unlock + log
- **Bedroom right tag** → turn everything off
- User context preserved (logs who scanned)

---

## Presence Detection & Home Modes

### Multi-Layer Presence Tracking
- **GPS-based distance sensors** (heading towards home, close to home, far away)
- **Network-based device tracking** (computers, Nintendo Switch)
- **Multiple people tracked:** Danny, Terina, Leo, Ashlee
- **Family calendar integration** (holiday detection)

### Home Modes
1. **Normal** - Everyone home
2. **Holiday** - Long distance away, fake presence lights
3. **No Children** - Kids away, different automation rules
4. **Naughty Step Mode** - Discipline mode (disables motion triggers in certain areas)

### Presence Automations
- Auto-disarm alarm when approaching home
- Turn on lights when arriving in the dark
- Announce delayed notifications
- Auto-lock house when everyone leaves
- Holiday fake presence (random lights 17:00-22:00)
- Children home in "No Children" mode → auto-switch to Normal

### Fake Presence During Holiday Mode
Random light selection during away periods:
- Downstairs: up to 3 lights ON simultaneously
- Upstairs: 1 light ON
- 15-minute intervals from sunset to 22:00
- Only when far away and armed_away

---

## Smart Home Connectivity

### Voice Assistants
- **Alexa Media Player** (custom component v5.9.0)
  - 5 Echo devices (1st Gen, Dot 2nd/3rd Gen, Show 10 2nd Gen, Show 5 1st Gen)
  - Script: `script.alexa_announce` for announcements
- **Home Assistant Mobile App** with notification actions

### Media & Entertainment
- **Google Chromecast** devices (Chromecast Ultra, Google TV)
- **Spotify integration** with source-following automation
- **Music follows Danny** via BLE area detection

---

## Blind & Cover Automation

### Hardware
- **IKEA FYRTUR/KADRILJ** roller blinds with repeaters
- **SwitchBot Blind Tilt** + Hub Mini
- **25 total covers** including roller shades

### Blind Control Conventions

Tilt position reference (SwitchBot Blind Tilt):
```
0    = Fully closed (no light through)
25   = Partially open (angled, some light, some privacy)
50   = Half open (maximum airflow while maintaining privacy)
75   = Mostly open (primarily for light/view)
100  = Fully open (no obstruction)
```

### Automation Logic

**Weather-based:**
- Close blinds when temperature drops (cold protection)
- Close blinds before sunset in bedrooms
- Adjust blind positions based on sun angle

**Presence-based:**
- Close bedroom blinds when occupant in bed after sunset
- Open blinds when waking up
- Leo's bed occupancy triggers blind closing (with window safety check)

**Safety Interlocks:**
- **Waits up to 3 hours for window to close** before closing blinds
- Prevents accidental entrapment or damage

### Blind Consolidation Pattern

When an action checks the same condition multiple times, consolidate into a single action:

```yaml
# WRONG - Redundant condition checking (condition checked, then re-checked in action)
conditions:
  - condition: numeric_state
    entity_id: cover.blind_left
    attribute: current_tilt_position
    below: 50
actions:
  - parallel:
      - if:
          - condition: numeric_state
            entity_id: cover.blind_left
            attribute: current_tilt_position
            below: 50
        then:
          - action: cover.set_cover_tilt_position
            ...

# CORRECT - Single action targeting all blinds
conditions:
  - condition: numeric_state
    entity_id: cover.blind_left
    attribute: current_tilt_position
    below: 50
actions:
  - action: cover.set_cover_tilt_position
    data:
      tilt_position: 50
    target:
      entity_id:
        - cover.blind_left
        - cover.blind_middle
        - cover.blind_right
```

**Benefit:** Reduces from 37 lines to 8 lines while maintaining exact behavior.

---

## Occupancy & Bed Detection

### Sophisticated Bed Occupancy Sensors
- **4-point pressure sensors** (ADS1115) - Detect occupied vs. unoccupied
- **BME680 air quality sensor** - Breathing detection for sleeping state
- **Custom IAQ calculation:** `log(gas_resistance) + 0.04 * humidity`
- Separate sensors for: Danny's bed, Ashlee's bed, Leo's bed

### Usage Patterns
- Bed occupancy triggers night mode automations
- Breathing detection distinguishes between "in bed" and "asleep"
- Integrates with heating and blind automation

---

## Notable Automation Patterns

### 1. Dynamic Illuminance Thresholds
Living room motion automation changes brightness thresholds based on Terina's work laptop:
- Laptop ON: 81 and 65 lux (need brighter light)
- Laptop OFF: 30 and 25 lux (okay with dimmer light)

### 2. Context-Aware Lighting Branches
```yaml
automation:
  - alias: "Room: Motion Detected - Lights"
    triggers:
      - trigger: state
        entity_id: binary_sensor.room_motion
        to: "on"
    actions:
      - choose:
          # Branch 1: Dark room - turn on lights normally
          - alias: "Room Dark - Turn Lights On"
            conditions:
              - condition: numeric_state
                entity_id: sensor.room_illuminance
                below: 30
            sequence:
              - action: scene.turn_on
                target:
                  entity_id: scene.room_lights_on

          # Branch 2: Bright room - Flash lights as motion signal
          - alias: "Room Bright - Flash Motion Signal"
            conditions:
              - condition: numeric_state
                entity_id: sensor.room_illuminance
                above: 30
            sequence:
              - action: script.flash_lights_yellow
```

### 3. Multi-Layer Safety Interlocks
- Window contact check before closing blinds (3-hour wait)
- Door closure verification before arming alarm
- Heating state checks before adjusting radiators
- Motion detection disabled during "Naughty Step Mode"
