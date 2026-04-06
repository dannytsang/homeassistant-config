[<- Back to Integrations README](README.md) · [Packages README](../README.md) · [Main README](../../README.md)

# Paperless-NGX Document Management

*Last updated: 2026-04-05*

Receives webhook events from Paperless-NGX when new documents are added and monitors the inbox document count via the REST API.

## Entities

| Entity | Type | Poll interval | Description |
|--------|------|---------------|-------------|
| `sensor.paperless_ngx_inbox_count` | REST sensor | 5 minutes | Number of documents currently awaiting action in the Paperless-NGX inbox |

## Automations

| Automation | Trigger | Mode | Description |
|------------|---------|------|-------------|
| Paperless: New Document | Webhook `POST` | Queued (max 10) | Sends a notification to `person.danny` with the document ID, name, correspondent, tags, and download URL |

### Webhook Payload Fields Used

| Field | Used for |
|-------|----------|
| `id` | Document ID included in notification |
| `name` | Document title |
| `correspondent` | Sender / correspondent name |
| `download_url` | Direct download link in notification |
| `tags` | Tag list appended to notification body |

## Notes

- The webhook accepts `POST` requests and is not restricted to local-only connections, allowing Paperless-NGX to call it from any network location.
- Credentials for the REST sensor (`paperless_inbox_url` and `paperless_inbox_token`) are stored in `secrets.yaml`.
- Reference implementation: <https://flemmingss.com/monitoring-paperless-ngx-in-home-assistant/>
