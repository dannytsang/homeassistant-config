[<- Back](README.md)
# Statistics 📊
I have 6,508 states (📉218) in Home Assistant.
By domain these are:
-   1 alarm_control_panel
-   434 automation 📈4
-   737 binary_sensor 📉107
-   197 button 📉2
-   28 calendar
-   20 camera 📈1
-   16 climate 📉2
-   2 conversation
-   3 counter
-   17 cover 📈8
-   411 device_tracker 📈8
-   16 event
-   1 fan
-   15 group 📈1
-   51 image
-   97 input_boolean 📈4
-   1 input_datetime
-   68 input_number
-   5 input_select
-   59 input_text
-   64 light 📈2
-   7 lock 📉16
-   22 media_player 📉2
-   181 number 📉2
-   4 person
-   3 remote
-   77 scene 📈2
-   3 schedule
-   169 script 📈4
-   161 select 📈4
-   3035 sensor 📉102
-   2 siren
-   1 stt
-   1 sun
-   360 switch 📉6
-   2 tag
-   12 text 📉2
-   11 timer
-   20 todo
-   1 tts
-   175 update
-   1 vacuum
-   3 wake_word
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