[<- Back to README](README.md)

# Statistics 📊
I have 6,111 states (📉1,160) in Home Assistant.
By domain these are:
- 2 ai_task
- 1 alarm_control_panel 📉1
- 379 automation 📉8
- 640 binary_sensor 📉79
- 249 button 📈11
- 33 calendar 📉20
- 10 camera 📉2
- 18 climate
- 5 conversation
- 1 counter
- 25 cover
- 324 device_tracker 📉49
- 44 event 📉1
- 3 fan
- 16 group
- 8 image
- 101 input_boolean
- 9 input_datetime
- 75 input_number 📉42
- 4 input_select
- 65 input_text
- 73 light 📉2
- 9 lock
- 26 media_player 📉2
- 10 notify 📈1
- 313 number 📉18
- 4 person
- 1 remote 📉2
- 67 scene 📉3
- 4 schedule
- 135 script 📉7
- 163 select 📉72
- 2567 sensor 📉603
- 1 siren 📈1
- 4 stt
- 1 sun
- 450 switch 📉113
- 2 tag
- 17 text 📉14
- 24 timer
- 13 todo 📉19
- 4 tts
- 196 update 📉10
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
