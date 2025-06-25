[<- Back](README.md)
# Statistics 📊
I have 6,378 states (📉264) in Home Assistant.
By domain these are:
- 1 alarm_control_panel
- 360 automation 📉3
- 635 binary_sensor 📉157
- 222 button 📈1
- 37 calendar
- 15 camera 📉5
- 17 climate
- 4 conversation 📈1
- 2 counter
- 25 cover
- 381 device_tracker 📈6
- 15 event 📈1
- 1 fan
- 17 group
- 1 image 📉50
- 98 input_boolean
- 3 input_datetime
- 88 input_number 📈19
- 4 input_select 📉1
- 58 input_text
- 66 light 📈1
- 10 lock
- 24 media_player
- 217 number 📈3
- 4 person
- 103 predbat 📈103
- 3 remote
- 77 scene
- 3 schedule
- 141 script 📈1
- 183 select 📈10
- 2892 sensor 📉217
- 2 siren
- 1 stt
- 1 sun
- 419 switch 📈7
- 2 tag
- 14 text
- 9 timer
- 20 todo
- 1 tts
- 184 update 📈10
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
