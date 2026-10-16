---
description: Build one accepted artefact, ending at green gates.
argument-hint: an artefact id, such as US-0003
---

Implement **$ARGUMENTS**.

Follow [PROC-0001](../proc/PROC-0001-intent-to-deploy.md). The id is the whole brief — everything else is read from the tree.

## 1. Refuse if it is not ready

Stop and say so, rather than building, if:

- the artefact's status is not `accepted` or `implemented` ([RULE-0013](../rules/RULE-0013-implement-accepted-artefacts-only.md)),
- it is a story whose acceptance criteria have no `verified_by` binding,
- it is a process with no stories — offer to author them instead ([SKILL-0002](../skills/SKILL-0002-write-a-story.md)).

A missing artefact is not a reason to improvise one. It is a reason to run the author command first.

## 2. Read the chain, not the conversation

Follow it from the artefact's own frontmatter: story → its process → the decisions constraining it → its budgets and specs. Read the `AGENTS.md` of every directory you will write in, and the rules in scope for it.

If you need a fact that is not in the tree, that is a gap in the tree. Say which artefact should carry it.

## 3. Branch

```bash
git switch main && git pull --ff-only
git switch -c feature/short-description
```

Never work on `main` ([RULE-0005](../rules/RULE-0005-start-on-a-new-branch.md)).

## 4. Write the tests first

The acceptance criteria already name them. `AC-NNNN-NN` binds to an exact test path and function — write that test, with that name, asserting that criterion. Do not invent a different definition of done.

## 5. Write the code

Comments are rare, short, and name the artefact they implement ([RULE-0004](../rules/RULE-0004-comments-are-short-and-name-the-artefact.md)). No client or customer name in anything tracked ([RULE-0001](../rules/RULE-0001-no-client-names.md)). No secret in any file ([RULE-0014](../rules/RULE-0014-no-secrets-in-the-repository.md)).

Facts about an external platform or library come from its documentation server, never from memory ([RULE-0017](../rules/RULE-0017-external-apis-from-the-documentation.md)).

## 6. Gate it

```bash
make fix && make harness-check
```

Then the code gates for what you touched, in order: format, lint, types, then tests ([RULE-0019](../rules/RULE-0019-code-is-checked-before-it-is-committed.md)). Run the eval scorecard too if you changed something an `EVAL` measures.

## 7. Move the status

An artefact whose code is merged and gated becomes `implemented`, in the same commit, with a changelog entry.

## Report back

Which criteria are met and which test proves each one. Say plainly if a criterion could not be met, and why — never report an artefact as done while one of its criteria is unproven.
