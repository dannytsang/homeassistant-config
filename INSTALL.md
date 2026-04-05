[<- Back to README](README.md)

## Installation

### Prerequisites

- A running [Home Assistant](https://home-assistant.io) instance (OS, Container, or Supervised)
- Git installed on the host (or use the [Git pull add-on](https://github.com/home-assistant/addons/tree/master/git_pull))
- A text editor add-on such as [Visual Studio Code](https://github.com/hassio-addons/addon-vscode) or File Editor

### Steps

1. Clone this repository into your Home Assistant config folder:
    ```
    git clone https://github.com/dannytsang/homeassistant-config.git .
    ```

2. Create your `secrets.yaml` from the provided sample:
    ```
    cp secrets.yaml.sample secrets.yaml
    ```
    Then fill in your own values (API keys, passwords, entity IDs specific to your setup).

3. Review `configuration.yaml` and any package files that reference environment-specific entities (device IDs, IP addresses, person names) and update them to match your environment.

4. Restart Home Assistant to load the new configuration.

### Post-Installation

- On the next `git push`, the [GitHub Actions CI workflow](README.md#workflows-️) will run a configuration check against a Home Assistant build. If the check passes, Home Assistant will pull down the changes and perform a local configuration check before restarting.
- The `custom_components` directory is included in this repository to allow CI to pass without additional setup.

> ⚠️ **Note:** This configuration is tailored to a specific home environment. Many automations and integrations will need adjustment before they work in a different setup.
