[<- Back to README](README.md)

# Statistics 📊
I have 7,604(📈96) states in Home Assistant.  
By domain these are:
- 2 ai_task
- 2 alarm_control_panel 📈1
- 384 automation 📈4
- 738 binary_sensor 📈11
- 276 button 📉2
- 52 calendar
- 15 camera 📈2
- 18 climate
- 4 conversation
- 1 counter
- 25 cover
- 458 device_tracker 📈13
- 27 event 📈2
- 2 fan
- 16 group
- 1 image
- 1 infrared
- 101 input_boolean 📉1
- 9 input_datetime
- 115 input_number
- 4 input_select
- 67 input_text 📉1
- 74 light
- 9 lock 📉1
- 29 media_player 📈1
- 8 notify 📈2
- 349 number 📈5
- 4 person
- 104 predbat 📈1
- 1 radio_frequency
- 3 remote
- 78 scene
- 4 schedule
- 141 script
- 243 select 📈5
- 3359 sensor 📈34
- 2 siren
- 4 stt
- 1 sun
- 567 switch 📈18
- 2 tag
- 31 text 📈1
- 22 timer
- 31 todo
- 4 tts
- 201 update 📈1
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
