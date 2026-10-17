---
id: ADR-0009
title: Outside providers sit behind interfaces with mocks first
type: adr
status: accepted
---

# ADR-0009 — Outside providers sit behind interfaces with mocks first

## Decision

The API reaches every outside provider through its own interface: one to send OTP messages, one to take
payments and refunds, and one to store images. The first version of each is a mock. Configuration picks
the version. Feature code never names a provider.

## Why

- The demo needs sign-in, payment and images now, before an SMS provider or payment gateway is chosen.
- Which payment gateway can serve Indian businesses is still open. An interface keeps that choice for later.
- Tests use the mocks, so they never send a message or move money.
- A real provider is then one new class and one configuration change, with no change to orders or sign-in.

## Instead of

- **Build against a real provider now.** It needs accounts, keys and compliance work for a demo, and it ties the order code to one vendor's API.
- **No abstraction, and swap the code later.** Cheaper today. Later, every caller has to be found and changed.

## Consequences

- The mock OTP sender sends nothing. In Development it writes the code to the API log, and a configured fixed code may replace the random one for demos.
- The mock payment gateway always succeeds and returns a made-up transaction reference. The app never collects card or bank details ([RULE-0014](../../harness/rules/RULE-0014-no-secrets-in-the-repository.md)).
- The mock image store writes to a local folder that git ignores.
- Before go-live, each mock is replaced by a real provider. Each replacement is its own decision.
