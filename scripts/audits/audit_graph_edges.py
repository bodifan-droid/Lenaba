from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

GRAPH = KNOWLEDGE / "name_graph.parquet"


def main():

    df = pd.read_parquet(GRAPH)

    print("=" * 60)
    print("LENABA GRAPH EDGE AUDIT")
    print("=" * 60)

    print(f"Edges : {len(df):,}")
    print()

    if "edge_type" in df.columns:

        print("Edge Types")
        print("-" * 60)

        counts = df["edge_type"].value_counts()

        for edge, count in counts.items():
            print(f"{edge:20} {count:>8,}")

        print("\nLargest connected sources")
        print("-" * 60)

        print(
            df.groupby("edge_type")["from_name"]
              .nunique()
              .sort_values(ascending=False)
        )

    else:
        print("No edge_type column found.")
        print("Columns:")
        print(df.columns.tolist())

    print("\nSample")
    print("-" * 60)

    print(df.head(20))


if __name__ == "__main__":
    main()