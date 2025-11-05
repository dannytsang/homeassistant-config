[<- Back](README.md)
# Statistics 📊
I have 6,871 states (📈272) in Home Assistant.
By domain these are:
- 2 ai_task
- 1 alarm_control_panel
- 388 automation 📈7
- 687 binary_sensor 📈24
- 242 button 📈17
- 41 calendar 📈2
- 12 camera 📉1
- 18 climate 📈2
- 4 conversation
- 1 counter
- 25 cover
- 401 device_tracker 📈7
- 17 event 📈1
- 1 fan
- 16 group
- 1 image
- 95 input_boolean
- 3 input_datetime
- 92 input_number 📈2
- 4 input_select
- 66 input_text 📈4
- 70 light 📈1
- 10 lock
- 25 media_player
- 1 notify
- 278 number 📈75
- 4 person
- 104 predbat
- 3 remote
- 76 scene 📈1
- 4 schedule
- 137 script 📈2
- 215 select 📈11
- 3067 sensor 📈117
- 2 siren
- 3 stt
- 1 sun
- 489 switch 📈6
- 2 tag
- 14 text
- 19 timer 📈8
- 20 todo
- 2 tts
- 193 update 📈2
- 1 vacuum
- 3 weather
- 11 zone

## How To ✋
To get the above numbers, use the template from [here](https://www.reddit.com/r/homeassistant/comments/plmy7e/use_this_template_and_show_us_some_details_about/?utm_medium=android_app&utm_source=share)
```
{% set ns = namespace(domains=[]) %}
{%- for s in states -%}
{%- set ns.domains = (ns.domains + [s.domain])|unique|list -%}
{%- endfor %}
I have {{ states|length  }} states in Home Assistant.
By domain these are;
{%- for domain in ns.domains %}
- {{ states[domain]|length }} {{ domain }}
{%- endfor %}
```
