[<- Back](README.md)
# Statistics 📊
I have 6,599 states (📈68) in Home Assistant.
By domain these are:
- 2 ai_task
- 1 alarm_control_panel
- 381 automation 📈3
- 663 binary_sensor 📈11
- 225 button 📉2
- 39 calendar 📈1
- 13 camera 📉2
- 16 climate
- 4 conversation
- 1 counter
- 25 cover
- 394 device_tracker 📈8
- 16 event 📈1
- 1 fan
- 16 group
- 1 image
- 95 input_boolean 📈1
- 3 input_datetime
- 90 input_number 📈2
- 4 input_select
- 62 input_text
- 69 light 📈1
- 10 lock
- 25 media_player 📈1
- 1 notify
- 219 number 📈2
- 4 person
- 103 predbat
- 3 remote
- 75 scene 📉1
- 4 schedule 📈1
- 135 script 📉4
- 204 select 📈3
- 2950 sensor 📈26
- 2 siren
- 3 stt 📈1
- 1 sun
- 483 switch 📈23
- 2 tag
- 14 text
- 11 timer
- 20 todo
- 2 tts
- 191 update 📉5
- 1 vacuum
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
