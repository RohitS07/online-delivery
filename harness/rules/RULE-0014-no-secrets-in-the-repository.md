---
id: RULE-0014
title: Secrets never enter the repository
type: rule
status: accepted
scope: repo
---

# RULE-0014 — Secrets never enter the repository

**Rule.** No token, password, private key, connection string or customer credential is committed, in any file, in any branch, at any time. Not in an example, not in a test fixture, not temporarily.

- Local values live in `.env`, which is ignored.
- Deployed values come from a secret manager through workload identity.
- Tests use obvious fakes that could not work if leaked.
- A secret that reaches a branch is rotated first and removed second. Removing it from history does not make it safe.

**Why.** Every branch in this repository is pushed, and one leaked credential can give full access to a customer's data.

**Enforced by.** `.gitignore`, a secret scan in CI, and push protection on the remote.
