# Roadmap — what is in scope, in build order

This file orders the in-scope work. Deferred work is in [BACKLOG.md](BACKLOG.md). Status lives on each artefact.
Work that is done is struck through here, and stays so the order is still readable.

## Phase 0 — First slice: the health check, end to end ([BPM-0001](bpm/BPM-0001-check-that-the-api-is-reachable.md))

[US-0001](stories/US-0001-the-api-accepts-browser-calls-only-from-configured-origins.md) comes first: [US-0002](stories/US-0002-a-visitor-sees-one-clear-api-status.md) needs an API the browser can call.

| Work | Artefacts |
|---|---|
| ~~Test runners for both apps~~ | [ADR-0003](adr/ADR-0003-test-the-api-with-xunit-and-the-app-with-vitest.md) |
| ~~API: CORS from configuration, HTTPS outside Development~~ | [US-0001](stories/US-0001-the-api-accepts-browser-calls-only-from-configured-origins.md), [SPEC-0001](specs/SPEC-0001-health-check-endpoint.md) |
| ~~App: Tailwind loaded, API client with a time limit, one API status~~ | [US-0002](stories/US-0002-a-visitor-sees-one-clear-api-status.md), [NFR-0001](nfr/NFR-0001-api-requests-from-the-app-time-out.md) |

## Phase 1 — Foundation for the village delivery platform

From [the source specification](delivery-service-specification.md). The processes are
[BPM-0002](bpm/BPM-0002-a-customer-orders-from-the-village-agent.md), [BPM-0003](bpm/BPM-0003-an-agent-runs-the-daily-stock-and-delivery-cycle.md),
[BPM-0004](bpm/BPM-0004-an-admin-manages-master-data-agents-and-settings.md) and [BPM-0005](bpm/BPM-0005-a-person-signs-up-or-signs-in-with-a-mobile-number.md).
[US-0003](stories/US-0003-the-app-is-written-in-typescript-and-still-shows-the-api-status.md) comes first, so nothing new is written in JavaScript.
[US-0007](stories/US-0007-a-person-reads-the-app-in-english-or-marathi.md) comes before [US-0006](stories/US-0006-a-person-signs-in-and-lands-in-the-area-for-their-role.md), so no screen is built with fixed text.

| Work | Artefacts |
|---|---|
| App: convert to strict TypeScript | [US-0003](stories/US-0003-the-app-is-written-in-typescript-and-still-shows-the-api-status.md), [ADR-0005](adr/ADR-0005-write-the-app-in-typescript.md) |
| API: database, migrations, and the cities, villages and categories | [US-0004](stories/US-0004-anyone-can-list-the-active-cities-villages-and-categories.md), [SPEC-0002](specs/SPEC-0002-cities-villages-and-categories.md), [ADR-0004](adr/ADR-0004-store-data-in-postgresql-through-ef-core-with-migrations.md) |
| API: OTP sign-in and tokens | [US-0005](stories/US-0005-a-person-proves-their-mobile-number-and-gets-a-token.md), [SPEC-0003](specs/SPEC-0003-sign-in-with-a-mobile-otp.md), [ADR-0006](adr/ADR-0006-sign-in-with-a-mobile-otp-and-a-jwt-bearer-token.md), [ADR-0007](adr/ADR-0007-business-dates-and-times-are-in-india-standard-time-from-an-injected-clock.md), [ADR-0009](adr/ADR-0009-outside-providers-sit-behind-interfaces-with-mocks-first.md) |
| App: English and Marathi | [US-0007](stories/US-0007-a-person-reads-the-app-in-english-or-marathi.md), [ADR-0010](adr/ADR-0010-the-app-shows-text-in-english-and-marathi-and-the-api-sends-codes.md) |
| App: sign-in, role routing and the three area shells | [US-0006](stories/US-0006-a-person-signs-in-and-lands-in-the-area-for-their-role.md) |

## Next phases — no ids yet

Ids are allocated when each phase is authored. [ADR-0008](adr/ADR-0008-work-out-the-daily-order-window-from-the-clock-with-no-scheduled-job.md) constrains phases 4 to 7.

1. Phase 2 — Onboarding: customer and agent sign-up, admin approves agents.
2. Phase 3 — Admin settings: open and close times, fees, holidays, village delivery hours.
3. Phase 4 — Agent daily stock: enter and update before the open time, pick earlier items.
4. Phase 5 — Customer browse and cart.
5. Phase 6 — Checkout: saved mock payment method, Pay Now, order confirmation, cancel and refund.
6. Phase 7 — Orders: customer history, agent daily list, status updates, in-app notifications.
7. Phase 8 — Agent PDFs: one order, and the day's purchase list.

## Open questions that change the order

- None. Accepting the seven ADRs unblocks every Phase 1 story.
