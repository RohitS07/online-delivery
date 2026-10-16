---
id: RULE-0008
title: Amend rather than stack when correcting the commit you just made
type: rule
status: accepted
scope: repo
---

# RULE-0008 — Amend rather than stack when correcting the commit you just made

**Rule.** When a change corrects the commit you just made — a typo, a value you retuned, review feedback on that same unit of work — amend it. Update the message too, so it describes what the commit now does.

```bash
git commit --amend
```

- Only for commits that have not been pushed.
- Only when it really is the same unit of work. An unrelated change gets its own commit, even if it lands seconds later.

**Why.** History should read as one logical change per commit, not as a trail of "fix previous commit".

**Enforced by.** Review of the branch history before merge.
