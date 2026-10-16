# AGENTS.md — context

What the product does. Stack-agnostic, slow-moving, and the only place a behaviour is defined.

## What lives here

| Directory | Type | Holds |
|---|---|---|
| `adr/` | `ADR-NNNN` | A decision, its alternative, and its consequences |
| `bpm/` | `BPM-NNNN` | A business process: actors, trigger, flow, failure modes, outcome |
| `stories/` | `US-NNNN` | One actor's slice of a process, with acceptance criteria |
| `specs/` | `SPEC-NNNN` | The interface or data contract an implementer builds to |
| `nfr/` | `NFR-NNNN` | A number, and the gate that enforces it |

`INDEX.md` and `registry.yaml` are generated. Never edit them by hand.
`BACKLOG.md` lists deferred work with no id, so the registry stays clean.
`ROADMAP.md` orders the in-scope work that has not shipped yet. Update it when a phase's artefacts change.
`glossary.md` holds one definition per term. If two artefacts disagree, the glossary wins.

## What does not live here

How we build things. That is `harness/`. If you are writing about branches, gates, releases
or reviews, you are writing a `PROC` or a `SKILL`, not a `BPM`.

## The chain

```
ADR ──constrains──▶ BPM ──▶ US ──▶ AC ──▶ test or eval
                     │        │
                     └──▶ SPEC ┘──▶ code
```

Every acceptance criterion binds to something executable. A criterion nothing checks is a wish,
and the coverage gate fails it.

## Working here

1. `make new TYPE=BPM TITLE="..."` — never pick an id by hand ([RULE-0012](../harness/rules/RULE-0012-ids-come-from-the-registry.md)).
2. Fill every `TODO`. One page. Plain words ([RULE-0003](../harness/rules/RULE-0003-artefacts-are-plain-and-short.md)).
3. Link decisions, never restate them ([RULE-0002](../harness/rules/RULE-0002-spec-links-the-decision.md)).
4. `make fix`.
5. Keep the `CHANGELOG.md` line in the same commit ([RULE-0011](../harness/rules/RULE-0011-agents-and-changelog-travel-together.md)).
6. `make harness-check`.

## Status

`draft` → `review` → `accepted` → `implemented`, or `superseded` with `superseded_by`.
Code may only be written against `accepted` and `implemented` ([RULE-0013](../harness/rules/RULE-0013-implement-accepted-artefacts-only.md)).

## Rules in scope

[RULE-0002](../harness/rules/RULE-0002-spec-links-the-decision.md), [RULE-0003](../harness/rules/RULE-0003-artefacts-are-plain-and-short.md), [RULE-0011](../harness/rules/RULE-0011-agents-and-changelog-travel-together.md), [RULE-0012](../harness/rules/RULE-0012-ids-come-from-the-registry.md), [RULE-0013](../harness/rules/RULE-0013-implement-accepted-artefacts-only.md), and [RULE-0001](../harness/rules/RULE-0001-no-client-names.md) everywhere.
