# Data Standard — Lenaba

**Version:** 1.0

## Source

Original dataset:

`data/raw/all-names.csv`

The original file is never edited.

## Current Dataset

* 97,697 records
* UTF-8
* 15 source fields

## Canonical Schema

| Field        | Type       |
| ------------ | ---------- |
| id           | UUID       |
| name         | TEXT       |
| gender       | TEXT       |
| origin       | TEXT       |
| country      | VARCHAR(2) |
| meaning      | TEXT       |
| variants     | TEXT       |
| popularity   | INTEGER    |
| first_letter | CHAR(1)    |
| syllables    | SMALLINT   |
| stresses     | TEXT       |
| slug         | TEXT       |

## Naming Rules

* Names use Title Case.
* Country uses ISO-3166 alpha-2 codes.
* Origin stores linguistic origin.
* Variants are comma-separated.

## Quality Rules

Every record must have:

* valid name
* valid gender
* slug
* first_letter
* UTF-8 encoding

## Pipeline

1. Audit
2. Clean
3. Enrich
4. Export
