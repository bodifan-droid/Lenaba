from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

GRAPH = KNOWLEDGE / "name_graph.parquet"
MASTER = KNOWLEDGE / "knowledge_master.parquet"


def main():

    graph = pd.read_parquet(GRAPH)
    master = pd.read_parquet(MASTER)

    degree = (
        graph.groupby("from_name")
        .size()
        .sort_values(ascending=False)
    )

    relation_stats = (
        graph["relation"]
        .value_counts()
        .sort_values(ascending=False)
    )

    all_names = set(master["name"].dropna().astype(str))
    graph_names = set(degree.index.astype(str))

    orphans = sorted(all_names - graph_names)

    print("=" * 55)
    print("LENABA NAME GRAPH AUDIT")
    print("=" * 55)

    print(f"Master names     : {len(all_names):,}")
    print(f"Graph nodes      : {len(graph_names):,}")
    print(f"Graph edges      : {len(graph):,}")
    print(f"Average degree   : {len(graph)/len(graph_names):.2f}")

    print("\nRelation types")
    print("-" * 55)
    print(relation_stats)

    print("\nTop connected names")
    print("-" * 55)
    print(degree.head(20))

    print("\nOrphan names")
    print("-" * 55)
    print(f"Total: {len(orphans):,}")

    if orphans:
        print(orphans[:20])


if __name__ == "__main__":
    main()