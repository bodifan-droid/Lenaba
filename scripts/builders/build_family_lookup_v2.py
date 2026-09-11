from __future__ import annotations

import ast
import pandas as pd

from scripts.lib.paths import KNOWLEDGE
from scripts.lib.schema_adapter import normalize_name_key

MASTER = KNOWLEDGE / "knowledge_master.parquet"
LEGACY = KNOWLEDGE / "canonical_families.parquet"
OUT = KNOWLEDGE / "family_lookup.parquet"


def to_list(value):

    if isinstance(value, list):
        return value

    if pd.isna(value):
        return []

    if isinstance(value, str):

        value = value.strip()

        if value.startswith("["):
            try:
                return ast.literal_eval(value)
            except Exception:
                pass

        if value == "":
            return []

        return [v.strip() for v in value.split(",") if v.strip()]

    return []


def add_alias(rows, canonical, alias):

    if not alias:
        return

    rows.append({
        "alias": alias,
        "canonical_name": canonical,
    })


def main():

    master = pd.read_parquet(MASTER)
    legacy = pd.read_parquet(LEGACY)

    rows = []

    # ---------- Legacy ----------
    for _, row in legacy.iterrows():

        add_alias(
            rows,
            row["canonical_name"],
            row["alias"],
        )

    # ---------- Production Master ----------
    for _, row in master.iterrows():

        canonical = row["name"]

        add_alias(rows, canonical, canonical)

        if "variants" in master.columns:
            for alias in to_list(row["variants"]):
                add_alias(rows, canonical, alias)

        if "equivalents" in master.columns:
            for alias in to_list(row["equivalents"]):
                add_alias(rows, canonical, alias)

    lookup = pd.DataFrame(rows)

    lookup["merge_key"] = (
        lookup["alias"]
        .apply(normalize_name_key)
    )

    lookup = (
        lookup.sort_values("canonical_name")
              .drop_duplicates("merge_key")
              .drop(columns="merge_key")
              .reset_index(drop=True)
    )

    lookup.to_parquet(OUT, index=False)

    print("=" * 45)
    print("FAMILY LOOKUP V2")
    print("=" * 45)
    print(f"Aliases : {len(lookup):,}")
    print(f"Families: {lookup['canonical_name'].nunique():,}")


if __name__ == "__main__":
    main()
