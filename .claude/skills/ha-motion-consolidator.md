# Claude Skill: Home Assistant Motion Automation Consolidator

**Status:** Skill Design Document
**Version:** 1.0
**Based On:** Phase 4 consolidation work (2026-01-23)

---

## Purpose

Consolidate multiple motion-based automations into fewer, more maintainable automations using trigger ID branching and choose blocks.

## When to Use

- Multiple automations trigger on same motion sensors with different actions
- Light on/off patterns (motion on → lights on, motion off → lights off)
- Different responses based on time of day or room state
- Context-aware motion handling (brightness, occupancy, etc.)

## Consolidation Patterns Recognized

### Pattern 1: Motion On/Off Split
**Before:** 2 automations
- Automation A: Motion detected → turn on lights
- Automation B: No motion → start timer

**After:** 1 automation with trigger IDs
```yaml
triggers:
  - trigger: state
    entity_id: sensor.motion
    to: "on"
    id: motion_on
  - trigger: state
    entity_id: sensor.motion
    to: "off"
    id: motion_off
actions:
  - choose:
      - conditions:
          - condition: trigger
            id: motion_on
        sequence: [turn on]
      - conditions:
          - condition: trigger
            id: motion_off
        sequence: [turn off]
```

### Pattern 2: Context-Aware Motion
**Before:** 2-3 automations with identical triggers
- Automation A: Light OFF + motion → turn on
- Automation B: Light ON (dim) + motion → turn on

**After:** 1 automation with OR condition
```yaml
conditions:
  - condition: or
    conditions:
      - condition: state
        entity_id: light.room
        state: "off"
      - and:
          - condition: state
            entity_id: light.room
            state: "on"
          - condition: numeric_state
            entity_id: light.room
            attribute: brightness
            below: 5
```

### Pattern 3: Time-Based Branching
**Before:** Multiple automations for different times
- Before bedtime variant
- After bedtime variant
- Night mode variant

**After:** Single automation with time-based choose branches
```yaml
actions:
  - choose:
      - alias: "Before Bedtime"
        conditions:
          - condition: time
            after: "07:00:00"
            before: input_datetime.childrens_bed_time
        sequence: [action A]
      - alias: "After Bedtime"
        conditions:
          - condition: time
            after: input_datetime.childrens_bed_time
        sequence: [action B]
```

## Analysis Process

1. **Identify related automations**
   - Same room or entity focus
   - Related triggers (motion on/off, sensor values)
   - Similar action types

2. **Check consolidation viability**
   - Do triggers differ only in `to:` or `for:` values?
   - Are actions mutually exclusive (can't both run)?
   - Can conditions be combined with OR/AND logic?

3. **Design consolidated structure**
   - Map existing automations to trigger IDs
   - Create choice branches for each automation
   - Ensure all original logic preserved

4. **Validate consolidation**
   - All original automations accounted for
   - No loss of functionality
   - Improved readability and maintainability

## Success Metrics

- ✅ Automation count reduced by 50%+
- ✅ Combined file size < sum of originals
- ✅ All trigger conditions preserved
- ✅ Clearer aliases for each branch
- ✅ Reduced code duplication

## Output

**For each consolidation:**
1. Consolidated automation YAML
2. Line count comparison (before/after)
3. Trigger ID mapping
4. Testing checklist
5. Git commit message

## Real-world Examples from Session

### Example 1: Porch Motion (2 → 1)
**Before:** 89 lines
- Automation: Motion on → turn on light
- Automation: Motion off → start timer

**After:** 37 lines
- Single automation with motion_on/motion_off branches
- Savings: 52 lines (-58%)

### Example 2: Kitchen Motion (8 → 3)
**Before:** Multiple motion-on + no-motion automations
**After:** Consolidated with choice branches by light zone
- Savings: ~35% reduction

### Example 3: Stairs Magic Mirror (2 → 1)
**Before:** Turn on automation + turn off automation
**After:** Single automation with motion/time-based branches
- Savings: 30 lines (-53%)

## Limitations

- ⚠️ Don't consolidate if automations have very different modes (single vs queued)
- ⚠️ Complex nested logic becomes harder to read
- ⚠️ Large choose blocks (10+ branches) should be split
- ⚠️ Safety-critical automations should be consolidated with caution

## Configuration Tips

- Use descriptive trigger ID names (motion_on, motion_off, morning, evening)
- Keep branch aliases short but clear
- Use `parallel:` for independent actions
- Maintain consistent `mode:` across consolidated automation
- Add comprehensive descriptions for complex consolidations

## Next Steps

1. Identify other consolidation candidates in living_room, kitchen, office
2. Document consolidation patterns in automation guidelines
3. Create automated detection for consolidation opportunities
4. Build validation to ensure consolidated logic equivalence

---

**Usage:** Invoke when reviewing motion automations for optimization opportunities
**Team:** Danny's Home Assistant optimization
**Last Updated:** 2026-01-23
