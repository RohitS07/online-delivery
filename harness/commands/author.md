---
description: Turn a requirement into harness artefacts. No code.
argument-hint: the requirement, in plain business language
---

Add this requirement to the context tree:

**$ARGUMENTS**

Follow [PROC-0001](../proc/PROC-0001-intent-to-deploy.md). This command stops before any code is written.

## 1. Decide what it is

Do not assume it is a process. Route it:

| If the requirement is | It becomes | Skill |
|---|---|---|
| Behaviour the product performs | **BPM** | [SKILL-0001](../skills/SKILL-0001-author-a-business-process.md) |
| A slice of an existing process, buildable | **US** with acceptance criteria | [SKILL-0002](../skills/SKILL-0002-write-a-story.md) |
| A choice between options, with a loser | **ADR** | [AGENTS.md](../../context/adr/AGENTS.md) |
| A number that should fail a build | **NFR** | — |
| Something always true, no threshold | **RULE** | — |
| An interface or data shape | **SPEC** | — |
| A measure of whether output is good | **EVAL** | — |

If it is two things, it is two artefacts. A requirement that names a decision *and* the behaviour that follows from it is an ADR plus a BPM, linked.

If it does not fit any row, say so and ask rather than forcing it into the nearest one.

## 2. Check it is not already written

Search [`context/INDEX.md`](../../context/INDEX.md) first. An existing artefact that nearly covers it is amended or superseded, not duplicated. A decision that changed is superseded, never edited into a different decision.

## 3. Write it

```bash
make new TYPE=BPM TITLE="Short sentence"
```

This allocates the id, writes the frontmatter and headings the type requires, and adds the changelog entry. Never pick an id by hand ([RULE-0012](../rules/RULE-0012-ids-come-from-the-registry.md)).

Then fill every `TODO`. Link every artefact you mention ([RULE-0015](../rules/RULE-0015-references-are-links.md)). Link decisions rather than restating them ([RULE-0002](../rules/RULE-0002-spec-links-the-decision.md)). Plain words, short sentences ([RULE-0003](../rules/RULE-0003-artefacts-are-plain-and-short.md)).

## 4. Set the status honestly

Leave it at `draft` while anything is still `TODO` — the gate enforces this. Move to `review` when it is complete but unagreed. Only a human moves it to `accepted`, and only an `accepted` artefact may be built against ([RULE-0013](../rules/RULE-0013-implement-accepted-artefacts-only.md)).

## 5. Gate it

```bash
make fix && make harness-check
```

## Report back

What you created, what you changed, what you deliberately did not write down, and any question whose answer would change the artefact. If the requirement conflicts with an accepted decision, say which one and stop — do not quietly write around it.
