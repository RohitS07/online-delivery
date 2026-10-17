---
id: US-0007
title: A person reads the app in English or Marathi
type: us
domain: identity
status: accepted
bpm: BPM-0005
actor: person
constrained_by: [ADR-0003, ADR-0005, ADR-0010]
---

# US-0007 — A person reads the app in English or Marathi

**As** a person in a village **I want** to read the app in Marathi or English, and have it remember my
choice **so that** I understand every screen.

Sets up translation under [ADR-0010](../adr/ADR-0010-the-app-shows-text-in-english-and-marathi-and-the-api-sends-codes.md),
starting from the first step of [BPM-0005](../bpm/BPM-0005-a-person-signs-up-or-signs-in-with-a-mobile-number.md).
It comes before [US-0006](US-0006-a-person-signs-in-and-lands-in-the-area-for-their-role.md), so no screen is
built with fixed text. The existing API status text moves into the translation files.

## Acceptance criteria

| Id | Criterion | Verified by |
|---|---|---|
| `AC-0007-01` | Given a first visit, when the app loads, then it is in English and the page's `lang` is `en` | `test:online-delivery-app/src/i18n/i18n.test.ts::defaultsToEnglish` |
| `AC-0007-02` | Given the language switcher, when Marathi is chosen, then the visible text is Marathi and `lang` is `mr` | `test:online-delivery-app/src/components/LanguageSwitcher.test.tsx::switchingShowsMarathi` |
| `AC-0007-03` | Given Marathi was chosen, when the app reloads, then it is still in Marathi | `test:online-delivery-app/src/components/LanguageSwitcher.test.tsx::choiceIsRemembered` |
| `AC-0007-04` | Given the English and Marathi translation files, when their keys are compared, then each has exactly the same keys | `test:online-delivery-app/src/i18n/i18n.test.ts::bothLanguagesHaveSameKeys` |
| `AC-0007-05` | Given Marathi is chosen and the API is healthy, when the status shows, then it is in Marathi | `test:online-delivery-app/src/components/ApiStatus.test.tsx::showsHealthyInMarathi` |
| `AC-0007-06` | Given an API error `code` with no translation, when it is shown, then the person sees a general error message in their language | `test:online-delivery-app/src/i18n/i18n.test.ts::unknownCodeFallsBackToGeneric` |
| `AC-0007-07` | Given a master-data item with `nameEn` and `nameMr`, when it is shown, then the name matches the chosen language | `test:online-delivery-app/src/i18n/localizedName.test.ts::picksNameForLanguage` |
