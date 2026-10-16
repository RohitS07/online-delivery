---
id: US-0001
title: The API accepts browser calls only from configured origins
type: us
domain: platform
status: accepted
bpm: BPM-0001
actor: operator
constrained_by: [ADR-0001, ADR-0002, ADR-0003]
---

# US-0001 — The API accepts browser calls only from configured origins

**As** the operator who deploys the API **I want** the browser origins it accepts, and its HTTPS
redirect, to follow each environment's configuration **so that** the app can call it from its own
address, no other website can, and nothing travels unencrypted outside development.

Builds the API side of [BPM-0001](../bpm/BPM-0001-check-that-the-api-is-reachable.md), under
[ADR-0001](../adr/ADR-0001-browser-origins-allowed-by-the-api-come-from-configuration.md) and
[ADR-0002](../adr/ADR-0002-redirect-http-to-https-outside-development-only.md). The endpoint is
[SPEC-0001](../specs/SPEC-0001-health-check-endpoint.md). Tests follow [ADR-0003](../adr/ADR-0003-test-the-api-with-xunit-and-the-app-with-vitest.md).

## Acceptance criteria

| Id | Criterion | Verified by |
|---|---|---|
| `AC-0001-01` | Given the API runs, when a client sends `GET /api/v1/health`, then it answers `200` with the `HealthResponse` body of [SPEC-0001](../specs/SPEC-0001-health-check-endpoint.md) | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/HealthEndpointTests.cs::ReturnsSpecBody` |
| `AC-0001-02` | Given `Cors:AllowedOrigins` lists `http://localhost:5173`, when a request comes from that origin, then the answer allows that origin | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/CorsTests.cs::AllowedOriginGetsCorsHeader` |
| `AC-0001-03` | Given an origin that is not listed, when a request comes from it, then the answer carries no `Access-Control-Allow-Origin` header | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/CorsTests.cs::UnlistedOriginGetsNoCorsHeader` |
| `AC-0001-04` | Given an endpoint that requires authorization, when a listed origin sends a preflight `OPTIONS`, then the preflight succeeds with CORS headers instead of `401` | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/CorsTests.cs::PreflightToProtectedEndpointSucceeds` |
| `AC-0001-05` | Given `Cors:AllowedOrigins` is empty, when a request comes from any origin, then the answer carries no `Access-Control-Allow-Origin` header | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/CorsTests.cs::EmptyListAllowsNoOrigin` |
| `AC-0001-06` | Given the Production environment with an HTTPS port, when a client sends a plain HTTP request, then it is redirected to HTTPS | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/HttpsRedirectTests.cs::ProductionRedirectsHttpToHttps` |
| `AC-0001-07` | Given the Development environment, when a client sends a plain HTTP request, then it is served without a redirect | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/HttpsRedirectTests.cs::DevelopmentServesHttp` |
