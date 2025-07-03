[<- Back](README.md)
# Statistics 📊
I have 6,287 states (📉91) in Home Assistant.
By domain these are:
- 1 alarm_control_panel
- 361 automation 📈1
- 630 binary_sensor 📉5
- 223 button 📈1
- 37 calendar
- 15 camera
- 17 climate
- 4 conversation
- 2 counter
- 25 cover
- 382 device_tracker 📈1
- 15 event
- 1 fan
- 17 group
- 1 image
- 98 input_boolean
- 3 input_datetime
- 88 input_number
- 4 input_select
- 59 input_text 📈1
- 66 light
- 10 lock
- 24 media_player
- 217 number
- 4 person
- 2 predbat 📉101
- 3 remote
- 77 scene
- 3 schedule
- 142 script 📈1
- 195 select 📈12
- 2888 sensor 📉4
- 2 siren
- 1 stt
- 1 sun
- 420 switch 📈1
- 2 tag
- 14 text
- 9 timer
- 20 todo
- 2 tts 📈1
- 184 update
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
