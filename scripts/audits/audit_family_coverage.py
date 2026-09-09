
from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

MASTER = KNOWLEDGE / "knowledge_master.parquet"
FAMILIES = KNOWLEDGE / "canonical_families.parquet"


def has_text(value):

    if value is None:
        return False

    if isinstance(value, str):
        return value.strip() != ""

    if isinstance(value, list):
        return len(value) > 0

    if hasattr(value, "size"):
        return value.size > 0

    return not pd.isna(value)


def main():

    master = pd.read_parquet(MASTER)
    families = pd.read_parquet(FAMILIES)

    lookup = master.set_index("name")

    rows = []

    for family_id, group in families.groupby("family_id"):

        aliases = group["alias"].tolist()

        coverage = {
            "meaning": False,
            "origin": False,
            "pronunciation": False,
        }

        for alias in aliases:

            if alias not in lookup.index:
                continue

            row = lookup.loc[alias]

            for field in coverage:
                if has_text(row.get(field)):
                    coverage[field] = True

        missing = [
            field
            for field, ok in coverage.items()
            if not ok
        ]

        rows.append({
            "family_id": family_id,
            "canonical_name": group.loc[group["is_canonical"], "canonical_name"].iloc[0],
            "family_size": len(aliases),
            "missing": missing,
        })

    audit = pd.DataFrame(rows)

    print("=" * 55)
    print("LENABA FAMILY COVERAGE")
    print("=" * 55)

    print(f"Families          : {len(audit):,}")
    print(f"Fully covered     : {(audit['missing'].str.len()==0).sum():,}")
    print(f"Need meaning      : {audit['missing'].apply(lambda x: 'meaning' in x).sum():,}")
    print(f"Need origin       : {audit['missing'].apply(lambda x: 'origin' in x).sum():,}")
    print(f"Need pronunciation: {audit['missing'].apply(lambda x: 'pronunciation' in x).sum():,}")

    print("\nLargest uncovered families:")
    print(
        audit[audit["missing"].str.len() > 0]
        .sort_values("family_size", ascending=False)
        .head(20)
        [["canonical_name", "family_size", "missing"]]
    )

    OUT = KNOWLEDGE / "family_coverage.parquet"
    audit.to_parquet(OUT, index=False)

    print(f"\nSaved: {OUT.name}")


if __name__ == "__main__":
    main()
