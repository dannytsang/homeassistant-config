[<- Back](README.md)
# Statistics 📊
I have 6,035 states (📈82) in Home Assistant.
By domain these are:
-   1 alarm_control_panel
-   411 automation 📈4
-   771 binary_sensor 📈23
-   160 button 📈1
-   28 calendar
-   19 camera
-   15 climate 📈1
-   2 conversation
-   3 counter 📉2
-   17 cover
-   356 device_tracker 📈12
-   15 event
-   1 fan
-   14 group
-   51 image
-   87 input_boolean 📉1
-   1 input_datetime
-   68 input_number 📈1
-   5 input_select
-   59 input_text
-   63 light
-   19 lock
-   23 media_player
-   174 number
-   4 person
-   15 proximity
-   4 remote
-   75 scene 📈4
-   2 schedule
-   153 script
-   154 select
-   2744 sensor 📈42
-   2 siren
-   1 stt
-   1 sun
-   346 switch 📈5
-   2 tag
-   12 text
-   11 timer 📉1
-   20 todo
-   1 tts
-   108 update 📉2
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