# Changelog

## [0.1.0] – Foundation Locked

### Added

* Lenaba brand identity
* Hidden L logo concept
* Brand Foundation documentation
* Data Standard documentation
* Roadmap
* Decision Log
* Data Pipeline structure
* `run_pipeline.py`
* Initial repository structure

### Dataset

* Imported `all-names.csv`
* 97,697 names
* Initial audit completed

## [0.1.5] – Data Pipeline Stable

### Added

- `scripts/lib/enrich.py`
- `scripts/lib/export.py`
- `scripts/lib/constants.py`
- Lookup Knowledge Base (`lookup.csv`)
- Automated unit tests (9 tests)

### Improved

- Modular pipeline architecture
- Shared constants
- SEO export
- Supabase export
- Parquet export
- Safer enrichment validation

### Status

Foundation complete. Ready for Supabase integration and Next.js MVP.

## [0.2.0] – Core Engine Complete

### Added

* SeedProvider
* Resolver Chain
* Pronunciation Engine
* Tag Generator
* SEO Writer
* Enrichment Pipeline
* Golden Queue
* Knowledge Seed v2 metadata

### Improved

* Offline-first enrichment
* IPA generation
* Human-readable pronunciation
* Semantic tagging
* SEO description generation

### Testing

* 20 automated tests passing

### Status

Core data engine complete. Ready for Next.js Mobile MVP.

## [0.2.5] – Content Foundation Complete

### Added

- Knowledge Vault architecture
- BaseProvider foundation
- Wikipedia Provider
- Wikidata Provider compatibility layer
- Editorial Queue (`campaign`, `stage`)
- Knowledge Batch v2
- Knowledge Audit tool
- Content Registry validation improvements

### Improved

- Provider Contract v1
- Safer Content Factory enrichment
- Stable offline-first enrichment workflow
- Better CSV handling (`low_memory=False`)
- Correct business-key validation (`id` + `name, gender`)

### Testing

- 22 automated tests passing
- 0 warnings

### Dataset

- 97,697 names maintained
- Golden 500 editorial workflow established
- IPA, Tags and SEO available for all Golden names
- Knowledge Vault expanded through batch enrichment

### Status

Content infrastructure complete. Ready to begin Golden 500 knowledge campaign and Mobile MVP.

## [0.2.6] – Repository Cleanup

### Added

- `scripts/lib/schema.py`
- `scripts/lib/paths.py`
- `scripts/cli.py`
- `builders/`, `audits/`, `pipeline/`, `importers/` structure

### Changed

- Unified project path management.
- Centralized data schema contract.
- Builders migrated into dedicated folder.
- Audit scripts separated from builders.
- Pipeline isolated into its own module.

### Improved

- Cleaner repository architecture.
- Single CLI entry point.
- Reduced duplicated path logic.
- Easier future GitHub Actions integration.

### Status

Repository architecture stabilized.
Ready for large-scale knowledge ingestion.

## [0.2.6] – Repository Cleanup

### Added

- `scripts/lib/schema.py`
- `scripts/lib/paths.py`
- `scripts/cli.py`
- `builders/`, `audits/`, `pipeline/`, `importers/` structure
- `knowledge_master.parquet`

### Changed

- Unified project path management.
- Centralized data schema contract.
- Builders migrated into dedicated folder.
- Audit scripts separated from builders.
- Pipeline isolated into its own module.

### Improved

- Single CLI entry point.
- Cleaner repository architecture.
- Imported 20,505 BehindTheName records.
- Knowledge Master now contains 20,645 canonical records.

### Status

Repository architecture stabilized.
Ready for Golden 500 enrichment and Mobile MVP.

# Changelog

## [0.1.0] – Foundation Locked

### Added

* Lenaba brand identity
* Hidden L logo concept
* Brand Foundation documentation
* Data Standard documentation
* Roadmap
* Decision Log
* Data Pipeline structure
* `run_pipeline.py`
* Initial repository structure

### Dataset

* Imported `all-names.csv`
* 97,697 names
* Initial audit completed

## [0.1.5] – Data Pipeline Stable

### Added

- `scripts/lib/enrich.py`
- `scripts/lib/export.py`
- `scripts/lib/constants.py`
- Lookup Knowledge Base (`lookup.csv`)
- Automated unit tests (9 tests)

### Improved

- Modular pipeline architecture
- Shared constants
- SEO export
- Supabase export
- Parquet export
- Safer enrichment validation

### Status

Foundation complete. Ready for Supabase integration and Next.js MVP.

## [0.2.0] – Core Engine Complete

### Added

* SeedProvider
* Resolver Chain
* Pronunciation Engine
* Tag Generator
* SEO Writer
* Enrichment Pipeline
* Golden Queue
* Knowledge Seed v2 metadata

### Improved

* Offline-first enrichment
* IPA generation
* Human-readable pronunciation
* Semantic tagging
* SEO description generation

### Testing

* 20 automated tests passing

### Status

Core data engine complete. Ready for Next.js Mobile MVP.

## [0.2.5] – Content Foundation Complete

### Added

- Knowledge Vault architecture
- BaseProvider foundation
- Wikipedia Provider
- Wikidata Provider compatibility layer
- Editorial Queue (`campaign`, `stage`)
- Knowledge Batch v2
- Knowledge Audit tool
- Content Registry validation improvements

### Improved

- Provider Contract v1
- Safer Content Factory enrichment
- Stable offline-first enrichment workflow
- Better CSV handling (`low_memory=False`)
- Correct business-key validation (`id` + `name, gender`)

### Testing

- 22 automated tests passing
- 0 warnings

### Dataset

- 97,697 names maintained
- Golden 500 editorial workflow established
- IPA, Tags and SEO available for all Golden names
- Knowledge Vault expanded through batch enrichment

### Status

Content infrastructure complete. Ready to begin Golden 500 knowledge campaign and Mobile MVP.

## [0.2.6] – Repository Cleanup

### Added

- `scripts/lib/schema.py`
- `scripts/lib/paths.py`
- `scripts/cli.py`
- `builders/`, `audits/`, `pipeline/`, `importers/` structure

### Changed

- Unified project path management.
- Centralized data schema contract.
- Builders migrated into dedicated folder.
- Audit scripts separated from builders.
- Pipeline isolated into its own module.

### Improved

- Cleaner repository architecture.
- Single CLI entry point.
- Reduced duplicated path logic.
- Easier future GitHub Actions integration.

### Status

Repository architecture stabilized.
Ready for large-scale knowledge ingestion.

## [0.2.6] – Repository Cleanup

### Added

- `scripts/lib/schema.py`
- `scripts/lib/paths.py`
- `scripts/cli.py`
- `builders/`, `audits/`, `pipeline/`, `importers/` structure
- `knowledge_master.parquet`

### Changed

- Unified project path management.
- Centralized data schema contract.
- Builders migrated into dedicated folder.
- Audit scripts separated from builders.
- Pipeline isolated into its own module.

### Improved

- Single CLI entry point.
- Cleaner repository architecture.
- Imported 20,505 BehindTheName records.
- Knowledge Master now contains 20,645 canonical records.

### Status

Repository architecture stabilized.
Ready for Golden 500 enrichment and Mobile MVP.

## [0.3.0] – Autonomous Knowledge Engine

### Added

- Knowledge Master (`knowledge_master.parquet`)
- BehindTheName import (20,505 names)
- Completion Levels (Bronze / Silver / Gold / Platinum)
- Name Graph (`name_graph.parquet`)
- BehindTheName Forms Merge
- Taxonomy Layer v1
- CLI command runner
- Builders/Audits architecture

### Improved

- Unified path management
- Canonical knowledge merge
- Resume-safe Golden Pack pipeline
- Form normalization
- Graph-based relationships
- Repository modularization

### Dataset

- 20,645 canonical knowledge records
- 255,803 graph relationships
- 20,501 equivalents imported
- 6,167 script mappings
- 17,444 names with taxonomy coverage

### Decisions

- Taxonomy v1 frozen as a future asset.
- Post-MVP integration planned for Taxonomy v2.

### Status

Autonomous Knowledge Engine complete.

Ready to begin Next.js Mobile MVP.

## [0.4.5] – Smart Knowledge Expansion

### Added

* `build_canonical_families.py`
* `canonical_families.parquet`
* Data Integrity Gate (`validate_master.py`)
* `audit_integrity.py`
* Graph optimization (Union-Find + progress logging)

### Improved

* BehindTheName ingestion workflow
* Family-first enrichment architecture
* Stable graph traversal
* NaN-safe processing

### Architecture

* 97,697 names confirmed as the single source of truth.
* BehindTheName designated as a donor knowledge source.
* `knowledge_master` redefined as a temporary enrichment cache.
* Canonical families prepared for Smart Queue.

### Status

Sprint v0.4.5 completed.
Ready for Smart Queue and Merge Engine.

## v0.5.0 — Execution Layer Foundation

### Added

- Execution Queue (4,261 tasks)
- Execution Batches (111 language batches)
- Language Resolver
- Smart Queue V3
- Behind Executor MVP
- Behind Cache
- HTML Snapshot test fixture

### Changed

- Switched from BehindTheName API strategy to HTML-based Smart Fetcher.
- Introduced resumable execution using `fetch_state.json`.

### Next

- Production HTML parser.
- Incremental fetch pipeline.
- Merge fetched data into knowledge_master.

# Changelog

## v0.6 — Data Platform

### Added

- Data Platform V1 architecture
- Official data layer documentation
- Single Source of Truth concept

### Changed

- Knowledge Master migration plan to 97,697 names
- Formal separation of data layers

### Fixed

- Documented historical pipeline divergence.

## v1.0 Data Platform Freeze

### Added

- Production Master (97,697)
- Family Lookup V2
- Family Merge Layer
- Legacy Patch Engine
- Platform Audit

### Changed

- Single Source of Truth migrated to Production Master.
- Family coverage increased from 0.10% to 89.96%.

### Fixed

- Merge idempotency
- Schema normalization
- Confidence normalization

# Changelog

All notable changes to Lenaba are documented here.

---

## [v0.8-autopilot] — Sprint 8

### Added

* Smart Queue v3
* Execution Queue
* Overnight Mode
* Resume support
* Human Delay
* Lunch & Coffee Break scheduling
* Family Verification
* Candidate Discovery
* Behind Cache replay
* Incremental Master updates
* Family Graph verification
* Etymology Graph synchronization

### Improved

* BehindTheName parser
* batch prioritization
* cache handling
* incremental merge
* execution stability
* list normalization
* parquet compatibility

### Fixed

* recursive batch loop
* cache replay crashes
* numpy/list handling
* Arrow serialization
* empty-array validation
* completed batch tracking

### Result

The BehindTheName execution queue now completes automatically without manual intervention, making Lenaba's first autonomous Data Engine operational.
