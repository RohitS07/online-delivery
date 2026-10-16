---
id: RULE-0003
title: Artefacts are written in plain, short sentences
type: rule
status: accepted
scope: context
---

# RULE-0003 — Artefacts are written in plain, short sentences

**Rule.** An artefact is written so that someone who has not read the rest of the repository understands it on one pass.

- Short sentences. One idea each.
- Everyday words. If a technical term is needed, use it once and move on.
- No filler: nothing "robust", "seamless", "world-class" or "best-in-class".
- An ADR states its decision first, in one or two sentences.
- An ADR says what was chosen instead, and why not. A decision with no alternative is not a decision.
- Keep the whole record under one page.

**Why.** Artefacts are read by people joining the project, by people outside engineering, and by agents deciding what they are allowed to do. Any of them can be stopped by a long sentence.

**Enforced by.** Review. The `frontmatter` gate checks structure, not wording, so this one is on the author.
