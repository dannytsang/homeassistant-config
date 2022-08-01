# Danny's Home Assistant 🏡
[![Home Assistant CI](https://github.com/dannytsang/homeassistant-config/actions/workflows/main.yml/badge.svg)](https://github.com/dannytsang/homeassistant-config/actions/workflows/main.yml)
<a href="https://twitter.com/DannyTsang" target="_blank"><img src="https://img.shields.io/twitter/follow/DannyTsang?color=blue&style=plastic"/></a>

# Introduction 📢
My ⚽goal with home automation is to never have to think about doing something mentally or physically. This can be turning on a 💡light through to household chores such as 👕washing clothes. Currently, my journey continues.

I have always been interested in technology starting from the x10 days. At the time, I was did not have the money or 🧬life experience to use the 💻technology at the time. Fast forward a few 📅decades, I'm fortunate enough to have the means and place to splurge on home automtion and [Home Assistant](https://home-assistant.io) is the key to all of this.

This project contains configuration files for [Home Assistant](https://home-assistant.io) used in the House of Tsang 曾)

More details to follow. Visit my 📜[blog](https://dannytsang.co.uk).

## Statistics 📊
I have 2425 states (📈143) in Home Assistant. More details [here](statistics.md).

# Hardware 🔩
More details [here](hardware.md).

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
More details [here](integrations.md).

# GitHub 🐱🐙
This repository contains the configuration files used. It will not contain everything e.g. password (A.K.A secrets.yaml) file as well as other configuration done in the User Interface (UI).

Whilst [Home Assistant](https://home-assistant.io) offer backup solution, it is a bit of all or nothing restore process whereas Git (or any versioning system) would allow incremental changes to be stored and reverted where necessary.

The goal is to use the web front end as much as possible and there has been a growing trend to move away from text (YAML) files however the version advantage is the reason i still use and store things here.

## Setup ⚙️
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

### Blueprints 📝
I have yet to explore this feature yet. See [here](https://github.com/dannytsang/homeassistant-config/issues/9).

### Camera 📸
Private directory to hold camera images. Predominantly used for sending images to [DeepStack](https://deepstack.cc/).

### ESPHome 🔌
Files related to managing the ESP microcontroller. See [ESPHome.io](https://esphome.io/) for more details.

### Packages 📦
See [packages readme](packages/README.md) for more details.

### Split Configurations 📦🪓
I use split configuration files to help manage and keep the `configuration.yaml` size down. The advantange is each type of configuration such as scripts, scenes, etc will be managed by [Home Assistant](https://home-assistant.io) UI with minimal setup.

### www 🌍
A public folder for holding any files such as images that does not need authentication. I use it for attaching images to notifications.

## Tags / Releases 🏷️
I will apply a tag before upgrading to a major/minor/monthly release of [Home Assistant](https://home-assistant.io). These will represent a snapshot of a (hopefully) stable configuration used prior to upgrading and a point to restore back to if needed.

# Miscellaneous 🦺
I tried the [Conbee II](https://phoscon.de/en/conbee2) USB stick and it was good however it was tied to a computer running Deconz which makes it harder to put in the house in a central location compared to the a hub like [Philips Hue](#controllers) or [SmartThings](#controllers).
