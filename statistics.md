[<- Back](README.md)
# Statistics 📊
I have 6,346 states (📈194) in Home Assistant.
By domain these are:
-   1 alarm_control_panel
-   422 automation 📈3
-   804 binary_sensor 📈24
-   180 button 📈15
-   28 calendar
-   19 camera
-   16 climate
-   2 conversation
-   3 counter
-   17 cover
-   378 device_tracker 📈18
-   17 event 📈2
-   1 fan
-   14 group
-   51 image
-   93 input_boolean 📈1
-   1 input_datetime
-   68 input_number
-   5 input_select
-   59 input_text
-   63 light
-   19 lock
-   21 media_player
-   176 number 📈3
-   4 person
-   3 remote
-   75 scene 📈1
-   2 schedule
-   159 script 📈5
-   155 select 📈1
-   2898 sensor 📈88
-   2 siren
-   1 stt
-   1 sun
-   351 switch 📈6
-   2 tag
-   12 text
-   11 timer
-   20 todo
-   1 tts
-   174 update 📈2
-   1 vacuum
-   2 wake_word
-   1 water_heater
-   3 weather
-   10 zone

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