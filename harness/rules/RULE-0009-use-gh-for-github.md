---
id: RULE-0009
title: Use the gh CLI for GitHub
type: rule
status: accepted
scope: repo
---

# RULE-0009 — Use the gh CLI for GitHub

**Rule.** All GitHub work — issues, pull requests, reviews, checks, releases — goes through the `gh` CLI. Do not scrape the web interface and do not hand-build API calls where a `gh` command exists.

**Authentication.** This is the one place a workstation and a Coder workspace differ ([RULE-0010](RULE-0010-local-development.md)).

- **In Coder** (`$CODER` is set). If `gh auth status` fails, authenticate with the Coder external auth token:
  ```bash
  gh auth status || coder external-auth access-token primary-github | gh auth login -p https --with-token
  ```
- **On a workstation.** Git authenticates with the credentials the repository was cloned with. `gh` uses the developer's own `gh auth login`. Never run the `coder` command outside Coder.

**Why.** One tool that works the same in a terminal, in CI and for an agent. Tokens are never copied into the repository or into a shell history.

**Enforced by.** [RULE-0014](RULE-0014-no-secrets-in-the-repository.md) blocks a token reaching the repository. In Coder, a `SessionStart` hook in `.claude/settings.json` runs the login above when a Claude session starts. The rest is convention, checked in review.
