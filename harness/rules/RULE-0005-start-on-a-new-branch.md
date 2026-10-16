---
id: RULE-0005
title: Start every task on a new branch
type: rule
status: accepted
scope: repo
---

# RULE-0005 — Start every task on a new branch

**Rule.** Every task starts with a new branch off current `main`, named `feature/`, `bugfix/`, `task/` or `chore/` followed by a short description. Never begin work on `main`.

```bash
git switch main && git pull --ff-only
git switch -c feature/short-description
```

**Why.** A branch per task keeps one change reviewable, keeps `main` releasable, and makes it possible to abandon work without unpicking it.

**Enforced by.** Branch protection on `main`.
