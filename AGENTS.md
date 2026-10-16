# AGENTS.md — Online Delivery Platform

An online delivery platform: a .NET REST API with PostgreSQL, and a mobile-first React web app that uses it.

## The workspace

Three git repositories, versioned independently:

| Directory | What | Repository |
|---|---|---|
| `.` (this one) | The harness and the context tree, shared by both apps | workspace repo |
| `online-delivery-api/` | ASP.NET Core API, EF Core, PostgreSQL in Docker. See its `AGENTS.md` | `online-delivery-api` |
| `online-delivery-app/` | React, Vite, Tailwind CSS, Axios. See its `AGENTS.md` | `online-delivery-app` |

The workspace repo ignores the two app directories. A feature that spans both is one set of
artefacts here, and one branch with the same name in each app repo it touches.

## Read this first

Every behaviour has an artefact in `context/`, every artefact has a stable id, and code is
written against artefacts, not against conversation.

| I need | Go to |
|---|---|
| A map of everything | `context/INDEX.md` |
| Why something was decided | `context/adr/` |
| What the product does | `context/bpm/` |
| Buildable work with acceptance criteria | `context/stories/` |
| An API route, DTO or data contract | `context/specs/` |
| A number that fails a build | `context/nfr/` |
| What I am not allowed to do | `harness/rules/` |
| How to do a repeatable task | `harness/skills/` |
| How we work | `harness/proc/` |
| What comes next, in order | `context/ROADMAP.md` |

## Before you write code

1. Find the artefact. No artefact, no code — write the artefact first with `/author` ([SKILL-0001](harness/skills/SKILL-0001-author-a-business-process.md), [SKILL-0002](harness/skills/SKILL-0002-write-a-story.md)).
2. Check its status. Only `accepted` and `implemented` may be built against ([RULE-0013](harness/rules/RULE-0013-implement-accepted-artefacts-only.md)). Build with `/implement`.
3. Read the rules in scope, and the `AGENTS.md` of each app you will change.
4. Branch in every repo you will change ([RULE-0005](harness/rules/RULE-0005-start-on-a-new-branch.md)). Never work on `main`.

## Building a feature across both apps

The API contract is written before either side is built.

1. **Contract.** A `SPEC` names the route, request DTO, response DTO and status codes.
2. **API.** Entity, migration, service, controller and validation, in `online-delivery-api/`.
3. **App.** The service in `src/services`, then the UI, in `online-delivery-app/`.
4. **Gates.** `make check` runs both apps' checks and tests.
5. **Report.** Summarise the API changes and the UI changes separately.

## Things that are always true

- **REST only.** The app reaches the API only through REST, at `/api/v1/...`.
- **One base URL setting.** The app reads the API base URL from `VITE_API_URL`.
- **Local ports.** API `http://localhost:5154`, app `http://localhost:5173`. Nowhere else.
- **No client or customer name** appears in anything tracked ([RULE-0001](harness/rules/RULE-0001-no-client-names.md)).
- **No secret** enters any repository, nor `.env`, `bin/`, `obj/` or `node_modules/` ([RULE-0014](harness/rules/RULE-0014-no-secrets-in-the-repository.md)).

## Before you open a pull request

```bash
make fix               # regenerate the registry and index, link bare references
make harness-check     # context gates: frontmatter, links, coverage, budgets, changelogs
make check             # lint, typecheck, build, then test, for both apps
```

The `pre-commit` hook refuses a commit whose staged files fail formatting, lint or the
compile ([RULE-0019](harness/rules/RULE-0019-code-is-checked-before-it-is-committed.md)); never commit with `--no-verify`. `make fmt` fixes formatting.

Ask the `reviewer` subagent to review the branch ([harness/agents/reviewer.md](harness/agents/reviewer.md)), then open the pull request with `gh` ([RULE-0009](harness/rules/RULE-0009-use-gh-for-github.md)).

## Code gates per stack

| Stack | Format | Lint | Types | Test |
|---|---|---|---|---|
| API (.NET 8) | `dotnet format` | `dotnet format --verify-no-changes` | `dotnet build -warnaserror` | `dotnet test` on `tests/*Tests.csproj` |
| App (React) | Prettier | Prettier check, ESLint | — (JavaScript) | `npm test`, once a runner is added |
| Harness (Python) | Ruff | Ruff | — | — |

## Writing

Short sentences, plain words ([RULE-0003](harness/rules/RULE-0003-artefacts-are-plain-and-short.md)). Comments are rare, short, and name the artefact
they implement ([RULE-0004](harness/rules/RULE-0004-comments-are-short-and-name-the-artefact.md)). Commit subjects are imperative and under 72 characters, with no `Co-authored-by` trailer ([RULE-0006](harness/rules/RULE-0006-commit-messages-are-short.md)).

## Layout

```
context/              what the product does — ADR, BPM, US, SPEC, NFR
harness/              how we build it — RULE, SKILL, PROC, agents, commands, gates, hooks
evals/                what good means — EVAL
online-delivery-api/  the API, its own repository
online-delivery-app/  the React app, its own repository
```

A directory with an `AGENTS.md` also has a `CHANGELOG.md`, updated in the same commit ([RULE-0011](harness/rules/RULE-0011-agents-and-changelog-travel-together.md)).
