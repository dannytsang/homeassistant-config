[<- Back](README.md)
# Statistics 📊
I have 6,902 states (📈31) in Home Assistant.
By domain these are:
- 2 ai_task
- 1 alarm_control_panel
- 384 automation 📉4
- 685 binary_sensor 📉2
- 241 button 📉1
- 41 calendar
- 13 camera 📈1
- 18 climate
- 4 conversation
- 1 counter
- 25 cover
- 408 device_tracker 📈7
- 22 event 📈5
- 1 fan
- 16 group
- 1 image
- 95 input_boolean
- 3 input_datetime
- 93 input_number 📈1
- 4 input_select
- 66 input_text
- 73 light 📈3
- 10 lock
- 25 media_player
- 1 notify
- 291 number 📈13
- 4 person
- 104 predbat
- 3 remote
- 75 scene 📈1
- 4 schedule
- 137 script
- 214 select 📉1
- 3077 sensor 📈10
- 2 siren
- 3 stt
- 1 sun
- 493 switch 📈4
- 2 tag
- 14 text
- 19 timer
- 20 todo
- 2 tts
- 189 update 📈4
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
