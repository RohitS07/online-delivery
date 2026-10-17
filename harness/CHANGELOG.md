# Changelog — harness

Newest first. See [RULE-0016](rules/RULE-0016-changelog-format.md).

## 2026-10-18

### Changed
- `hooks/pre_commit.py` runs `tsc --noEmit` in a Node app when a staged `.ts` or `.tsx` file changes ([ADR-0005](../context/adr/ADR-0005-write-the-app-in-typescript.md))

## 2026-10-16

### Changed
- `hooks/pre_commit.py` formats and builds the API through `OnlineDelivery.sln`, tests included
- `hooks/`: one set of hooks serves the workspace and both app repositories; `pre-commit` checks C# with `dotnet format` and `dotnet build -warnaserror`, the app with Prettier and ESLint, and runs the context gate on any markdown change
- `gates/harness_check.py` skips `bin/`, `obj/` and `dist/`
- [RULE-0018](rules/RULE-0018-documentation-servers-are-reached-only-through-mcp-tools.md): no documentation server is configured yet

## 2026-09-26

### Added
- [RULE-0001](rules/RULE-0001-no-client-names.md)..[RULE-0019](rules/RULE-0019-code-is-checked-before-it-is-committed.md), [SKILL-0001](skills/SKILL-0001-author-a-business-process.md)..[SKILL-0002](skills/SKILL-0002-write-a-story.md), [PROC-0001](proc/PROC-0001-intent-to-deploy.md)..[PROC-0002](proc/PROC-0002-author-context.md): the generic harness, seeded from an earlier project
- `gates/harness_check.py`: the context gate, `make new` scaffolding and the generated registry and index. An id in inline code is an example, not a reference, so it is not resolved
- `hooks/commit-msg` ([RULE-0006](rules/RULE-0006-commit-messages-are-short.md)) and `hooks/pre-commit` ([RULE-0019](rules/RULE-0019-code-is-checked-before-it-is-committed.md)), with no app configured yet
- `commands/author.md` and `commands/implement.md`, available as `/author` and `/implement`
- `agents/reviewer.md`: a read-only subagent that reviews a branch against its artefacts, on a lighter model at medium effort
- [AGENTS.md](AGENTS.md) describes the commands and agents; `commands/` and `agents/` hold nothing else, since Claude Code loads every file in them
