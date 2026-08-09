[<- Back to README](README.md)

# Statistics 📊
I have 7,271 states (📈80) in Home Assistant.
By domain these are:
- 2 ai_task
- 2 alarm_control_panel 📈1
- 387 automation 📈13
- 719 binary_sensor 📈10
- 238 button 📉35
- 53 calendar 📈1
- 12 camera 📉1
- 18 climate
- 5 conversation 📈1
- 1 counter
- 25 cover
- 373 device_tracker 📉66
- 45 event 📈20
- 3 fan 📈1
- 16 group
- 8 image 📈7
- 1 infrared 📈1
- 101 input_boolean 📈2
- 9 input_datetime 📈2
- 117 input_number 📈3
- 4 input_select
- 65 input_text 📉3
- 75 light 📉1
- 9 lock 📉1
- 28 media_player 📈1
- 9 notify 📈8
- 331 number 📉1
- 4 person
- 104 predbat 📈1
- 1 radio_frequency 📈1
- 3 remote
- 70 scene 📉8
- 4 schedule
- 142 script 📈1
- 235 select 📈7
- 3170 sensor 📈57
- 1 sun
- 563 switch 📈25
- 2 tag
- 31 text 📈16
- 24 timer 📈3
- 32 todo 📈1
- 4 tts
- 206 update 📈15
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
