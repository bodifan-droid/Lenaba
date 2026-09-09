# Lenaba Roadmap

## Week 1 — Foundation

* [x] Brand
* [x] Logo
* [x] Repository
* [ ] Data Pipeline

## Architecture Freeze (v0.4.5)

**Single Source of Truth**

* Main database: **97,697 names**
* BehindTheName: donor knowledge only
* `knowledge_master`: temporary enrichment cache
* Providers enrich the main database through Smart Queue and Merge Engine.

### Deferred after MVP

* Taxonomy v2
* Graph Ranking
* Recommendation Engine
* Advanced Family Scoring

## Sprint v0.5 — Full Coverage

### Day 1 (Done)

- [x] Execution Queue
- [x] Execution Batches
- [x] Language Resolver
- [x] Smart Queue V3
- [x] Behind Executor MVP
- [x] Behind Cache
- [x] HTML Snapshot (Yamila)

### Day 2 (Next)

- [ ] Production HTML Parser
- [ ] Dry Run (5 names)
- [ ] Arabic batch
- [ ] Merge into knowledge_master
- [ ] Cache integration
- [ ] Resume after interruption


## Week 2 — UX/UI

* Wireframes
* Design System
* Interactive Prototype

## Future Assets (Post-MVP)

### Taxonomy v2

Status: Dormant Asset

Goal:
Complete the taxonomy model and integrate it into the product after the Mobile MVP.

Tasks:

- Refine taxonomy structure.
- Separate language and domain categories.
- Generate taxonomy index.
- Add SEO category pages.
- Add taxonomy filters inside the app.

## Week 3 — Backend

* Supabase
* Authentication
* API

## Week 4 — Frontend

* Next.js
* Search
* Filters
* Favorites
* Couple Match MVP

## Week 5 — SEO Engine

* 97k Name Pages
* Category Pages
* Sitemap

## Week 6 — Launch

* Vercel
* Google Search Console
* Product Hunt
* Pinterest
* Reddit

## Future Roadmap

### Phase 2

* AI Name Match
* Sound-alike Recommendations
* Family Sharing
* Name Battles

### Phase 3

* Native iOS App
* Native Android App
* Global Rankings
* Pronunciation Audio
