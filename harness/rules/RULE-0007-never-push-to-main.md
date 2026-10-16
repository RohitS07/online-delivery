---
id: RULE-0007
title: Never push to main, changes land through a pull request
type: rule
status: accepted
scope: repo
---

# RULE-0007 — Never push to main, changes land through a pull request

**Rule.** `main` is never pushed to directly. Every change arrives as a pull request that passes the gates and is approved by a person.

- Open the pull request with `gh pr create`, with a title in the same style as a commit subject.
- The body states what changed, which artefact ids it implements, and how it was verified.
- Do not merge your own pull request without an approval.
- Do not force-push a branch someone else is reviewing.

**Why.** The gates are the whole point of the harness. A direct push skips every one of them.

**Enforced by.** Branch protection requiring a passing gate run and one approval.
