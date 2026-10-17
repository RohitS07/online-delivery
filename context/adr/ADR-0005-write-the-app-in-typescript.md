---
id: ADR-0005
title: Write the app in TypeScript
type: adr
status: accepted
---

# ADR-0005 — Write the app in TypeScript

## Decision

The React app is written in TypeScript with `strict` on. Source files are `.ts` and `.tsx`. The type
check, `tsc --noEmit`, is part of `make typecheck` and fails the build. DTO types in `src/types` mirror
the API's SPECs.

## Why

- The app is about to grow from one screen to three role areas, with carts, orders and money. Types catch wrong field names and missed states before a person does.
- A DTO type per SPEC makes a contract change visible in the app as a compile error.
- The app has about ten source files today. Converting now is an afternoon. Converting later is a project.
- The product specification suggests TypeScript for the frontend.

## Instead of

- **Stay on JavaScript.** No migration work, but every API field is a guess until it fails at runtime.
- **JavaScript with JSDoc types.** Checkable by the same compiler, but noisier to write and easy to skip, so the checks end up partial.

## Consequences

- The app gets `typescript` and a `tsconfig.json`. ESLint gets its TypeScript plugin.
- Existing tests are renamed to `.ts` or `.tsx`, and the acceptance criteria that bind to them change paths in the same commit.
- The App row of the code-gates table in the workspace `AGENTS.md`, and the app's own `AGENTS.md`, change from JavaScript to TypeScript.
- No `any` without a comment naming why.
