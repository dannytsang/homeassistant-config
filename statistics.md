[<- Back](README.md)
[<- Back to README](README.md)

# Statistics 📊
I have 7,191 states in Home Assistant.  
By domain these are:
- 2 ai_task
- 1 alarm_control_panel
- 374 automation
- 709 binary_sensor 📈2
- 273 button
- 52 calendar
- 13 camera
- 18 climate
- 4 conversation
- 1 counter
- 25 cover
- 439 device_tracker 📈7
- 25 event 📈2
- 2 fan 📈1
- 16 group
- 1 image
- 99 input_boolean
- 7 input_datetime 📈4
- 114 input_number 📈20
- 4 input_select
- 68 input_text
- 76 light
- 10 lock
- 27 media_player
- 1 notify
- 332 number 📈2
- 4 person
- 103 predbat 📉1
- 3 remote
- 78 scene 📉1
- 4 schedule
- 141 script 📉1
- 228 select 📈3
- 3113 sensor 📉62
- 2 siren
- 4 stt
- 1 sun
- 538 switch 📈23
- 2 tag
- 15 text
- 21 timer
- 31 todo
- 4 tts
- 191 update 📈1
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
