---
id: BPM-0005
title: A person signs up or signs in with a mobile number
type: bpm
domain: identity
status: accepted
actors: [person, app, API, OTP provider]
triggers: [a person who is not signed in opens the app]
constrained_by: [ADR-0006, ADR-0009, ADR-0010]
stories: [US-0005, US-0006, US-0007]
---

# BPM-0005 — A person signs up or signs in with a mobile number

## Purpose

A person proves they hold an Indian mobile number and reaches the part of the app for their role: customer, agent or admin.

## Flow

1. The person chooses English or Marathi, then enters their mobile number.
2. The API sends a one-time code through the OTP provider ([ADR-0009](../adr/ADR-0009-outside-providers-sit-behind-interfaces-with-mocks-first.md)). The mock sends nothing and logs the code in Development.
3. The person enters the code. The API checks it ([ADR-0006](../adr/ADR-0006-sign-in-with-a-mobile-otp-and-a-jwt-bearer-token.md)).
4. For a known number, the API returns a token with the user's role, and the app opens that role's area.
5. For an unknown number, the API returns a short-lived registration token. The person then signs up as a customer or an agent.
6. A customer gives their name, address, landmark, city and village. They can use the app at once.
7. An agent gives their name and the one village they will serve. They wait for an admin's approval ([BPM-0004](BPM-0004-an-admin-manages-master-data-agents-and-settings.md)) before they can enter stock.
8. The person signs out, or their token expires, and the app returns to sign-in.

## Decision points

- Is the number a valid Indian mobile number? If not, no code is sent.
- Is the code right, unexpired and within the attempt limit? If not, no token is issued.
- Is the user blocked? A blocked user gets no token, and an existing token stops working.
- Is the user an agent who is still waiting? They sign in and see that they are waiting for approval.

## Failure modes

- Too many code requests or wrong codes. The API refuses for a while.
- The code expires before it is entered.
- The token expires. The next API call is refused, and the app returns to sign-in.

## Outcome

A person is signed in as exactly one role, in their language, or is told clearly why not. No password exists anywhere.
