---
id: RULE-0001
title: No client or customer name in anything tracked
type: rule
status: accepted
scope: repo
---

# RULE-0001 — No client or customer name in anything tracked

**Rule.** No client, customer or partner name appears in code, comments, docstrings, commit messages, branch names, pull request titles or bodies, or any document in this repository. Describe the situation instead: "a customer", "a pilot customer", "the customer's own settings".

**Why.** A product sold to many customers must not read as if it were built for one. A name in the history is both a leak and a misleading signal about what the code is for.

**Enforced by.** The `names` gate in `make harness-check`, against a list supplied outside the repository: `harness/gates/banned_names.local.txt` locally, which is gitignored, and `HARNESS_BANNED_NAMES` in CI.
