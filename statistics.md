[<- Back](README.md)
# Statistics 📊
I have 6,642 states (📈14) in Home Assistant.
By domain these are:
- 1 alarm_control_panel
- 357 automation 📉17
- 792 binary_sensor 📈3
- 221 button 📈8
- 37 calendar 📈6
- 20 camera
- 17 climate
- 3 conversation
- 2 counter 📉2
- 25 cover
- 375 device_tracker 📈13
- 14 event 📉2
- 1 fan
- 17 group
- 51 image
- 98 input_boolean
- 3 input_datetime 📈2
- 69 input_number
- 5 input_select
- 58 input_text 📉1
- 65 light
- 10 lock
- 24 media_player
- 214 number 📈15
- 4 person
- 3 remote
- 77 scene 📉1
- 3 schedule
- 140 script 📉34
- 173 select 📈8
- 3109 sensor 📉2
- 2 siren
- 1 stt
- 1 sun
- 412 switch 📈16
- 2 tag
- 14 text 📈2
- 9 timer 📉2
- 20 todo
- 1 tts
- 174 update 📈2
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
