---
id: US-0006
title: A person signs in and lands in the area for their role
type: us
domain: identity
status: accepted
bpm: BPM-0005
actor: person
constrained_by: [ADR-0003, ADR-0005, ADR-0006, ADR-0010]
---

# US-0006 — A person signs in and lands in the area for their role

**As** a customer, agent or admin **I want** to sign in with my number and a code and land in my own
area **so that** I see only what my role is for.

Builds the app side of sign-in in [BPM-0005](../bpm/BPM-0005-a-person-signs-up-or-signs-in-with-a-mobile-number.md),
against [SPEC-0003](../specs/SPEC-0003-sign-in-with-a-mobile-otp.md). The token is kept as
[ADR-0006](../adr/ADR-0006-sign-in-with-a-mobile-otp-and-a-jwt-bearer-token.md) says. All text comes through
[US-0007](US-0007-a-person-reads-the-app-in-english-or-marathi.md). The customer and agent areas are
mobile-first. The admin area is laid out for a desktop. Each area is an empty shell with a heading and
sign-out. Later stories fill it.

## Acceptance criteria

| Id | Criterion | Verified by |
|---|---|---|
| `AC-0006-01` | Given no one is signed in, when any area is opened, then the app shows the sign-in page | `test:online-delivery-app/src/app/routes.test.tsx::signedOutPersonGoesToSignIn` |
| `AC-0006-02` | Given the sign-in page, when it loads, then it also shows the API status of [US-0002](US-0002-a-visitor-sees-one-clear-api-status.md) | `test:online-delivery-app/src/pages/SignInPage.test.tsx::showsApiStatus` |
| `AC-0006-03` | Given `12345` is entered, when the person asks for a code, then no request is sent and the field shows that the number is not valid | `test:online-delivery-app/src/pages/SignInPage.test.tsx::invalidNumberSendsNothing` |
| `AC-0006-04` | Given a valid number, when the API answers `202`, then the code step shows, with resend disabled for 30 seconds | `test:online-delivery-app/src/pages/SignInPage.test.tsx::validNumberShowsCodeStep` |
| `AC-0006-05` | Given the API answers `otp.invalid`, when the code is checked, then the page shows that error's translated text | `test:online-delivery-app/src/pages/SignInPage.test.tsx::showsTranslatedErrorCode` |
| `AC-0006-06` | Given a right code for a customer, when it is checked, then the customer area opens | `test:online-delivery-app/src/pages/SignInPage.test.tsx::customerLandsInCustomerArea` |
| `AC-0006-07` | Given a right code for an agent, when it is checked, then the agent area opens | `test:online-delivery-app/src/pages/SignInPage.test.tsx::agentLandsInAgentArea` |
| `AC-0006-08` | Given a right code for an admin, when it is checked, then the admin area opens | `test:online-delivery-app/src/pages/SignInPage.test.tsx::adminLandsInAdminArea` |
| `AC-0006-09` | Given the answer is `registrationRequired`, when it arrives, then the app opens a sign-up page that says sign-up is coming | `test:online-delivery-app/src/pages/SignInPage.test.tsx::newNumberGoesToSignUp` |
| `AC-0006-10` | Given a signed-in customer, when they open the admin area, then they are sent to the customer area | `test:online-delivery-app/src/app/routes.test.tsx::wrongRoleGoesToOwnArea` |
| `AC-0006-11` | Given a stored token, when the app reloads, then it asks `/auth/me` and stays signed in | `test:online-delivery-app/src/app/routes.test.tsx::reloadKeepsSession` |
| `AC-0006-12` | Given the API answers `401` or `403 user.blocked` to any call, when it arrives, then the token is removed and the sign-in page shows | `test:online-delivery-app/src/services/apiClient.test.ts::unauthorizedSignsOut` |
| `AC-0006-13` | Given a signed-in person, when they sign out, then the token is removed and the sign-in page shows | `test:online-delivery-app/src/app/routes.test.tsx::signOutReturnsToSignIn` |
