# Home Assistant Notification Patterns & Script Reference

**Last Updated:** 2026-01-22
**Scope:** Notifications, Scripts, Smart Alerts

---

## Notification System Architecture

### Multi-Channel Delivery
- **Direct notifications** (Mobile App, Slack, Discord, Telegram)
- **Home log** (in-app logging with debug/normal levels)
- **Delayed announcement queue** (Alexa announcements)
- **Mobile app action buttons** (Interactive responses)

### Notification Features
- **Interactive buttons:**
  - Blind position adjustments
  - Fan on/off
  - Appliance toggling (fridge, freezer)
  - Server fan control
- Mobile app action router with button mapping
- Delayed notification buffering and announcement
- Fridge/freezer temperature alerts
- **Quiet hours with smart exceptions** (keyword-based bypass)

---

## Smart Quiet Hours with Keyword Exceptions

**Purpose:** Allow critical messages to bypass quiet hours while respecting sleep/focus time

**Implementation Location:** `packages/integrations/messaging/notifications.yaml` lines 115-151

### Hardcoded Keywords
- **Safety:** `emergency`, `fire`, `gas`, `water`, `leak`
- **Security:** `intruder`, `alarm`, `breach`, `danger`, `alert`
- **Priority:** `critical`, `urgent`

### Behavior Matrix

| Quiet Hours | Message Contains Keyword | Priority | Result |
|-------------|--------------------------|----------|--------|
| OFF | N/A | any | ✅ Send |
| ON | YES | any | ✅ Send (keyword bypass) |
| ON | NO | high/critical | ✅ Send (priority override) |
| ON | NO | normal | ❌ Block |
| ON | suppress_if_quiet=false | NO | ✅ Send (user opt-out) |

### Condition Logic in send_direct_notification

The quiet hours check uses an OR condition with multiple branches:

```yaml
115:      - if:
116:          - or:
117:              - alias: "Quiet time is OFF"
118:                condition: state
119:                entity_id: schedule.notification_quiet_time
120:                state: "off"
121:
122:              - alias: "Quiet time ON but suppress_if_quiet is FALSE"
123:                and:
124:                  - condition: state
125:                    entity_id: schedule.notification_quiet_time
126:                    state: "on"
127:                  - condition: template
128:                    value_template: "{{ not v_suppress_if_quiet }}"
129:
130:              - alias: "Quiet time ON but message contains bypass keyword"
131:                and:
132:                  - condition: state
133:                    entity_id: schedule.notification_quiet_time
134:                    state: "on"
135:                  - condition: template
136:                    value_template: >
137:                      {%- set keywords = ['emergency', 'fire', 'gas', 'water', 'leak', 'intruder', 'alarm', 'breach', 'danger', 'alert', 'critical', 'urgent'] %}
138:                      {%- for keyword in keywords %}
139:                        {%- if keyword.lower() in message.lower() %}
140:                          true
141:                        {%- endif %}
142:                      {%- endfor %}
143:
144:              - alias: "Quiet time ON but priority is NOT 'normal'"
145:                and:
146:                  - condition: state
147:                    entity_id: schedule.notification_quiet_time
148:                    state: "on"
149:                  - condition: template
150:                    value_template: "{{ v_priority != 'normal' }}"
151:        then:
152:          # Process notification
```

### How It Works

1. **Lines 117-120:** If quiet hours are OFF, always send
2. **Lines 122-128:** If quiet hours ON but suppress_if_quiet is FALSE (user opted out), send
3. **Lines 130-142:** If quiet hours ON, check if message contains any bypass keyword (case-insensitive)
   - Line 137: Hardcoded keyword list as Jinja2 array
   - Line 138: Loops through each keyword
   - Line 139: Case-insensitive substring match (`in` operator)
   - Line 140: Returns `true` if ANY keyword found
   - Line 142: Empty/no matches returns nothing (falsy)
4. **Lines 144-150:** If quiet hours ON but priority is high/critical, send anyway

### Keyword Matching Algorithm

```yaml
136:                    value_template: >
137:                      {%- set keywords = ['emergency', 'fire', 'gas', 'water', 'leak', 'intruder', 'alarm', 'breach', 'danger', 'alert', 'critical', 'urgent'] %}
138:                      {%- for keyword in keywords %}
139:                        {%- if keyword.lower() in message.lower() %}
140:                          true
141:                        {%- endif %}
142:                      {%- endfor %}
```

- Line 137: Hardcoded keyword array with common emergency/safety keywords
- Line 138: Loops through each keyword
- Line 139: Case-insensitive substring match (`in` operator, keyword already lowercase, message converted to lowercase)
- Line 140: Returns `true` on first match (early exit not possible in Jinja2, but last true value persists)
- Line 142: Empty/no matches returns nothing (falsy)

### To Change Keywords

Edit line 137 in `send_direct_notification` script to add/remove keywords from the array.

Example addition: `'flooding'`, `'intruder_detected'`, `'power_loss'`

### Related Code Patterns

- Integration with `schedule.notification_quiet_time` entity
- Used in: `send_direct_notification`, `send_direct_notification_with_url`, `send_home_log_with_local_attachments`

---

## Complete Script Reference Catalog

**Purpose:** Quick lookup to prevent script duplication and find existing implementations

### Core Notification Scripts (637+ calls total)

| Script | Purpose | Call Count | Parameters | Reusable |
|--------|---------|-----------|------------|----------|
| `send_to_home_log` | Log message to home log system | 504 | message, title, log_level | ✅ Core |
| `send_direct_notification` | Send mobile app notification | 637 | message, title, suppress_if_quiet, priority | ✅ Core |
| `send_direct_notification_with_url` | Mobile notification + URL attachment | 25+ | message, title, url | ✅ Core |
| `send_actionable_notification_with_2_buttons` | Mobile notification + 2 action buttons | 45+ | message, title, button1_action, button1_label, button2_action, button2_label | ✅ Core |
| `send_actionable_notification_with_3_buttons` | Mobile notification + 3 action buttons | 30+ | message, title, button1_*, button2_*, button3_* | ✅ Core |
| `send_to_home_assistant_with_url_attachment` | Multi-platform notification with attachment | 25+ | Varies by platform | ✅ Core |

### System Control Scripts

| Script | Purpose | When to Use | Reusable |
|--------|---------|------------|----------|
| `set_alarm_to_armed_away_mode` | Arm alarm (away mode) | Leaving home, guest mode | ✅ Yes |
| `set_alarm_to_armed_home_mode` | Arm alarm (home mode) | Evening, family returning | ✅ Yes |
| `set_alarm_to_disarmed_mode` | Disarm alarm | Arriving home, mobile action | ✅ Yes |
| `lock_front_door` | Lock front door (Nuki) | Leaving home, security | ✅ Yes |
| `unlock_front_door` | Unlock front door (Nuki) | Arriving home, NFC tag | ✅ Yes |
| `turn_everything_off` | Master OFF sequence (lights + devices) | Bedtime, emergency | ✅ Yes |
| `set_central_heating_to_home_mode` | Set heating to home temperature | Arriving home | ✅ Yes |
| `set_central_heating_to_away_mode` | Set heating to away temperature | Leaving home | ✅ Yes |
| `everybody_leave_home` | Execute leave-home sequence | Last person leaves | ✅ Yes |
| `alexa_announce` | Announce via Alexa speakers | Notifications, alerts | ✅ Yes |

### Helper/Utility Scripts

| Script | Purpose | When to Use | Reusable |
|--------|---------|------------|----------|
| `get_clock_emoji` | Return time-based clock emoji (⏰ format) | 28 instances in 9 files | ✅ Pattern |
| `send_actionable_notification_to_home_assistant_with_2_buttons` | Mobile notification (internal version) | Device-specific notifications | ✅ Core |
| `send_actionable_notification_to_home_assistant_with_3_buttons` | Mobile notification (internal version) | Device-specific notifications | ✅ Core |
| `check_conservatory_airer` | Check airer temperature/humidity conditions | Airer scheduling | ❌ Room-specific |
| `turn_off_conservatory_airer` | Turn off conservatory airer | Airer automation | ❌ Room-specific |
| `living_room_flash_lounge_lights_red` | Flash living room lights red | Motion alerts | ❌ Room-specific |
| `flash_lights_yellow` | Flash lights yellow | Motion signals | ✅ Generic |

---

## Script Decision Tree

**Need to send a notification?**
- Mobile app only → `send_direct_notification`
- Mobile app + URL attachment → `send_direct_notification_with_url`
- Mobile app + action buttons (2) → `send_actionable_notification_with_2_buttons`
- Mobile app + action buttons (3) → `send_actionable_notification_with_3_buttons`
- Internal logging → `send_to_home_log`

**Need to control security/climate?**
- Arm/disarm alarm → `set_alarm_to_*_mode`
- Lock/unlock door → `lock_front_door` / `unlock_front_door`
- Heating control → `set_central_heating_to_*_mode`
- Master OFF → `turn_everything_off`

**Need a utility?**
- Clock emoji → `get_clock_emoji`
- Flash lights → `flash_lights_yellow` (generic) or room-specific version
- Room-specific logic → Check room package first, may already exist

---

## Creating New Scripts

### Before Creating a New Script, Check:
1. Does a similar script already exist? (Check this reference)
2. Can you use an existing script with variables?
3. Can you consolidate with existing logic?

### Only Create New Scripts If:
- No existing script performs the needed function
- Cannot be achieved with existing scripts + variables
- Function is reusable (not room-specific)

### Example: What NOT to Create
- Don't create `bedroom_turn_off_lights` - use `turn_everything_off` or `light.turn_off` action directly
- Don't create `living_room_send_notification` - use `send_direct_notification` with parameters
- Don't create room-specific versions of generic scripts - pass room as parameter instead

### Best Practices
- Keep scripts focused on one function
- Make parameters explicit with descriptions
- Use response_variables for returning data
- Document parameters and examples
- Consider reusability before creating
