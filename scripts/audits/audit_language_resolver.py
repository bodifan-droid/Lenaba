
from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

RESOLVER = KNOWLEDGE / "language_resolver.parquet"


def main():

    df = pd.read_parquet(RESOLVER)

    print("=" * 55)
    print("LENABA LANGUAGE RESOLVER AUDIT")
    print("=" * 55)

    print(f"Resolved names : {len(df):,}")
    print(f"Languages found : {df['dominant_language'].nunique():,}")

    print("\nTop languages")
    print("-" * 55)
    print(df["dominant_language"].value_counts().head(20))

    print("\nHighest-confidence examples")
    print("-" * 55)
    print(
        df.sort_values(
            ["confidence", "sources_found"],
            ascending=False,
        )
        .head(20)
        [["name", "dominant_language", "confidence", "sources_found"]]
    )


if __name__ == "__main__":
    main()
