---
id: PROC-0001
title: From intent to deployment
type: proc
status: accepted
---

# PROC-0001 — From intent to deployment

The one path every change takes.

```mermaid
flowchart TD
  I["Intent: request, defect, idea"] --> A{"Is it written down<br/>in context/?"}
  A -->|no| S["/author: write or extend the artefacts<br/>SKILL-0001 SKILL-0002"]
  A -->|yes| B["Branch RULE-0005"]
  S --> R{"Accepted by a person?"}
  R -->|no| S
  R -->|yes| B
  B --> W["/implement: build against accepted artefacts RULE-0013"]
  W --> G["make harness-check + code gates"]
  G -->|fail| W
  G -->|pass| PR["Pull request RULE-0007"]
  PR --> H["Human approval"]
  H --> D["Deploy"]
```

**The rule behind it.** Agents propose, gates dispose. Agent quality varies; the gate matrix does not. Every gate is a command a person can run identically.

**Nothing skips a step.** A one-line fix takes the same path. It is fast because the path is fast, not because it was skipped.
