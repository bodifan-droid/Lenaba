from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

TAXONOMY = KNOWLEDGE / "name_taxonomy.parquet"


def main():

    df = pd.read_parquet(TAXONOMY)

    print("=" * 55)
    print("LENABA TAXONOMY AUDIT")
    print("=" * 55)

    print(f"Entries        : {len(df):,}")
    print(f"Unique names   : {df['name'].nunique():,}")
    print(f"Categories     : {df['taxonomy_type'].nunique():,}")

    print("\nTop Categories")
    print("-" * 55)
    print(df["taxonomy_type"].value_counts().head(20))

    print("\nTop Values")
    print("-" * 55)
    print(df["taxonomy_value"].value_counts().head(20))

    print("\nSample")
    print("-" * 55)
    print(df.head(20))


if __name__ == "__main__":
    main()