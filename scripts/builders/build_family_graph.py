from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

GRAPH = KNOWLEDGE / "etymology_graph.parquet"
OUT = KNOWLEDGE / "family_graph.parquet"

RELATIONS = [
    "root",
    "variant",
    "language_variant",
    "equivalent",
    "related",
    "diminutive",
    "feminine",
    "masculine",
    "surname",
]


def unique(values):

    seen = set()
    result = []

    for v in values:

        if not isinstance(v, str):
            continue

        v = v.strip()

        if not v or v in seen:
            continue

        seen.add(v)
        result.append(v)

    return result


def main():

    if not GRAPH.exists():
        raise FileNotFoundError(GRAPH)

    graph = pd.read_parquet(GRAPH)

    rows = []

    for name, group in graph.groupby("from_name"):

        row = {
            "name": name,
        }

        for relation in RELATIONS:

            values = group.loc[
                group["relation"] == relation,
                "to_name",
            ].tolist()

            row[relation] = unique(values)

        rows.append(row)

    df = pd.DataFrame(rows)

    df.to_parquet(OUT, index=False)

    print("=" * 45)
    print("FAMILY GRAPH BUILT")
    print("=" * 45)
    print(f"Names : {len(df):,}")
    print(f"Output: {OUT}")


if __name__ == "__main__":
    main()
