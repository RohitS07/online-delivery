---
id: SKILL-0001
title: Author a business process
type: skill
status: accepted
---

# SKILL-0001 — Author a business process

1. Scaffold it with `make new TYPE=BPM TITLE="..."`. Never pick an id by hand. See [RULE-0012](../rules/RULE-0012-ids-come-from-the-registry.md).
2. Fill the frontmatter: domain, actors, triggers, and the decisions that constrain it (`constrained_by`).
3. Write purpose, flow, decision points, failure modes and outcome. One page. One diagram at most.
4. Link decisions rather than restating them. See [RULE-0002](../rules/RULE-0002-spec-links-the-decision.md).
5. Keep it about the product's behaviour. How we build it belongs in a PROC.
6. Leave it at `status: review` until it has stories. Code may not be written against it yet. See [RULE-0013](../rules/RULE-0013-implement-accepted-artefacts-only.md).
7. Check the changelog entry `make new` added, in the same commit. See [RULE-0011](../rules/RULE-0011-agents-and-changelog-travel-together.md).

**Gate.** `make fix && make harness-check`.
