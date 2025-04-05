[<- Back](README.md)
# Statistics 📊
I have 6,628 states (📈81) in Home Assistant.
By domain these are:
- 1 alarm_control_panel
- 374 automation 📉62
- 789 binary_sensor 📈41
- 213 button 📈15
- 31 calendar 📈3
- 20 camera
- 17 climate 📈2
- 3 conversation 📈1
- 4 counter 📈1
- 25 cover 📈7
- 362 device_tracker 📉51
- 16 event
- 1 fan
- 17 group
- 51 image
- 98 input_boolean 📈1
- 1 input_datetime
- 69 input_number 📈1
- 5 input_select
- 59 input_text
- 65 light 📈1
- 10 lock 📈3
- 24 media_player 📈2
- 199 number 📈18
- 4 person
- 3 remote
- 78 scene 📈1
- 3 schedule
- 174 script 📈5
- 165 select 📈3
- 3111 sensor 📈54
- 2 siren
- 1 stt
- 1 sun
- 396 switch 📈34
- 2 tag
- 12 text
- 11 timer
- 20 todo
- 1 tts
- 172 update 📉1
- 1 vacuum
- 3 wake_word
- 1 water_heater
- 3 weather
- 10 zone

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
