[<- Back to Integrations README](../README.md) · [Packages README](../../README.md) · [Main README](../../../README.md)

# Messaging Platforms

Package for messaging and notification platform integrations.

## Overview

This package provides centralized notification delivery across multiple platforms including Slack, Discord, Telegram, and the Home Assistant mobile app.

## Quick Links

| Document | Purpose |
|----------|---------|
| [Integrations Overview](../README.md) | Overview of all integration packages |
| [Main Packages README](../../README.md) | Architecture and organization guidelines |

## Related Integrations

| Integration | Connection |
|-------------|------------|
| [Energy](../energy/README.md) | Solar forecast and battery notifications |
| [Transport](../transport/README.md) | Tesla charging rate notifications |
| [HVAC](../hvac/README.md) | Heating and hot water alerts |

## Notification Scripts

The messaging package provides standardized notification scripts used throughout the home automation:

- `script.send_to_home_log` - Log events to the home log
- `script.send_direct_notification` - Send priority notifications to mobile devices
- Platform-specific notification services for Slack, Discord, Telegram
