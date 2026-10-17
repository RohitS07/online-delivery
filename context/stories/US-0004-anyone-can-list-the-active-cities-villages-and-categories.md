---
id: US-0004
title: Anyone can list the active cities, villages and categories
type: us
domain: administration
status: implemented
bpm: BPM-0004
actor: visitor
constrained_by: [ADR-0003, ADR-0004, ADR-0010]
---

# US-0004 — Anyone can list the active cities, villages and categories

**As** a visitor who is about to sign up **I want** the API to list the cities, villages and categories
the platform serves, in English and Marathi **so that** I can choose my village, and later screens can
filter by category.

Builds the API side of the master-data read in [BPM-0004](../bpm/BPM-0004-an-admin-manages-master-data-agents-and-settings.md),
to [SPEC-0002](../specs/SPEC-0002-cities-villages-and-categories.md). It brings in the database under
[ADR-0004](../adr/ADR-0004-store-data-in-postgresql-through-ef-core-with-migrations.md). Admin editing comes in a later story.

## Acceptance criteria

| Id | Criterion | Verified by |
|---|---|---|
| `AC-0004-01` | Given a new test database, when the tests start, then the schema and seed data come from the EF Core migrations, in PostgreSQL | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/ReferenceDataTests.cs::SchemaAndSeedComeFromMigrations` |
| `AC-0004-02` | Given the seed data, when a client sends `GET /api/v1/cities` with no token, then it gets `200` with Mumbai and Pune, each with its two villages, both names, and 3 delivery hours | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/ReferenceDataTests.cs::CitiesReturnSeedWithVillages` |
| `AC-0004-03` | Given a village is made inactive, when cities are listed, then that village is missing and its city is still there | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/ReferenceDataTests.cs::InactiveVillageIsHidden` |
| `AC-0004-04` | Given a city is made inactive, when cities are listed, then neither the city nor any of its villages is returned | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/ReferenceDataTests.cs::InactiveCityHidesItsVillages` |
| `AC-0004-05` | Given the seed data, when a client sends `GET /api/v1/categories` with no token, then it gets `200` with the six seeded categories, sorted by English name | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/ReferenceDataTests.cs::CategoriesReturnSeedSorted` |
| `AC-0004-06` | Given a second city with the same English name, when it is saved, then the database refuses it | `test:online-delivery-api/tests/OnlineDelivery.Api.Tests/ReferenceDataTests.cs::CityNameIsUnique` |
