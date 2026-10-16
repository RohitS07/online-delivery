---
id: RULE-0015
title: Every artefact reference is a link
type: rule
status: accepted
scope: repo
---

# RULE-0015 — Every artefact reference is a link

**Rule.** Whenever prose names an artefact, it is a markdown link to that artefact's file.

```markdown
Retries stop at three. See [NFR-0002](../nfr/NFR-0002-retry-budget.md).
```

Not `See NFR-0002.`

The link is a relative path from the file doing the referring, so it works in the GitHub UI,
in an editor and in a local preview alike.

**Where it does not apply.**

- **Frontmatter.** `constrained_by: [ADR-0004, ADR-0005]` stays a plain list. It is data the
  gates read, not prose a person follows.
- **Code blocks, inline code and diagrams.** An id there is illustrating something, not
  pointing at it.
- **An artefact naming itself**, such as its own title heading.
- **Changelogs.** They are a historical log rather than navigation, and they are mostly ranges.
- **Acceptance criterion ids.** They are rows in a story, not files of their own.

**Why.** A bare id is a dead end. The reader either already knows what it means, or has to
search for it — and the whole point of the id scheme is that following the chain is cheap.

**Enforced by.** The `linkstyle` gate in `make harness-check`, which also fails a reference
that does not resolve. `make linkfix` rewrites bare references for you.
