[<- Back](README.md)
# Statistics 📊
I have 7,102 states (📈200) in Home Assistant.
By domain these are:
- 2 ai_task
- 1 alarm_control_panel
- 389 automation 📈5
- 710 binary_sensor 📈25
- 254 button 📈13
- 41 calendar
- 13 camera
- 18 climate
- 4 conversation
- 1 counter
- 25 cover
- 418 device_tracker 📈10
- 23 event 📈1
- 1 fan
- 16 group
- 1 image
- 95 input_boolean
- 3 input_datetime
- 94 input_number 📈1
- 4 input_select
- 68 input_text 📈2
- 77 light 📈4
- 10 lock
- 25 media_player
- 1 notify
- 350 number 📈59
- 4 person
- 104 predbat



- 3 remote
- 77 scene 📈2
- 4 schedule
- 139 script 📈2
- 222 select 📈8
- 3110 sensor 📈133
- 2 siren
- 4 stt 📈1
- 1 sun
- 512 switch 📈19
- 2 tag
- 22 text 📈8
- 20 timer 📈1
- 20 todo
- 4 tts 📈2
- 193 update 📈4
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
