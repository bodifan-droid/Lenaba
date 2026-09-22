# Lenaba Roadmap

## Phase 1 — Data Platform

- [x] Cleaning
- [x] Normalization
- [x] Enrichment
- [x] Families
- [x] Language Resolver
- [x] Smart Queue
- [x] Execution Queue
- [x] Behind Parser
- [x] Cache
- [x] Etymology Graph
- [ ] Master V2 (97k)

## Sprint 9 — Data Platform & Family Script Engine

Sprint 9
[x] Family Engine V2 (Completed)

## Sprint 9 — Family Engine V2

- [x] Family-first processing
- [x] Family metadata propagation
- [x] Duplicate-row handling
- [x] Dynamic queue refresh
- [x] Checkpoint & Resume

## Sprint 10 — Data Quality

### Priority

- [ ] Editorial Queue workflow
- [ ] Missing BTN review pipeline
- [ ] Family QA
- [ ] Canonical validation
- [ ] Origin & Meaning expansion
- [x] ADR-011 — Canonical Data Flow

### Goal

Transform Lenaba into a scalable content platform where AI generates canonical family knowledge and the local Content Compiler creates unique SEO pages for every name.

### Milestones

#### Phase 1 – Queue Platform

* Queue Sync
* Queue Orchestrator
* Fetch Doctor
* Execution Engine

#### Phase 2 – Family Script Engine

* family_scripts.parquet
* family_script_builder.py
* AI Canonical Script
* Family Fun Fact

#### Phase 3 – Content Compiler

* Intro Builder
* Meaning Builder
* History Builder
* Popularity Builder
* Pronunciation Builder
* Stress Builder
* Palindrome Builder
* SEO Builder
* FAQ Builder
* Synonym Engine

#### Phase 4 – Generator Safety

* generator_staging.parquet
* generator_changes.parquet
* Batch IDs
* approve_batch.py
* rollback_batch.py
* Confidence Gates

#### Phase 5 – Mass Parsing

* BehindTheName pass
* Wikidata pass
* Queue replay
* Final enrichment

### Sprint 10 Preview

Lenaba Studio (internal admin platform).


## Phase 2 — Backend

- [ ] Supabase
- [ ] API
- [ ] Authentication

## Phase 3 — Website

- [ ] Next.js
- [ ] Search
- [ ] Name Pages
- [ ] SEO

## Phase 4 — Mobile

- [ ] React Native
- [ ] iOS
- [ ] Android

## Phase 5 — Scale

- [ ] Background parser
- [ ] Additional donors
- [ ] AI enrichment
