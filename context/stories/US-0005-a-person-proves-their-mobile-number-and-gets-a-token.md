---
id: US-0005
title: A person proves their mobile number and gets a token
type: us
domain: identity
status: accepted
bpm: BPM-0005
actor: person
constrained_by: [ADR-0003, ADR-0004, ADR-0006, ADR-0007, ADR-0009, ADR-0010]
---

# US-0005 — A person proves their mobile number and gets a token

**As** a person with an Indian mobile number **I want** to get a one-time code and swap it for a token
**so that** I can use the app as my role without a password.

Builds the API side of sign-in in [BPM-0005](../bpm/BPM-0005-a-person-signs-up-or-signs-in-with-a-mobile-number.md),
to [SPEC-0003](../specs/SPEC-0003-sign-in-with-a-mobile-otp.md), under [ADR-0006](../adr/ADR-0006-sign-in-with-a-mobile-otp-and-a-jwt-bearer-token.md).
Codes go through the mock OTP sender of [ADR-0009](../adr/ADR-0009-outside-providers-sit-behind-interfaces-with-mocks-first.md). Tests set the time with a fake clock ([ADR-0007](../adr/ADR-0007-business-dates-and-times-are-in-india-standard-time-from-an-injected-clock.md)). Sign-up itself is a later story.

## Acceptance criteria

| Id | Criterion | Verified by |
|---|---|---|
| `AC-0005-01` | Given a valid number written as `98765 43210`, when a code is requested, then the API answers `202` and the OTP sender gets one 6-digit code for `+919876543210` | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/AuthOtpTests.cs::RequestSendsCode` |
| `AC-0005-02` | Given `12345`, when a code is requested, then the API answers `400 mobile.invalid` and nothing is sent | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/AuthOtpTests.cs::InvalidNumberIsRefused` |
| `AC-0005-03` | Given a code was sent 10 seconds ago, when another is requested, then the API answers `429 otp.tooSoon` | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/AuthOtpTests.cs::ResendTooSoonIsRefused` |
| `AC-0005-04` | Given 5 codes in the last hour, when a 6th is requested, then the API answers `429 otp.tooManyRequests` | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/AuthOtpTests.cs::SixthRequestInAnHourIsRefused` |
| `AC-0005-05` | Given an unknown number and a blocked number, when codes are requested, then both answers are identical to a known number's | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/AuthOtpTests.cs::RequestDoesNotRevealAccount` |
| `AC-0005-06` | Given a code was sent, when the database is read, then it holds only a hash of the code | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/AuthOtpTests.cs::CodeIsStoredHashed` |
| `AC-0005-07` | Given a known customer and the right code, when it is verified, then the answer is `signedIn` with a 7-day access token whose `role` is `Customer` | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/AuthVerifyTests.cs::KnownNumberGetsAccessToken` |
| `AC-0005-08` | Given an unknown number and the right code, when it is verified, then the answer is `registrationRequired` with a 15-minute registration token and no user | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/AuthVerifyTests.cs::UnknownNumberGetsRegistrationToken` |
| `AC-0005-09` | Given 4 wrong codes, when a 5th wrong code is sent, then the API answers `429 otp.tooManyAttempts`, and the right code then gets `400 otp.expired` | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/AuthVerifyTests.cs::FifthWrongCodeVoidsCode` |
| `AC-0005-10` | Given a code sent 5 minutes and 1 second ago, or a code already used, when it is verified, then the API answers `400 otp.expired` | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/AuthVerifyTests.cs::ExpiredOrUsedCodeIsRefused` |
| `AC-0005-11` | Given a blocked user and the right code, when it is verified, then the API answers `403 user.blocked` and issues no token | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/AuthVerifyTests.cs::BlockedUserGetsNoToken` |
| `AC-0005-12` | Given an access token, when `GET /api/v1/auth/me` is called, then it answers `200` with the user. With a registration token or none, it answers `401` | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/AuthMeTests.cs::MeAcceptsOnlyAccessTokens` |
| `AC-0005-13` | Given a token issued before the user was blocked, when `GET /api/v1/auth/me` is called, then it answers `403 user.blocked` | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/AuthMeTests.cs::BlockedUserTokenStopsWorking` |
| `AC-0005-14` | Given `Auth:FirstAdmin` is configured and no admin exists, when the API starts, then that number exists as an active `Admin` | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/AuthMeTests.cs::FirstAdminComesFromConfiguration` |
