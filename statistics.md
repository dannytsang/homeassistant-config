[<- Back](README.md)
# Statistics 📊
I have 6,726 states (📈380) in Home Assistant.
By domain these are:
-   1 alarm_control_panel
-   428 automation 📈6
-   844 binary_sensor 📈40
-   199 button 📈19
-   28 calendar
-   19 camera
-   18 climate 📈2
-   2 conversation
-   3 counter
-   25 cover 📈8
-   403 device_tracker 📈25
-   16 event 📉1
-   1 fan
-   14 group
-   51 image
-   93 input_boolean
-   1 input_datetime
-   68 input_number
-   5 input_select
-   59 input_text
-   62 light 📈1
-   23 lock 📈4
-   24 media_player 📈3
-   183 number 📈7
-   4 person
-   3 remote
-   75 scene
-   3 schedule 📈1
-   165 script 📈6
-   157 select 📈2
-   3137 sensor 📈139
-   2 siren
-   1 stt
-   1 sun
-   366 switch 📈17
-   2 tag
-   14 text 📈2
-   1 time 📈1
-   11 timer
-   20 todo
-   1 tts
-   175 update 📈1
-   1 vacuum
-   3 wake_word 📈1
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