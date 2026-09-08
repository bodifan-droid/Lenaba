from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE
from scripts.lib.validate_master import run_integrity_gate

GRAPH = KNOWLEDGE / "name_graph.parquet"
MASTER = KNOWLEDGE / "knowledge_master.parquet"
OUT = KNOWLEDGE / "canonical_families.parquet"


class UnionFind:

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, x):

        if pd.isna(x):
            return None

        self.parent.setdefault(x, x)
        self.rank.setdefault(x, 0)

        # Ітеративний find (без рекурсії)
        root = x
        while self.parent[root] != root:
            root = self.parent[root]

        # Path compression
        while x != root:
            parent = self.parent[x]
            self.parent[x] = root
            x = parent

        return root

    def union(self, a, b):

        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            return

        # Union by rank
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra

        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1


def score(row):

    completion = {
        "platinum": 4,
        "gold": 3,
        "silver": 2,
        "bronze": 1,
        "empty": 0,
    }

    return (
        completion.get(getattr(row, "completion_level", "empty"), 0),
        bool(getattr(row, "verified", False)),
        getattr(row, "confidence", 0),
    )


def main():

    graph = pd.read_parquet(GRAPH)
    master = pd.read_parquet(MASTER)

    run_integrity_gate(master)

    uf = UnionFind()

    total = len(graph)
    for i, edge in enumerate(graph.itertuples(index=False), start=1):

        if pd.isna(edge.from_name) or pd.isna(edge.to_name):
            continue

        uf.union(edge.from_name, edge.to_name)

        if i % 50000 == 0:
            print(f"Processed edges: {i:,}/{total:,}")

    groups = {}

    total = len(master)

    for i, name in enumerate(master["name"], start=1):

        if pd.isna(name):
            continue

        root = uf.find(name)

        if root is None:
            continue

        groups.setdefault(root, []).append(name)

        if i % 5000 == 0:
            print(f"Grouped names: {i:,}/{total:,}")

    master_scores = {
        row.name: score(row)
        for row in master.itertuples(index=False)
    }

    rows = []

    for names in groups.values():

        ranked = sorted(
            names,
            key=lambda n: (
                master_scores.get(n, (0, False, 0)),
                n,
            ),
            reverse=True,
        )

        canonical = ranked[0]

        for alias in ranked:

            rows.append({
                "family_id": uf.find(alias),
                "canonical_name": canonical,
                "alias": alias,
                "is_canonical": alias == canonical,
            })

    families = pd.DataFrame(rows)

    print(f"Families found : {len(groups):,}")
    print(f"Largest family : {max(len(v) for v in groups.values()):,}")

    families.to_parquet(OUT, index=False)

    print("=" * 45)
    print("CANONICAL FAMILIES BUILT")
    print("=" * 45)
    print(f"Families : {families['family_id'].nunique():,}")
    print(f"Aliases  : {len(families):,}")
    print(f"Output   : {OUT.name}")


if __name__ == "__main__":
    main()