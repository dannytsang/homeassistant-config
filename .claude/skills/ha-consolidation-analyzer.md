# Claude Skill: Home Assistant Consolidation Analyzer

**Status:** Skill Design Document
**Version:** 1.0
**Based On:** Phases 4.1-4.5 (Consolidation Work, 2026-01-23)

---

## Purpose

Identify consolidation opportunities in Home Assistant automations by analyzing trigger/condition/action patterns and recommending which automations can be merged.

## When to Use

- After reviewing a new room package
- During code audit phase
- When optimizing automation count
- Before refactoring motion automations
- When consolidating similar patterns

## Consolidation Opportunity Detection

### Type 1: Identical Triggers, Different Conditions

**Pattern:**
```yaml
# Automation A
triggers:
  - trigger: state
    entity_id: binary_sensor.motion
    to: "on"
conditions:
  - condition: state
    entity_id: light.room
    state: "off"
actions:
  - action: scene.turn_on
    target:
      entity_id: scene.lights_on

# Automation B (similar)
triggers:
  - trigger: state
    entity_id: binary_sensor.motion
    to: "on"
conditions:
  - condition: state
    entity_id: light.room
    state: "on"
  - condition: numeric_state
    entity_id: light.room
    attribute: brightness
    below: 5
actions:
  - action: scene.turn_on
    target:
      entity_id: scene.lights_on
```

**Consolidation Score:** HIGH (95%)
**Recommendation:** Use OR condition + single automation

### Type 2: Motion On/Off Pair

**Pattern:**
```yaml
# Automation A: Motion on → light on
triggers:
  - trigger: state
    entity_id: binary_sensor.motion
    to: "on"
    for: "00:02:00"

# Automation B: Motion off → timer start
triggers:
  - trigger: state
    entity_id: binary_sensor.motion
    to: "off"
    for: "00:01:00"
```

**Consolidation Score:** CRITICAL (99%)
**Recommendation:** Single automation with trigger IDs

### Type 3: Time-Based Variants

**Pattern:**
```yaml
# Automation A: Before bedtime
triggers:
  - trigger: state
    entity_id: binary_sensor.motion
    to: "on"
conditions:
  - condition: time
    after: "07:00:00"
    before: input_datetime.childrens_bed_time

# Automation B: After bedtime
triggers:
  - trigger: state
    entity_id: binary_sensor.motion
    to: "on"
conditions:
  - condition: time
    after: input_datetime.childrens_bed_time
```

**Consolidation Score:** HIGH (85%)
**Recommendation:** Single automation with time branches

### Type 4: Context-Aware Variants

**Pattern:**
```yaml
# Different automations for different room states
# - Lights off + motion → turn on
# - Lights dim + motion → turn on bright
# - Lights on bright + motion → no action
```

**Consolidation Score:** MEDIUM (70%)
**Recommendation:** Use nested conditions or choose blocks

## Analysis Framework

### Step 1: Catalog Automations
```
For each room package:
- Count total automations
- Group by type (motion, door, timer, schedule)
- Identify related automations
```

### Step 2: Identify Candidates
```
For each group:
- Do they share triggers? (Same sensor)
- Do they share entity domain? (All lights)
- Are they mutually exclusive?
- Can conditions be combined?
```

### Step 3: Score Consolidation
```
Scoring factors (0-100):
+ Shared triggers: +40 points
+ Identical actions: +30 points
+ Mutually exclusive conditions: +20 points
+ Same automation mode: +10 points
- Complex nesting required: -15 points
- Safety-critical differences: -20 points
```

### Step 4: Recommend Approach
```
Score 80-100:  CRITICAL consolidation
Score 60-79:   HIGH priority consolidation
Score 40-59:   MEDIUM priority consolidation
Score 0-39:    LOW or NO consolidation
```

## Real-world Analysis: Stairs Package

### Before Analysis
```
Motion automations: 7
- 2 ambient light automations (motion on, different times)
- 2 before-bedtime automations (light off vs dim)
- 2 after-bedtime automations (midnight split)
- 1 magic mirror trigger
- 2 magic mirror variants (on/off)
- 2 no-motion handlers (upstairs vs bottom)
```

### Consolidation Map
```
Group 1: Before-bedtime motion (2 → 1)
├─ Light off + motion
└─ Light dim + motion
Score: 95% → CONSOLIDATE ✅

Group 2: Magic mirror control (2 → 1)
├─ Motion detected → turn on
└─ No motion at night → turn off
Score: 90% → CONSOLIDATE ✅

Group 3: No-motion handlers (2 → 1)
├─ Upstairs motion off
└─ Bottom motion off (fallback)
Score: 85% → CONSOLIDATE ✅
```

### After Analysis
```
Motion automations: 4 (from 7)
- 1 before-bedtime consolidated
- 1 after-bedtime (unchanged)
- 1 magic mirror consolidated
- 1 no-motion consolidated

Savings: 3 automations (-43%)
         ~85 lines of YAML
         Improved maintainability
```

## Consolidation Readiness Checklist

### Pre-Consolidation Assessment
- [ ] Identified similar automations (same sensor/entity)
- [ ] Analyzed triggers (same? different?)
- [ ] Examined conditions (mutually exclusive?)
- [ ] Reviewed actions (independent? sequential?)
- [ ] Checked automation modes (compatible?)
- [ ] Scored consolidation opportunity
- [ ] Planned trigger ID naming
- [ ] Designed branch structure

### Consolidation Safety Check
- [ ] Safety-critical automations identified
- [ ] Fallback logic preserved
- [ ] No loss of original functionality
- [ ] All trigger paths covered
- [ ] Error handling maintained

## Output: Consolidation Report

### Template
```markdown
## Room: [Room Name]

### Current State
- Total automations: X
- Motion automations: Y
- Lines of YAML: Z

### Consolidation Opportunities

#### Opportunity 1: [Description]
- Automations: [ID1], [ID2]
- Triggers: [Shared/Different]
- Conditions: [Pattern]
- Actions: [Pattern]
- Score: [XX]%
- Recommendation: [CONSOLIDATE/CONSIDER/SKIP]
- Estimated savings: [X] lines, [Y] automations
- Complexity: [Low/Medium/High]

#### Summary
- Total consolidations: N
- Total savings: X automations, Y lines
- Time estimate: Z minutes
- Risk level: [Low/Medium/High]
```

## Consolidation Patterns Summary

| Pattern | Candidates | Savings | Risk | Recommendation |
|---------|-----------|---------|------|-----------------|
| Motion on/off pair | 2-3 | 40-60% | Low | Always consolidate |
| Context-aware light | 2-3 | 30-40% | Low | Consolidate with OR |
| Time-based variants | 2-5 | 20-40% | Low | Consolidate branches |
| Room state variants | 3-5 | 30-50% | Medium | Consolidate carefully |
| Safety + regular | 2-3 | 20-30% | High | Use fallback pattern |

## Future Enhancements

### Automated Detection
```
Implement pattern matching for:
1. Identical trigger entities
2. Non-overlapping conditions
3. Similar action entities
4. Mutually exclusive state checks
```

### Smart Recommendations
```
Generate consolidation blueprints:
1. Suggest trigger ID names
2. Design branch conditions
3. Recommend action structure
4. Calculate savings
```

### Impact Analysis
```
Predict consolidation effects:
1. Complexity vs readability trade-off
2. Automation count reduction
3. Line count savings
4. Maintenance burden
```

## Integration Points

**Phase 4 (Consolidation)** → Identify opportunities
**Phase 5 (Quality Assurance)** → Validate after consolidation
**Pre-commit** → Suggest consolidations on modified files
**Audit** → Annual consolidation opportunity review

## Metrics Tracked

- Consolidation Score (0-100)
- Automation Count (Before/After)
- Line Count (Before/After)
- Safety Risk Level
- Complexity Level
- Estimated Implementation Time

## Limitations

- ⚠️ Cannot predict all logic interactions
- ⚠️ Overrides of core patterns not detected
- ⚠️ Performance implications not analyzed
- ⚠️ Requires human validation

## Best Practices

1. **Consolidate incrementally** - One pattern at a time
2. **Test thoroughly** - Use automation traces to verify
3. **Document decisions** - Why consolidated or not
4. **Keep safety first** - Don't consolidate safety-critical automations without caution
5. **Review complexity** - Large choose blocks become hard to maintain

## Next Steps

1. Catalog all motion automations across remaining rooms
2. Create consolidation roadmap
3. Prioritize by impact (savings vs risk)
4. Execute consolidations by room
5. Track metrics

---

**Usage:** Invoke during architecture review phases to identify consolidation opportunities
**Team:** Danny's Home Assistant optimization
**Last Updated:** 2026-01-23
