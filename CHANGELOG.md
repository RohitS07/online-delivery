# Changelog — repository root

Newest first. See [RULE-0016](harness/rules/RULE-0016-changelog-format.md).

## 2026-10-16

### Added
- The harness adopted for the online delivery workspace: the API and the app stay separate repositories, ignored here
- `Makefile`: `install`, per-stack `fmt`, `lint`, `typecheck`, `build` and `test` for .NET and React, `check`, `db-up`, `db-down`, `run-api` and `run-app`

### Changed
- `Makefile`: API targets run on `OnlineDelivery.sln`, so they cover its tests; `make test-api` runs `dotnet test`
- `AGENTS.md` names the project, its three repositories, the cross-stack workflow and its invariants, merged from the old `CLAUDE.md`
- `.mcp.json` has no servers: the app does not use shadcn/ui
- CI gates the context tree and the harness code; each app repository runs its own checks
- `pyproject.toml` declares the Python version, so uv stops warning on every run

### Removed
- The root `.prettierrc.json`: the app carries its own

## 2026-09-26

### Added
- The harness and an empty context tree, seeded from an earlier project
- `AGENTS.md`, with `CLAUDE.md` linked to it and a review by the `reviewer` subagent before each pull request, and `README.md` with the setup steps, the reviewer, and how the harness works with other coding agents
- `Makefile`: the context gate, scaffolding and hooks targets, and `fmt`, `lint`, `typecheck` and `test`
- `.mcp.json` with the `shadcn` documentation server, and `.claude/` with its settings, format hook, and `commands` and `agents` linked to `harness/`
- CI: the context gate and the Python checks
