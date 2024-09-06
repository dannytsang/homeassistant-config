[<- Back](README.md)
# Statistics 📊
I have 6,152 states (📈117) in Home Assistant.
By domain these are:
-   1 alarm_control_panel
-   419 automation 📈8
-   780 binary_sensor 📈9
-   165 button 📈5
-   28 calendar
-   19 camera
-   16 climate 📈1
-   2 conversation
-   3 counter
-   17 cover
-   360 device_tracker 📈4
-   15 event
-   1 fan
-   14 group
-   51 image
-   92 input_boolean 📈5
-   1 input_datetime
-   68 input_number
-   5 input_select
-   59 input_text
-   63 light
-   19 lock
-   21 media_player 📉2
-   173 number 📉1
-   4 person
-   3 remote 📉1
-   74 scene 📉1
-   2 schedule
-   153 script
-   154 select
-   2786 sensor 📈42
-   1 stt
-   1 sun
-   345 switch 📉1
-   2 tag
-   12 text
-   11 timer
-   20 todo
-   1 tts
-   172 update 📈64
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