[<- Back](../README.md)
# Integrations 🖧

Integration-specific configuration organized by functional domain. Each package is self-contained — removing an integration only requires deleting its package file.

## Quick Links

| Category | Description | Documentation |
|----------|-------------|---------------|
| [Energy](energy/README.md) | Solar, battery, grid monitoring, EV charging, Octopus Agile | [README](energy/README.md) · [Solar Assistant](energy/solar_assistant_README.md) |
| [HVAC](hvac/README.md) | Heating, ventilation, air conditioning (Hive, Eddi) | [README](hvac/README.md) |
| [Messaging](messaging/README.md) | Notifications (Slack, Discord, Telegram, Mobile) | [README](messaging/README.md) |
| [Transport](transport/README.md) | Tesla vehicles (TeslaMate integration) | [README](transport/README.md) |

## HACS Integrations

An amazing community store for interfaces and integrations not available natively in [Home Assistant](https://home-assistant.io). [HACS](https://hacs.xyz/) plugs a hole where things not officially supported can be easily installed. Because it's community supported, use with caution.

### Notable HACS Integrations

| Integration | Purpose | Documentation |
|-------------|---------|---------------|
| **Frigate NVR** | Real-time video detection using TensorFlow | [GitHub](https://github.com/blakeblackshear/frigate-hass-integration) |
| **GlowMarkt** | Smart meter real-time data via API/MQTT | [Display and CAD](https://shop.glowmarkt.com/products/display-and-cad-combined-for-smart-meter-customers) |
| **hassio-ecoflow-cloud** | EcoFlow power station management | [GitHub](https://github.com/tolwi/hassio-ecoflow-cloud) |
| **TeslaMate** | Comprehensive Tesla vehicle telemetry via MQTT | [Docs](https://docs.teslamate.org/) |

### Native Integrations

| Integration | Purpose | Docs |
|-------------|---------|------|
| **Unifi** | Network-based presence detection | [Home Assistant](https://www.home-assistant.io/integrations/unifi/) |
| **CO2 Signal** | Carbon intensity data | [Home Assistant](https://www.home-assistant.io/integrations/co2signal/) |
| **Network UPS Tool** | UPS monitoring | [Home Assistant](https://www.home-assistant.io/integrations/nut/) |
| **Slack** | Notifications | [Home Assistant](https://www.home-assistant.io/integrations/slack/) |

## Related Documentation

- [Rooms](../rooms/README.md) - Room-specific configuration
- [Main Packages README](../README.md) - Overview of the packages architecture

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
* [Network UPS Tool](https://www.home-assistant.io/integrations/nut/)
* [Slack](https://www.home-assistant.io/integrations/slack/)
