# Hardware 🔩
I have gradually built up a lot of hardware overtime to from sensors to switches which allow automations to come to life. As part of this journey, I learnt a lot and amassed a lot of different devices with varying compatibilities. This is the beauty of [Home Assistant](https://home-assistant.io) to use multiple eco systems together.

[Home Assistant](https://home-assistant.io) is running on a custom built computer running [Unraid](https://unraid.net/) as the base Operating System.

## <a name="controllers"></a>Hubs / Controllers
At the heart of everything are hubs / controllers. These are devices that bridge the different protocols to talk to computers. For example Zigbee to WiFi.
*   [SMLIGHT SLZB-06](https://smlight.tech/product/slzb-06/)

## Amazon
We are an Echo/Alexa household due to the compatibility it has with devices. This is less of an issue since moving to [Home Assistant](https://home-assistant.io).
*   [Echo 1st Gen](https://www.amazon.com/Amazon-Echo-Bluetooth-Speaker-with-WiFi-Alexa-White/dp/B00X4WHP5E?th=1)
*   [Echo dot 2nd Gen](https://www.amazon.co.uk/Amazon-Echo-Dot-2nd-Gen/dp/B01DFKBL68)
*   [Echo dot 3rd Gen](https://www.amazon.co.uk/All-new-Echo-Dot-3rd-Gen/dp/B07PFFMV56/ref=sr_1_2?dchild=1&keywords=echo+dot+white&qid=1629415420&sr=8-2)
*   [Echo show 10 2nd Gen](https://www.amazon.co.uk/All-New-Echo-Show-2nd-Gen/dp/B0793G9T6T?th=1)
*   [Echo show 5 1st Gen](https://www.amazon.co.uk/amazon-echo-show-5-compact-smart-display-with-alexa/dp/B07KD7TJD6?th=1)

## Aqara
Great value devices.
*   [MCCGQ11LM 153](https://www.aqara.com/eu/product/door-and-window-sensor/)
*   [T1M](https://www.aqara.com/eu/product/ceiling-light-t1m/)

## Aruba
Replaced Unifi with Aruba for their PPSK, controllerless setup. Basic support in Home Assistant.
*   [Aruba 505](https://www.arubanetworks.com/en-gb/products/wireless/access-points/indoor-access-points/500-series/)

## Broadlink
An alternative to the now end of life Harmony Hub from Logitech. I have the [RM4 Pro](https://www.ibroadlink.com/products/ir+rf).

## Ecowitt
Weather station for more local and accurate weather data. Unfortunately, it does not provide forecast data.
*   [Wittboy](https://shop.ecowitt.com/en-gb/products/wittboy?variant=41794776006818) The rain sensor fails to accurately read rain.

## Elgato
I love Elgato products. They are generally well designed however you do pay a price.
*   [Key Light](https://www.elgato.com/en/key-light)
*   [Stream Deck](https://www.elgato.com/en/stream-deck)

## Everything Smart Home
From Everything Smart Home, Lewis has created an ESP32 mmWave kit.
*   [EP1 Kit](https://shop.everythingsmart.io/products/everything-presence-one-kit)

## Expressif
Makes chips and used in popular commercial IOT applications like [Tuya](https://www.tuya.com/). I use Wemos variant of the older ESP8266 (see below) and the newer ESP32. To manage all of these, I use ESPHome.
*   [ESP32 CP2102](https://www.espressif.com/en/products/socs/esp32)

## Feasycom
*   [FSC-BP108](https://www.feasycom.com/bluetooth-5-1-waterproof-bluetooth-beacon) Waterproof (IP67) Bluetooth Low Energy iBeacon. A cheaper version of an Apple Air Tag.

## GLEDOPTO
Third party WLED to Zigbee controller.
*   [RGBW CCT 1D](https://www.gledopto.eu/rgbw-controller-zigbee-compatible-eng)

## Glowmarkt
An in home display (IHD) that supports live smart meter reading to APIs and MQTT.
*   [CAD](https://shop.glowmarkt.com/products/display-and-cad-combined-for-smart-meter-customers)

## Google
Really like the casting feature to share content however found it was relatiely unstable and would loose connectivity or stop playing.
*   [Chromecast Ultra](https://store.google.com/nz/product/chromecast_ultra?hl=en-GB)
*   [Google TV](https://store.google.com/gb/product/chromecast_google_tv?hl=en-GB)

## Growatt
Solar manufacturer. I use Solar Assistant to get local and faster updates.
*   SPH3000 Inverter
*   [GBLI 6532 Battery](https://www.ginverter.com/products/gbli-6532-battery) 

## <a name="hive"></a>Hive Home
Probably the first smart house item we purchased in 2010. I have since upgraded to gen 2 of the hardware which has improved on reliablilty on the hub.
*   [Hive 2 (SLT3)](https://www.hivehome.com/shop/smart-heating/hive-active-heating?icid=mname%3Amega-menu.iname%3Ahive-active-heating)

## HP
Rock solid printer however limited support in Home Assistant for mine. For example, it does not say how much toner is left.
*   [HP M402DW](https://www.printerland.co.uk/product/hp-laserjet-pro-m402dw/138809)

## Ikea
Love the Ikea blinds. They are easy to get hold of compared to other products and once you get over the pairing, they have worked flawlessly.
*   [FYRTUR](https://www.ikea.com/gb/en/p/fyrtur-block-out-roller-blind-wireless-battery-operated-grey-60408181/)
*   [KADRILJ](https://www.ikea.com/gb/en/p/kadrilj-roller-blind-wireless-battery-operated-grey-30408154/)
*   [TRÅDFRI Signal Repeater](https://www.ikea.com/gb/en/p/tradfri-signal-repeater-80424255/)
*   [TRÅDFRI Remote control](https://www.ikea.com/gb/en/p/tradfri-remote-control-30443124/)

## Lifx
The light output is one of the best in terms of lumens. The colours are generally very good. The downside has been pairing them to the WiFi on Android has been hit and miss. Once connected, there has been no issues.
*   [Candle White to Warm](https://uk.lifx.com/collections/lamps-and-pendants/products/candle-white-to-warm)
*   [Color A19](https://www.lifx.com/products/lifx-color-a19)
*   [Mini White](https://eu.lifx.com/products/lifx-mini-white)

## Logitech
Until Broadlink came along, Logitech was the only player in town to integrate remote control. The hub has been unstable however there were no alternatives at the time. I haven't integrated any automations as a result.
*   [Harmony Elite](https://www.logitech.com/en-gb/products/harmony/harmony-elite.915-000257.html?crid=60)

## myEnergi
UK based solar designer/manufacturer.
*   [Eddi](https://www.myenergi.com/eddi-power-diverter/) Solar diverter or a fancy relay to turn on electrical devices on or off when there is excess solar.
*   [Zappi](https://www.myenergi.com/zappi-ev-charger/) EV charger

## OralB
A toothbrush manufacturer that now supports bluetooth enabled electric toothbrushes.
*   [6000N](https://www.oralb.co.uk/en-gb/products/electric-toothbrushes/oral-b-smart-6-6000n-white-electric-toothbrush)

## <a name="philipshue"></a>Philips Hue
Well engineered and personally, asthetically pleasing compared to some of it's competitor. Whilst I have a Hue Hub, not all Hue devices are paired to the hue Hub e.g motion sensors are paired to the Samsung SmartThings hub.
*   Dimmer switch
*   [Motion sensor](https://www.philips-hue.com/en-gb/p/hue-motion-sensor/8718696743171)
*   [Outdoor (motion) sensor](https://www.philips-hue.com/en-gb/p/hue-outdoor-sensor/8718699625474)
*   [White and colour ambiance (E14)](https://www.philips-hue.com/en-gb/p/hue-white-and-colour-ambiance-single-bulb-e14/8718696695166)
*   [White and colour ambiance (E27)](https://www.philips-hue.com/en-gb/p/hue-white-and-colour-ambiance-1-pack-e27/8718699673109#overview)

## Raspberry Pi Foundation
A powerful and relatively cheap SOC board to power home projects. I have these monitoring UPS through to in home display (dashboard) through to monitoring 3D prints using Octoprint.
*   [Raspberry Pi 4 model B](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
*   [Raspberry Pi 3 model B](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/)

## Ring
Does not have all the support with [Home Assistant](https://home-assistant.io), however [HACS](https://hacs.xyz/) fills the gap. Not too many issues to report and works well in general. The 1st generation alarm works with 2nd generation sensors.
*   [Doorbell 2](https://en-uk.ring.com/products/video-doorbell-2)
*   [Security 1st Gen](https://www.amazon.co.uk/ring-alarm-5-piece-kit-home-security-system-with-optional-assisted-monitoring-no-long-term-commitments-works-with-alexa/dp/B087Q3BR8M0)
*   [Ring Alarm Contact Sensor 1st Gen](https://www.amazon.co.uk/gp/product/B07QRZ8TNY/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
*   [Ring Alarm Contact Sensor 2nd Gen](https://www.amazon.co.uk/ring-alarm-contact-sensor-2nd-generation/dp/B08L5BZFJ7/ref=sr_1_3?crid=2EHCOKQXDB8D&keywords=ring+alarm&qid=1640880930&sprefix=ring+alarm%2Caps%2C81&sr=8-3)
*   [Ring Alarm Motion Sensor 1st Gen](https://www.amazon.co.uk/gp/product/B07QQV5RCZ/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
*   [Ring Alarm Motion Sensor 2nd Gen](https://www.amazon.co.uk/ring-alarm-motion-detector-2nd-generation/dp/B08J6C5JJN/ref=sr_1_1_sspa?crid=1CS8GPODHRQ0A&keywords=ring+alarm+motion&qid=1640881018&sprefix=ring+alarm+motion%2Caps%2C80&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExRE9SRE1PSEtHNk0mZW5jcnlwdGVkSWQ9QTA2OTcyMDVUSE9KMFJJSjI4R00mZW5jcnlwdGVkQWRJZD1BMDMzMTIwNzVIUFE2TFFYV1ZRRiZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=)
*   [Stickup Cam Elite](https://en-uk.ring.com/products/stick-up-security-camera-elite)

## <a name="smartthings"></a>Samsung SmartThings
Some real gems that Samsung has made like the multipurpose sensor where Philips doesn't have. Generally reliable and well packaged.
*   [Multipurpose Sensor](https://www.samsung.com/uk/smartthings/sensor/smartthings-multipurpose-sensor-gp-u999sjvlaea/)
*   [Smart Plug 2019](https://www.samsung.com/uk/smartthings/outlet/smartthings-smart-plug-gp-wou019bbdwg/)
*   [Water Leak Sensors v3](https://www.samsung.com/uk/smartthings/sensors-plug-f-wtr-uk-v3/)

## Shelly
I like their hardware relays and fits into 35mm back boxes and allows switches to function normally.
*   [Plus 1PM](https://shelly.cloud/shelly-plus-1pm/)

## Sonoff
Relatively cheap hardware and some unique offering however lacks out of the box support.
*   [USB Smart Adaptor](https://sonoff.tech/product/diy-smart-switch/micro/)
*   [USB Smart Adaptor Zigbee](https://sonoff.tech/product/diy-smart-switches/zbmicro/)

## SwitchBot
The first curtain rod devices. It uses bluetooth which isn't great for range so I pair it with the hub mini
*   [SwitchBot Blind Tilt](https://uk.switch-bot.com/products/switchbot-blind-tilt)
*   [Hub Mini](https://uk.switch-bot.com/products/switchbot-hub-mini)

## TP Link
Bought one of these as a potential replacement to the Belkin Wemos which had the killer feature of time to switch off when it was powered on built into the app/plugs. The TP Link did not have that but it does have all the other features like power monitoring. This has been installed behind a hard to reach metal white goods where Zigbee was not strong enough to reach but WiFi was.
*   [HS110](https://www.tp-link.com/uk/home-networking/smart-plug/hs110/)
*   [KP115](https://www.tp-link.com/uk/home-networking/smart-plug/kp115/)
*   [KP303](https://www.tp-link.com/uk/home-networking/smart-plug/kp303/)

## TuYa
Very well priced IoT device manufacturer. I am using the temperature sensor for inside the fridge and freezers. The radiator values are closes to the Tado TRVs. It's not as well built but the idea is you don't need to touch it.
*   [ZigBee Temperature And Humidity Sensor](https://www.aliexpress.com/item/1005003718187629.html) 
*   [TH02Z](https://www.aliexpress.com/item/1005006485984753.html?spm=a2g0o.order_list.order_list_main.10.4ebe1802YLANmt)
*   [TRV TV02](https://www.aliexpress.com/item/1005003119636318.html)
*   [ZY-M100-L](https://www.aliexpress.com/item/1005006618917798.html?spm=a2g0o.order_list.order_list_main.5.4ebe1802YLANmt)

## Ubiquiti
Fully kitted networking gear of choice and provides really good integration with [Home Assistant](https://home-assistant.io). I have also gone towards their cameras and protect system.
*   [G4 Instant](https://techspecs.ui.com/unifi/cameras-nvrs/camera-g4-instant)
*   [G5 Flex](https://techspecs.ui.com/unifi/cameras-nvrs/uvc-g5-flex)
*   [G5 Turret Ultra](https://techspecs.ui.com/unifi/cameras-nvrs/uvc-g5-turret-ultra?s=uk)
*   [Unifi Dream Machine Pro](https://uk.store.ui.com/uk/en/collections/unifi-dream-machine/products/udm-pro)
*   Unifi Swtich 8
*   [Unifi Switch Lite 8 PoE](https://techspecs.ui.com/unifi/switching/usw-lite-8-poe)
*   [Unifi Switch Lite 16 PoE](https://techspecs.ui.com/unifi/switching/usw-lite-16-poe)
*   [Unifi Swtich 8 60W](https://uk.store.ui.com/uk/en/collections/unifi-switching-utility-poe/products/us-8-60w?variant=us-8-60w)
*   [Unifi Switch 24](https://uk.store.ui.com/uk/en/collections/unifi-switching-standard-ethernet)

## UseeLink
A no name zigbee brand.
*   [SM-0306E-2W](https://www.amazon.co.uk/dp/B09JWP6TJG?psc=1&ref=ppx_yo2ov_dt_b_product_details) Sockets are individually controllable. USBs are all controlled together as a group. I wish it had power monitoring as well.

## Wemos
Small WiFi development board with an ESP8266 chip. I'm using [ESPHome](https://esphome.io/) firmware.
*   [D1 mini pro](https://www.wemos.cc/en/latest/d1/d1_mini_pro.html)

## Zemismart
*   [ZM16-TYZB](https://www.zemismart.com/products/zm16-tyzb-eu)
