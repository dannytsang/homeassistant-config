# Danny's Home Assistant 🏡
<a href="https://travis-ci.com/github/dannytsang/homeassistant-config" target="_blank"><img src="https://img.shields.io/travis/com/dannytsang/homeassistant-config?style=plastic"/></a>
<a href="https://twitter.com/DannyTsang" target="_blank"><img src="https://img.shields.io/twitter/follow/DannyTsang?color=blue&style=plastic"/></a>

# Introduction 📢
My ⚽goal with home automation is to never have to think about doing something mentally or physically. This can be turning on a 💡light through to household chores such as 👕washing clothes. Currently, my journey continues.

I have always been interested in technology starting from the x10 days. At the time, I was did not have the money or 🧬life experience to use the 💻technology at the time. Fast forward a few 📅decades, I'm fortunate enough to have the means and place to splurge on home automtion and [Home Assistant](https://home-assistant.io) is the key to all of this.

This project contains configuration files for [Home Assistant](https://home-assistant.io) used in the House of Tsang 曾)

More details to follow. Visit my 📜[blog](https://dannytsang.co.uk).

## Statistics 📊
To get the template for the below stats, see [here](https://www.reddit.com/r/homeassistant/comments/plmy7e/use_this_template_and_show_us_some_details_about/?utm_medium=android_app&utm_source=share)
I have 2048 states in Home Assistant.
By domain these are:
- 1 alarm_control_panel
- 1 alert
- 216 automation
- 318 binary_sensor
- 2 button
- 35 calendar
- 51 camera
- 7 climate
- 2 counter
- 5 cover
- 130 device_tracker
- 45 group
- 10 image_processing
- 41 input_boolean
- 2 input_datetime
- 1 input_select
- 28 input_text
- 33 light
- 6 media_player
- 2 number
- 4 person
- 7 proximity
- 3 remote
- 100 scene
- 43 script
- 1 select
- 894 sensor
- 1 sun
- 48 switch
- 1 water_heater
- 3 weather
- 7 zone

## Hardware 🔩
I have gradually built up a lot of hardware overtime to from sensors to switches which allow automations to come to life. As part of this journey, I learnt a lot and amassed a lot of different devices with varying compatibilities. This is the beauty of [Home Assistant](https://home-assistant.io) which allows me to cross eco system compatibility.

[Home Assistant](https://home-assistant.io) is running on a Dell OptiPlex 3060 SFF running [Unraid](https://unraid.net/) as the base Operating System.

### Hubs / Controllers
At the heart of everything are hubs / controllers. These are devices that bridge the different protocols to talk to computers. For example Zigbee to WiFi.
* [Philips Hue Hub v2](https://www.philips-hue.com/en-us/p/hue-bridge/046677458478)
* [Samsung SmartThings v3](https://www.samsung.com/uk/smartthings/hub-f-hub-uk-v3/)
* <strike>[Conbee II](https://phoscon.de/en/conbee2)</strike> - Currently having stability issues where the USB device is disconnected/not detected.

### Amazon
We are an Echo/Alexa household due to the compatibility it has with devices. This is less of an issue since moving to [Home Assistant](https://home-assistant.io).
* [Echo 1st Gen](https://www.amazon.com/Amazon-Echo-Bluetooth-Speaker-with-WiFi-Alexa-White/dp/B00X4WHP5E?th=1)
* [Echo dot 2nd Gen](https://www.amazon.co.uk/Amazon-Echo-Dot-2nd-Gen/dp/B01DFKBL68)
* [Echo dot 3rd Gen](https://www.amazon.co.uk/All-new-Echo-Dot-3rd-Gen/dp/B07PFFMV56/ref=sr_1_2?dchild=1&keywords=echo+dot+white&qid=1629415420&sr=8-2)
* [Echo show 10 2nd Gen](https://www.amazon.co.uk/All-New-Echo-Show-2nd-Gen/dp/B0793G9T6T?th=1)
* [Echo show 5 1st Gen](https://www.amazon.co.uk/amazon-echo-show-5-compact-smart-display-with-alexa/dp/B07KD7TJD6?th=1)

### Broadlink
An alternative to the now end of life Harmony Hub from Logitech. I have the [RM4 Pro](https://www.ibroadlink.com/products/ir+rf).

### <strike><a name="currentcost"></a>CurrentCost</strike>
<strike>A long standing device I had before [Home Assistant](https://home-assistant.io), it uses a clamp and battery to read electricity usage from the meter. Later, they came out with plugs that sense power draw as well. All of this is using [Energy@Home](https://github.com/dannytsang/energyathome) to store readings and present it in [Home Assistant](https://home-assistant.io).</strike>
* <strike>[Data Cable](http://www.currentcost.com/product-datacable.html)</strike>
* <strike>[Envi](http://www.currentcost.com/product-cc128.html)</strike>
* <strike>[Individual Application Monitors](http://www.currentcost.com/product-iams.html)</strike>
Replaced with SmartThings and GlowMarkt.

### Elgato
I love Elgato products. They are generally well designed however you do pay a price.
* [Key Light](https://www.elgato.com/en/key-light)
* [Stream Deck](https://www.elgato.com/en/stream-deck)

### GLEDOPTO
Third party WLED to Zigbee controller.
* RGB CCT 1D

### Google
Really like the casting feature to share content however found it was relatiely unstable and would loose connectivity or stop playing.
* [Chromecast](https://store.google.com/gb/product/chromecast?hl=en-GB)
* [Chromecast Ultra](https://store.google.com/nz/product/chromecast_ultra?hl=en-GB)

### Hive Home
Probably the first smart house item we purchased in 2010. There are a lot better options now and it works but has reliablility issues and would look to replace at some point.
* Hive 1 (SLT2)

### Hyperion
Software to replicate the Philips Hue HDMI sync in a DIY way. I have not managed to get the SK6812 LED strips to work yet but the HDMI capture has been used for notifications and a preview of what's being watched.
* [SK6812](https://www.aliexpress.com/item/32549394249.html?spm=a2g0s.9042311.0.0.584a4c4d07qBv6)
* [ZasLuke USB Capture Card](https://www.amazon.co.uk/gp/product/B08DJ4SXMX/ref=ppx_yo_dt_b_asin_title_o09_s00?ie=UTF8&psc=1)

### Ikea
Love the Ikea blinds. They are easy to get hold of compared to other products and once you get over the pairing, they have worked flawlessly.
* [FYRTUR](https://www.ikea.com/gb/en/p/fyrtur-block-out-roller-blind-wireless-battery-operated-grey-60408181/)
* [KADRILJ](https://www.ikea.com/gb/en/p/kadrilj-roller-blind-wireless-battery-operated-grey-30408154/)
* [TRÅDFRI GU10](https://www.ikea.com/gb/en/p/tradfri-led-bulb-gu10-400-lumen-wireless-dimmable-white-spectrum-90408603/)
* [TRÅDFRI Remote control](https://www.ikea.com/gb/en/p/tradfri-remote-control-30443124/)

### Lifx
The light output is one of the best in terms of lumens. The colours are generally very good. The downside has been pairing them to the WiFi on Android has been hit and miss. Once connected, there has been no issues.
* [Candle White to Warm](https://uk.lifx.com/collections/lamps-and-pendants/products/candle-white-to-warm)
* [Color A19](https://www.lifx.com/products/lifx-color-a19)
* Color 1000
* [Mini White](https://eu.lifx.com/products/lifx-mini-white)

### Logitech
Until Broadlink came along, Logitech was the only player in town to integrate remote control. The hub has been unstable however there were no alternatives at the time. I haven't integrated any automations as a result.
* [Harmony Elite](https://www.logitech.com/en-gb/products/harmony/harmony-elite.915-000257.html?crid=60)

### Philips Hue
Well engineered and personally, asthetically pleasing compared to some of it's competitor. Whilst I have a Hue Hub, not all Hue devices are paired to the hue Hub e.g motion sensors are paired to the Samsung SmartThings hub.
* Dimmer switch
* [Motion sensor](https://www.philips-hue.com/en-gb/p/hue-motion-sensor/8718696743171)
* [Outdoor (motion) sensor](https://www.philips-hue.com/en-gb/p/hue-outdoor-sensor/8718699625474)
* [Play light bar](https://www.philips-hue.com/en-gb/p/hue-white-and-colour-ambiance-play-light-bar-double-pack/7820230P7)
* [White and colour ambiance (E14)](https://www.philips-hue.com/en-gb/p/hue-white-and-colour-ambiance-single-bulb-e14/8718696695166)
* [White and colour ambiance (E27)](https://www.philips-hue.com/en-gb/p/hue-white-and-colour-ambiance-1-pack-e27/8718699673109#overview)

### Raspberry Pi Foundation
A powerful and relatively cheap SOC board to power home projects. I have these monitoring UPS through to in home display (dashboard).
* [Raspberry Pi 4 model B](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
* [Raspberry Pi 3 model B](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/)

### Ring
Does not have all the support with [Home Assistant](https://home-assistant.io), however [HACS](https://hacs.xyz/) fills the gap. Not too many issues to report and works well in general.
* [Doorbell 2](https://en-uk.ring.com/products/video-doorbell-2)
* [Security 1st Gen](https://www.amazon.co.uk/ring-alarm-5-piece-kit-home-security-system-with-optional-assisted-monitoring-no-long-term-commitments-works-with-alexa/dp/B087Q3BR8M0)
* [Stickup Cam Elite](https://en-uk.ring.com/products/stick-up-security-camera-elite)

### Roku
Relatively cheap and usable media streaming device (compared to a PlayStation). Has a wide variety of support for apps and more reliable than Chromecast devices.
* [NowTV Smart Stick](https://www.nowtv.com/ie/smart-tv-stick)
* [Streaming stick+](https://www.roku.com/en-gb/products/streaming-stick-plus)

### Samsung SmartThings
Some real gems that Samsung has made like the multipurpose sensor where Philips doesn't have. Generally reliable and well packaged.
* [Multipurpose Sensor](https://www.samsung.com/uk/smartthings/sensor/smartthings-multipurpose-sensor-gp-u999sjvlaea/)
* [Smart Plug 2019](https://www.samsung.com/uk/smartthings/outlet/smartthings-smart-plug-gp-wou019bbdwg/)
* [Water Leak Sensors v3](https://www.samsung.com/uk/smartthings/sensors-plug-f-wtr-uk-v3/)

### Sonoff
Relatively cheap hardware and some unique offering however lacks out of the box support.
* [USB Smart Adaptor](https://sonoff.tech/product/diy-smart-switch/micro/)

### Ubiquiti
Fully kitted networking gear of choice and provides really good integration with [Home Assistant](https://home-assistant.io).
* [Unifi AC Lite](https://www.ui.com/unifi/unifi-ap-ac-lite/)
* [Unifi Security Gateway](https://www.ui.com/unifi-routing/usg/)
* Unifi Swtich 8
* [Unifi Switch 24](https://store.ui.com/collections/unifi-network-switching/products/usw-24)

### Wemos
Small WiFi development board with an ESP8266 chip. I'm using [ESPHome](https://esphome.io/) firmware.
* [D1 mini pro](https://www.wemos.cc/en/latest/d1/d1_mini_pro.html)

# Addons ➕
This is not an exhaustive list and it changes quite a lot. Too keep up to date, please subscribe to my [blog](https://dannytsang.co.uk).
* [Git pull](https://github.com/home-assistant/addons/tree/master/git_pull)
* [Home Assistant Google Drive Backup](https://github.com/sabeechen/hassio-google-drive-backup)
* [Log Viewer](https://github.com/hassio-addons/addon-log-viewer)
* [Mosquitto broker](https://github.com/home-assistant/addons/tree/master/mosquitto)
* [Ring Device Integration via MQTT](https://github.com/tsightler/ring-mqtt-ha-addon)
* [Samba Backup](https://github.com/thomasmauerer/hassio-addons/tree/master/samba-backup)
* [Visual Studio Code](https://github.com/hassio-addons/addon-vscode)

# Integrations 🖧
There are too many to list and changes now and then so I will list the ones that will help explain configurations. These may include integrations from [HACS](https://hacs.xyz/).

### HACS
An amazing community store (almost) from interface to integrations not available natively in [Home Assistant](https://home-assistant.io). [HACS](https://hacs.xyz/) plugs a hole where things are not officially supported can be easily installed. Because it's community supported, use with caution.

### Frigate NVR
[Frigate](https://github.com/blakeblackshear/frigate-hass-integration) performs real time image/video detection using Google's TensorFlow machine learning technology. The key difference is the real time where it will take a stream from a camera and process it in real time. When it detects something, it will alert Home Assistant and you can do what you want with that state change / event.

### GlowMarkt
The [Display and CAD](https://shop.glowmarkt.com/products/display-and-cad-combined-for-smart-meter-customers) replaced the in home display provided by my energy provider and has the added benefit of direct smart meter "real time" data via API and MQTT. It is more accurate than the [CurrentCost](#currentcost) because it reads directly from the meter. Also it should have gas usage but I am unable to get this to work at the moment.

### Unifi
[Ubiquiti Unifi](https://www.home-assistant.io/integrations/unifi/) allows for network based presence detection. The advantage is the integration will poll for devices from the controller which would be aware of the network where as the UPnP integration relies on network scans instead.

Other noteworthy mentions:
* [CO2 Signal](https://www.home-assistant.io/integrations/co2signal/)
* [HASS-Deepstack-face](https://github.com/robmarkcole/HASS-Deepstack-face)
* [HASS-Deepstack-object](https://github.com/robmarkcole/HASS-Deepstack-object)
* [IFTTT](https://www.home-assistant.io/integrations/ifttt/)
* [Network UPS Tool](https://www.home-assistant.io/integrations/nut/)
* [Slack](https://www.home-assistant.io/integrations/slack/)

# GitHub 🐱🐙
This repository contains the configuration files used. It will not contain everything e.g. password (A.K.A secrets.yaml) file as well as other configuration done in the User Interface (UI).

Whilst [Home Assistant](https://home-assistant.io) offer backup solution, it is a bit of all or nothing restore process where as Git (or any versioning system) would allow incremental changes to be stored and reverted where necessary.

## Setup ⚙️
I use the UI as much as possible to create and maintain changes. There's currently a general movement towards the UI within [Home Assistant](https://home-assistant.io) such as setup of integrations being removed from the configuration files. I generally support this move to make it easier for everyone.

All changes are performed in the UI where possible and if they are held in configuration files then it will end up in Git where possible.

I use the Visual Studio Code add-on to edit files in [Home Assistant](https://home-assistant.io) or if I really have to the File Editor add-on on my mobile deives.

Visual Studio Code addon includes a Git client so all changes are managed through the text editor.

## Workflows 🖇️
The advantage of using a source code management system like Git is the ability to use hooks to trigger actions (as well as other advantages).

I use GitHub actions to verify the changes committed by running it against [Home Assistant](https://home-assistant.io) builds. If successful, [Home Assistant](https://home-assistant.io) will pull down the changes and if the changes are configuration related (as opposed to readme / markdown files) then it will perform another local configuration check and restart to pick up the changes.

For this reason, the `custom_components` is stored in the repository to allow a successful build and configuration check.

## Structure 🧱
This repository's top level is the /config folder where typically the configuration.yaml file resides. More details can be found [here](https://www.home-assistant.io/docs/configuration/).

I use some of the "advance" configuration options such as [split configuration](https://www.home-assistant.io/docs/configuration/splitting_configuration/) and [packages](https://www.home-assistant.io/docs/configuration/packages/).

### Blueprints
I have yet to explore this feature yet.

### Camera
Private directory to hold camera images. Predominantly used for sending images to [DeepStack](https://deepstack.cc/).

### ESPHome
Files related to managing the ESP microcontroller. See [ESPHome.io](https://esphome.io/) for more details.

### Packages
See [packages readme](packages/README.md) for more details.

### Split Configurations
I use split configuration files to help manage and keep the `configuration.yaml` size down. The advantange is each type of configuration such as scripts, scenes, etc will be managed by [Home Assistant](https://home-assistant.io) UI with minimal setup.

### www
A public folder for holding any files such as images that does not need authentication. I use it for attaching images to notifications.

## Tags / Releases 🏷️
I will apply a tag before upgrading to a major/minor/monthly release of [Home Assistant](https://home-assistant.io). These will represent a snapshot of a (hopefully) stable configuration used prior to upgrading and a point to restore back to if needed.
