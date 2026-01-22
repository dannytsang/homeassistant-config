# Home Assistant Hardware & Infrastructure

**Last Updated:** 2026-01-22
**Scope:** Network, Power, Networking, ESPHome Devices

---

## Network & Core Infrastructure

### Networking
- **Ubiquiti Unifi Dream Machine Pro** (network hub, NVR)
- **Aruba networking** (replaced Unifi for PPSK controllerless setup)
- **SMLIGHT SLZB-06** (Zigbee hub)
- Multiple Unifi switches with PoE

### Power Infrastructure
- **3 UPS systems** (Living Room, Server, Computer) with battery runtime monitoring
- **Shelly switches** (EM, Plus 1PM, Plus 1PM Mini)
- **TP-Link Kasa Smart plugs** (HS110, KP115, KP303)
- **Sonoff USB adapters** (WiFi and Zigbee variants)
- **Samsung SmartThings plugs** (power monitoring)

---

## ESPHome Custom Devices (13 devices)

### Occupancy & Presence Detection
- **bed.yaml** - 4-point ADS1115 pressure sensors + BME680 air quality
  - Custom IAQ calculation: `log(gas_resistance) + 0.04 * humidity`
- **ashlees-bed.yaml** - Ashlee's bedroom sensors
- **leos-bed.yaml** - Leo's bedroom sensors
- **bathroom-motion.yaml** - Motion detection
- **conservatory-motion.yaml** - Conservatory motion
- **living-room-motion.yaml** - Living room occupancy
- **everything-presence-one/lite** - mmWave presence detection
- **apollo-r-pro-1-eth-ef755c.yaml** - Multi-sensor device

### Monitoring Devices
- **office.yaml** - Office environment sensors
- **boiler.yaml** - Boiler monitoring
- **central-heating.yaml** - Heating control
- **water-softener.yaml** - Water softener status

### Common Packages
- `esp32-base.yaml` - ESP32 configuration
- `bluetooth-base.yaml` - Bluetooth support

---

## Specialized Devices & Integrations

### Personal Devices
- **Garmin Epix Pro Gen 2** (smartwatch sync)
- **Oral-B Electric Toothbrush** (Bluetooth)

### Kitchen & Cooking
- **MEATER Plus** (meat thermometer)
- Fridge/freezer temperature alerts

### Maker & Hobbies
- **3D Printer monitoring** via OctoPrint
  - Print started → log + turn on light
  - 50% complete → notification
  - Finished → notification + turn off light
  - Paused mid-print → alert
  - **Left unattended → immediate alert** (runs when no one home)

### Weather
- **Ecowitt Wittboy** weather station

### IR/RF Control
- **Broadlink RM4 Pro** (IR/RF remote replacement)

---

## Custom Components & Extensions

1. **alexa_media** (v5.9.0) - Alexa Media Player integration (alandtse)
2. **myenergi** (CJNE/ha-myenergi) - Zappi EV charger and Eddi diverter
3. **llmvision** - LLM-based vision/AI integration
4. **retry** - Retry logic for unreliable devices
5. **delete** - File deletion integration
