---
id: RULE-0016
title: Changelogs run newest first, grouped by change type
type: rule
status: accepted
scope: repo
---

# RULE-0016 — Changelogs run newest first, grouped by change type

**Rule.** One dated entry per day, newest at the top, with changes grouped by type.

```markdown
## 2026-09-22

### Superseded
- ADR-0012 by ADR-0024 — the load test showed the first choice could not scale

### Changed
- ADR-0016: exclude the discount from both hashes

## 2026-09-21

### Added
- ADR-0001..ADR-0022, seeded from the first plans
```

**The groups**, and nothing else: `Added`, `Changed`, `Superseded`, `Removed`, `Fixed`.
Each appears at most once per dated entry. A second `### Changed` under the same date is two
edits that should have been one list.

`Superseded` rather than "Deprecated", because that is the word the artefact lifecycle uses.
An entry says what changed and, where it is not obvious, why in half a line.

**Newest first**, because nobody opens a changelog to read forward from the beginning. They
open it to find out what just changed. A second entry on the same day merges into that day's
heading rather than appending below it.

**No version numbers, no `[Unreleased]`.** There is no release of `context/`.

**References may stay plain.** [RULE-0015](RULE-0015-references-are-links.md) exempts changelogs,
because entries are mostly ranges. A link is still allowed, and its path is checked like any other.

**Every artefact is named in its log.** An artefact that reaches the tree without an entry is an artefact nobody can find again. A range such as `ADR-0001..ADR-0022` covers every id in it. `make new` adds the entry for you.

**Enforced by.** The `changelog` gate in `make harness-check`: headings must be `## YYYY-MM-DD`,
dates must descend, group headings must be one of the five, and every artefact must be named in its log.
