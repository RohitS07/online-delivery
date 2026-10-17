---
id: ADR-0008
title: Work out the daily order window from the clock with no scheduled job
type: adr
status: accepted
---

# ADR-0008 — Work out the daily order window from the clock with no scheduled job

## Decision

Whether stock can be edited and whether orders can be placed are worked out on each request, from the
current IST time ([ADR-0007](ADR-0007-business-dates-and-times-are-in-india-standard-time-from-an-injected-clock.md)),
the open and close settings, and the holiday list. Every stock item belongs to one service date. "Clearing"
stock at the close means only that items of a past date are no longer offered. Nothing runs at 8:00 or 18:00.

## Why

- A job that must run at exactly 8:00 and 18:00 can be late, run twice, or not run while the API restarts. A rule worked out per request cannot miss.
- Old stock stays in the database as history for orders and reports. It is never deleted.
- A setting change takes effect without restarting or rescheduling anything.
- Tests set the clock and call the API. They do not wait for a timer.

## Instead of

- **A scheduled job that flips each village between closed, open and closed, and deletes leftover stock.** Simple to picture, but it adds a moving part that can fail silently, and deleting stock loses history.
- **Status flags set by the agent pressing open and close.** It depends on a person being on time, which is the problem the fixed window solves.

## Consequences

- Every stock and order query filters by service date.
- New window times take effect from the next service date. A change made during an open window does not move that day's open or close.
- Things that must happen at the close, such as a notification, are triggered when someone next asks, or come with a later decision.
