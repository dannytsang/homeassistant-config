[<- Back to README](README.md)

# Statistics 📊
I have 6,989(📉656) in Home Assistant.
By domain these are:
- 2 ai_task
- 2 alarm_control_panel
- 387 automation 📉2
- 713 binary_sensor 📉22
- 259 button 📉18
- 32 calendar 📉20
- 12 camera 📉3
- 18 climate
- 5 conversation 📈1
- 1 counter
- 25 cover
- 342 device_tracker 📉121
- 55 event 📈27
- 3 fan
- 16 group
- 8 image 📈7
- 1 infrared
- 101 input_boolean
- 9 input_datetime
- 123 input_number 📈7
- 4 input_select
- 65 input_text 📉2
- 75 light
- 8 lock 📉1
- 27 media_player 📉1
- 10 notify
- 334 number 📉15
- 4 person
- 105 predbat 📈1
- 1 radio_frequency
- 2 remote 📉1
- 70 scene 📉8
- 4 schedule
- 142 script
- 219 select 📉24
- 2966 sensor 📉417
- 4 stt
- 1 sun
- 543 switch 📉25
- 2 tag
- 29 text 📉2
- 24 timer 📈1
- 13 todo 📉18
- 4 tts
- 204 update 📈2
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
