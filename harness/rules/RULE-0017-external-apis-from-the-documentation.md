---
id: RULE-0017
title: Code against an external platform is written from its documentation, never from memory
type: rule
status: accepted
scope: repo
---

# RULE-0017 — Code against an external platform is written from its documentation, never from memory

**Rule.** A change that touches an external platform, SDK or component library checks that platform's documentation first, through its documentation server where one is configured ([RULE-0018](RULE-0018-documentation-servers-are-reached-only-through-mcp-tools.md)). Field names, method names, limits, environment variables and argument shapes are never recalled from memory.

**Why.** A plausible but wrong field or method name is the most common failure in generated code, and it looks correct in review. SDKs change shape between major versions.

**A platform fact carries an expiry.** A limit, a quota or a capability is true as of a version.
Any artefact asserting one records what it was checked against, and when:

```yaml
verified_against: API 2026-07, checked 2026-09-22
```

Re-checking at a version bump is then a procedure rather than a memory exercise. The gate cannot
check whether a number is true; it can check that the claim says when it was last known to be.

**Enforced by.** Type checking against the pinned SDK catches a wrong method name. What types cannot catch is checked against the documentation in review.
