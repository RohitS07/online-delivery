---
id: SPEC-0002
title: Cities, villages and categories
type: spec
domain: administration
status: accepted
bpm: BPM-0004
constrained_by: [ADR-0004, ADR-0010]
---

# SPEC-0002 — Cities, villages and categories

Two read endpoints. No authentication, because sign-up needs them before there is a token. Both
answer `200 OK`. They list only active rows, sorted by English name.

`GET /api/v1/cities` returns each active city with its active villages.

```json
[
  { "id": 1, "nameEn": "Mumbai", "nameMr": "मुंबई",
    "villages": [ { "id": 3, "nameEn": "Matheran", "nameMr": "माथेरान", "deliveryHours": 3 } ] }
]
```

`GET /api/v1/categories` returns each active category.

```json
[ { "id": 1, "nameEn": "Dairy", "nameMr": "दुग्धजन्य पदार्थ" } ]
```

## Entities

| Entity | Holds | Key |
|---|---|---|
| `City` | `NameEn`, `NameMr`, `IsActive` | `Id`, an integer. `NameEn` is unique. |
| `Village` | `CityId`, `NameEn`, `NameMr`, `DeliveryHours` (whole hours, 1 or more), `IsActive` | `Id`, an integer. `NameEn` is unique within its city. |
| `Category` | `NameEn`, `NameMr`, `IsActive` | `Id`, an integer. `NameEn` is unique. |
| `CityResponse`, `VillageResponse`, `CategoryResponse` | The fields in the examples above | DTOs, not stored |

## Seed data

Added by a migration ([ADR-0004](../adr/ADR-0004-store-data-in-postgresql-through-ef-core-with-migrations.md)), all active. Every village starts with 3 delivery hours.

| City | Villages |
|---|---|
| Pune (पुणे) | Mulshi (मुळशी), Jejuri (जेजुरी) |
| Mumbai (मुंबई) | Pali (पाली), Matheran (माथेरान) |

Categories: Groceries (किराणा), Vegetables (भाजीपाला), Fruits (फळे), Dairy (दुग्धजन्य पदार्थ),
Household (घरगुती वस्तू), Personal care (वैयक्तिक काळजी).

## Rules

- Both languages are always present ([ADR-0010](../adr/ADR-0010-the-app-shows-text-in-english-and-marathi-and-the-api-sends-codes.md)). The app picks one to show.
- A city with no active village is still listed, with an empty `villages` array.
- An inactive city hides all its villages, even active ones.
- JSON property names are camelCase.

## Must never

- Return an inactive city, village or category.
- Return an EF Core entity instead of a DTO.
- Delete a city, village or category that an order or agent refers to. They are made inactive instead.
