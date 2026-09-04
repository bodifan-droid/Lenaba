from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd

from scripts.lib.origin import OriginResolver
from scripts.lib.pronunciation import cmu_to_ipa, human_pronunciation
from scripts.lib.tagger import generate_tags
from scripts.lib.seo_writer import write_description
from scripts.lib.knowledge import KnowledgeCache

REGISTRY = ROOT / "data" / "content" / "content_registry.parquet"

resolver = OriginResolver()
cache = KnowledgeCache()


def enrich_row(row: pd.Series) -> pd.Series:
    if row["status"] == "published":
        return row
    name = row["name"]

    # ---------- Knowledge Vault ----------
    record = cache.get(name)

    if record:

        if not row.get("meaning") and record.meaning:
            row["meaning"] = record.meaning

        if not row.get("origin") and record.origin:
            row["origin"] = record.origin
            row["origin_done"] = True

        if not row.get("ipa") and record.ipa:
            row["ipa"] = record.ipa
            row["ipa_done"] = True

        if not row.get("pronunciation") and record.pronunciation:
            row["pronunciation"] = record.pronunciation

        row["source"] = record.source
        row["verified"] = record.verified
        row["confidence"] = 1.0 if record.verified else 0.8

    # ---------- Origin ----------
    if not row.get("origin"):
        origin = resolver.resolve(name)
        if origin:
            row["origin"] = origin
            row["origin_done"] = True
            row["source"] = "resolver_chain"
            row["confidence"] = 0.99

    # ---------- IPA ----------
    phonetic = row.get("phonetic")

    if phonetic and not row.get("ipa"):
        if isinstance(phonetic, list):
            phonetic = " ".join(phonetic)

        row["ipa"] = cmu_to_ipa(str(phonetic))
        row["ipa_done"] = True

    # ---------- Human pronunciation ----------
    if not row.get("pronunciation"):
        row["pronunciation"] = human_pronunciation(name)

    # ---------- Tags ----------
    tags = generate_tags(
        name,
        row.get("meaning"),
        row.get("origin"),
    )

    row["seo_description"] = write_description(
        name,
        row.get("meaning"),
        row.get("origin"),
        tags,
    )

    row["seo_done"] = True

    # ---------- Meaning flag ----------
    meaning = row.get("meaning")

    row["meaning_done"] = (
        isinstance(meaning, str)
        and meaning.strip() != ""
    )

    # ---------- Status ----------
    row["status"] = "enriched"
    row["processed_at"] = datetime.utcnow().isoformat()

    return row


def main():
    df = pd.read_parquet(REGISTRY)

    before = (df["status"] == "pending").sum()

    df = df.apply(enrich_row, axis=1)

    df.to_parquet(REGISTRY, index=False)

    df.to_csv(
        ROOT / "data" / "content" / "content_registry.csv",
        index=False,
    )

    after = (df["status"] == "pending").sum()

    print("=" * 45)
    print("LENABA CONTENT FACTORY")
    print("=" * 45)
    print(f"Pending before: {before:,}")
    print(f"Pending after : {after:,}")
    print(f"Enriched       : {len(df)-after:,}")


if __name__ == "__main__":
    main()