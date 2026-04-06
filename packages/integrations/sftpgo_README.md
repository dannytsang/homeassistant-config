[<- Back to Integrations README](README.md) · [Packages README](../README.md) · [Main README](../../README.md)

# SFTPGo File Server

*Last updated: 2026-04-05*

Provides a shell command wrapper for downloading files from an SFTPGo file server. Used by the UniFi Protect integration to fetch camera snapshot images for use in notifications.

Integration reference: <https://www.home-assistant.io/integrations/shell_command/>

## Shell Commands

| Command | Description |
|---------|-------------|
| `shell_command.download_unifi_image` | Downloads a file from SFTPGo via the SFTPGo REST API using `curl` |

### Parameters

The shell command is templated and accepts the following variables at call time:

| Variable | Description |
|----------|-------------|
| `password` | SFTPGo API password (passed at call time; not stored in this file) |
| `base_url` | Base URL of the SFTPGo instance |
| `share_id` | SFTPGo share identifier |
| `source_path` | Path of the file to download within the share (URL-encoded automatically) |
| `destination_path` | Local filesystem path to write the downloaded file to |

## Usage

This command is called by `unifi_protect.yaml` to retrieve camera snapshot images before sending them in notifications. The `source_path` value is URL-encoded and path-separator characters are additionally percent-encoded (`/` → `%2F`) to satisfy the SFTPGo API.

## Notes

- No credentials are hard-coded in this file; the `password` is supplied by the calling context.
- The `curl` call uses HTTP Basic authentication with an empty username (`-u ':{{ password }}'`).
