from __future__ import annotations

import ast
import sys
from pathlib import Path

import pandas as pd

# -------------------------
# Project paths
# -------------------------

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.btn_family_parser import parse_family

# -------------------------
# Files
# -------------------------

CACHE = ROOT / "data" / "outputs" / "behind_cache.parquet"

OUT_FAMILIES = ROOT / "data" / "knowledge" / "canonical_families_v2.parquet"
OUT_RELATIONS = ROOT / "data" / "knowledge" / "family_relations.parquet"


def to_list(value):
    """Convert list-like values from parquet."""

    if value is None:
        return []

    if isinstance(value, list):
        return value

    try:
        return ast.literal_eval(value)
    except Exception:
        return []


def run():

    print("=" * 50)
    print("LENABA FAMILY PARSER V2")
    print("=" * 50)

    if not CACHE.exists():
        print("behind_cache.parquet not found.")
        return

    cache = pd.read_parquet(CACHE)

    families = []
    relations = []

    for _, row in cache.iterrows():

        canonical = str(row["canonical_name"]).strip().upper()

        families.append({
            "family_id": canonical,
            "family_slug": canonical.lower() + "-family",
            "canonical_name": canonical,
            "alias": canonical,
            "language": row.get("usage"),
            "source": "behindthename",
        })

        # ---------- Variants ----------

        for variant in to_list(row.get("variants")):

            alias = str(variant).strip().upper()

            if alias == canonical:
                continue

            families.append({
                "family_id": canonical,
                "family_slug": canonical.lower() + "-family",
                "canonical_name": canonical,
                "alias": alias,
                "language": row.get("usage"),
                "source": "behindthename",
            })

        # ---------- Historical ----------

        root = row.get("root")

        if isinstance(root, str) and root.strip():

            relations.append({
                "from_family": canonical,
                "to_family": root.strip().upper(),
                "relation": "historical_parent",
            })

    families_df = pd.DataFrame(families)

    if families_df.empty:
        print("No families parsed.")
        return

    families_df = families_df.drop_duplicates(
        ["canonical_name", "alias"]
    )

    families_df.to_parquet(
        OUT_FAMILIES,
        index=False,
    )

    pd.DataFrame(relations).to_parquet(
        OUT_RELATIONS,
        index=False,
    )
    pd.DataFrame(relations).to_parquet(OUT_RELATIONS, index=False)

    print()
    print("Families :", len(families))
    print("Relations:", len(relations))


if __name__ == "__main__":
    run()
