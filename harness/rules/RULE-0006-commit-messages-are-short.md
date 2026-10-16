---
id: RULE-0006
title: Commit messages are short and imperative
type: rule
status: accepted
scope: repo
---

# RULE-0006 — Commit messages are short and imperative

**Rule.** A subject line in the imperative mood, under 72 characters, describing what the commit does.

```
Add the export of a report
Fix the retry of a failed job
Pin the API version in one constant
```

- No prefix tags, no ticket numbers in the subject, no trailing full stop.
- A body only when the reason is not obvious. Wrap it at 72 characters and explain why, not what.
- Reference artefact ids in the body when the change implements one: `Implements US-0003.`
- One logical change per commit. Commit after each unit of work that stands on its own, not once at the end.
- No `Co-authored-by` trailer, from a person or a tool. A squash merge copies every commit's trailers into `main`, where they bury the message.

**Why.** The log is read far more often than it is written, usually while looking for when something changed.

**Enforced by.** The `commit-msg` hook in `harness/hooks/`, installed once per clone with `make hooks`. It rejects a subject over 72 characters, a trailing full stop, a prefix tag and a `Co-authored-by` trailer. The imperative mood is checked in review.
