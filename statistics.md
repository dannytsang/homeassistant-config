[<- Back to README](README.md)

# Statistics 📊
I have 6,896 states (📈785) in Home Assistant.
By domain these are:
- 2 ai_task
- 2 alarm_control_panel 📈1
- 384 automation 📈5
- 753 binary_sensor 📈113
- 260 button 📈11
- 35 calendar 📈2
- 12 camera 📈2
- 18 climate
- 5 conversation
- 1 counter
- 25 cover
- 329 device_tracker 📈5
- 53 event 📈9
- 3 fan
- 16 group
- 8 image
- 1 infrared 📈1
- 101 input_boolean
- 9 input_datetime
- 126 input_number 📈51
- 4 input_select
- 65 input_text
- 72 light 📉1
- 9 lock
- 28 media_player 📈2
- 10 notify
- 346 number 📈33
- 4 person
- 108 predbat 📈108
- 1 radio_frequency 📈1
- 3 remote 📈2
- 67 scene
- 4 schedule
- 135 script
- 239 select 📈76
- 2790 sensor 📈223
- 1 siren
- 4 stt
- 1 sun
- 553 switch 📈103
- 2 tag
- 33 text 📈16
- 17 time 📈17
- 24 timer
- 13 todo
- 4 tts
- 201 update 📈5
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
