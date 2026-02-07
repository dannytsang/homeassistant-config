[<- Back](README.md)
# Statistics 📊
I have 7,138 states (📈36) in Home Assistant.
By domain these are:
- 2 ai_task
- 1 alarm_control_panel
- 374 automation 📉15
- 707 binary_sensor 📉3
- 273 button 📈19
- 51 calendar 📈10
- 13 camera
- 18 climate
- 4 conversation
- 1 counter
- 25 cover
- 427 device_tracker 📈9
- 23 event
- 1 fan
- 16 group
- 1 image
- 97 input_boolean 📈2
- 3 input_datetime
- 94 input_number
- 4 input_select
- 68 input_text
- 76 light 📉1
- 10 lock
- 26 media_player 📈1
- 1 notify
- 330 number 📉20
- 4 person
- 104 predbat
- 3 remote
- 79 scene 📈2
- 4 schedule
- 142 script 📈3
- 225 select 📈3
- 3137 sensor 📈27
- 2 siren
- 4 stt
- 1 sun
- 510 switch 📉2
- 2 tag
- 15 text 📉7
- 21 timer 📈1
- 30 todo 📈10
- 4 tts
- 190 update 📉3
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
