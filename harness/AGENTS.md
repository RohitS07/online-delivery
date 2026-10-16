# AGENTS.md — harness

How we build. Procedures, constraints and the gates that enforce them.

## What lives here

| Directory | Type | Holds |
|---|---|---|
| `rules/` | `RULE-NNNN` | A constraint that is always true, and how it is enforced |
| `skills/` | `SKILL-NNNN` | A repeatable task: steps, validation, gate |
| `proc/` | `PROC-NNNN` | A workflow spanning roles and gates |
| `gates/` | — | The executable checks. `harness_check.py` is the context gate |
| `hooks/` | — | Git hooks: `commit-msg` ([RULE-0006](rules/RULE-0006-commit-messages-are-short.md)) and `pre-commit` ([RULE-0019](rules/RULE-0019-code-is-checked-before-it-is-committed.md)). Run `make hooks` once per clone to use them |
| `agents/` | — | Subagents, each with a narrow tool allowlist. [`.claude/agents`](../.claude/agents) links here |
| `commands/` | — | Slash commands: `/author` and `/implement`. [`.claude/commands`](../.claude/commands) links here |

## Rule, skill or process?

- **Rule** — always true, one sentence, enforced by a gate where possible. *"Secrets never enter the repository."*
- **Skill** — one repeatable task an agent performs. *"Write a user story."*
- **Process** — a workflow across roles and gates. *"From intent to deployment."*

If it describes what the *product* does, it is a `BPM` in `context/`, not anything here.

## Commands and agents

Each file in `commands/` or `agents/` is one command or one agent, and nothing else lives there:
Claude Code loads every markdown file in them.

| | Use it when |
|---|---|
| `/author` | A requirement is not written down yet. Produces artefacts, never code |
| `/implement` | An accepted artefact needs building. Refuses anything not accepted |
| `reviewer` | A branch is ready for review. Read-only; checks it against its artefacts and reports |

The fork between the commands is [PROC-0001](proc/PROC-0001-intent-to-deploy.md): is it written
down in `context/`? No means author first. That is why the build prompt can be one line.

A subagent works in its own context and returns only its report, so the calling session stays
small. Give each one only the tools its job needs, and the cheapest model that does it well.
Commands a person runs rather than prompts live in the `Makefile`; `make help` lists them.

## The gates

```bash
make harness-check    # frontmatter, links, coverage, status, budgets, changelogs, names
```

Code gates, run per change: format, lint, types, then tests. Add each app's gates to the
`Makefile`, the `pre-commit` hook and CI in the same change that adds the app.

**Agents propose, gates dispose.** Agent quality varies; the gate matrix does not.
Every gate is a command a person can run identically.

## Rules you will hit most

| | |
|---|---|
| [RULE-0001](rules/RULE-0001-no-client-names.md) | No client or customer name in anything tracked |
| [RULE-0004](rules/RULE-0004-comments-are-short-and-name-the-artefact.md) | Comments are short and name their artefact |
| [RULE-0005](rules/RULE-0005-start-on-a-new-branch.md) | Start on a new branch |
| [RULE-0013](rules/RULE-0013-implement-accepted-artefacts-only.md) | Build only against accepted artefacts |
| [RULE-0014](rules/RULE-0014-no-secrets-in-the-repository.md) | Secrets never enter the repository |
| [RULE-0017](rules/RULE-0017-external-apis-from-the-documentation.md) | External platforms are coded from their documentation |

## Enforcement first

A rule a model has to remember is a rule that fails under context pressure. If a rule can be
checked by a hook, it must be. Add the check in the same change as the rule.
