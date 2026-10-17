---
id: BPM-0004
title: An admin manages master data, agents and settings
type: bpm
domain: administration
status: accepted
actors: [admin, app, API]
triggers: [an admin signs in, a new agent signs up and waits for approval]
constrained_by: [ADR-0004, ADR-0006, ADR-0008, ADR-0010]
stories: [US-0004]
---

# BPM-0004 — An admin manages master data, agents and settings

## Purpose

An admin keeps the cities, villages, categories, agents and platform settings right, so customers and agents work from the same facts.

## Flow

1. An admin signs in ([ADR-0006](../adr/ADR-0006-sign-in-with-a-mobile-otp-and-a-jwt-bearer-token.md)). There is no sign-up to the admin role.
2. The admin manages cities, villages and categories, each with an English and a Marathi name ([ADR-0010](../adr/ADR-0010-the-app-shows-text-in-english-and-marathi-and-the-api-sends-codes.md)). Anyone, signed in or not, can list the active ones.
3. The admin sets each village's delivery hours. The close time plus these hours is the village's expected delivery time.
4. The admin reviews agents waiting for approval and approves one for a village that has no approved agent.
5. The admin blocks or unblocks customers and agents. Replacing a village's agent means blocking the current one, then approving a waiting one.
6. The admin sets the platform settings: open time (default 8:00), close time (default 18:00), delivery fee (default ₹90), platform fee (default ₹10), and holidays.
7. The admin views and cancels orders. A cancelled paid order is refunded through the mock.

## Decision points

- Does the village already have an approved agent? If so, another agent cannot be approved for it.
- Is a window open when a time setting changes? The new time applies from the next service date ([ADR-0008](../adr/ADR-0008-work-out-the-daily-order-window-from-the-clock-with-no-scheduled-job.md)).
- Does a fee change touch existing orders? No. Fees apply to new orders only.
- Can a village or city be removed? It is made inactive, never deleted, so old orders still resolve.

## Failure modes

- Delivery hours that would push the expected delivery time past midnight are refused.
- A close time not later than the open time is refused.
- Blocking the only agent of a village leaves it showing "Service will start soon in your village".

## Outcome

Master data, agents and settings are in one consistent state. Every customer and agent sees only active places, approved agents and the settings for the service date.
