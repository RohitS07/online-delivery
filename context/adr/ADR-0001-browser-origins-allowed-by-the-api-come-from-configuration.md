---
id: ADR-0001
title: Browser origins allowed by the API come from configuration
type: adr
status: review
---

# ADR-0001 — Browser origins allowed by the API come from configuration

## Decision

The API allows cross-origin browser calls only from the origins listed in configuration, under
`Cors:AllowedOrigins`. Development lists `http://localhost:5173`. An empty list allows no browser origin.

## Why

- The app and the API run at different addresses in every environment, so the browser needs CORS to let the app call the API.
- Each environment has its own app address. Configuration changes per environment without a code change.
- Listing origins means another website cannot call the API from a visitor's browser.

## Instead of

- **Origins written in `Program.cs`.** This is how it works today. Every new environment would need a code change and a release.
- **Allow any origin.** Simple, but any site could call the API with a visitor's browser. That gets dangerous as soon as there is a login.
- **A Vite proxy in development, so no CORS is needed locally.** It hides CORS mistakes until production, where the app and the API are still at different addresses.

## Consequences

- Every deployed environment must set `Cors:AllowedOrigins`, or the app cannot reach the API from a browser.
- CORS must run before authorization in the API's pipeline. Otherwise a browser's preflight to a protected endpoint is refused before CORS can answer it.
- Origins are not secrets, so they may live in `appsettings.{Environment}.json`.
