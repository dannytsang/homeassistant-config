# /packages folder
Contains YAML files in a form of packages. See [here](https://www.home-assistant.io/docs/configuration/packages/#create-a-packages-folder) for more details.

The main reason I use packages is to better manage configurations from automations to sensors in a way that makes sense to me. This is at the detriment of being able to maange them from the UI (Lovelace). To help with this, I do move things from packages to UI supported files and back again.

The root folder contains files as a catch all for any files that do not fit the folder structure below.

### rooms
Configuration organised by rooms in the house. This is probably a bad way of organising files however it makes it easy for me to recall why things sit.
