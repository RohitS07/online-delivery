---
id: ADR-0007
title: Business dates and times are in India Standard Time from an injected clock
type: adr
status: accepted
---

# ADR-0007 — Business dates and times are in India Standard Time from an injected clock

## Decision

Every business date and time (the service date, the order window, the expected delivery time) is
worked out in India Standard Time, UTC+05:30. Moments are stored in UTC. The API reads the time only
through .NET's `TimeProvider`, which is injected, and never through `DateTime.Now` or `DateTime.UtcNow`.

## Why

- Every user is in India. "Today" and "18:00" mean the Indian day and the Indian clock, wherever the server runs. Azure servers run on UTC.
- India has no daylight saving, so the offset never changes.
- Storing UTC keeps moments comparable, and converting at the edge is one rule.
- An injected clock lets a test set the time to 7:59 or 18:01 and check the window, without waiting.

## Instead of

- **The server's local time.** It changes with the host and is UTC in the cloud. Orders would open at 13:30 IST.
- **Store local IST times in the database.** It works for one country, but every comparison with a UTC moment needs care, and it breaks if the platform ever spans time zones.

## Consequences

- One service in the API turns a UTC moment into an IST service date and time, and every feature uses it.
- Tests use a fake time provider.
- The app shows times as the API sends them, labelled in IST. It never works out the service date from the phone's clock.
