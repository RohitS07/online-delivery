---
id: SPEC-0001
title: Health check endpoint
type: spec
domain: platform
status: review
bpm: BPM-0001
constrained_by: [ADR-0001, ADR-0002]
---

# SPEC-0001 — Health check endpoint

`GET /api/v1/health`. No request body, no authentication. Answers `200 OK` with a `HealthResponse`.

```json
{ "status": "healthy", "service": "online-delivery-api", "timestamp": "2026-10-16T09:30:00Z" }
```

## Entities

| Entity | Holds | Key |
|---|---|---|
| `HealthResponse` | `status`: always `healthy` when the API answers. `service`: always `online-delivery-api`. `timestamp`: the server's current time, UTC, ISO 8601 | none, it is not stored |

## Rules

- The response is a `HealthResponse` DTO, not an anonymous object. JSON property names are camelCase.
- `healthy` means the API process is up and answering. It does not check the database yet.
- Browser calls follow [ADR-0001](../adr/ADR-0001-browser-origins-allowed-by-the-api-come-from-configuration.md); the transport follows [ADR-0002](../adr/ADR-0002-redirect-http-to-https-outside-development-only.md).

## Must never

- Require authentication. It is the check that runs before anything else works.
- Reveal the host name, version, environment, configuration or any secret.
- Redirect in Development.
