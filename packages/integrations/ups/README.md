[<- Back to Integrations README](../README.md) · [Packages README](../../README.md) · [Main README](../../../README.md)

# UPS — Uninterruptible Power Supply Monitoring

*Last updated: 2026-04-05*

Monitors six UPS units via the Network UPS Tools (NUT) integration. Sends direct notifications on error or warning conditions and logs recovery when power is restored. Template sensors calculate real-time power draw in watts for each unit.

Integration reference: <https://www.home-assistant.io/integrations/nut/>

---

## Automations

| Name | ID | Trigger | Conditions | Action |
|---|---|---|---|---|
| UPS: Status Change | `1591963855737` | Any monitored UPS status sensor → `unavailable` | None | Choose action based on status value (see below) |

### Status Change Logic

| Status Value(s) | Severity | Response |
|---|---|---|
| `OB DISCHRG`, `OL OFF`, `ALARM OL RB` | Error | `script.send_direct_notification` — push alert |
| `unavailable`, `OB DISCHRG`, `OL OFF`, `ALARM OL RB` | Warning | `script.send_to_home_log` — log entry |
| `OL CHRG` | Recovery | `script.send_direct_notification` — success notification |
| `OL` | Normal | `script.send_to_home_log` — log entry |

---

## Template Sensors

Each sensor calculates real power using the formula:

```
power_watts = (load_percent / 100) × nominal_real_power
```

Sensors return `0` W when the UPS is not in an `OL` or `OL CHRG` state.

| Sensor Name | Unique ID | Source Entities | Nominal Power |
|---|---|---|---|
| 3D Printer UPS Power | `31406205-681f-472d-8be1-a7908383de89` | `sensor.threedprinterups_load`, `sensor.threedprinterups_status` | 405 W (hardcoded) |
| Family Computer UPS Power | `b2271d4a-7456-49b8-9530-7595fdbb6caf` | `sensor.familycomputerups_load`, `sensor.familycomputerups_nominal_real_power` | Dynamic |
| Kitchen UPS Power | `aad5419d-c50d-41db-a170-0f1419a4842c` | `sensor.kitchen_ups_load`, `sensor.kitchen_ups_nominal_real_power` | Dynamic |
| Living Room UPS Power | `b34e6d2e-8a46-489a-afcb-551a0e4b9f0a` | `sensor.lounge_ups_load`, `sensor.lounge_ups_nominal_real_power` | Dynamic |
| Office UPS Power | `64c705e9-619e-4cfd-9e97-fa722556041e` | `sensor.computer_ups_load`, `sensor.computer_ups_nominal_real_power` | Dynamic |
| Server UPS Power | `6868a338-192a-4f68-949a-9157b434ec4f` | `sensor.server_ups_load`, `sensor.server_ups_nominal_real_power` | Dynamic |

All sensors have `device_class: power`, `unit_of_measurement: W`, `state_class: measurement`.

---

## Monitored Status Entities

| Friendly Name | Status Entity |
|---|---|
| Living Room UPS | `sensor.lounge_ups_status_data` |
| Office (Computer) UPS | `sensor.computer_ups_status` |
| Server UPS | `sensor.server_ups_status_data` |
| 3D Printer UPS | `sensor.threedprinterups_status_data` |
| Family Computer UPS | `sensor.familycomputerups_status_data` |

---

## Dependencies

- NUT integration — provides all `sensor.*_ups_*` entities
- `script.send_direct_notification` — push notifications
- `script.send_to_home_log` — structured logging
