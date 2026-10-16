---
id: RULE-0011
title: A directory with an AGENTS.md has a CHANGELOG.md
type: rule
status: accepted
scope: repo
---

# RULE-0011 — A directory with an AGENTS.md has a CHANGELOG.md

**Rule.** Every directory carrying an `AGENTS.md` also carries a `CHANGELOG.md`, and a change to anything under that directory adds an entry in the same commit. Directories without an `AGENTS.md` have neither; git history covers them.

Entries name artefact ids rather than describing prose, newest first and grouped by change
type. The format is [RULE-0016](RULE-0016-changelog-format.md):

```markdown
## 2026-09-21

### Added
- BPM-0006, US-0001..US-0007, SPEC-0001

### Changed
- ADR-0016: exclude the discount from both hashes
```

`context/adr/` carries its own changelog, because a changed decision is the change most worth
being able to find.

**Why.** An agent needs to know what changed in the context it is about to rely on, without reading the whole git history. A diff shows what changed in a process; only the changelog says why it was worth changing.

**Enforced by.** The `changelog` gate in `make harness-check`, which fails a directory with an `AGENTS.md` and no `CHANGELOG.md`.
