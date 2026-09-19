from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.parsing import to_list

NAMES = ROOT / "data" / "enriched" / "names.parquet"
CACHE = ROOT / "data" / "outputs" / "behind_cache.parquet"

OUT = ROOT / "data" / "knowledge" / "family_registry.parquet"
REL = ROOT / "data" / "knowledge" / "family_relations.parquet"

def run():

    print("=" * 50)
    print("LENABA FAMILY GENERATOR")
    print("=" * 50)

    cache = pd.read_parquet(CACHE)

    registry = []
    relations = []

    for _, row in cache.iterrows():

        canonical = str(row["canonical_name"]).strip().upper()

        registry.append({
            "family_id": canonical,
            "canonical_name": canonical,
            "member": canonical,
            "member_type": "canonical",
            "language": row.get("usage"),
        })

        # -------- Variants --------

        for v in to_list(row.get("variants")):

            registry.append({
                "family_id": canonical,
                "canonical_name": canonical,
                "member": str(v).strip().upper(),
                "member_type": "variant",
                "language": row.get("usage"),
            })

        # -------- Diminutives --------

        for v in to_list(row.get("diminutives")):

            registry.append({
                "family_id": canonical,
                "canonical_name": canonical,
                "member": str(v).strip().upper(),
                "member_type": "diminutive",
                "language": row.get("usage"),
            })

        # -------- Other languages --------

        for v in to_list(row.get("other_languages")):

            registry.append({
                "family_id": canonical,
                "canonical_name": canonical,
                "member": str(v).strip().upper(),
                "member_type": "language_variant",
                "language": row.get("usage"),
            })

        # -------- Historical --------

        root = row.get("root")

        if isinstance(root, str) and root.strip():

            relations.append({
                "from_family": canonical,
                "to_family": root.strip().upper(),
                "relation": "historical_parent",
            })

    registry = (
        pd.DataFrame(registry)
        .drop_duplicates(["family_id", "member"])
    )

    registry.to_parquet(OUT, index=False)
    pd.DataFrame(relations).drop_duplicates().to_parquet(REL, index=False)

    print()
    print(f"Families : {registry['family_id'].nunique():,}")
    print(f"Members  : {len(registry):,}")
    print(f"Relations: {len(relations):,}")

if __name__ == "__main__":
    run()
