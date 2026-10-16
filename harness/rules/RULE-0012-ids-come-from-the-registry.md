---
id: RULE-0012
title: Artefact ids come from the registry, never by hand
type: rule
status: accepted
scope: context
---

# RULE-0012 — Artefact ids come from the registry, never by hand

**Rule.** Allocate an id with `make new TYPE=BPM TITLE="..."`, or `make id TYPE=BPM` to see the next one. An id is used once, never reused and never renumbered. Retiring an artefact means setting `status: superseded` and naming `superseded_by`, not deleting the file.

**Why.** Ids are referenced from code comments, tests, evals and commit messages. A renumbered id silently points at the wrong thing.

**Enforced by.** The `ids` gate fails on a duplicate, on a filename that does not match its id, and on a registry that is out of date. A gap in the sequence is allowed.
