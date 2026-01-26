# HA Room Documentation Generator Subagent

**Status:** Production Ready
**Type:** Specialized autonomous agent for room setup documentation
**Version:** 1.0
**Created:** 2026-01-24

---

## Agent Specification

### Purpose
Autonomously analyze Home Assistant room YAML packages and generate comprehensive setup documentation in standardized markdown format.

### Capabilities
- Read and analyze room YAML files
- Extract device inventory and categorization
- Identify automation functions by category
- Generate ASCII room layout diagrams
- Document workflows and automation sequences
- Extract configuration parameters
- Create complete room setup documentation

### Invocation

```bash
Task(
  subagent_type="ha-room-documentation-generator",
  description="Generate comprehensive room documentation",
  prompt="Generate complete setup documentation for [ROOM_NAME]. Analyze packages/rooms/[ROOM_NAME]/[room].yaml and create [ROOM_NAME]-SETUP.md file with full device inventory, automation functions, workflows, and configuration."
)
```

### Output
- Room setup markdown file: `packages/rooms/[ROOM]/[ROOM]-SETUP.md`
- Sections:
  1. Device Inventory (categorized table)
  2. Automation Functions (by category with descriptions)
  3. Room Layout ASCII Diagram
  4. Key Automation Workflows
  5. Configuration Parameters
  6. Helper Entities
  7. Scripts
  8. Sensors
  9. Status Indicators
  10. Key Features Checklist
  11. File Structure

### Quality Checklist
- [ ] All automations categorized
- [ ] All devices listed in inventory
- [ ] All workflows documented
- [ ] Room layout diagram accurate
- [ ] Configuration parameters listed
- [ ] Helper entities documented
- [ ] Scripts/actions explained
- [ ] Status indicators documented
- [ ] All 10 sections complete
- [ ] Markdown formatting correct
- [ ] ASCII diagrams render properly
- [ ] No broken internal references

### Success Criteria
✅ Complete room documentation generated
✅ All sections present and accurate
✅ Formatting matches OFFICE-SETUP.md template
✅ Device inventory complete and categorized
✅ Automation descriptions clear and comprehensive
✅ Workflows documented with ASCII diagrams
✅ Configuration parameters all listed
✅ File created in correct location

### Reference Template
See: OFFICE-SETUP.md (office/OFFICE-SETUP.md)

### Reference Skill
See: ha-room-documentation-generator.md (.claude/skills/)

---

## Rooms To Document

### Priority 1 (High Activity)
- Kitchen (packages/rooms/kitchen/kitchen.yaml)
- Living Room (packages/rooms/living_room/living_room.yaml)
- Bedroom (packages/rooms/bedroom/bedroom.yaml)

### Priority 2 (Medium Activity)
- Conservatory (packages/rooms/conservatory/conservatory.yaml)
- Stairs (packages/rooms/stairs/stairs.yaml)
- Porch (packages/rooms/porch/porch.yaml)

### Priority 3 (Specialized)
- Front Garden (packages/rooms/front_garden/front_garden.yaml)
- Back Garden (packages/rooms/back_garden/back_garden.yaml)
- Other sub-packages as needed

---

## Agent Workflow

1. **Identify target room**
   - Locate YAML file in packages/rooms/[ROOM]/

2. **Extract device information**
   - Scan for all entity_id references
   - Categorize by domain (light, switch, sensor, etc.)
   - Document function and role

3. **Categorize automations**
   - Group by primary function
   - Extract automation IDs and aliases
   - Document triggers, conditions, actions
   - Identify relationships

4. **Analyze workflows**
   - Identify time-based sequences
   - Document cascading automations
   - Map automation interactions

5. **Design room layout**
   - Create ASCII diagram
   - Place devices with emoji icons
   - Show device relationships

6. **Extract configuration**
   - Find all input_* helpers
   - Document parameters and ranges
   - Note default values

7. **Generate markdown**
   - Use 10-section template
   - Apply formatting standards
   - Ensure readability
   - Validate all links

8. **Save documentation**
   - Create [ROOM]-SETUP.md
   - Location: packages/rooms/[ROOM]/[ROOM]-SETUP.md
   - Add to git staging

---

## Template Reference

Location: packages/rooms/office/OFFICE-SETUP.md

Key sections:
- Device Inventory (table)
- Automation Functions (by category)
- Room Layout ASCII (visual)
- Key Workflows (with flow diagrams)
- Configuration Parameters
- Helper Entities
- Scripts
- Sensors
- Status Indicators
- Key Features (checklist)
- File Structure

---

## Instructions for Agent

### Step 1: Read Target Room YAML
```
File: packages/rooms/[ROOM]/[room].yaml
Extract: All automations, conditions, actions, entity references
```

### Step 2: Extract Devices
```
Search for:
- light.* (lighting devices)
- switch.* (switches)
- binary_sensor.* (binary sensors)
- sensor.* (numeric sensors)
- input_boolean.*, input_number.*, input_datetime.*, input_select.* (helpers)
- cover.* (covers/blinds)
- group.* (device groups)

Categorize by domain and function
```

### Step 3: Categorize Automations
```
Group by primary function:
- Motion/Presence
- Lighting/Scenes
- Climate/Temperature
- Security/Locks
- Time-based
- PC/Device integration
- Notifications
- Other

For each: ID, alias, triggers, conditions, actions
```

### Step 4: Create Device Inventory Table
```
Columns:
- Category (Lighting, Motion, Environment, Climate, etc.)
- Device name (entity_id format)
- Device type (what kind of device)
- Function (what it does)

Example:
| Lighting | light.kitchen_table_white | Color Temperature Light | Main ambient lighting |
```

### Step 5: Document Automation Functions
```
For each category:
- Emoji header
- Category name
- Triggers (what starts it)
- Logic (how it decides)
- Related automation IDs
- Safety features (if any)
```

### Step 6: Create Room Layout ASCII
```
Elements:
- Room boundary (╔═════╗ style)
- Device positions with emoji
- Labels and descriptions
- Direction markers (NORTH/SOUTH/EAST/WEST)
- Relationships between devices

Example:
╔═════════════════════╗
║ 🪟 Window           ║
║ ▼ Motorized Blind   ║
║                     ║
║ 💡 Lights           ║
║ 🌡️ Thermometer      ║
║ 📏 Motion Sensor    ║
╚═════════════════════╝
```

### Step 7: Document Workflows
```
For each time period or scenario:
- Title (e.g., "Morning Routine")
- ASCII flow diagram
- Decision tree
- Key actions

Example:
Morning Routine (8:00 AM):
├─ Check brightness
├─ Check if occupied
├─ Open blinds if needed
└─ Adjust lighting
```

### Step 8: Extract Configuration
```
Find all:
- input_number.* (with ranges)
- input_boolean.* (purpose)
- input_datetime.* (purpose)
- input_select.* (options)

Document:
- Entity name
- Purpose/description
- Typical values or range
```

### Step 9: Generate Markdown
```
Apply template structure:
1. Header with metadata
2. Device Inventory
3. Automation Functions (by category)
4. Room Layout Diagram
5. Key Workflows
6. Configuration Parameters
7. Helper Entities
8. Scripts
9. Sensors
10. Status Indicators
11. Key Features Checklist
12. File Structure
13. Metadata footer
```

### Step 10: Save and Validate
```
File location: packages/rooms/[ROOM]/[ROOM]-SETUP.md

Validate:
- All sections present
- Formatting correct
- No broken references
- ASCII diagrams render
- All automation IDs listed
```

---

## Success Metrics

- ✅ Documentation file created for each room
- ✅ All devices documented and categorized
- ✅ All automations described with context
- ✅ Room layout diagrams created
- ✅ Workflows documented with ASCII diagrams
- ✅ Configuration parameters listed
- ✅ Consistent formatting across all room docs
- ✅ 1000+ lines per comprehensive room setup

---

## Agent Constraints

**Do:**
- ✅ Read YAML files carefully
- ✅ Extract exact entity IDs (no typos)
- ✅ Categorize systematically
- ✅ Create clear ASCII diagrams
- ✅ Use consistent formatting
- ✅ Document all sections
- ✅ Cross-reference automation IDs

**Don't:**
- ❌ Modify YAML files
- ❌ Create incomplete documentation
- ❌ Miss devices or automations
- ❌ Invent information
- ❌ Skip sections
- ❌ Use inconsistent formatting

---

## Integration with Skills

**Related Skills:**
- ha-room-documentation-generator.md (methodology)
- ha-motion-consolidator.md (automation patterns)
- ha-consolidation-analyzer.md (optimization)
- ha-yaml-quality-reviewer.md (validation)

**Outputs:**
- Room setup markdown files
- Device inventory documentation
- Automation architecture understanding
- Future optimization roadmap

---

**Agent Type:** ha-room-documentation-generator
**Created:** 2026-01-24
**Status:** Ready for deployment
