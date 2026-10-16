# Project harness

A starting structure for a repository that is specified before it is built. It holds the
harness — rules, skills, processes, gates, git hooks and two Claude Code commands — and an
empty context tree to fill.

Every behaviour gets an artefact with a stable id, every artefact links to the decision that
constrains it, and every acceptance criterion binds to a test or an eval. Code is written
against artefacts, not against conversation.

```
ADR ──constrains──▶ BPM ──▶ US ──▶ AC ──▶ test or eval
                     │        │
                     └──▶ SPEC ┘──▶ code
```

| Where | What |
|---|---|
| [`context/`](context/) | What the product does — decisions, processes, stories, specs, budgets. Empty to start |
| [`harness/`](harness/) | How we build it — rules, skills, processes, gates, hooks, commands |
| [`evals/`](evals/) | What "good" means — metrics with thresholds. Empty to start |
| [`context/INDEX.md`](context/INDEX.md) | Generated map of every artefact |

Agents start at [`AGENTS.md`](AGENTS.md); `CLAUDE.md` is a symlink to it. It routes to everything else.

## The artefact types

Every document is one of ten types. The acronym is the type, the number is permanent.

| Type | Stands for | What it is | Lives in |
|---|---|---|---|
| **ADR** | Architecture Decision Record | A choice that was made, why, and what was rejected. Not a plan — a record | [`context/adr/`](context/adr/) |
| **BPM** | Business Process Model | What the product actually does, step by step, in business terms | [`context/bpm/`](context/bpm/) |
| **US** | User Story | A slice of a process small enough to build, from one actor's point of view | [`context/stories/`](context/stories/) |
| **AC** | Acceptance Criterion | One testable condition of a story, written given / when / then, bound to a test | inside its story |
| **SPEC** | Specification | An interface or data contract: entities, fields, states, ordering | [`context/specs/`](context/specs/) |
| **NFR** | Non-Functional Requirement | A quality constraint with a number attached — how fast, how big, how accurate. Not a feature | [`context/nfr/`](context/nfr/) |
| **RULE** | Rule | Something always true, that no change may violate | [`harness/rules/`](harness/rules/) |
| **SKILL** | Skill | How to carry out one repeatable build task correctly | [`harness/skills/`](harness/skills/) |
| **PROC** | Procedure | How we work: a development or operations workflow | [`harness/proc/`](harness/proc/) |
| **EVAL** | Evaluation | A quality measure with a threshold that can fail a build | [`evals/`](evals/) |

**The difference between an NFR and an EVAL** is what they measure. An NFR is a property of
the system — latency, payload size, cost. An EVAL is a property of the output — whether it
is any good.

**The difference between a RULE and an NFR** is whether there is a number. A rule is absolute
and has no threshold to tune. An NFR has a budget you could argue about.

### What each type must carry

`make new` writes the frontmatter and headings below, with a `TODO` in every field still to
answer. The gate refuses a `TODO` in anything past `draft`.

| Type | Frontmatter | Body |
|---|---|---|
| ADR | `id, title, type, status` | Decision, Why, Instead of, Consequences |
| BPM | `id, title, type, domain, status, actors, triggers` | Purpose, Flow, Decision points, Failure modes, Outcome |
| US | `id, title, type, domain, status, bpm, actor` | As / I want / so that, and an acceptance-criteria table |
| SPEC | `id, title, type, domain, status, bpm` | Entities, Rules, Must never |
| NFR | `id, title, type, domain, status, budget, enforced_by` | What it constrains, how it is checked, what a failure means |
| RULE | `id, title, type, status, scope` | Rule, Why, Enforced by |
| SKILL | `id, title, type, status` | Numbered steps, and the gate |
| PROC | `id, title, type, status` | Numbered steps, and the one thing not to do |
| EVAL | `id, title, type, domain, status, metric, threshold` | Question, Dataset, Metrics, Why it gates |

Optional keys the gates read: `constrained_by` (the ADRs an artefact follows), `stories` (on a
BPM), `superseded_by` and `supersedes`.

### How the numbers work

Ids are flat and global per type: `ADR-0001`, `BPM-0017`, `NFR-0011`. They are allocated in
order by `make new`, and once allocated they never change and are never reused. A gap in the
sequence is normal and means nothing. To find something by subject, use
[`context/INDEX.md`](context/INDEX.md) rather than the file names.

Acceptance criteria are the one exception: `AC-0003-02` takes its first number from the story
that owns it, so an id tells you where it lives.

### Status, and what it means for you

Every artefact carries a status: `draft` → `review` → `accepted` → `implemented`.
**Only `accepted` and `implemented` may be built against** ([RULE-0013](harness/rules/RULE-0013-implement-accepted-artefacts-only.md)), and only a
person moves an artefact to `accepted`. A decision that stops being true is not edited or
deleted — it is marked `superseded` and points at the one that replaced it, so the reasoning
stays readable after the fact.

## The two commands

Both are Claude Code slash commands. [`.claude/commands`](.claude/commands) links to
[`harness/commands/`](harness/commands/).

**`/author <requirement in plain words>`** turns a requirement into artefacts, and writes no
code. It decides which type the requirement is (a decision and the behaviour that follows from it
are two artefacts), checks the index for one that already covers it, scaffolds with `make new`,
fills every field, links what it mentions, sets the status to `review`, and runs the gates. It
stops and asks if the requirement conflicts with an accepted decision.

**`/implement <id>`** builds one accepted artefact. The id is the whole brief. It refuses an
artefact that is not `accepted`, follows the chain from the story to its process, decisions,
specs and budgets, branches, writes the tests the acceptance criteria name first, then the code,
runs the gates, and moves the artefact to `implemented`. It reports which test proves each
criterion.

The fork between them is [PROC-0001](harness/proc/PROC-0001-intent-to-deploy.md): is it written
down in `context/`? No means `/author` first, then a person accepts it, then `/implement`.

## The reviewer

**`reviewer`** is a Claude Code subagent, in [`harness/agents/`](harness/agents/), which
[`.claude/agents`](.claude/agents) links to. After `/implement`, ask for it by name ("review this
branch with the reviewer"), or `@`-mention it. It checks the branch against the artefacts it
implements: each artefact was `accepted` before the branch, each acceptance criterion has its
named test and the test asserts it, the rules held, and the gates pass. It reports and never edits.

It runs in its own context and returns only its report, so the session that wrote the code stays
small and does not mark its own work. It runs on a lighter model at medium effort, set in its
frontmatter (`model`, `effort`).

## With other coding agents

The harness does not depend on Claude Code. What enforces it is the `Makefile`, the git hooks
and CI, and every agent and person goes through them alike.

- **`AGENTS.md`** is the shared convention most coding agents read at the root and in each
  directory. `CLAUDE.md` exists only because Claude Code reads that name.
- **The commands and the reviewer** are plain markdown. Their frontmatter is Claude Code's,
  and another agent ignores it. Point that agent at the file: "follow
  `harness/commands/implement.md` for `US-0003`", or "review this branch as
  `harness/agents/reviewer.md` says". If it has its own place for saved prompts, link the files
  there as `.claude/` does, rather than copying them.
- **`.mcp.json`** is read by Claude Code. Other agents configure MCP servers in their own files;
  add the same servers there ([RULE-0018](harness/rules/RULE-0018-documentation-servers-are-reached-only-through-mcp-tools.md)).
- **`.claude/settings.json`** hooks are Claude Code's. The format-on-edit hook only saves a
  refused commit; the `pre-commit` hook is what enforces formatting, for any tool.

## Setup

The gate and the git hooks run on the exact Python in `.python-version` (3.14), from the
project's own `.venv`, never the system `python3` ([RULE-0010](harness/rules/RULE-0010-local-development.md)). uv installs both.

1. Install uv, with the standalone installer
   ([other methods](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh     # macOS and Linux
   wget -qO- https://astral.sh/uv/install.sh | sh      # where curl is missing
   brew install uv                                     # or with Homebrew
   ```

   On Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`.
   Open a new shell, then check it with `uv --version`.

2. Make the environment:

   ```bash
   uv sync
   ```

   uv reads `.python-version`, downloads that Python if it is not installed, and creates `.venv`
   with the dev tools in `uv.lock` (Ruff and Pyright). `.venv/bin/python --version` should print
   `Python 3.14`. Any `make` target runs `uv sync` itself when `.venv` is missing.

3. Use the git hooks, and run the gate:

   ```bash
   make hooks
   make harness-check
   ```

## Make commands

```bash
make new TYPE=BPM TITLE="Returns and exchanges"   # scaffold an artefact and log it
make fix                                          # regenerate the registry and index, link bare references
make harness-check                                # run every context gate; CI runs the same
make hooks                                        # once per clone: use harness/hooks in all three repos
make install                                      # .venv, dotnet restore, npm ci
make fmt                                          # format Python, C# and the React app
make check                                        # lint, typecheck, build, then test, both apps
make db-up / make run-api / make run-app          # PostgreSQL, the API on :5154, the app on :5173
```

In this workspace the API (`online-delivery-api/`) and the app (`online-delivery-app/`) are their
own git repositories inside the workspace repository, which ignores them. `make hooks` points all
three at `harness/hooks`, and each app repository runs the same checks in its own CI.

`make harness-check` checks frontmatter, that every artefact reference resolves and is a link,
that every acceptance criterion is bound to something executable, that `AGENTS.md` files stay
within budget, and that a directory carrying an `AGENTS.md` also has a current `CHANGELOG.md`.

## Starting a new project from this

1. Copy this directory, then `git init` and commit on a branch.
2. Follow [Setup](#setup): install uv, `uv sync`, `make hooks`, `make harness-check`.
3. Copy `harness/gates/banned_names.local.txt.example` to `banned_names.local.txt` and list the
   client names to keep out ([RULE-0001](harness/rules/RULE-0001-no-client-names.md)). In CI, set `HARNESS_BANNED_NAMES`.
4. Rewrite the top of [`AGENTS.md`](AGENTS.md): the project's name, one line on what it is, and its invariants.
5. For the `shadcn` MCP server, add `shadcn` as a dev dependency at the root, or point
   `.mcp.json` at the UI app's `node_modules` with `--cwd` ([RULE-0018](harness/rules/RULE-0018-documentation-servers-are-reached-only-through-mcp-tools.md)).
6. `/author` the first decisions and processes.

When an app is added, add its targets to the `Makefile`, its project to
`harness/hooks/pre_commit.py`, its job to CI, and an `AGENTS.md` with a `CHANGELOG.md` if agents
work in it.
