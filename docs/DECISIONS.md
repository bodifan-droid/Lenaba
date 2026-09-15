Lenaba Decision Log

This document records permanent product decisions.

Day 1
Brand
Brand name: Lenaba
Domain: lenaba.com
Positioning
Mobile-first
Global audience
Premium but friendly
Tagline

Find the one name you both love.

Typography
Plus Jakarta Sans
Colors
Warm Ivory
Soft Teal
Soft Sky
Blush Sand
Logo
Hidden L
Two people
Continuous line
Day 3
Repository

Project initialized on GitHub.

Data Strategy
Python
DuckDB
Supabase
Dataset
Original file remains untouched.
All transformations happen through scripts.
Roadmap Locked

Foundation → UX → Backend → Frontend → SEO → Launch

Decision: Taxonomy v1 is considered a completed asset but postponed for product integration until after the Mobile MVP.

## ADR-009 — Family First Architecture

AI generates knowledge only for canonical families.

Variants are generated locally.

Benefits:

* consistent facts
* lower API cost
* scalable regeneration

---

## ADR-010 — Knowledge ≠ Content

Separate:

* Family Knowledge
* Structured Facts
* Editorial Content

Content is always compiled.

---

## ADR-011 — Content Compiler

Pages are built from reusable content blocks instead of static AI-written articles.

Benefits:

* one-click regeneration
* controlled uniqueness
* reusable SEO system

---

## ADR-012 — Queue as Source of Truth

`execution_queue` becomes the central orchestration layer.

All executors work through canonical families.
