[<- Back to Integrations README](README.md) · [Packages README](../README.md) · [Main README](../../README.md)

# OwnTracks

Publishes Home Assistant device tracker locations to MQTT in OwnTracks format for Danny, Terina, and Leo.

---

## Overview

Three automations mirror each family member's device tracker state to MQTT whenever their location changes. This allows OwnTracks-compatible apps and services to consume location data sourced from Home Assistant (e.g. for timeline history). See the [inspiration post](https://devblog.yvn.no/posts/replacing-maps-timeline-with-owntracks/) for background.

---

## Automations

| ID | Alias | Device Tracker | MQTT Topic |
|----|-------|---------------|------------|
| `1744064001680` | People: Update Danny's Owntracks | `device_tracker.danny_s_phone` | `owntracks/danny/iphone` |
| `1744064001681` | People: Update Terina's Owntracks | `device_tracker.oneplus_10` | `owntracks/terina/oneplus` |
| `1744064001682` | People: Update Leo's Owntracks | `device_tracker.leos_iphone` | `owntracks/leo/iphone` |

All three automations run in `single` mode and publish a retained MQTT message on every state change.

### Published payload fields

Each message is an OwnTracks `location` type with the following fields sourced from the device tracker attributes:

| Field | Source attribute | Default |
|-------|-----------------|---------|
| `lat` | `latitude` | — |
| `lon` | `longitude` | — |
| `alt` | `altitude` | `0` |
| `vac` | `vertical_accuracy` | `0` |
| `acc` | `gps_accuracy` | `0` |
| `vel` | `speed` | `0` |
| `cog` | `course` | `0` |
| `tst` | `now().timestamp()` | — |

---

## Entities

| Entity | Description |
|--------|-------------|
| `device_tracker.danny_s_phone` | Danny's iPhone device tracker |
| `device_tracker.oneplus_10` | Terina's OnePlus device tracker |
| `device_tracker.leos_iphone` | Leo's iPhone device tracker |

---

## Dependencies

- **Integration:** MQTT (broker)
- Messages are published with `retain: true`

---

*Last updated: 2026-04-05*
