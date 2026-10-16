---
id: ADR-0002
title: Redirect HTTP to HTTPS outside Development only
type: adr
status: implemented
---

# ADR-0002 — Redirect HTTP to HTTPS outside Development only

## Decision

Outside the Development environment, the API redirects every plain HTTP request to HTTPS. In
Development it serves plain HTTP on `http://localhost:5154` and does not redirect.

## Why

- Phone numbers, one-time passwords and orders must never cross a network unencrypted.
- The redirect is in the API's own code, where review and tests can see it, not only in a hosting setting.
- Locally, the app calls `http://localhost:5154`. A redirect there would send it to a second port with a development certificate, which breaks the browser call.

## Instead of

- **Redirect in every environment.** This is how the code started. It breaks the local HTTP setup, which is why the line is commented out today.
- **Never redirect, and rely on Azure's "HTTPS only" setting.** That setting lives outside the repository. It can be switched off or missed in a new environment, and nothing in the code would notice.

## Consequences

- Each environment outside Development must know its HTTPS port, or the redirect cannot happen.
- Where a proxy ends TLS in front of the API, as Azure App Service does, the API must read the original scheme from forwarded headers. Otherwise it treats HTTPS requests as HTTP and redirects them again. To be checked against the Azure documentation when hosting is set up.
- Local development traffic is unencrypted. It stays on `localhost`.
