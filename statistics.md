[<- Back](README.md)
# Statistics 📊
I have 6,547 states (📈38) in Home Assistant.
By domain these are:
- 1 alarm_control_panel
- 436 automation 📈2
- 748 binary_sensor 📈11
- 198 button 📈1
- 28 calendar
- 20 camera
- 15 climate 📈1
- 2 conversation
- 3 counter
- 17 cover
- 413 device_tracker 📈2
- 16 event
- 1 fan
- 17 group 📈2
- 51 image
- 97 input_boolean
- 1 input_datetime
- 68 input_number
- 5 input_select
- 59 input_text
- 64 light
- 7 lock
- 22 media_player
- 181 number
- 4 person
- 3 remote
- 77 scene
- 3 schedule
- 169 script
- 161 select
- 3057 sensor 📈22
- 2 siren
- 1 stt
- 1 sun
- 362 switch 📈2
- 2 tag
- 12 text
- 11 timer
- 20 todo
- 1 tts
- 173 update 📉2
- 1 vacuum
- 3 wake_word
- 1 water_heater
- 3 weather
- 10 zone

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