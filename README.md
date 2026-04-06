# Danny's Home Assistant 🏡
This repository contains my personal Home Assistant configuration for automating and monitoring my smart home environment. It covers lights, sensors, automations, integrations, and more.

[![Home Assistant CI](https://github.com/dannytsang/homeassistant-config/actions/workflows/push.yml/badge.svg)](https://github.com/dannytsang/homeassistant-config/actions/workflows/push.yml)
<a href="https://twitter.com/DannyTsang" target="_blank"><img src="https://img.shields.io/twitter/follow/DannyTsang?color=blue&style=plastic"/></a>
![GitHub repo size](https://img.shields.io/github/repo-size/dannytsang/homeassistant-config)
![GitHub last commit](https://img.shields.io/github/last-commit/dannytsang/homeassistant-config)
![GitHub stars](https://img.shields.io/github/stars/dannytsang/homeassistant-config?style=social)

## Table of Contents

- [Introduction](#introduction-)
- [Documentation Index](#documentation-index-)
- [Hardware](#hardware-)
- [Addons](#addons-)
- [Integrations](#integrations-)
- [GitHub](#github-)
- [Miscellaneous](#miscellaneous-)

---

## Documentation Index 📚

Quick reference to all documentation in this repository, sorted by category.

### Core Documentation

| Document | Description | Last Updated |
|----------|-------------|--------------|
| [README.md](README.md) | This file — project overview and navigation | 2026-04-01 |
| [INSTALL.md](INSTALL.md) | Installation and setup instructions | 2026-04-01 |
| [hardware.md](hardware.md) | Complete hardware inventory by manufacturer | 2026-04-01 |
| [statistics.md](statistics.md) | Entity counts and system statistics | 2026-04-01 |

### Package Documentation

| Category | Document | Description | Last Updated |
|----------|----------|-------------|--------------|
| **Packages** | [packages/README.md](packages/README.md) | Package architecture and organization | 2026-04-01 |
| **Rooms** | [packages/rooms/README.md](packages/rooms/README.md) | Room-based configuration overview | 2026-04-01 |
| **Integrations** | [packages/integrations/README.md](packages/integrations/README.md) | Integration packages overview | 2026-04-01 |

### Room Documentation

| Room | README | Setup Guide | Last Updated |
|------|--------|-------------|--------------|
| Attic | [README](packages/rooms/attic_README.md) | — | 2026-03-29 |
| Back Garden | [README](packages/rooms/back_garden_README.md) | — | 2026-03-29 |
| Bathroom | [README](packages/rooms/bathroom_README.md) | — | 2026-03-29 |
| Bedroom | [README](packages/rooms/bedroom/README.md) | [SETUP](packages/rooms/bedroom/BEDROOM-SETUP.md) | 2026-04-01 |
| Bedroom 2 | [README](packages/rooms/bedroom2_README.md) | — | 2026-03-29 |
| Bedroom 3 | [README](packages/rooms/bedroom3_README.md) | — | 2026-03-29 |
| Conservatory | [README](packages/rooms/conservatory/README.md) | — | 2026-04-01 |
| Front Garden | [README](packages/rooms/front_garden_README.md) | — | 2026-03-29 |
| Kitchen | [README](packages/rooms/kitchen/README.md) | [SETUP](packages/rooms/kitchen/KITCHEN-SETUP.md) | 2026-04-01 |
| Living Room | [README](packages/rooms/living_room/README.md) | [SETUP](packages/rooms/living_room/LIVING-ROOM-SETUP.md) | 2026-04-01 |
| Office | [README](packages/rooms/office/README.md) | [SETUP](packages/rooms/office/OFFICE-SETUP.md) | 2026-04-01 |
| Porch | [README](packages/rooms/porch/README.md) | [SETUP](packages/rooms/porch/PORCH-SETUP.md) | 2026-04-01 |
| Stairs | [README](packages/rooms/stairs/README.md) | [SETUP](packages/rooms/stairs/STAIRS-SETUP.md) | 2026-04-01 |
| Utility | [README](packages/rooms/utility_README.md) | — | 2026-03-31 |

### Integration Documentation

| Integration | Document | Description | Last Updated |
|-------------|----------|-------------|--------------|
| **Energy (Core)** | [README](packages/integrations/energy/README.md) | Solar, battery, grid monitoring | 2026-04-01 |
| **Octopus Energy** | [README](packages/integrations/energy/octopus_energy_README.md) | Agile tariff integration | 2026-04-01 |
| **Predbat** | [README](packages/integrations/energy/predbat_README.md) | Battery optimization | 2026-04-01 |
| **Solcast** | [README](packages/integrations/energy/solcast_README.md) | Solar forecasting | 2026-04-01 |
| **Solar Assistant** | [README](packages/integrations/energy/solar_assistant_README.md) | Inverter monitoring | 2026-04-01 |
| **Zappi** | [README](packages/integrations/energy/zappi_README.md) | EV charger integration | 2026-04-01 |
| **Alarm** | [README](packages/integrations/alarm_README.md) | House alarm system | 2026-04-01 |
| **HVAC** | [README](packages/integrations/hvac/README.md) | Heating and climate control | 2026-04-01 |
| **Messaging** | [README](packages/integrations/messaging/README.md) | Notifications (Slack, Discord, Telegram) | 2026-04-01 |
| **Transport** | [README](packages/integrations/transport/README.md) | Tesla/TeslaMate integration | 2026-04-01 |
| **Google Travel** | [README](packages/integrations/transport/google_travel_README.md) | Travel time estimates | 2026-04-01 |

---

## Introduction 📢
My ⚽goal with home automation is to never have to think about doing something mentally or physically. This can be turning on a 💡light through to household chores such as 👕washing clothes. Currently, my journey continues.

I have always been interested in technology starting from the x10 days. At the time, I did not have the money or 🧬life experience to use the 💻technology at the time. Fast forward a few 📅decades, I'm fortunate enough to have the means and place to splurge on home automation and [Home Assistant](https://home-assistant.io) is the key to all of this.

This project contains configuration files for [Home Assistant](https://home-assistant.io) used in the House of Tsang 曾)

More details on my 📜[website](https://dannytsang.com).

> ⚠️ **Note:** This configuration is highly specific to my environment. Some parts may not work without adaptation.

### Statistics 📊
I have 7,191 states in Home Assistant. More details [here](statistics.md).

## Hardware 🔩
More details [here](hardware.md).

## Addons ➕
This is not an exhaustive list and it changes quite a lot. Too keep up to date, please subscribe to my [blog](https://dannytsang.com).
* [ESPHome](https://esphome.io/)
* [Git pull](https://github.com/home-assistant/addons/tree/master/git_pull)
* [Home Assistant Google Drive Backup](https://github.com/sabeechen/hassio-google-drive-backup)
* [Log Viewer](https://github.com/hassio-addons/addon-log-viewer)
* [Ring Device Integration via MQTT](https://github.com/tsightler/ring-mqtt-ha-addon)
* [Visual Studio Code](https://github.com/hassio-addons/addon-vscode)

Add-ons that I run outside of Home Assistant:
* [EMQX](https://github.com/hassio-addons/addon-emqx)
* [Grafana](https://github.com/hassio-addons/addon-grafana)
* [Zigbee2MQTT](https://github.com/zigbee2mqtt/hassio-zigbee2mqtt)

## Integrations 🖧
More details [here](/packages/integrations/README.md).

## GitHub 🐱🐙
This repository contains the configuration files used. It will not contain everything e.g. password (A.K.A secrets.yaml) file as well as other configuration done in the User Interface (UI).

Whilst [Home Assistant](https://home-assistant.io) offer backup solution depending on your install, it is a bit of all or nothing restore process whereas Git (or any versioning system) would allow incremental changes to be stored and reverted where necessary.

The goal is to use the web front end as much as possible and there has been a growing trend to move away from text (YAML) files however the versioning advantage is the reason i still use and store things here.

### Setup ⚙️
All changes are performed in the UI where possible and if they are held in configuration files then it will end up in Git where possible.

I use the Visual Studio Code add-on to edit files in [Home Assistant](https://home-assistant.io) or if I really have to the File Editor add-on on my mobile devices.

Visual Studio Code addon includes a Git client so all changes are managed through the text editor.

### Workflows 🖇️
The advantage of using a source code management system like Git is the ability to use hooks to trigger actions (as well as other advantages).

I use GitHub actions to verify the changes committed by running it against [Home Assistant](https://home-assistant.io) builds. If successful, [Home Assistant](https://home-assistant.io) will pull down the changes and if the changes are configuration related (as opposed to readme / markdown files) then it will perform another local configuration check and restart to pick up the changes. More details on this can be found [here](https://dannytsang.com/home-assistant-continuous-integration-workflow-2023/)

For this reason, the `custom_components` is stored in the repository to allow a successful build and configuration check.

### Folder Structure 📂
This repository's top level is the /config folder where typically the configuration.yaml file resides. More details can be found [here](https://www.home-assistant.io/docs/configuration/).

I use some of the "advance" configuration options such as [split configuration](https://www.home-assistant.io/docs/configuration/splitting_configuration/) and [packages](https://www.home-assistant.io/docs/configuration/packages/).


```
packages/               # See README.md in folder
  └── integrations/     # Integration based YAML files
  └── rooms/            # Room based YAML files
blueprints/             # Blueprints for automations
camera/                 # Private directory to hold camera images
esphome/                # Files related to managing the ESP micro controller
lovelace/               # Dashboard configs
scripts/                # Automation scripts
www/                    # A public folder for holding any files such as images that does not need authentication
automations.yaml        # UI automation file
configurations.yaml     # Home Assistant's main configuration file
scene.yaml              # UI scene file
script.yaml             # UI script file
```

### Tags / Releases 🏷️
I will apply a tag around the time of upgrading to a monthly release of [Home Assistant](https://home-assistant.io). These will represent a snapshot of a (hopefully) stable configuration used prior to upgrading and a point to restore back to if needed. The `main` branch will contain the latest changes so there is no *latest* tag.

I encountered issues with branching using VSCode Server add-on in Home Assistant. I was always switching away from a branch so I generally stay away from using this method.
