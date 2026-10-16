# Roadmap — what is in scope, in build order

This file orders the in-scope work. Deferred work is in [BACKLOG.md](BACKLOG.md). Status lives on each artefact.
Work that is done is struck through here, and stays so the order is still readable.

## Phase 0 — First slice: the health check, end to end ([BPM-0001](bpm/BPM-0001-check-that-the-api-is-reachable.md))

[US-0001](stories/US-0001-the-api-accepts-browser-calls-only-from-configured-origins.md) comes first: [US-0002](stories/US-0002-a-visitor-sees-one-clear-api-status.md) needs an API the browser can call.

| Work | Artefacts |
|---|---|
| Test runners for both apps | [ADR-0003](adr/ADR-0003-test-the-api-with-xunit-and-the-app-with-vitest.md) |
| ~~API: CORS from configuration, HTTPS outside Development~~ | [US-0001](stories/US-0001-the-api-accepts-browser-calls-only-from-configured-origins.md), [SPEC-0001](specs/SPEC-0001-health-check-endpoint.md) |
| App: Tailwind loaded, API client with a time limit, one API status | [US-0002](stories/US-0002-a-visitor-sees-one-clear-api-status.md), [NFR-0001](nfr/NFR-0001-api-requests-from-the-app-time-out.md) |

## Open questions that change the order

- None yet. Accepting the three ADRs unblocks both stories.
