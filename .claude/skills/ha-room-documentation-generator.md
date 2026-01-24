# Claude Skill: Home Assistant Room Documentation Generator

**Status:** Production Ready
**Version:** 1.0
**Created:** 2026-01-24
**Based On:** Office Setup Documentation Example

---

## Purpose

Generate comprehensive, standardized room documentation for Home Assistant packages by analyzing automation YAML files and creating structured markdown guides that describe devices, capabilities, functions, and room layout.

---

## When to Use

- After creating a new room package
- When reviewing existing room configurations
- For documentation completeness audits
- To onboard team members or future self
- Before sharing automation setup with others
- When a room's automation complexity warrants documentation

---

## Documentation Structure

### Section 1: Device Inventory

**Purpose:** Catalog all devices in the room

**Format:** Table with columns:
- Category (Lighting, Motion, Environment, Climate, etc.)
- Device name (entity_id format)
- Device type (what kind of device it is)
- Function (what it does)

**Sources:**
- Light entities (`light.*`)
- Binary sensors (`binary_sensor.*`)
- Numeric sensors (`sensor.*`)
- Switches (`switch.*`)
- Covers (`cover.*`)
- Groups (`group.*`)
- Extract from automation files

**Example:**
```yaml
| Lighting | light.office_2 | Color Temperature Light | Main ambient lighting |
```

---

### Section 2: Automation Functions

**Purpose:** Explain each major automation category

**For Each Automation Category:**
1. **Emoji Header** + Category Name (e.g., 🔆 Motion-Based Lighting)
2. **Triggers:** What starts this automation
3. **Logic:** How it decides what to do
4. **Related Automations:** Link automation IDs

**Key Information to Extract:**
- Trigger types (state, numeric_state, time, event, etc.)
- Conditions (time windows, entity states, thresholds)
- Actions (scene turns, service calls, notifications)
- Variables used
- Timing (delays, timers, durations)

**Template:**
```markdown
### [Emoji] [Category Name]

**Triggers:** [What starts it]

**Logic:**
- [Decision point 1]
- [Decision point 2]

**Safety Features:**
- [Safety mechanism 1]

**Related Automations:**
- [ID] - [Alias]
```

---

### Section 3: Room Layout ASCII Diagram

**Purpose:** Visual representation of room and device placement

**Elements to Include:**
- Room boundaries (╔═════╗ style box)
- Device positions with emoji icons
- Device labels and descriptions
- Sensor placement
- Lighting locations
- Direction markers (NORTH/SOUTH/EAST/WEST)

**Emoji Reference:**
- 💡 = Light
- 🪟 = Window/Blind
- 🌡️ = Thermometer
- 📏 = Motion sensor
- 💻 = Computer
- 🖥️ = Monitor/Desktop
- 💨 = Fan
- 🎙️ = Audio device
- 🎮 = Gaming device
- 📡 = Network/Remote
- 🐾 = Motion indicator
- 🚷 = No motion
- ☀️ = Sun-related
- 🔌 = Power/Plug

**Example Structure:**
```
        NORTH (Morning Sun)
╔═════════════════════════════════════╗
║  🪟 Window                          ║
║  ▼ Motorized Blind                  ║
║                                     ║
║  ┌──────────┐                       ║
║  │   Desk   │  💡 Lights            ║
║  │          │                       ║
║  │ 💻 PC    │  🌡️ Sensors          ║
║  └──────────┘                       ║
║                                     ║
╚═════════════════════════════════════╝
       SOUTH (Afternoon Sun)
```

---

### Section 4: Key Automation Workflows

**Purpose:** Explain how automations interact over time

**For Each Major Time Period:**
1. **Title:** What time of day/condition
2. **ASCII Flow Diagram:** How automations trigger
3. **Decision Tree:** What logic applies

**Time Periods to Consider:**
- Morning routine (8:00 AM)
- During work/active hours
- After work/sunset
- Evening
- Night
- All-day/weather-based

**Template:**
```markdown
### [Time Period/Scenario]

[ASCII diagram showing flow]

**Decision Tree:**
1. Is [condition]? → Continue
2. Check [parameter]
3. Apply [action]
```

---

### Section 5: Configuration Parameters

**Purpose:** List all configurable input helpers and thresholds

**Include:**
- `input_number.*` entities (thresholds, times)
- `input_boolean.*` entities (enable/disable switches)
- `input_datetime.*` entities (time-based inputs)
- `input_select.*` entities (mode selections)

**Format:**
```markdown
### [Category]
- `entity_id` - Description (value/range)
```

---

### Section 6: Helper Entities

**Purpose:** Document supporting Home Assistant entities

**Categories:**
- Input Booleans (enable/disable automations)
- Timers (delays, countdowns)
- Groups (device collections)
- Input Numbers (thresholds)

**Format:** List with descriptions

---

### Section 7: Scripts & Actions

**Purpose:** Document custom scripts used by automations

**For Each Script:**
- Script name
- Purpose
- When called
- What it does

**Example:**
```markdown
### Blind Control
- `office_open_blinds` - Opens blinds to 50% tilt
- `office_close_blinds` - Fully closes blinds (0% tilt)
```

---

### Section 8: Sensors

**Purpose:** Document custom sensors and history stats

**Include:**
- History stats sensors
- Template sensors
- Calculated values

---

### Section 9: Status Indicators

**Purpose:** Explain notification/status lights if present

**If RGB Status Light:**
- Colors used
- What each color means
- Trigger conditions
- Duration shown

---

### Section 10: Key Features Summary

**Purpose:** Highlight unique capabilities

**Format:** Checklist with ✅ emoji

**Include Top 8-10 Features:**
- What makes this room special
- Advanced automations
- Unique integrations
- User-facing capabilities

---

## Analysis Process

### Step 1: Identify Room Package

```bash
# Find room YAML files
find packages/rooms/[room_name] -name "*.yaml"

# Get basic stats
wc -l [room].yaml
grep -c "^  - id:" [room].yaml  # Count automations
```

### Step 2: Extract Device Information

**Search for:**
- All `entity_id:` references (what devices are used)
- Device domains (light, sensor, switch, cover, etc.)
- Device names and grouping patterns

**Document:**
- Entity IDs
- Device types
- Functions in automations

### Step 3: Categorize Automations

**Group by function:**
- Motion/Presence
- Lighting
- Temperature/Climate
- Window/Blinds
- Computer/Device
- Notifications
- Time-based

**For each category:**
- Extract automation IDs and aliases
- Identify triggers
- Map conditions
- Document actions

### Step 4: Identify Workflows

**Look for:**
- Time-based sequences
- Cascading automations
- Conditional branches
- Long-running timers

**Document interaction flow:**
- What happens after X?
- What blocks Y?
- When does Z activate?

### Step 5: Sketch Room Layout

**Based on:**
- Device placement hints in descriptions
- Typical room layouts
- Device function (windows = perimeter, desk = center)
- Automation patterns (sun tracking suggests window orientation)

**Create ASCII diagram:**
- Room outline
- Device placement with emoji
- Labels and descriptions

### Step 6: Extract Configuration

**Find all input helpers:**
```bash
grep -E "input_number\.|input_boolean\.|input_datetime\." [room].yaml
```

**Document:**
- Entity names
- Purpose
- Typical values

### Step 7: Generate Markdown

**Template structure:**
1. Header with metadata
2. Device inventory table
3. Automation functions (by category)
4. Room layout diagram
5. Workflow diagrams
6. Configuration parameters
7. Helper entities
8. Scripts section
9. Sensors section
10. Status indicators
11. Key features
12. File structure
13. Footer with metadata

---

## Output Format

**File Location:** `packages/rooms/[room_name]/[ROOM_NAME]-SETUP.md`

**File Naming Convention:**
- All caps room name
- Hyphenated format
- `SETUP.md` suffix
- Example: `OFFICE-SETUP.md`, `KITCHEN-SETUP.md`, `LIVING-ROOM-SETUP.md`

**File Size:** Typically 1000-2000 lines (comprehensive)

**Metadata Section:**
- Created date
- Room name
- Primary focus/purpose
- Documentation version

---

## Quality Checklist

### Content Completeness
- [ ] All automations categorized
- [ ] All devices listed in inventory
- [ ] All workflows documented
- [ ] Room layout diagram created
- [ ] Configuration parameters listed
- [ ] Helper entities documented
- [ ] Scripts/actions explained
- [ ] Status indicators documented

### Structure Quality
- [ ] Clear section headers
- [ ] Consistent formatting
- [ ] Table formatting correct
- [ ] ASCII diagrams render properly
- [ ] Code blocks formatted
- [ ] Links work (if internal refs)
- [ ] Emoji used appropriately

### Accuracy
- [ ] Automation IDs correct
- [ ] Entity names match YAML
- [ ] Logic descriptions accurate
- [ ] Workflow sequences correct
- [ ] Thresholds/parameters correct
- [ ] Room layout realistic

### Usability
- [ ] Easy to scan
- [ ] Quick reference section (top 8-10 features)
- [ ] Related automations linked
- [ ] Clear explanations (non-technical where possible)
- [ ] Examples provided
- [ ] Edge cases documented

---

## Common Patterns to Document

### Pattern 1: Motion-Based Lighting
**Triggers:** Motion on/off
**Logic:** Brightness-aware, timer-delayed off
**Variables:** Light level thresholds

### Pattern 2: Temperature Control
**Triggers:** Numeric thresholds
**Logic:** Graduated response (warning → action → emergency)
**Variables:** Temp thresholds, time windows

### Pattern 3: Sun/Blind Management
**Triggers:** Sun events, brightness, position
**Logic:** Azimuth/elevation tracking, time-based fallback
**Variables:** Sun angles, brightness thresholds

### Pattern 4: PC/Device Integration
**Triggers:** Device presence/state
**Logic:** Cascading actions (on/off at time intervals)
**Variables:** Time delays, related devices

### Pattern 5: Notification System
**Triggers:** Various conditions
**Logic:** Status light colors, duration, priority
**Variables:** Colors, durations, conditions

---

## Template Document

```markdown
# [Room Name] Setup Documentation

**Created:** [Date]
**Room:** [Room Name] ([Description/Purpose])
**Focus:** [Primary automation focus - Lighting/Climate/PC/etc.]

---

## Device Inventory

[Table with Category | Device | Type | Function]

---

## Automation Functions

### [Emoji] [Category Name]
[Details...]

---

## Room Layout & Device Placement

[ASCII diagram]

---

## Key Automation Workflows

### [Time Period/Scenario]
[Flow diagram and decision tree]

---

## Configuration Parameters

[Grouped lists of input helpers]

---

## Helper Entities

[Groups, timers, booleans]

---

## Scripts

[Custom scripts used]

---

## Sensors

[Sensors and history stats]

---

## Status Indicators

[Notification lights, color meanings]

---

## Key Features

[Checklist of top 8-10 features]

✅ [Feature 1]
✅ [Feature 2]
...

---

## File Structure

[Directory layout]

---

**Last Updated:** [Date]
**Documentation Version:** 1.0
**Automation Count:** [N]
**Device Count:** [N]
**Configuration Files:** [N]
```

---

## Usage Instructions

### For Claude (When Generating Docs)

1. **Read the room YAML file** completely
2. **Extract all device entities** from automations
3. **Categorize automations** by function
4. **Analyze workflows** - how do they interact?
5. **Sketch room layout** - typical setup for the room type
6. **Create ASCII diagram** - visual representation
7. **Document workflows** - morning/during/evening routines
8. **Extract configuration** - all input helpers
9. **Generate markdown** - using template structure
10. **Quality check** - verify accuracy and completeness

### For Future Reference

1. **Use this skill when:**
   - Creating documentation for any room
   - Onboarding new team members
   - Planning room automation expansion
   - Sharing setup with others
   - Building automation portfolio

2. **Adapt for different room types:**
   - Bedroom: Focus on sleep/wake cycles, privacy
   - Kitchen: Focus on appliances, cooking
   - Living Room: Focus on entertainment, comfort
   - Office: Focus on work ergonomics, PC integration
   - Bathroom: Focus on humidity, ventilation

3. **Scale documentation complexity:**
   - Simple rooms: 500-800 lines
   - Medium complexity: 1000-1500 lines
   - Highly automated: 1500-2000+ lines

---

## Examples by Room Type

### Bedroom Documentation Would Focus On:
- Sleep/wake cycles
- Circadian lighting
- Temperature comfort
- Morning/evening routines
- Privacy features (blinds)
- Alarm integration

### Kitchen Documentation Would Focus On:
- Appliance integration
- Motion-based task lighting
- Temperature management
- Multiple motion zones
- Notification lights
- Cooking automation

### Living Room Documentation Would Focus On:
- Entertainment systems
- Comfort lighting
- Guest mode
- Movie/TV automation
- Multiple occupancy
- Social spaces

---

## Benefits of This Skill

✅ **Standardized Documentation** - Consistent format across all rooms
✅ **Easy Onboarding** - New users understand automation quickly
✅ **Maintenance Reference** - Quick lookup for configurations
✅ **Future Planning** - See what's possible in room automation
✅ **Knowledge Preservation** - Document why automations work this way
✅ **Portfolio Building** - Showcase your Home Assistant expertise
✅ **Debugging Aid** - Understand automation flow when troubleshooting
✅ **Communication** - Explain setup to family/guests/technical support

---

## Integration with Other Skills

**Before Generating Docs:**
- Use Consolidation Analyzer to identify optimization opportunities
- Use Motion Consolidator if motion automations can be merged
- Use YAML Quality Reviewer to ensure config is clean

**After Generating Docs:**
- Use Reflection Reviewer to update docs when automations change
- Use Motion Consolidator if docs reveal consolidation opportunities
- Share docs with team for feedback

---

## Future Enhancements

### Version 1.1 (Planned)
- Automated device extraction from YAML
- Device family categorization
- Automation dependency mapping
- Cross-room reference detection

### Version 2.0 (Planned)
- Interactive HTML generation
- Real-time device status display
- Automation execution logs
- Performance metrics

### Version 3.0 (Planned)
- Multi-room comparison
- Home-wide documentation
- Automation templates
- Setup recommendations

---

## Best Practices

1. **Be Thorough** - Document every automation and device
2. **Be Clear** - Explain in user-friendly language
3. **Use Examples** - Show real automation scenarios
4. **Maintain Accuracy** - Double-check automation IDs and logic
5. **Keep Updated** - Refresh when automations change
6. **Use Emojis** - Improve visual scanning
7. **Create Diagrams** - ASCII art helps visualize
8. **Link References** - Cross-reference related automations

---

## Next Steps

1. Use this skill to document remaining rooms
2. Gather feedback from documentation users
3. Refine template based on room types
4. Create quick-reference cards (1 page per room)
5. Build home automation portfolio
6. Share setup with Home Assistant community

---

**Usage:** Invoke when creating comprehensive room setup documentation
**Team:** Danny's Home Assistant optimization
**Created:** 2026-01-24
**Status:** Production Ready
