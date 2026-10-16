---
id: RULE-0004
title: Code comments are short and name the artefact they implement
type: rule
status: accepted
scope: repo
---

# RULE-0004 — Code comments are short and name the artefact they implement

**Rule.** Write as few comments as possible. Where one is needed, keep it to a line or two, and name the artefact it implements.

```python
# Retries stop at three: NFR-0002.
MAX_ATTEMPTS = 3
```

- Comment the reason, never the mechanics. The code already says what it does.
- A comment that restates the line below it is deleted, not improved.
- A non-obvious rule, threshold or exclusion carries its artefact id, so the reason is one click away.
- A module implementing a process names that process at the top, in one line.

**Why.** A reader who hits a surprising line needs to know why, and the why lives in `context/`. An id turns a mystery into a lookup. Long comments go stale and then mislead.

**Enforced by.** Review. The `links` gate resolves ids found in markdown; ids in code are checked in review.
