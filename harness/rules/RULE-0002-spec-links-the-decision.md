---
id: RULE-0002
title: A spec links its decision record instead of restating it
type: rule
status: accepted
scope: context
---

# RULE-0002 — A spec links its decision record instead of restating it

**Rule.** A decision is written once, in an ADR. Every other artefact references it by id. No spec, process or story restates the reasoning.

**Why.** A decision copied into four documents is a decision that will be changed in one of them.

**Enforced by.** The `links` gate resolves every reference, and review rejects duplicated reasoning.
