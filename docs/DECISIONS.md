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
## ADR-009 – Family-first Processing

**Status:** Accepted

### Decision

Lenaba processes families instead of individual names.

### Why

BehindTheName pages describe relationships between multiple names. Parsing every variant separately caused duplicate work and inconsistent family assignments.

### Result

- One BTN page updates the whole family.
- Duplicate database rows receive the same family metadata.
- Execution Queue works on completed families rather than repeated names.


## ADR-009 — Family-first Processing

**Status:** Accepted

### Decision

Lenaba processes families instead of individual names.

### Why

BehindTheName pages describe relationships between multiple names. Parsing every variant separately caused duplicate work and inconsistent family assignments.

### Result

- One BTN request updates the whole family.
- Duplicate database rows receive identical family metadata.
- Execution Queue operates on completed families.
- Interrupted runs can safely resume.

## ADR-010 — Resume-first Execution

**Status:** Accepted

### Decision

Completed families are skipped before HTML cache or network requests.

### Result

- Faster repeated runs.
- HTML cache is used only for unfinished families.
- Execution Queue becomes the single source of truth for progress.

## ADR-010 — Knowledge ≠ Content

Separate:

* Family Knowledge
* Structured Facts
* Editorial Content

Content is always compiled.

---

## ADR-011 — Canonical Data Flow

**Status:** Accepted

### Decision

Lenaba uses a three-stage data pipeline for all structured BehindTheName data.

### Canonical flow

BehindTheName
      ↓
fetch_results.parquet
      ↓
knowledge_master.parquet
      ↓
names.parquet

### Responsibilities

| Layer                      | Purpose                                             |
| -------------------------- | --------------------------------------------------- |
| `fetch_results.parquet`    | Immutable journal of parsed BTN facts.              |
| `knowledge_master.parquet` | Canonical knowledge store (Single Source of Truth). |
| `names.parquet`            | Serving database used by the website and apps.      |

### Rules

- BTN never writes directly to `names.parquet`.
- Every newly parsed fact is first stored in `fetch_results.parquet`.
- `master_writer.py` synchronizes new facts into `knowledge_master.parquet`.
- `build_family_completion.py` propagates missing structured fields into `names.parquet`.
- Existing populated fields are never overwritten (`fill only empty`).

### Why

This architecture prevents duplicated logic, avoids rebuilding knowledge from HTML, allows reproducible imports, and keeps one canonical source for structured name data.
