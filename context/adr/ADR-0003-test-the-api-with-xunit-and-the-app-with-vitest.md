---
id: ADR-0003
title: Test the API with xUnit and the app with Vitest
type: adr
status: implemented
---

# ADR-0003 — Test the API with xUnit and the app with Vitest

## Decision

API tests use xUnit, and run the real API in memory with `Microsoft.AspNetCore.Mvc.Testing`. App
tests use Vitest with React Testing Library in a jsdom browser.

## Why

- Acceptance criteria name a test by path and name. Both apps need a test runner before the first story can be built.
- xUnit is the default for .NET test projects, and the in-memory test server exercises the real pipeline: CORS, redirects, routing.
- Vitest reads the app's existing Vite configuration, so tests and the app build the same way.
- React Testing Library tests what the visitor sees, not component internals.

## Instead of

- **NUnit or MSTest for the API.** Both work. Neither is better here, and xUnit has the most ASP.NET Core examples.
- **Jest for the app.** It needs its own transform and module setup next to Vite's, and the two drift apart.
- **Only end-to-end browser tests, such as Playwright.** Slow, and they need both apps running. They may come later, alongside these.

## Consequences

- The API gets a test project in `online-delivery-api/tests/`, and `<Compile Remove="tests/**" />` in its project file.
- The app gets `vitest`, `jsdom` and `@testing-library/react` as pinned dev dependencies, and an `npm test` script.
- `make test` and both apps' CI start running real tests.
