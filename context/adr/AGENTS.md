# AGENTS.md — decisions

One decision per file. Everything else in the repository links here rather than restating a
decision ([RULE-0002](../../harness/rules/RULE-0002-spec-links-the-decision.md)), so these
files are the single place a choice is argued.

## Structure

```markdown
# ADR-NNNN — Title

## Decision      One or two sentences. What we are doing. First, before any reasoning.
## Why           Three to five bullets in plain words.
## Instead of    The alternative, and why not. A decision with no alternative is not a decision.
## Consequences  What this commits us to, including what it costs.
```

`make new TYPE=ADR TITLE="..."` writes these headings for you.

`Instead of` is not optional. If nothing was rejected, nothing was decided, and the file
belongs somewhere else — usually as a rule or a spec.

## Writing

Short sentences, everyday words, under a page
([RULE-0003](../../harness/rules/RULE-0003-artefacts-are-plain-and-short.md)). These are read by
people joining the project, by people outside engineering and by agents deciding what they
are allowed to do. Any of them can be stopped by a long sentence.

## Superseding versus editing

**Edit in place** when the decision still holds and the writing does not: a clearer sentence,
a consequence nobody had noticed, a link. The record of what changed is the entry in
[CHANGELOG.md](CHANGELOG.md), which says what moved and why.

**Supersede** when the decision itself changes. Never edit one decision into a different one —
the old one is why the code looks the way it does, and deleting that reasoning leaves the code
unexplained.

```yaml
# in the old file
status: superseded
superseded_by: ADR-NNNN

# in the new file
supersedes: [ADR-MMMM]
```

The new record says why the old one no longer holds. That is the whole reason supersession
beats editing: the reasoning survives.

## Status

`review` while it is being argued. `accepted` once it holds. Code may only be written against
`accepted` ([RULE-0013](../../harness/rules/RULE-0013-implement-accepted-artefacts-only.md)).
`superseded` requires `superseded_by`, and the gate enforces it.

## After any change here

`make fix`, then add a `CHANGELOG.md` entry in the same commit
([RULE-0011](../../harness/rules/RULE-0011-agents-and-changelog-travel-together.md),
[RULE-0016](../../harness/rules/RULE-0016-changelog-format.md)). Decisions are the artefacts
most worth being able to ask "what changed, and when" about.
