---
id: ADR-0010
title: The app shows text in English and Marathi and the API sends codes
type: adr
status: accepted
---

# ADR-0010 — The app shows text in English and Marathi and the API sends codes

## Decision

Every piece of text the app shows comes from a translation file, in English and Marathi, through
`react-i18next`. The person picks the language, and the app remembers it on that device. English is the
default. The API never sends text meant for a person. Errors are `ProblemDetails` with a stable `code`,
such as `otp.expired`, which the app translates. Master data, such as city names, is stored in both languages.

## Why

- Most customers are Marathi speakers in Maharashtra villages. A screen in their language is the difference between using the app and not.
- Adding translation to every screen later means touching every screen again. Doing it from the first screen costs little.
- A code is stable while its wording changes, and one code serves every language.
- `react-i18next` is the most used React translation library, and it handles plurals and placeholders.

## Instead of

- **English now, translation later.** Cheaper for slice 1. Every screen built before it gets reworked.
- **The API returns translated messages, chosen by `Accept-Language`.** It puts wording into the API, and every new language becomes an API release.
- **A small hand-made dictionary.** Fine for ten strings. Plurals and placeholders get reinvented badly.

## Consequences

- No user-facing text is written directly in a component. Lint or review catches it.
- Marathi text needs a native speaker's review before go-live.
- Every API error has a `code`, and each code has a translation in both languages.
- Master-data entities have an English and a Marathi name.
