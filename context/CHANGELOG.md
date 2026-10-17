# Changelog — context

Newest first. See [RULE-0016](../harness/rules/RULE-0016-changelog-format.md).
Decisions have their own log in [adr/CHANGELOG.md](adr/CHANGELOG.md).

## 2026-10-18

### Changed
- [US-0003](stories/US-0003-the-app-is-written-in-typescript-and-still-shows-the-api-status.md): implemented in `online-delivery-app`
- [US-0002](stories/US-0002-a-visitor-sees-one-clear-api-status.md): its acceptance criteria bind to the tests' new `.ts` and `.tsx` paths, after the move to TypeScript

## 2026-10-17

### Added
- [BPM-0002](bpm/BPM-0002-a-customer-orders-from-the-village-agent.md): a customer orders from the village agent
- [BPM-0003](bpm/BPM-0003-an-agent-runs-the-daily-stock-and-delivery-cycle.md): an agent runs the daily stock and delivery cycle
- [BPM-0004](bpm/BPM-0004-an-admin-manages-master-data-agents-and-settings.md): an admin manages master data, agents and settings
- [BPM-0005](bpm/BPM-0005-a-person-signs-up-or-signs-in-with-a-mobile-number.md): a person signs up or signs in with a mobile number
- [SPEC-0002](specs/SPEC-0002-cities-villages-and-categories.md): cities, villages and categories
- [SPEC-0003](specs/SPEC-0003-sign-in-with-a-mobile-otp.md): sign in with a mobile OTP
- [US-0003](stories/US-0003-the-app-is-written-in-typescript-and-still-shows-the-api-status.md): the app is written in TypeScript and still shows the API status
- [US-0004](stories/US-0004-anyone-can-list-the-active-cities-villages-and-categories.md): anyone can list the active cities, villages and categories
- [US-0005](stories/US-0005-a-person-proves-their-mobile-number-and-gets-a-token.md): a person proves their mobile number and gets a token
- [US-0006](stories/US-0006-a-person-signs-in-and-lands-in-the-area-for-their-role.md): a person signs in and lands in the area for their role
- [US-0007](stories/US-0007-a-person-reads-the-app-in-english-or-marathi.md): a person reads the app in English or Marathi

### Changed
- [BPM-0001](bpm/BPM-0001-check-that-the-api-is-reachable.md): lists [US-0003](stories/US-0003-the-app-is-written-in-typescript-and-still-shows-the-api-status.md), which converts its app side to TypeScript
- `ROADMAP.md`: Phase 1, the foundation for the village delivery platform, and the order of the phases after it
- `BACKLOG.md`: the parts of the source specification left out of the core flow
- `glossary.md`: service date, order window, village agent, delivery hours, delivery fee, platform fee, registration token
- `delivery-service-specification.md`: added as the source document, with the business model agreed in discussion
- `AGENTS.md`: names the source document and says artefacts win over it

## 2026-10-16

### Added
- [BPM-0001](bpm/BPM-0001-check-that-the-api-is-reachable.md): check that the API is reachable
- [SPEC-0001](specs/SPEC-0001-health-check-endpoint.md): health check endpoint
- [NFR-0001](nfr/NFR-0001-api-requests-from-the-app-time-out.md): API requests from the app time out
- [US-0001](stories/US-0001-the-api-accepts-browser-calls-only-from-configured-origins.md): the API accepts browser calls only from configured origins
- [US-0002](stories/US-0002-a-visitor-sees-one-clear-api-status.md): a visitor sees one clear API status

### Changed
- [US-0002](stories/US-0002-a-visitor-sees-one-clear-api-status.md), [NFR-0001](nfr/NFR-0001-api-requests-from-the-app-time-out.md): implemented in `online-delivery-app`; [BPM-0001](bpm/BPM-0001-check-that-the-api-is-reachable.md) is implemented with both its stories
- [US-0001](stories/US-0001-the-api-accepts-browser-calls-only-from-configured-origins.md), [SPEC-0001](specs/SPEC-0001-health-check-endpoint.md): implemented in `online-delivery-api`

## 2026-09-26

### Added
- The empty context tree: `bpm/`, `stories/`, `specs/`, `nfr/`, the roadmap, the backlog and the glossary
