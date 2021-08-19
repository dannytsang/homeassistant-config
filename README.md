# Danny's Home Assistant
<a href="https://travis-ci.com/github/dannytsang/homeassistant-config" target="_blank"><img src="https://img.shields.io/travis/com/dannytsang/homeassistant-config?style=plastic"/></a>
<a href="https://twitter.com/DannyTsang" target="_blank"><img src="https://img.shields.io/twitter/follow/DannyTsang?color=blue&style=plastic"/></a>

Configuration files for [Home Assistant](https://home-assistant.io) used in the House of Tsangs.

More details to follow. Visit my [blog](https://dannytsang.co.uk) in the mean time.

## Hardware
I have gradually built up a lot of hardware overtime to from sensors to switches which allow automations to come to life. As part of this journey, I learnt a lot and amassed a lot of different devices with varying compatibilities. This is the beauty of [Home Assistant](https://home-assistant.io) which allows me to cross eco system compatibility.

### Hubs / Controllers
At the heart of everything are hubs / controllers. These are devices that bridge the different protocols to talk to computers. For example Zigbee to WiFi.
 * [Philips Hue Hub v2](https://www.philips-hue.com/en-us/p/hue-bridge/046677458478)
 * [Samsung SmartThings v3](https://www.samsung.com/uk/smartthings/hub-f-hub-uk-v3/)
 * [Conbee II](https://phoscon.de/en/conbee2)

### Aqara
I have just started to look at this manufacturer since I got the Conbee II stick.
 * [Temperature and Humidity Sensor](https://www.aqara.com/en/temperature_humidity_sensor.html)

### CurrentCost
A long standing device I had before [Home Assistant](https://home-assistant.io), it uses a clamp and battery to read electricity usage from the meter. Later, they came out with plugs that sense power draw as well. All of this is using [Energy@Home](https://github.com/dannytsang/energyathome) to store readings and present it in [Home Assistant](https://home-assistant.io).
 * [Data Cable](http://www.currentcost.com/product-datacable.html)
 * [Envi](http://www.currentcost.com/product-cc128.html)
 * [Individual Application Monitors](http://www.currentcost.com/product-iams.html)

### Elgato
I love Elgato products. They are generally well designed however you do pay a price.
 * [Key Light](https://www.elgato.com/en/key-light)
 * [Stream Deck](https://www.elgato.com/en/stream-deck)

### Google
Really like the casting feature to share content however found it was relatiely unstable and would loose connectivity or stop playing.
 * [Chromecast](https://store.google.com/gb/product/chromecast?hl=en-GB)
 * [Chromecast Ultra](https://store.google.com/nz/product/chromecast_ultra?hl=en-GB)

### Hive Home
Probably the first smart house item we purchased in 2010. There are a lot better options now and it works but has reliablility issues and would look to replace at some point.
 * Hive 1 (SLT2)

### Lifx
The light output is one of the best in terms of lumens. The colours are generally very good. The downside has been pairing them to the WiFi on Android has been hit and miss. Once connected, there has been no issues.
 * [Candle White to Warm](https://uk.lifx.com/collections/lamps-and-pendants/products/candle-white-to-warm)
 * [Color A19](https://www.lifx.com/products/lifx-color-a19)
 * Color 1000
 * [Mini White](https://eu.lifx.com/products/lifx-mini-white)

### Philips Hue
Well engineered and personally, asthetically pleasing compared to some of it's competitor. Whilst I have a Hue Hub, not all Hue devices are paired to the hue Hub e.g motion sensors are paired to the Samsung SmartThings hub.
 * Dimmer switch
 * [Motion sensor](https://www.philips-hue.com/en-gb/p/hue-motion-sensor/8718696743171)
 * [Outdoor (motion) sensor](https://www.philips-hue.com/en-gb/p/hue-outdoor-sensor/8718699625474)
 * [Play light bar](https://www.philips-hue.com/en-gb/p/hue-white-and-colour-ambiance-play-light-bar-double-pack/7820230P7)
 * [White and colour ambiance (E14)](https://www.philips-hue.com/en-gb/p/hue-white-and-colour-ambiance-single-bulb-e14/8718696695166)
 * [White and colour ambiance (E27)](https://www.philips-hue.com/en-gb/p/hue-white-and-colour-ambiance-1-pack-e27/8718699673109#overview)
