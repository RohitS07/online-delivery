---
id: SPEC-0003
title: Sign in with a mobile OTP
type: spec
domain: identity
status: accepted
bpm: BPM-0005
constrained_by: [ADR-0004, ADR-0006, ADR-0007, ADR-0009, ADR-0010]
---

# SPEC-0003 — Sign in with a mobile OTP

Three endpoints. Errors are `ProblemDetails` with a `code` ([ADR-0010](../adr/ADR-0010-the-app-shows-text-in-english-and-marathi-and-the-api-sends-codes.md)).

**`POST /api/v1/auth/otp`**, anonymous. Body `{ "mobileNumber": "98765 43210" }`. Answers `202 Accepted`
with `{ "resendAfterSeconds": 30, "expiresInSeconds": 300 }`. The same answer for known, unknown and blocked numbers.

| Status | `code` | When |
|---|---|---|
| 400 | `mobile.invalid` | Not an Indian mobile number |
| 429 | `otp.tooSoon` | Less than 30 seconds since the last code for this number |
| 429 | `otp.tooManyRequests` | More than 5 codes for this number in the last hour |

**`POST /api/v1/auth/otp/verify`**, anonymous. Body `{ "mobileNumber": "+919876543210", "code": "482913" }`. Answers `200 OK`:

```json
{ "result": "signedIn", "accessToken": "eyJ…", "expiresAt": "2026-10-24T09:30:00Z",
  "user": { "id": "7d3f…", "role": "Customer", "status": "Active", "name": "Demo Customer" } }
{ "result": "registrationRequired", "registrationToken": "eyJ…", "expiresAt": "2026-10-17T09:45:00Z", "user": null }
```

| Status | `code` | When |
|---|---|---|
| 400 | `otp.invalid` | Wrong code, attempts left |
| 400 | `otp.expired` | No unexpired, unused code for this number |
| 429 | `otp.tooManyAttempts` | The 5th wrong code. That code can no longer be used. |
| 403 | `user.blocked` | The code is right, but the user is blocked |

**`GET /api/v1/auth/me`**, with an access token. Answers `200 OK` with the `user` object above.
`401` with no token, a bad or expired token, or a registration token. `403 user.blocked` for a blocked user.

## Entities

| Entity | Holds | Key |
|---|---|---|
| `User` | `MobileNumber` (`+91` and 10 digits), `Name` (empty until sign-up), `Role` (`Customer`, `Agent`, `Admin`), `Status` (`Active`, `Waiting`, `Blocked`), `CreatedAt` (UTC) | `Id`, a GUID. `MobileNumber` is unique. |
| `OtpChallenge` | `MobileNumber`, `CodeHash`, `ExpiresAt`, `FailedAttempts`, `UsedAt`, `CreatedAt` (all moments UTC) | `Id`, a GUID |

## Rules

- A mobile number is 10 digits starting with 6, 7, 8 or 9. A leading `+91` or `91`, spaces and hyphens are accepted and removed. It is stored as `+91XXXXXXXXXX`.
- A code is 6 random digits from a cryptographic generator. It lasts 5 minutes, works once, and a new code replaces any earlier one.
- The code goes out through the OTP sender of [ADR-0009](../adr/ADR-0009-outside-providers-sit-behind-interfaces-with-mocks-first.md). The time comes from the injected clock ([ADR-0007](../adr/ADR-0007-business-dates-and-times-are-in-india-standard-time-from-an-injected-clock.md)).
- The access token is a JWT signed with `Jwt:SigningKey` (a secret, at least 32 bytes). It carries `sub` (the user id) and `role`, and lasts 7 days.
- The registration token is a JWT with `purpose: registration` and the mobile number. It lasts 15 minutes and is accepted only by the sign-up endpoints of a later SPEC.
- Every authorized request checks that the user still exists and is not blocked ([ADR-0006](../adr/ADR-0006-sign-in-with-a-mobile-otp-and-a-jwt-bearer-token.md)).
- At start-up the API creates the first admin from `Auth:FirstAdmin:MobileNumber` and `Auth:FirstAdmin:Name`, if no admin exists. Development also seeds one demo customer and one demo agent from `appsettings.Development.json`, using numbers no phone uses.

## Must never

- Store or log a code in plain text, except the mock's log line in Development.
- Tell the caller of `/auth/otp` whether a number is registered or blocked.
- Accept a registration token where an access token is needed.
- Create an `Admin` through any endpoint.
- Put the signing key in any `appsettings*.json` ([RULE-0014](../../harness/rules/RULE-0014-no-secrets-in-the-repository.md)).
