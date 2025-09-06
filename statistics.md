[<- Back](README.md)
# Statistics 📊
I have 6,531 states (📈53) in Home Assistant.
By domain these are:
- 2 ai_task 📉1
- 1 alarm_control_panel
- 378 automation 📈9
- 652 binary_sensor 📈2
- 227 button 📈2
- 38 calendar 📈1
- 15 camera
- 16 climate 📉1
- 4 conversation
- 1 counter
- 25 cover 📈1
- 386 device_tracker
- 15 event
- 1 fan
- 16 group
- 1 image
- 94 input_boolean 📉5
- 3 input_datetime
- 88 input_number 📈3
- 4 input_select
- 62 input_text 📈1
- 68 light 📈1
- 10 lock
- 24 media_player
- 1 notify
- 217 number
- 4 person
- 103 predbat
- 3 remote
- 76 scene 📈1
- 3 schedule
- 139 script 📈3
- 201 select 📈4
- 2924 sensor 📉8
- 2 siren
- 2 stt
- 1 sun
- 460 switch 📈37
- 2 tag
- 14 text
- 11 timer 📈1
- 20 todo
- 2 tts
- 196 update 📈1
- 1 vacuum
- 3 wake_word
- 1 water_heater
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
