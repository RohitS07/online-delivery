---
id: ADR-0004
title: Store data in PostgreSQL through EF Core with migrations
type: adr
status: accepted
---

# ADR-0004 — Store data in PostgreSQL through EF Core with migrations

## Decision

The API stores its data in PostgreSQL through Entity Framework Core with the Npgsql provider. Every
schema change is an EF Core migration. Seed data that every environment needs, such as the first cities
and villages, is part of a migration. API tests that touch the database run against a real PostgreSQL
started in Docker by Testcontainers.

## Why

- PostgreSQL already runs locally in Docker, and Azure offers it as a managed service.
- EF Core is the standard data layer for ASP.NET Core and keeps queries in typed C#.
- Migrations are reviewed in the pull request like code, and every environment reaches the same schema the same way.
- Tests against real PostgreSQL catch what an in-memory fake hides: constraints, unique indexes, case rules and date handling.

## Instead of

- **Dapper with hand-written SQL.** Faster for hot queries, but every mapping and schema change is manual work. Dapper can still be added for a report that needs it.
- **The EF Core in-memory provider or SQLite for tests.** Quick, but neither behaves like PostgreSQL, and tests would pass on code that fails in production.
- **Creating the schema with `EnsureCreated`.** No history and no upgrade path once real data exists.

## Consequences

- The API gets the EF Core, Npgsql and design-time packages, a `DbContext`, and a `Migrations/` folder.
- In Development the API applies pending migrations at start-up. In other environments migrations run as a deployment step, never on start-up.
- The connection string is a secret: user-secrets locally, a secret manager when deployed ([RULE-0014](../../harness/rules/RULE-0014-no-secrets-in-the-repository.md)).
- `make test-api` and CI need Docker running.
- Entities never leave the API. Endpoints return DTOs.
