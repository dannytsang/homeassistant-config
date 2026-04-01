[<- Back](README.md)
[<- Back to README](README.md)

# Statistics 📊
I have 7,191 states (📈53) in Home Assistant.
By domain these are:
- 2 ai_task
- 1 alarm_control_panel
- 374 automation
- 707 binary_sensor
- 273 button
- 52 calendar 📈1
- 13 camera
- 18 climate
- 4 conversation
- 1 counter
- 25 cover
- 432 device_tracker 📈5
- 23 event
- 1 fan
- 16 group
- 1 image
- 99 input_boolean 📈2
- 3 input_datetime
- 94 input_number
- 4 input_select
- 68 input_text
- 76 light
- 10 lock
- 27 media_player 📈1
- 1 notify
- 330 number
- 4 person
- 104 predbat
- 3 remote
- 79 scene
- 4 schedule
- 142 script
- 225 select
- 3175 sensor 📈38
- 2 siren
- 4 stt
- 1 sun
- 515 switch 📈5
- 2 tag
- 15 text
- 21 timer
- 31 todo 📈1
- 4 tts
- 190 update
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
