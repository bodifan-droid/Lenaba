from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

GRAPH = KNOWLEDGE / "etymology_graph.parquet"


def main():

    df = pd.read_parquet(GRAPH)

    print("=" * 55)
    print("LENABA ETYMOLOGY GRAPH")
    print("=" * 55)

    print(f"Relations : {len(df):,}")
    print(f"Names     : {df['from_name'].nunique():,}")

    print("\nRelation types")
    print("-" * 55)
    print(df["relation"].value_counts())

    print("\nSample")
    print("-" * 55)
    print(df.head(20))


if __name__ == "__main__":
    main()
