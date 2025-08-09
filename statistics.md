[<- Back](README.md)
# Statistics 📊
I have 6,478 states (📈181) in Home Assistant.
By domain these are:
- 3 ai_task 📈3
- 1 alarm_control_panel
- 369 automation 📈8
- 650 binary_sensor 📈20
- 225 button 📈2
- 37 calendar
- 15 camera
- 17 climate
- 4 conversation
- 1 counter 📉1
- 24 cover 📉1
- 386 device_tracker 📈4
- 15 event
- 1 fan
- 16 group 📉1
- 1 image
- 99 input_boolean 📈1
- 3 input_datetime
- 85 input_number 📉3
- 4 input_select
- 61 input_text 📈2
- 67 light 📈1
- 10 lock
- 24 media_player
- 217 number
- 4 person
- 103 predbat 📈101
- 3 remote
- 75 scene 📉2
- 3 schedule
- 136 script 📉6
- 197 select 📈2
- 2932 sensor 📈44
- 2 siren
- 2 stt 📈1
- 1 sun
- 423 switch 📈3
- 2 tag
- 14 text
- 10 timer 📈1
- 20 todo
- 2 tts
- 195 update 📈11
- 1 vacuum
- 3 wake_word
- 1 water_heater
- 3 weather
- 11 zone 📈1

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
