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