from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

GRAPH = KNOWLEDGE / "name_graph.parquet"
MASTER = KNOWLEDGE / "knowledge_master.parquet"

INVALID = {
    "",
    "[]",
    "[ ]",
    "nan",
    "None",
}


def valid(name):

    if pd.isna(name):
        return False

    name = str(name).strip()

    if name in INVALID:
        return False

    if name.startswith("[") and "(" in name:
        return False

    return True


def main():

    graph = pd.read_parquet(GRAPH)

    before = len(graph)

    # чистимо сміття
    graph = graph[
        graph["from_name"].apply(valid)
        & graph["to_name"].apply(valid)
    ]

    # самопосилання
    graph = graph[
        graph["from_name"].str.lower()
        != graph["to_name"].str.lower()
    ]

    # двосторонність
    reverse = graph.rename(
        columns={
            "from_name": "to_name",
            "to_name": "from_name",
        }
    )

    graph = (
        pd.concat([graph, reverse], ignore_index=True)
        .drop_duplicates()
    )

    after = len(graph)

    # graph score
    score = (
        graph.groupby("from_name")
        .size()
        .reset_index(name="graph_score")
    )

    master = pd.read_parquet(MASTER)

    master = master.merge(
        score,
        how="left",
        left_on="name",
        right_on="from_name",
    )

    master["graph_score"] = (
        master["graph_score"]
        .fillna(0)
        .astype(int)
    )

    master = master.drop(columns=["from_name"])

    # сироти
    orphans = master[
        master["graph_score"] == 0
    ][["name", "graph_score"]]

    graph.to_parquet(GRAPH, index=False)
    master.to_parquet(MASTER, index=False)

    orphans.to_csv(
        KNOWLEDGE / "graph_orphans.csv",
        index=False,
    )

    print("=" * 50)
    print("GRAPH INTEGRITY COMPLETE")
    print("=" * 50)
    print(f"Edges before : {before:,}")
    print(f"Edges after  : {after:,}")
    print(f"Orphans      : {len(orphans):,}")
    print(f"Graph score  : added to knowledge_master")