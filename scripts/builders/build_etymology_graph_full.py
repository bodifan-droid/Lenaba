from __future__ import annotations

import ast
import pandas as pd

from scripts.lib.paths import KNOWLEDGE

MASTER = KNOWLEDGE / "knowledge_master.parquet"
OUT = KNOWLEDGE / "etymology_graph.parquet"


LIST_FIELDS = [
    ("variants", "variant"),
    ("equivalents", "equivalent"),
    ("related", "related"),
]


def to_list(value):

    if isinstance(value, list):
        return value

    if value is None or pd.isna(value):
        return []

    if isinstance(value, str):

        value = value.strip()

        if not value:
            return []

        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            pass

        return [v.strip() for v in value.split(",") if v.strip()]

    return []


def main():

    master = pd.read_parquet(MASTER)

    rows = []

    for _, row in master.iterrows():

        name = row["name"]

        root = row.get("root")

        if isinstance(root, str) and root.strip():
            rows.append({
                "from_name": name,
                "relation": "root",
                "to_name": root.strip(),
                "target_language": None,
                "source": "master",
            })

        for column, relation in LIST_FIELDS:

            if column not in master.columns:
                continue

            for value in to_list(row[column]):

                rows.append({
                    "from_name": name,
                    "relation": relation,
                    "to_name": value,
                    "target_language": None,
                    "source": "master",
                })

    df = pd.DataFrame(rows).drop_duplicates()

    df.to_parquet(OUT, index=False)

    print("=" * 45)
    print("FULL ETYMOLOGY GRAPH BUILT")
    print("=" * 45)
    print(f"Relations : {len(df):,}")


if __name__ == "__main__":
    main()
