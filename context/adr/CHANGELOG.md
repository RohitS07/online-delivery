# Changelog — decisions

Newest first. See [RULE-0016](../../harness/rules/RULE-0016-changelog-format.md).

## 2026-10-18

### Changed
- [ADR-0005](ADR-0005-write-the-app-in-typescript.md): implemented, the app is strict TypeScript and `make typecheck` checks it

## 2026-10-17

### Added
- [ADR-0004](ADR-0004-store-data-in-postgresql-through-ef-core-with-migrations.md): store data in PostgreSQL through EF Core with migrations
- [ADR-0005](ADR-0005-write-the-app-in-typescript.md): write the app in TypeScript
- [ADR-0006](ADR-0006-sign-in-with-a-mobile-otp-and-a-jwt-bearer-token.md): sign in with a mobile OTP and a JWT bearer token
- [ADR-0007](ADR-0007-business-dates-and-times-are-in-india-standard-time-from-an-injected-clock.md): business dates and times are in India Standard Time from an injected clock
- [ADR-0008](ADR-0008-work-out-the-daily-order-window-from-the-clock-with-no-scheduled-job.md): work out the daily order window from the clock with no scheduled job
- [ADR-0009](ADR-0009-outside-providers-sit-behind-interfaces-with-mocks-first.md): outside providers sit behind interfaces with mocks first
- [ADR-0010](ADR-0010-the-app-shows-text-in-english-and-marathi-and-the-api-sends-codes.md): the app shows text in English and Marathi and the API sends codes

## 2026-10-16

### Added
- [ADR-0001](ADR-0001-browser-origins-allowed-by-the-api-come-from-configuration.md): browser origins allowed by the API come from configuration
- [ADR-0002](ADR-0002-redirect-http-to-https-outside-development-only.md): redirect HTTP to HTTPS outside Development only
- [ADR-0003](ADR-0003-test-the-api-with-xunit-and-the-app-with-vitest.md): test the API with xUnit and the app with Vitest

### Changed
- [ADR-0003](ADR-0003-test-the-api-with-xunit-and-the-app-with-vitest.md): implemented, with xUnit in the API and Vitest in the app
- [ADR-0001](ADR-0001-browser-origins-allowed-by-the-api-come-from-configuration.md), [ADR-0002](ADR-0002-redirect-http-to-https-outside-development-only.md): implemented in `online-delivery-api`

## 2026-09-26

### Added
- The empty decisions directory
