# Lenaba Data Schema

> Auto-generated. Do not edit manually.

Files scanned: **44**

## Summary

| File | Rows | Columns | Primary key |
|---|---:|---:|---|
| `data/cache/knowledge_cache.parquet` | 201 | 7 | `name` |
| `data/cache/knowledge_cache.parquet` | ERROR | - | `-` |
| `data/cleaned/name_stats.parquet` | 97697 | 6 | `name` |
| `data/cleaned/name_stats.parquet` | ERROR | - | `-` |
| `data/cleaned/name_variants.parquet` | 28023 | 3 | `canonical_name` |
| `data/cleaned/name_variants.parquet` | ERROR | - | `-` |
| `data/cleaned/names.parquet` | 97697 | 10 | `name` |
| `data/cleaned/names.parquet` | ERROR | - | `-` |
| `data/cleaned/names_cleaned.csv` | 97697 | 18 | `name` |
| `data/cleaned/names_cleaned.csv` | ERROR | - | `-` |
| `data/cleaned/names_cleaned.parquet` | 97697 | 18 | `name` |
| `data/cleaned/names_cleaned.parquet` | ERROR | - | `-` |
| `data/cleaned/phonetics.parquet` | 153484 | 4 | `name` |
| `data/cleaned/phonetics.parquet` | ERROR | - | `-` |
| `data/content/content_registry.csv` | 97697 | 46 | `name` |
| `data/content/content_registry.csv` | ERROR | - | `-` |
| `data/content/content_registry.parquet` | 97697 | 46 | `name` |
| `data/content/content_registry.parquet` | ERROR | - | `-` |
| `data/content/golden_500.csv` | 500 | 41 | `name` |
| `data/content/golden_500.csv` | ERROR | - | `-` |
| `data/content/packs/golden_pack_001.parquet` | 100 | 46 | `name` |
| `data/content/packs/golden_pack_001.parquet` | ERROR | - | `-` |
| `data/content/packs/golden_pack_002.parquet` | 200 | 46 | `name` |
| `data/content/packs/golden_pack_002.parquet` | ERROR | - | `-` |
| `data/enriched/lookup.csv` | 3 | 13 | `name` |
| `data/enriched/lookup.csv` | ERROR | - | `-` |
| `data/enriched/names.parquet` | 97697 | 30 | `name` |
| `data/enriched/names.parquet` | ERROR | - | `-` |
| `data/enriched/names_enriched.csv` | 97697 | 28 | `name` |
| `data/enriched/names_enriched.csv` | ERROR | - | `-` |
| `data/enriched/names_seo.csv` | 97697 | 9 | `name` |
| `data/enriched/names_seo.csv` | ERROR | - | `-` |
| `data/enriched/names_supabase.csv` | 97697 | 27 | `name` |
| `data/enriched/names_supabase.csv` | ERROR | - | `-` |
| `data/imports/behind_the_name/dataset3.csv` | 20505 | 14 | `name` |
| `data/imports/behind_the_name/dataset3.csv` | ERROR | - | `-` |
| `data/knowledge/canonical_families.parquet` | 20644 | 4 | `family_id` |
| `data/knowledge/canonical_families.parquet` | ERROR | - | `-` |
| `data/knowledge/etymology_graph.parquet` | 419064 | 5 | `Unknown` |
| `data/knowledge/etymology_graph.parquet` | ERROR | - | `-` |
| `data/knowledge/execution_batches.parquet` | 111 | 4 | `Unknown` |
| `data/knowledge/execution_batches.parquet` | ERROR | - | `-` |
| `data/knowledge/execution_queue.parquet` | 5299 | 9 | `family_id` |
| `data/knowledge/execution_queue.parquet` | ERROR | - | `-` |
| `data/knowledge/family_coverage.parquet` | 8140 | 4 | `family_id` |
| `data/knowledge/family_coverage.parquet` | ERROR | - | `-` |
| `data/knowledge/family_graph.parquet` | 20359 | 15 | `name` |
| `data/knowledge/family_graph.parquet` | ERROR | - | `-` |
| `data/knowledge/family_lookup.parquet` | 130008 | 2 | `alias` |
| `data/knowledge/family_lookup.parquet` | ERROR | - | `-` |
| `data/knowledge/integrity_reports/duplicate_ids.csv` | 20552 | 58 | `name` |
| `data/knowledge/integrity_reports/duplicate_ids.csv` | ERROR | - | `-` |
| `data/knowledge/integrity_reports/missing_names.csv` | 1 | 58 | `name` |
| `data/knowledge/integrity_reports/missing_names.csv` | ERROR | - | `-` |
| `data/knowledge/knowledge_master.parquet` | 97697 | 55 | `name` |
| `data/knowledge/knowledge_master.parquet` | ERROR | - | `-` |
| `data/knowledge/language_resolver.parquet` | 17495 | 5 | `name` |
| `data/knowledge/language_resolver.parquet` | ERROR | - | `-` |
| `data/knowledge/name_graph.parquet` | 255803 | 3 | `Unknown` |
| `data/knowledge/name_graph.parquet` | ERROR | - | `-` |
| `data/knowledge/name_taxonomy.parquet` | 934376 | 4 | `name` |
| `data/knowledge/name_taxonomy.parquet` | ERROR | - | `-` |
| `data/knowledge/new_name_candidates.parquet` | 380 | 10 | `name` |
| `data/knowledge/new_name_candidates.parquet` | ERROR | - | `-` |
| `data/knowledge/smart_queue.parquet` | 4261 | 6 | `family_id` |
| `data/knowledge/smart_queue.parquet` | ERROR | - | `-` |
| `data/knowledge/smart_queue_v2.parquet` | 4261 | 10 | `family_id` |
| `data/knowledge/smart_queue_v2.parquet` | ERROR | - | `-` |
| `data/knowledge/smart_queue_v3.parquet` | 5299 | 12 | `family_id` |
| `data/knowledge/smart_queue_v3.parquet` | ERROR | - | `-` |
| `data/knowledge/template_candidates.csv` | 60 | 58 | `name` |
| `data/knowledge/template_candidates.csv` | ERROR | - | `-` |
| `data/outputs/behind_cache.parquet` | 31 | 15 | `canonical_name` |
| `data/outputs/behind_cache.parquet` | ERROR | - | `-` |
| `data/outputs/fetch_results.parquet` | 53 | 14 | `family_id` |
| `data/outputs/fetch_results.parquet` | ERROR | - | `-` |
| `data/outputs/legacy_patch.parquet` | 20644 | 9 | `name` |
| `data/outputs/legacy_patch.parquet` | ERROR | - | `-` |
| `data/raw/all-names.csv` | 97697 | 15 | `name` |
| `data/raw/all-names.csv` | ERROR | - | `-` |
| `data/reports/missing_meanings.csv` | 97694 | 2 | `name` |
| `data/reports/missing_meanings.csv` | ERROR | - | `-` |
| `data/seed/golden_500.csv` | 500 | 5 | `name` |
| `data/seed/golden_500.csv` | ERROR | - | `-` |
| `data/seed/knowledge_seed.csv` | 51 | 14 | `name` |
| `data/seed/knowledge_seed.csv` | ERROR | - | `-` |
| `data/seed/knowledge_seed.parquet` | 51 | 14 | `name` |
| `data/seed/knowledge_seed.parquet` | ERROR | - | `-` |

## data/cache/knowledge_cache.parquet

- **Rows:** 201
- **Columns:** 7
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `name` | `str` |
| `meaning` | `str` |
| `origin` | `str` |
| `ipa` | `str` |
| `pronunciation` | `str` |
| `source` | `str` |
| `verified` | `bool` |

### Sample

## data/cache/knowledge_cache.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/cleaned/name_stats.parquet

- **Rows:** 97,697
- **Columns:** 6
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `id` | `int64` |
| `name` | `str` |
| `popularity_score` | `int64` |
| `first_seen_year` | `int64` |
| `last_seen_year` | `int64` |
| `peak_year` | `int64` |

### Sample

## data/cleaned/name_stats.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/cleaned/name_variants.parquet

- **Rows:** 28,023
- **Columns:** 3
- **Primary key:** `canonical_name`

### Columns

| Column | Type |
|---|---|
| `canonical_id` | `int64` |
| `canonical_name` | `str` |
| `variant` | `str` |

### Sample

## data/cleaned/name_variants.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/cleaned/names.parquet

- **Rows:** 97,697
- **Columns:** 10
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `id` | `int64` |
| `name` | `str` |
| `gender` | `str` |
| `slug` | `str` |
| `first_letter` | `str` |
| `length` | `int64` |
| `syllables` | `int64` |
| `is_biblical` | `bool` |
| `is_palindrome` | `bool` |
| `is_unisex` | `bool` |

### Sample

## data/cleaned/names.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/cleaned/names_cleaned.csv

- **Rows:** 97,697
- **Columns:** 18
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `id` | `int64` |
| `gender` | `str` |
| `name` | `str` |
| `variants` | `str` |
| `popularity_score` | `int64` |
| `first_seen_year` | `int64` |
| `last_seen_year` | `int64` |
| `peak_year` | `int64` |
| `is_biblical` | `bool` |
| `is_palindrome` | `bool` |
| `phonetic` | `str` |
| `first_letter` | `str` |
| `stresses` | `str` |
| `syllables` | `int64` |
| `alliteration` | `float64` |
| `is_unisex` | `bool` |
| `slug` | `str` |
| `length` | `int64` |

### Sample

## data/cleaned/names_cleaned.csv

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/cleaned/names_cleaned.parquet

- **Rows:** 97,697
- **Columns:** 18
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `id` | `int64` |
| `gender` | `str` |
| `name` | `str` |
| `variants` | `object` |
| `popularity_score` | `int64` |
| `first_seen_year` | `int64` |
| `last_seen_year` | `int64` |
| `peak_year` | `int64` |
| `is_biblical` | `bool` |
| `is_palindrome` | `bool` |
| `phonetic` | `object` |
| `first_letter` | `str` |
| `stresses` | `object` |
| `syllables` | `int64` |
| `alliteration` | `float64` |
| `is_unisex` | `bool` |
| `slug` | `str` |
| `length` | `int64` |

### Sample

## data/cleaned/names_cleaned.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/cleaned/phonetics.parquet

- **Rows:** 153,484
- **Columns:** 4
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `name_id` | `int64` |
| `name` | `str` |
| `phonetic` | `str` |
| `stress_pattern` | `str` |

### Sample

## data/cleaned/phonetics.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/content/content_registry.csv

- **Rows:** 97,697
- **Columns:** 46
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `id` | `int64` |
| `gender` | `str` |
| `name` | `str` |
| `variants` | `str` |
| `popularity_score` | `int64` |
| `first_seen_year` | `int64` |
| `last_seen_year` | `int64` |
| `peak_year` | `int64` |
| `is_biblical` | `bool` |
| `is_palindrome` | `bool` |
| `phonetic` | `str` |
| `first_letter` | `str` |
| `stresses` | `str` |
| `syllables` | `int64` |
| `alliteration` | `float64` |
| `is_unisex` | `bool` |
| `slug` | `str` |
| `length` | `int64` |
| `origin` | `str` |
| `country` | `str` |
| `meaning` | `str` |
| `pronunciation` | `str` |
| `verified` | `object` |
| `confidence` | `float64` |
| `source` | `str` |
| `source_url` | `float64` |
| `last_reviewed` | `str` |
| `notes` | `str` |
| `priority` | `int64` |
| `tier` | `str` |
| `status` | `str` |
| `meaning_done` | `bool` |
| `origin_done` | `bool` |
| `ipa_done` | `bool` |
| `tags_done` | `bool` |
| `seo_done` | `bool` |
| `reviewed` | `bool` |
| `published` | `bool` |
| `processed_at` | `str` |
| `pipeline_version` | `str` |
| `content_hash` | `str` |
| `ipa` | `str` |
| `tags` | `str` |
| `seo_description` | `str` |
| `campaign` | `str` |
| `stage` | `str` |

### Sample

## data/content/content_registry.csv

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/content/content_registry.parquet

- **Rows:** 97,697
- **Columns:** 46
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `id` | `int64` |
| `gender` | `str` |
| `name` | `str` |
| `variants` | `str` |
| `popularity_score` | `int64` |
| `first_seen_year` | `int64` |
| `last_seen_year` | `int64` |
| `peak_year` | `int64` |
| `is_biblical` | `bool` |
| `is_palindrome` | `bool` |
| `phonetic` | `str` |
| `first_letter` | `str` |
| `stresses` | `str` |
| `syllables` | `int64` |
| `alliteration` | `float64` |
| `is_unisex` | `bool` |
| `slug` | `str` |
| `length` | `int64` |
| `origin` | `str` |
| `country` | `str` |
| `meaning` | `str` |
| `pronunciation` | `str` |
| `verified` | `object` |
| `confidence` | `float64` |
| `source` | `str` |
| `source_url` | `float64` |
| `last_reviewed` | `str` |
| `notes` | `str` |
| `priority` | `int64` |
| `tier` | `str` |
| `status` | `str` |
| `meaning_done` | `bool` |
| `origin_done` | `bool` |
| `ipa_done` | `bool` |
| `tags_done` | `bool` |
| `seo_done` | `bool` |
| `reviewed` | `bool` |
| `published` | `bool` |
| `processed_at` | `str` |
| `pipeline_version` | `str` |
| `content_hash` | `str` |
| `ipa` | `str` |
| `tags` | `str` |
| `seo_description` | `str` |
| `campaign` | `str` |
| `stage` | `str` |

### Sample

## data/content/content_registry.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/content/golden_500.csv

- **Rows:** 500
- **Columns:** 41
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `id` | `int64` |
| `gender` | `str` |
| `name` | `str` |
| `variants` | `str` |
| `popularity_score` | `int64` |
| `first_seen_year` | `int64` |
| `last_seen_year` | `int64` |
| `peak_year` | `int64` |
| `is_biblical` | `bool` |
| `is_palindrome` | `bool` |
| `phonetic` | `str` |
| `first_letter` | `str` |
| `stresses` | `str` |
| `syllables` | `int64` |
| `alliteration` | `float64` |
| `is_unisex` | `bool` |
| `slug` | `str` |
| `length` | `int64` |
| `origin` | `str` |
| `country` | `str` |
| `meaning` | `str` |
| `pronunciation` | `str` |
| `verified` | `object` |
| `confidence` | `float64` |
| `source` | `str` |
| `source_url` | `float64` |
| `last_reviewed` | `str` |
| `notes` | `str` |
| `priority` | `int64` |
| `tier` | `str` |
| `status` | `str` |
| `meaning_done` | `bool` |
| `origin_done` | `bool` |
| `ipa_done` | `bool` |
| `tags_done` | `bool` |
| `seo_done` | `bool` |
| `reviewed` | `bool` |
| `published` | `bool` |
| `processed_at` | `float64` |
| `pipeline_version` | `str` |
| `content_hash` | `str` |

### Sample

## data/content/golden_500.csv

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/content/packs/golden_pack_001.parquet

- **Rows:** 100
- **Columns:** 46
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `id` | `int64` |
| `gender` | `str` |
| `name` | `str` |
| `variants` | `str` |
| `popularity_score` | `int64` |
| `first_seen_year` | `int64` |
| `last_seen_year` | `int64` |
| `peak_year` | `int64` |
| `is_biblical` | `bool` |
| `is_palindrome` | `bool` |
| `phonetic` | `str` |
| `first_letter` | `str` |
| `stresses` | `str` |
| `syllables` | `int64` |
| `alliteration` | `float64` |
| `is_unisex` | `bool` |
| `slug` | `str` |
| `length` | `int64` |
| `origin` | `str` |
| `country` | `str` |
| `meaning` | `str` |
| `pronunciation` | `str` |
| `verified` | `bool` |
| `confidence` | `float64` |
| `source` | `str` |
| `source_url` | `float64` |
| `last_reviewed` | `str` |
| `notes` | `str` |
| `priority` | `int64` |
| `tier` | `str` |
| `status` | `str` |
| `meaning_done` | `bool` |
| `origin_done` | `bool` |
| `ipa_done` | `bool` |
| `tags_done` | `bool` |
| `seo_done` | `bool` |
| `reviewed` | `bool` |
| `published` | `bool` |
| `processed_at` | `str` |
| `pipeline_version` | `str` |
| `content_hash` | `str` |
| `ipa` | `str` |
| `tags` | `str` |
| `seo_description` | `str` |
| `campaign` | `str` |
| `stage` | `str` |

### Sample

## data/content/packs/golden_pack_001.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/content/packs/golden_pack_002.parquet

- **Rows:** 200
- **Columns:** 46
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `id` | `int64` |
| `gender` | `str` |
| `name` | `str` |
| `variants` | `str` |
| `popularity_score` | `int64` |
| `first_seen_year` | `int64` |
| `last_seen_year` | `int64` |
| `peak_year` | `int64` |
| `is_biblical` | `bool` |
| `is_palindrome` | `bool` |
| `phonetic` | `str` |
| `first_letter` | `str` |
| `stresses` | `str` |
| `syllables` | `int64` |
| `alliteration` | `float64` |
| `is_unisex` | `bool` |
| `slug` | `str` |
| `length` | `int64` |
| `origin` | `str` |
| `country` | `str` |
| `meaning` | `str` |
| `pronunciation` | `str` |
| `verified` | `bool` |
| `confidence` | `float64` |
| `source` | `str` |
| `source_url` | `float64` |
| `last_reviewed` | `str` |
| `notes` | `str` |
| `priority` | `int64` |
| `tier` | `str` |
| `status` | `str` |
| `meaning_done` | `bool` |
| `origin_done` | `bool` |
| `ipa_done` | `bool` |
| `tags_done` | `bool` |
| `seo_done` | `bool` |
| `reviewed` | `bool` |
| `published` | `bool` |
| `processed_at` | `str` |
| `pipeline_version` | `str` |
| `content_hash` | `str` |
| `ipa` | `str` |
| `tags` | `str` |
| `seo_description` | `str` |
| `campaign` | `str` |
| `stage` | `str` |

### Sample

## data/content/packs/golden_pack_002.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/enriched/lookup.csv

- **Rows:** 3
- **Columns:** 13
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `name` | `str` |
| `gender` | `str` |
| `origin` | `str` |
| `country` | `str` |
| `meaning` | `str` |
| `pronunciation` | `str` |
| `variants` | `str` |
| `verified` | `bool` |
| `confidence` | `int64` |
| `source` | `str` |
| `source_url` | `float64` |
| `last_reviewed` | `str` |
| `notes` | `str` |

### Sample

## data/enriched/lookup.csv

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/enriched/names.parquet

- **Rows:** 97,697
- **Columns:** 30
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `id` | `int64` |
| `gender` | `str` |
| `name` | `str` |
| `variants` | `str` |
| `popularity_score` | `int64` |
| `first_seen_year` | `int64` |
| `last_seen_year` | `int64` |
| `peak_year` | `int64` |
| `is_biblical` | `bool` |
| `is_palindrome` | `bool` |
| `first_letter` | `str` |
| `stresses` | `str` |
| `syllables` | `int64` |
| `alliteration` | `float64` |
| `is_unisex` | `bool` |
| `slug` | `str` |
| `length` | `int64` |
| `origin` | `str` |
| `country` | `str` |
| `meaning` | `str` |
| `pronunciation` | `str` |
| `verified` | `object` |
| `confidence` | `float64` |
| `source` | `str` |
| `source_url` | `float64` |
| `last_reviewed` | `str` |
| `notes` | `str` |
| `tags` | `object` |
| `ipa` | `str` |
| `phonetic_lookup` | `str` |

### Sample

## data/enriched/names.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/enriched/names_enriched.csv

- **Rows:** 97,697
- **Columns:** 28
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `id` | `int64` |
| `gender` | `str` |
| `name` | `str` |
| `variants` | `str` |
| `popularity_score` | `int64` |
| `first_seen_year` | `int64` |
| `last_seen_year` | `int64` |
| `peak_year` | `int64` |
| `is_biblical` | `bool` |
| `is_palindrome` | `bool` |
| `phonetic` | `str` |
| `first_letter` | `str` |
| `stresses` | `str` |
| `syllables` | `int64` |
| `alliteration` | `float64` |
| `is_unisex` | `bool` |
| `slug` | `str` |
| `length` | `int64` |
| `origin` | `str` |
| `country` | `str` |
| `meaning` | `str` |
| `pronunciation` | `str` |
| `verified` | `object` |
| `confidence` | `float64` |
| `source` | `str` |
| `source_url` | `float64` |
| `last_reviewed` | `str` |
| `notes` | `str` |

### Sample

## data/enriched/names_enriched.csv

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/enriched/names_seo.csv

- **Rows:** 97,697
- **Columns:** 9
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `name` | `str` |
| `slug` | `str` |
| `origin` | `str` |
| `meaning` | `str` |
| `gender` | `str` |
| `first_letter` | `str` |
| `title` | `str` |
| `description` | `str` |
| `canonical` | `str` |

### Sample

## data/enriched/names_seo.csv

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/enriched/names_supabase.csv

- **Rows:** 97,697
- **Columns:** 27
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `id` | `int64` |
| `name` | `str` |
| `gender` | `str` |
| `origin` | `str` |
| `country` | `str` |
| `meaning` | `str` |
| `pronunciation` | `str` |
| `variants` | `str` |
| `popularity_score` | `int64` |
| `first_seen_year` | `int64` |
| `last_seen_year` | `int64` |
| `peak_year` | `int64` |
| `is_biblical` | `bool` |
| `is_palindrome` | `bool` |
| `is_unisex` | `bool` |
| `phonetic` | `str` |
| `stresses` | `str` |
| `syllables` | `int64` |
| `first_letter` | `str` |
| `length` | `int64` |
| `slug` | `str` |
| `verified` | `object` |
| `confidence` | `float64` |
| `source` | `str` |
| `source_url` | `float64` |
| `last_reviewed` | `str` |
| `notes` | `str` |

### Sample

## data/enriched/names_supabase.csv

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/imports/behind_the_name/dataset3.csv

- **Rows:** 20,505
- **Columns:** 14
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `Unnamed: 0` | `int64` |
| `equivalents` | `str` |
| `feminine_forms` | `str` |
| `full_forms` | `str` |
| `gender` | `str` |
| `masculine_forms` | `str` |
| `meaning` | `str` |
| `name` | `str` |
| `origin` | `str` |
| `other_forms` | `str` |
| `other_readings` | `str` |
| `pronounciation` | `str` |
| `scripts` | `str` |
| `short_forms` | `str` |

### Sample

## data/imports/behind_the_name/dataset3.csv

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/canonical_families.parquet

- **Rows:** 20,644
- **Columns:** 4
- **Primary key:** `family_id`

### Columns

| Column | Type |
|---|---|
| `family_id` | `str` |
| `canonical_name` | `str` |
| `alias` | `str` |
| `is_canonical` | `bool` |

### Sample

## data/knowledge/canonical_families.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/etymology_graph.parquet

- **Rows:** 419,064
- **Columns:** 5
- **Primary key:** `Unknown`

### Columns

| Column | Type |
|---|---|
| `from_name` | `str` |
| `relation` | `str` |
| `to_name` | `str` |
| `target_language` | `object` |
| `source` | `str` |

### Sample

## data/knowledge/etymology_graph.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/execution_batches.parquet

- **Rows:** 111
- **Columns:** 4
- **Primary key:** `Unknown`

### Columns

| Column | Type |
|---|---|
| `batch_key` | `str` |
| `tasks` | `int64` |
| `names` | `int64` |
| `avg_gain` | `float64` |

### Sample

## data/knowledge/execution_batches.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/execution_queue.parquet

- **Rows:** 5,299
- **Columns:** 9
- **Primary key:** `family_id`

### Columns

| Column | Type |
|---|---|
| `family_id` | `str` |
| `canonical_name` | `str` |
| `family_size` | `int64` |
| `executor` | `str` |
| `batch_key` | `str` |
| `dominant_language` | `float64` |
| `missing` | `object` |
| `priority` | `int64` |
| `estimated_gain` | `int64` |

### Sample

## data/knowledge/execution_queue.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/family_coverage.parquet

- **Rows:** 8,140
- **Columns:** 4
- **Primary key:** `family_id`

### Columns

| Column | Type |
|---|---|
| `family_id` | `str` |
| `canonical_name` | `str` |
| `family_size` | `int64` |
| `missing` | `object` |

### Sample

## data/knowledge/family_coverage.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/family_graph.parquet

- **Rows:** 20,359
- **Columns:** 15
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `name` | `str` |
| `root` | `object` |
| `variant` | `object` |
| `language_variant` | `object` |
| `equivalent` | `object` |
| `related` | `object` |
| `diminutive` | `object` |
| `feminine` | `object` |
| `masculine` | `object` |
| `surname` | `object` |
| `verified_family` | `object` |
| `family_status` | `str` |
| `family_source` | `str` |
| `family_last_verified` | `str` |
| `family_id` | `object` |

### Sample

## data/knowledge/family_graph.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/family_lookup.parquet

- **Rows:** 130,008
- **Columns:** 2
- **Primary key:** `alias`

### Columns

| Column | Type |
|---|---|
| `alias` | `str` |
| `canonical_name` | `str` |

### Sample

## data/knowledge/family_lookup.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/integrity_reports/duplicate_ids.csv

- **Rows:** 20,552
- **Columns:** 58
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `name` | `str` |
| `meaning` | `str` |
| `origin` | `str` |
| `ipa` | `str` |
| `pronunciation` | `str` |
| `variants` | `str` |
| `tags` | `str` |
| `source` | `str` |
| `verified` | `bool` |
| `language` | `str` |
| `tier` | `float64` |
| `confidence` | `float64` |
| `resolver` | `str` |
| `updated_at` | `str` |
| `id` | `float64` |
| `gender` | `str` |
| `popularity_score` | `float64` |
| `first_seen_year` | `float64` |
| `last_seen_year` | `float64` |
| `peak_year` | `float64` |
| `is_biblical` | `float64` |
| `is_palindrome` | `float64` |
| `phonetic` | `str` |
| `first_letter` | `float64` |
| `stresses` | `str` |
| `syllables` | `float64` |
| `alliteration` | `float64` |
| `is_unisex` | `float64` |
| `slug` | `float64` |
| `length` | `float64` |
| `country` | `float64` |
| `source_url` | `float64` |
| `last_reviewed` | `float64` |
| `notes` | `float64` |
| `priority` | `float64` |
| `status` | `float64` |
| `meaning_done` | `object` |
| `origin_done` | `object` |
| `ipa_done` | `object` |
| `tags_done` | `object` |
| `seo_done` | `object` |
| `reviewed` | `object` |
| `published` | `object` |
| `processed_at` | `float64` |
| `pipeline_version` | `float64` |
| `content_hash` | `float64` |
| `seo_description` | `float64` |
| `campaign` | `float64` |
| `stage` | `float64` |
| `equivalents` | `str` |
| `scripts` | `str` |
| `completion_level` | `str` |
| `short_forms` | `str` |
| `full_forms` | `str` |
| `feminine_forms` | `str` |
| `masculine_forms` | `str` |
| `other_forms` | `str` |
| `other_readings` | `str` |

### Sample

## data/knowledge/integrity_reports/duplicate_ids.csv

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/integrity_reports/missing_names.csv

- **Rows:** 1
- **Columns:** 58
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `name` | `float64` |
| `meaning` | `str` |
| `origin` | `str` |
| `ipa` | `float64` |
| `pronunciation` | `float64` |
| `variants` | `str` |
| `tags` | `float64` |
| `source` | `str` |
| `verified` | `bool` |
| `language` | `float64` |
| `tier` | `float64` |
| `confidence` | `float64` |
| `resolver` | `float64` |
| `updated_at` | `float64` |
| `id` | `float64` |
| `gender` | `str` |
| `popularity_score` | `float64` |
| `first_seen_year` | `float64` |
| `last_seen_year` | `float64` |
| `peak_year` | `float64` |
| `is_biblical` | `float64` |
| `is_palindrome` | `float64` |
| `phonetic` | `float64` |
| `first_letter` | `float64` |
| `stresses` | `float64` |
| `syllables` | `float64` |
| `alliteration` | `float64` |
| `is_unisex` | `float64` |
| `slug` | `float64` |
| `length` | `float64` |
| `country` | `float64` |
| `source_url` | `float64` |
| `last_reviewed` | `float64` |
| `notes` | `float64` |
| `priority` | `float64` |
| `status` | `float64` |
| `meaning_done` | `float64` |
| `origin_done` | `float64` |
| `ipa_done` | `float64` |
| `tags_done` | `float64` |
| `seo_done` | `float64` |
| `reviewed` | `float64` |
| `published` | `float64` |
| `processed_at` | `float64` |
| `pipeline_version` | `float64` |
| `content_hash` | `float64` |
| `seo_description` | `float64` |
| `campaign` | `float64` |
| `stage` | `float64` |
| `equivalents` | `str` |
| `scripts` | `str` |
| `completion_level` | `str` |
| `short_forms` | `float64` |
| `full_forms` | `float64` |
| `feminine_forms` | `float64` |
| `masculine_forms` | `float64` |
| `other_forms` | `float64` |
| `other_readings` | `float64` |

### Sample

## data/knowledge/integrity_reports/missing_names.csv

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/knowledge_master.parquet

- **Rows:** 97,697
- **Columns:** 55
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `id` | `int64` |
| `gender` | `str` |
| `name` | `str` |
| `variants` | `str` |
| `popularity_score` | `int64` |
| `first_seen_year` | `int64` |
| `last_seen_year` | `int64` |
| `peak_year` | `int64` |
| `is_biblical` | `bool` |
| `is_palindrome` | `bool` |
| `phonetic` | `str` |
| `first_letter` | `str` |
| `stresses` | `str` |
| `syllables` | `int64` |
| `alliteration` | `float64` |
| `is_unisex` | `bool` |
| `slug` | `str` |
| `length` | `int64` |
| `origin` | `str` |
| `country` | `str` |
| `meaning` | `str` |
| `pronunciation` | `str` |
| `verified` | `object` |
| `confidence` | `float64` |
| `source` | `str` |
| `source_url` | `float64` |
| `last_reviewed` | `str` |
| `notes` | `str` |
| `equivalents` | `object` |
| `_score` | `float64` |
| `priority` | `float64` |
| `tier` | `str` |
| `status` | `str` |
| `meaning_done` | `object` |
| `origin_done` | `object` |
| `ipa_done` | `object` |
| `tags_done` | `object` |
| `seo_done` | `object` |
| `reviewed` | `object` |
| `published` | `object` |
| `processed_at` | `str` |
| `pipeline_version` | `str` |
| `content_hash` | `str` |
| `ipa` | `str` |
| `tags` | `str` |
| `seo_description` | `str` |
| `campaign` | `str` |
| `stage` | `str` |
| `family_id` | `object` |
| `batch_key` | `object` |
| `api_status` | `object` |
| `fetched_at` | `object` |
| `usage` | `str` |
| `root` | `str` |
| `other_languages` | `object` |

### Sample

## data/knowledge/knowledge_master.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/language_resolver.parquet

- **Rows:** 17,495
- **Columns:** 5
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `name` | `str` |
| `dominant_language` | `str` |
| `confidence` | `float64` |
| `sources_found` | `int64` |
| `languages` | `object` |

### Sample

## data/knowledge/language_resolver.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/name_graph.parquet

- **Rows:** 255,803
- **Columns:** 3
- **Primary key:** `Unknown`

### Columns

| Column | Type |
|---|---|
| `from_name` | `str` |
| `to_name` | `str` |
| `relation` | `str` |

### Sample

## data/knowledge/name_graph.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/name_taxonomy.parquet

- **Rows:** 934,376
- **Columns:** 4
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `name` | `str` |
| `taxonomy_type` | `str` |
| `taxonomy_value` | `str` |
| `source_field` | `str` |

### Sample

## data/knowledge/name_taxonomy.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/new_name_candidates.parquet

- **Rows:** 380
- **Columns:** 10
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `name` | `str` |
| `discovered_from` | `str` |
| `relation` | `str` |
| `language` | `str` |
| `source` | `str` |
| `first_seen_batch` | `object` |
| `first_seen_family` | `str` |
| `discovered_at` | `str` |
| `family` | `str` |
| `status` | `str` |

### Sample

## data/knowledge/new_name_candidates.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/smart_queue.parquet

- **Rows:** 4,261
- **Columns:** 6
- **Primary key:** `family_id`

### Columns

| Column | Type |
|---|---|
| `family_id` | `str` |
| `canonical_name` | `str` |
| `family_size` | `int64` |
| `completion_level` | `str` |
| `missing` | `object` |
| `priority` | `int64` |

### Sample

## data/knowledge/smart_queue.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/smart_queue_v2.parquet

- **Rows:** 4,261
- **Columns:** 10
- **Primary key:** `family_id`

### Columns

| Column | Type |
|---|---|
| `family_id` | `str` |
| `canonical_name` | `str` |
| `family_size` | `int64` |
| `completion_level` | `str` |
| `missing` | `object` |
| `reason` | `str` |
| `can_generate_local` | `bool` |
| `api_needed` | `bool` |
| `estimated_gain` | `int64` |
| `priority` | `int64` |

### Sample

## data/knowledge/smart_queue_v2.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/smart_queue_v3.parquet

- **Rows:** 5,299
- **Columns:** 12
- **Primary key:** `family_id`

### Columns

| Column | Type |
|---|---|
| `family_id` | `str` |
| `canonical_name` | `str` |
| `family_size` | `int64` |
| `dominant_language` | `str` |
| `language_confidence` | `float64` |
| `completion_level` | `str` |
| `missing` | `object` |
| `route` | `str` |
| `api_needed` | `bool` |
| `estimated_gain` | `int64` |
| `priority` | `int64` |
| `family_status` | `str` |

### Sample

## data/knowledge/smart_queue_v3.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/knowledge/template_candidates.csv

- **Rows:** 60
- **Columns:** 58
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `name` | `str` |
| `meaning` | `float64` |
| `origin` | `float64` |
| `ipa` | `str` |
| `pronunciation` | `float64` |
| `variants` | `str` |
| `tags` | `str` |
| `source` | `str` |
| `verified` | `bool` |
| `language` | `float64` |
| `tier` | `str` |
| `confidence` | `float64` |
| `resolver` | `float64` |
| `updated_at` | `float64` |
| `id` | `float64` |
| `gender` | `str` |
| `popularity_score` | `float64` |
| `first_seen_year` | `float64` |
| `last_seen_year` | `float64` |
| `peak_year` | `float64` |
| `is_biblical` | `bool` |
| `is_palindrome` | `bool` |
| `phonetic` | `str` |
| `first_letter` | `str` |
| `stresses` | `str` |
| `syllables` | `float64` |
| `alliteration` | `float64` |
| `is_unisex` | `bool` |
| `slug` | `str` |
| `length` | `float64` |
| `country` | `float64` |
| `source_url` | `float64` |
| `last_reviewed` | `float64` |
| `notes` | `float64` |
| `priority` | `float64` |
| `status` | `str` |
| `meaning_done` | `bool` |
| `origin_done` | `bool` |
| `ipa_done` | `bool` |
| `tags_done` | `bool` |
| `seo_done` | `bool` |
| `reviewed` | `bool` |
| `published` | `bool` |
| `processed_at` | `str` |
| `pipeline_version` | `str` |
| `content_hash` | `str` |
| `seo_description` | `str` |
| `campaign` | `str` |
| `stage` | `str` |
| `equivalents` | `float64` |
| `scripts` | `float64` |
| `completion_level` | `str` |
| `short_forms` | `float64` |
| `full_forms` | `float64` |
| `feminine_forms` | `float64` |
| `masculine_forms` | `float64` |
| `other_forms` | `float64` |
| `other_readings` | `float64` |

### Sample

## data/knowledge/template_candidates.csv

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/outputs/behind_cache.parquet

- **Rows:** 31
- **Columns:** 15
- **Primary key:** `canonical_name`

### Columns

| Column | Type |
|---|---|
| `canonical_name` | `str` |
| `url` | `str` |
| `html_hash` | `str` |
| `fetched_at` | `str` |
| `parsed_ok` | `bool` |
| `gender` | `str` |
| `usage` | `str` |
| `pronunciation` | `str` |
| `meaning` | `str` |
| `root` | `str` |
| `variants` | `object` |
| `other_languages` | `object` |
| `equivalents` | `object` |
| `related` | `object` |
| `script` | `object` |

### Sample

## data/outputs/behind_cache.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/outputs/fetch_results.parquet

- **Rows:** 53
- **Columns:** 14
- **Primary key:** `family_id`

### Columns

| Column | Type |
|---|---|
| `family_id` | `object` |
| `canonical_name` | `str` |
| `batch_key` | `object` |
| `meaning` | `str` |
| `origin` | `object` |
| `pronunciation` | `str` |
| `api_status` | `object` |
| `fetched_at` | `object` |
| `gender` | `str` |
| `usage` | `str` |
| `root` | `str` |
| `variants` | `object` |
| `other_languages` | `object` |
| `status` | `str` |

### Sample

## data/outputs/fetch_results.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/outputs/legacy_patch.parquet

- **Rows:** 20,644
- **Columns:** 9
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `name` | `str` |
| `meaning` | `str` |
| `origin` | `str` |
| `pronunciation` | `str` |
| `variants` | `object` |
| `equivalents` | `str` |
| `confidence` | `float64` |
| `verified` | `bool` |
| `source` | `str` |

### Sample

## data/outputs/legacy_patch.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/raw/all-names.csv

- **Rows:** 97,697
- **Columns:** 15
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `sex` | `str` |
| `name` | `str` |
| `alt_spellings` | `str` |
| `n_sum` | `int64` |
| `year_min` | `int64` |
| `year_max` | `int64` |
| `year_pop` | `int64` |
| `biblical` | `float64` |
| `palindrome` | `float64` |
| `phones` | `str` |
| `first_letter` | `str` |
| `stresses` | `str` |
| `syllables` | `int64` |
| `alliteration_first` | `float64` |
| `unisex` | `float64` |

### Sample

## data/raw/all-names.csv

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/reports/missing_meanings.csv

- **Rows:** 97,694
- **Columns:** 2
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `name` | `str` |
| `gender` | `str` |

### Sample

## data/reports/missing_meanings.csv

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/seed/golden_500.csv

- **Rows:** 500
- **Columns:** 5
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `priority` | `int64` |
| `name` | `str` |
| `gender` | `str` |
| `country` | `str` |
| `status` | `str` |

### Sample

## data/seed/golden_500.csv

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/seed/knowledge_seed.csv

- **Rows:** 51
- **Columns:** 14
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `name` | `str` |
| `meaning` | `str` |
| `origin` | `str` |
| `ipa` | `str` |
| `pronunciation` | `str` |
| `variants` | `str` |
| `tags` | `str` |
| `source` | `str` |
| `verified` | `bool` |
| `language` | `str` |
| `tier` | `int64` |
| `confidence` | `int64` |
| `resolver` | `str` |
| `updated_at` | `str` |

### Sample

## data/seed/knowledge_seed.csv

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---

## data/seed/knowledge_seed.parquet

- **Rows:** 51
- **Columns:** 14
- **Primary key:** `name`

### Columns

| Column | Type |
|---|---|
| `name` | `str` |
| `meaning` | `str` |
| `origin` | `str` |
| `ipa` | `str` |
| `pronunciation` | `str` |
| `variants` | `object` |
| `tags` | `object` |
| `source` | `str` |
| `verified` | `bool` |
| `language` | `str` |
| `tier` | `int64` |
| `confidence` | `int64` |
| `resolver` | `str` |
| `updated_at` | `str` |

### Sample

## data/seed/knowledge_seed.parquet

**Error:** ``Import tabulate` failed.  Use pip or conda to install the tabulate package.`

---
