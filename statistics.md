[<- Back to README](README.md)

# Statistics 📊
I have 7,645(📈41) states in Home Assistant.  
By domain these are:
- 2 ai_task
- 2 alarm_control_panel
- 389 automation 📈5
- 735 binary_sensor 📉3
- 277 button 📈1
- 52 calendar
- 15 camera
- 18 climate
- 4 conversation
- 1 counter
- 25 cover
- 463 device_tracker 📈5
- 28 event 📈1
- 3 fan 📈1
- 16 group
- 1 image
- 1 infrared
- 101 input_boolean
- 9 input_datetime
- 116 input_number 📈1
- 4 input_select
- 67 input_text
- 75 light 📈1
- 9 lock
- 28 media_player 📉1
- 10 notify 📈2
- 349 number
- 4 person
- 104 predbat
- 1 radio_frequency
- 3 remote
- 78 scene
- 4 schedule
- 142 script 📈1
- 243 select
- 3383 sensor 📈24
- 2 siren
- 4 stt
- 1 sun
- 568 switch 📈1
- 2 tag
- 31 text
- 23 timer 📈1
- 31 todo
- 4 tts
- 202 update 📈1
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
