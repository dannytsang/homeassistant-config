[<- Back](README.md)
# Integrations 🖧
There are too many to list and changes now and then so I will list the ones that will help explain configurations. These may include integrations from [HACS](https://hacs.xyz/).

## HACS
An amazing community store (almost) from interface to integrations not available natively in [Home Assistant](https://home-assistant.io). [HACS](https://hacs.xyz/) plugs a hole where things are not officially supported can be easily installed. Because it's community supported, use with caution.

## Frigate NVR
[Frigate](https://github.com/blakeblackshear/frigate-hass-integration) performs real time image/video detection using Google's TensorFlow machine learning technology. The key difference is the real time where it will take a stream from a camera and process it in real time. When it detects something, it will alert Home Assistant and you can do what you want with that state change / event.

## GlowMarkt
The [Display and CAD](https://shop.glowmarkt.com/products/display-and-cad-combined-for-smart-meter-customers) replaced the in home display provided by my energy provider and has the added benefit of direct smart meter "real time" data via API and MQTT for gas and electricity.

## Unifi
[Ubiquiti Unifi](https://www.home-assistant.io/integrations/unifi/) allows for network based presence detection. The advantage is the integration will poll for devices from the controller which would be aware of the network where as the UPnP integration relies on network scans instead.

Other noteworthy mentions:
* [CO2 Signal](https://www.home-assistant.io/integrations/co2signal/)
* [HASS-Deepstack-face](https://github.com/robmarkcole/HASS-Deepstack-face)
* [HASS-Deepstack-object](https://github.com/robmarkcole/HASS-Deepstack-object)
* [IFTTT](https://www.home-assistant.io/integrations/ifttt/)
* [Network UPS Tool](https://www.home-assistant.io/integrations/nut/)
* [Slack](https://www.home-assistant.io/integrations/slack/)
