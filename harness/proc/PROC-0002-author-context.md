---
id: PROC-0002
title: Author or change a context artefact
type: proc
status: accepted
---

# PROC-0002 — Author or change a context artefact

1. Decide the artefact type. A decision is an ADR. Product behaviour is a BPM. A slice of work is a US. A contract is a SPEC. A number is an NFR. A constraint is a RULE. A procedure is a SKILL. A quality measure is an EVAL.
2. Scaffold it: `make new TYPE=BPM TITLE="..."`. It allocates the id and logs the addition. See [RULE-0012](../rules/RULE-0012-ids-come-from-the-registry.md).
3. Write it. Short sentences, plain words, one page. See [RULE-0003](../rules/RULE-0003-artefacts-are-plain-and-short.md).
4. Link, never restate. See [RULE-0002](../rules/RULE-0002-spec-links-the-decision.md).
5. Regenerate the derived files and link bare references: `make fix`.
6. Keep the changelog line in the same commit. See [RULE-0011](../rules/RULE-0011-agents-and-changelog-travel-together.md).
7. Run `make harness-check` before opening the pull request.

**Changing an existing artefact.** Edit it, and say in the changelog what changed and, if the meaning changed rather than the wording, why. A decision that is no longer true is superseded by a new ADR, never edited into a different decision.

**The one thing not to do.** Do not write code in the same step. An artefact is `review` until a person accepts it. See [RULE-0013](../rules/RULE-0013-implement-accepted-artefacts-only.md).
