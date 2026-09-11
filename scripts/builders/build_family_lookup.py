from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE
from scripts.lib.schema_adapter import normalize_name_key

FAMILIES = KNOWLEDGE / "canonical_families.parquet"
OUT = KNOWLEDGE / "family_lookup.parquet"


def main():

    df = pd.read_parquet(FAMILIES)

    lookup = (
        df[["alias", "canonical_name", "is_canonical"]]
        .drop_duplicates()
        .copy()
    )

    lookup["merge_key"] = lookup["alias"].apply(normalize_name_key)

    lookup = (
        lookup.sort_values(["canonical_name", "is_canonical"], ascending=[True, False])
              .drop_duplicates("merge_key", keep="first")
              .reset_index(drop=True)
    )

    lookup.to_parquet(OUT, index=False)

    print("=" * 45)
    print("FAMILY LOOKUP BUILT")
    print("=" * 45)
    print(f"Aliases  : {len(lookup):,}")
    print(f"Families : {lookup['canonical_name'].nunique():,}")


if __name__ == "__main__":
    main()
