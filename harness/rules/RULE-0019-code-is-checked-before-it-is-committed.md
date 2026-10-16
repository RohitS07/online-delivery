---
id: RULE-0019
title: Code is checked before it is committed
type: rule
status: accepted
scope: repo
---

# RULE-0019 — Code is checked before it is committed

**Rule.** Every commit passes the `pre-commit` hook. It checks the staged files' formatting and lint, and the types of every project they touch. A commit it refuses is fixed, with `make fmt` for formatting, and committed again. Never commit with `--no-verify`, and never switch a check off in a file to get a commit through.

The checks come before the tests: format, lint, types, then tests. The hook does not run the tests. They run after it, with `make test`, and in CI after the same checks.

**Why.** A problem found when committing costs seconds. Found in CI, it costs a push, a wait and another commit. A tool that finds it in seconds should never leave it for a test run or a reviewer.

**Enforced by.** `harness/hooks/pre-commit`, installed with the other hooks by `make hooks`. Each new app is added to the project lists at the top of `harness/hooks/pre_commit.py`. CI runs the same checks over the whole repository before the tests.
