# Changelog — context

Newest first. See [RULE-0016](../harness/rules/RULE-0016-changelog-format.md).
Decisions have their own log in [adr/CHANGELOG.md](adr/CHANGELOG.md).

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
