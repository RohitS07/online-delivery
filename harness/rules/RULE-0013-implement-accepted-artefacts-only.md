---
id: RULE-0013
title: Code may only implement accepted artefacts
type: rule
status: accepted
scope: repo
---

# RULE-0013 — Code may only implement accepted artefacts

**Rule.** Code is written against artefacts with status `accepted` or `implemented`. A `draft` or `review` artefact is a proposal. If code is needed, get the artefact accepted first. Only a person moves an artefact to `accepted`.

**Why.** A `review` artefact is still being argued about. Building against it produces work that is thrown away, and it settles the argument by accident.

**Enforced by.** The `/implement` command refuses an artefact that is not accepted. The `status` gate fails an accepted artefact that links a superseded decision.
