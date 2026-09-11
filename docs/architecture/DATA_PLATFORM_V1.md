# Lenaba Data Platform V1

> Official data architecture before Website & Apps development.

Version: v0.6

---

# Goal

Lenaba has one single source of truth.

The platform stores every known name in one unified knowledge base.

Current target:

- 97,697 names
- one Knowledge Master
- all builders work from the same foundation.

---

# Data Layers

## Layer 1 — Raw Imports

Purpose:

Original imported datasets.

Location:

data/imports/

Never edited manually.

---

## Layer 2 — Cleaned

Purpose:

Normalized records.

Location:

data/cleaned/

Outputs:

- names_cleaned.parquet
- names.parquet
- phonetics.parquet
- name_variants.parquet
- name_stats.parquet

Produced by:

scripts/pipeline/

---

## Layer 3 — Enriched

Purpose:

Global dictionary.

Current size:

97,697 names.

Main file:

data/enriched/names.parquet

This becomes the foundation of the platform.

---

## Layer 4 — Knowledge Master

Purpose:

Unified production database.

Target:

97,697 names.

Built from:

1. Enriched base
2. Knowledge Seed
3. Golden Packs
4. BehindTheName Fetch
5. Future donors

Output:

data/knowledge/knowledge_master.parquet

Every Builder uses this file.

---

## Layer 5 — Knowledge Artifacts

Generated automatically.

Includes:

- canonical_families.parquet
- language_resolver.parquet
- smart_queue_v3.parquet
- execution_queue.parquet
- execution_batches.parquet
- etymology_graph.parquet
- family_coverage.parquet
- name_graph.parquet
- taxonomy

These files must never become primary sources.

---

## Layer 6 — Content

Purpose:

Editorial workflow.

Location:

data/content/

Files:

- content_registry.parquet
- golden_pack_001.parquet
- golden_pack_002.parquet

These are editorial patches.

They never replace the Master.

---

## Layer 7 — Cache

Purpose:

Avoid duplicate requests.

Files:

- behind_cache.parquet
- fetch_results.parquet

Used by:

BehindTheName executor.

---

# Execution Flow

Raw Imports
↓

Clean
↓

Normalize
↓

Enrich
↓

Knowledge Master
↓

Families
↓

Language Resolver
↓

Smart Queue
↓

Execution Queue
↓

Website
API
iOS
Android

---

# Rules

1. One Source of Truth.
2. Builders never overwrite the Global Dictionary.
3. Content is additive.
4. Fetch fills missing knowledge only.
5. Every artifact must be reproducible.

---

# Current Status

| Layer            | Status             |
| ---------------- | ------------------ |
| Raw              | ✅                  |
| Clean            | ✅                  |
| Normalize        | ✅                  |
| Enriched         | ✅                  |
| Knowledge Master | 🚧 Migration to 97k |
| Families         | ✅                  |
| Language         | ✅                  |
| Queue            | ✅                  |
| Parser           | ✅                  |
| Cache            | ✅                  |

---

# Roadmap

Completed:

- Pipeline v0.1
- Knowledge Builders
- Family Engine
- Smart Queue
- Execution Queue
- Behind Parser
- Cache
- Etymology Graph

Next:

- Master V2
- Next.js website
- React Native apps
- Public API

Status: FROZEN
Production Master: 97,697
Family Coverage: 89.96%
