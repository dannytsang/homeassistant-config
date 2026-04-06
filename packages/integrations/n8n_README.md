[<- Back to Integrations README](README.md) · [Packages README](../README.md) · [Main README](../../README.md)

# n8n — Workflow Automation Integration

*Last updated: 2026-04-05*

Provides shell command helpers used by other integrations to interact with n8n workflows and SFTPGo. Currently defines the command for deleting UniFi Protect camera snapshots from SFTPGo via an n8n webhook.

---

## Shell Commands

| Command | Description |
|---|---|
| `shell_command.delete_unifi_image` | Sends a `POST` request to an n8n webhook to delete a file from SFTPGo. Authenticates with `username`/`password` and passes `file_path` as JSON body to `webhook_url`. |

### `delete_unifi_image` Parameters

| Parameter | Description |
|---|---|
| `username` | SFTPGo credentials username |
| `password` | SFTPGo credentials password |
| `file_path` | Path of the file to delete in SFTPGo |
| `webhook_url` | n8n webhook URL that handles the delete operation |

> **Note:** This shell command is currently commented out in `unifi_protect.yaml` (pending implementation). It is defined here so it is available when the delete flow is enabled.

---

## Dependencies

- n8n — workflow automation platform; hosts the webhook that proxies the SFTPGo delete request
- SFTPGo — file transfer server storing camera snapshots (see `sftpgo.yaml`)
- `input_text.n8n_delete_sftpgo_unifi_share_file_webhook_url` — the n8n webhook URL used by `delete_unifi_image`
- `unifi_protect.yaml` — consumer of the delete command (currently pending)
