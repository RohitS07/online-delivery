---
id: US-0002
title: A visitor sees one clear API status
type: us
domain: platform
status: review
bpm: BPM-0001
actor: visitor
constrained_by: [ADR-0003]
---

# US-0002 — A visitor sees one clear API status

**As** a visitor opening the app **I want** to see one clear status for the API, styled like the
rest of the app **so that** I know whether the app can work, and am never left waiting.

Builds the app side of [BPM-0001](../bpm/BPM-0001-check-that-the-api-is-reachable.md), against
[SPEC-0001](../specs/SPEC-0001-health-check-endpoint.md), within the time limit in
[NFR-0001](../nfr/NFR-0001-api-requests-from-the-app-time-out.md). Tests follow
[ADR-0003](../adr/ADR-0003-test-the-api-with-xunit-and-the-app-with-vitest.md).

## Acceptance criteria

| Id | Criterion | Verified by |
|---|---|---|
| `AC-0002-01` | Given the API has not answered yet, when the app loads, then it shows only "Checking the API…" | `test:online-delivery-app/src/components/ApiStatus.test.jsx::showsOnlyCheckingWhileWaiting` |
| `AC-0002-02` | Given the API answers with `status: healthy`, when the answer arrives, then the app shows only "API is healthy" | `test:online-delivery-app/src/components/ApiStatus.test.jsx::showsOnlyHealthyWhenApiAnswers` |
| `AC-0002-03` | Given the API answers with an error or cannot be reached, when the request fails, then the app shows only "Unable to reach the API" | `test:online-delivery-app/src/components/ApiStatus.test.jsx::showsOnlyUnreachableWhenRequestFails` |
| `AC-0002-04` | Given the API never answers, when the time limit of [NFR-0001](../nfr/NFR-0001-api-requests-from-the-app-time-out.md) passes, then the app shows only "Unable to reach the API" | `test:online-delivery-app/src/components/ApiStatus.test.jsx::showsUnreachableAfterTimeout` |
| `AC-0002-05` | Given the shared API client, when it is created, then its timeout is 10 seconds | `test:online-delivery-app/src/services/apiClient.test.js::timesOutAfterTenSeconds` |
| `AC-0002-06` | Given `VITE_API_URL` is not set, when the app checks the API, then no request is sent and the app shows only "Unable to reach the API: VITE_API_URL is not set" | `test:online-delivery-app/src/components/ApiStatus.test.jsx::namesMissingApiUrl` |
| `AC-0002-07` | Given the app's stylesheet, when it is loaded, then it imports Tailwind CSS and none of the Vite demo theme | `test:online-delivery-app/src/styles.test.js::loadsTailwindWithoutDemoTheme` |
