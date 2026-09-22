# ADR-013 — Family Graph Union

**Status:** Accepted

## Context

Behind the Name повертає кілька незалежних типів зв'язків між іменами:

- family_members
- variants
- other_languages
- diminutives
- feminine_forms
- masculine_forms

Раніше Lenaba використовувала лише `family_members` як основу сім'ї. Через це частина пов'язаних імен (наприклад Bogdana, Boban або Bahdan) випадала із сімейного графа.

Ми також виявили, що окремі колонки `feminine_forms` і `masculine_forms` не можуть бути джерелом істини, оскільки парситься лише одна сторінка сім'ї.

## Decision

Під час парсингу будується **Family Graph Union**.

Сім'я визначається як об'єднання всіх структурованих зв'язків BTN.

```python
family_sources = [
    "family_members",
    "variants",
    "other_languages",
    "diminutives",
    "feminine_forms",
    "masculine_forms",
]
