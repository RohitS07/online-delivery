---
id: BPM-0001
title: Check that the API is reachable
type: bpm
domain: platform
status: accepted
actors: [visitor, app, API]
triggers: [the visitor opens the app]
constrained_by: [ADR-0001, ADR-0002]
stories: [US-0001, US-0002]
---

# BPM-0001 — Check that the API is reachable

## Purpose

The visitor sees whether the app can reach the API, before any feature depends on it.

## Flow

1. The visitor opens the app. The app shows that it is checking the API.
2. The app reads the API address from its configuration.
3. The app asks the API for its health, as [SPEC-0001](../specs/SPEC-0001-health-check-endpoint.md) defines, within the time limit in [NFR-0001](../nfr/NFR-0001-api-requests-from-the-app-time-out.md).
4. The API accepts the call only if the app's address is an allowed origin ([ADR-0001](../adr/ADR-0001-browser-origins-allowed-by-the-api-come-from-configuration.md)), and only over HTTPS outside Development ([ADR-0002](../adr/ADR-0002-redirect-http-to-https-outside-development-only.md)).
5. The app replaces "checking" with exactly one result: healthy, or unreachable.

## Decision points

- Is the API address configured? If not, the app shows unreachable and names the missing setting, without making a call.
- Is the app's origin allowed? If not, the browser blocks the answer and the app shows unreachable.
- Did the API answer in time, with a healthy status? If not, the app shows unreachable.

## Failure modes

- The API address is missing from the app's configuration.
- The API is down, or its address is wrong.
- The app's origin is not in the API's allowed list.
- The API does not answer within the time limit.
- The API answers with an error status.

## Outcome

The visitor sees one state at a time: checking, healthy or unreachable. Never two at once, and never stuck on checking.
