---
id: ADR-0006
title: Sign in with a mobile OTP and a JWT bearer token
type: adr
status: accepted
---

# ADR-0006 — Sign in with a mobile OTP and a JWT bearer token

## Decision

Every role (customer, agent and admin) signs in with an Indian mobile number and a one-time code. The
API checks the code and issues a signed JWT. The token carries the user's id and one role: `Customer`,
`Agent` or `Admin`. The app sends it as `Authorization: Bearer` on every call. There are no passwords.

## Why

- Village customers know their phone number. Passwords get forgotten, and resets cost support time.
- One way of signing in for all three roles is one flow to build, test and secure.
- A bearer header is not sent automatically by the browser, so cross-site request forgery does not apply.
- A JWT lets each request be authorized without a session store, which suits more than one API instance.

## Instead of

- **ASP.NET Core Identity with passwords.** A large surface (password rules, resets, lockout) that the users do not want.
- **An external identity provider.** Strong, but it adds a paid service and a second sign-in screen before the product is proven. It can replace this later, because the API only checks a token.
- **Cookie sessions.** They need anti-forgery tokens on every write, and they are harder across the app's and the API's different addresses.

## Consequences

- The token signing key is a secret ([RULE-0014](../../harness/rules/RULE-0014-no-secrets-in-the-repository.md)).
- The app keeps the token in `localStorage`, so any script injected into the app could read it. The app must never render untrusted HTML.
- A token cannot be taken back before it expires. The API therefore checks on each request that the user is not blocked.
- The first admin is created from configuration. There is no sign-up path to the admin role.
- Codes are sent through the OTP provider interface of [ADR-0009](ADR-0009-outside-providers-sit-behind-interfaces-with-mocks-first.md).
