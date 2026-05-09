[<- Back to README](README.md)

# Statistics 📊
I have 7,508 (📈317) states in Home Assistant.
By domain these are:
- 2 ai_task
- 1 alarm_control_panel
- 380 automation 📈6
- 727 binary_sensor 📈18
- 278 button 📈5
- 52 calendar
- 13 camera
- 18 climate
- 4 conversation
- 1 counter
- 25 cover
- 445 device_tracker 📈6
- 25 event
- 2 fan
- 16 group
- 1 image
- 1 infrared 📈1
- 102 input_boolean 📈3
- 9 input_datetime 📈2
- 115 input_number 📈1
- 4 input_select
- 68 input_text
- 74 light 📉2
- 10 lock
- 28 media_player 📈1
- 6 notify 📈5
- 344 number 📈12
- 4 person
- 103 predbat
- 1 radio_frequency 📈1
- 3 remote
- 78 scene
- 4 schedule
- 141 script
- 238 select 📈10
- 3325 sensor 📈212
- 2 siren
- 4 stt
- 1 sun
- 549 switch 📈11
- 2 tag
- 30 text 📈15
- 22 timer 📈1
- 31 todo
- 4 tts
- 200 update 📈9
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
