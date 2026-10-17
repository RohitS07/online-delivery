---
id: US-0003
title: The app is written in TypeScript and still shows the API status
type: us
domain: platform
status: accepted
bpm: BPM-0001
actor: developer
constrained_by: [ADR-0003, ADR-0005]
---

# US-0003 — The app is written in TypeScript and still shows the API status

**As** a developer about to build the role areas **I want** the app converted to strict TypeScript
before it grows **so that** wrong field names and missed states fail the build, not the customer.

Converts the existing app under [ADR-0005](../adr/ADR-0005-write-the-app-in-typescript.md). The visible
behaviour of [US-0002](US-0002-a-visitor-sees-one-clear-api-status.md) does not change. Its tests are
renamed to `.tsx`, and its acceptance criteria get the new paths in the same commit. Tests follow
[ADR-0003](../adr/ADR-0003-test-the-api-with-xunit-and-the-app-with-vitest.md).

## Acceptance criteria

| Id | Criterion | Verified by |
|---|---|---|
| `AC-0003-01` | Given the app's `src` folder, when its files are listed, then no `.js` or `.jsx` file is left | `test:online-delivery-app/src/typescript.test.ts::noJavaScriptSourceLeft` |
| `AC-0003-02` | Given `tsconfig.json`, when it is read, then `strict` is `true` | `test:online-delivery-app/src/typescript.test.ts::tsconfigIsStrict` |
| `AC-0003-03` | Given `package.json`, when it is read, then a `typecheck` script runs `tsc --noEmit`, and `make typecheck` runs that script | `test:online-delivery-app/src/typescript.test.ts::typecheckScriptRunsTsc` |
| `AC-0003-04` | Given the API answers as [SPEC-0001](../specs/SPEC-0001-health-check-endpoint.md) says, when the health service reads it, then it returns a typed `HealthResponse` from `src/types` | `test:online-delivery-app/src/services/healthService.test.ts::returnsTypedHealthResponse` |
| `AC-0003-05` | Given the converted app, when the [US-0002](US-0002-a-visitor-sees-one-clear-api-status.md) tests run as `.tsx`, then they all pass unchanged in what they check | `test:online-delivery-app/src/components/ApiStatus.test.tsx::showsOnlyHealthyWhenApiAnswers` |
