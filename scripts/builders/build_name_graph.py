from __future__ import annotations

import pandas as pd

import ast

from scripts.lib.paths import KNOWLEDGE

MASTER = KNOWLEDGE / "knowledge_master.parquet"
GRAPH = KNOWLEDGE / "name_graph.parquet"

RELATION_COLUMNS = {
    "variants": "variant",
    "equivalents": "equivalent",
    "short_forms": "short_form",
    "full_forms": "full_form",
    "feminine_forms": "feminine_form",
    "masculine_forms": "masculine_form",
    "other_forms": "other_form",
    "other_readings": "other_reading",
}


def to_list(value):

    if value is None:
        return []

    if isinstance(value, list):
        return value

    if hasattr(value, "tolist"):
        return value.tolist()

    if pd.isna(value):
        return []

    if isinstance(value, str):

        value = value.strip()

        if not value or value == "[]":
            return []

        # Розбираємо рядок виду "['Alex','Lex']"
        if value.startswith("[") and value.endswith("]"):
            try:
                parsed = ast.literal_eval(value)

                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass

        return [value]

    return [str(value)]


def main():

    df = pd.read_parquet(MASTER)

    edges = []

    for _, row in df.iterrows():

        source = row.get("name")

        # пропускаємо порожні імена
        if pd.isna(source):
            continue

        source = str(source).strip()

        if not source:
            continue

        for column, relation in RELATION_COLUMNS.items():

            if column not in df.columns:
                continue

            for target in to_list(row.get(column)):

                target = str(target).strip()

                if target in {"[]", "[ ]", "nan", "None"}:
                    continue

                if not target:
                    continue

                if target.lower() == source.lower():
                    continue

                edges.append({
                    "from_name": source,
                    "to_name": target,
                    "relation": relation,
                })

            # двосторонній зв'язок
            edges.append({
                "from_name": target,
                "to_name": source,
                "relation": relation,
            })

    graph = pd.DataFrame(edges)

    graph = (
        graph
        .drop_duplicates()
        .sort_values(
            ["from_name", "relation", "to_name"]
        )
        .reset_index(drop=True)
    )

    graph.to_parquet(GRAPH, index=False)

    print("=" * 45)
    print("NAME GRAPH BUILT")
    print("=" * 45)
    print(f"Nodes : {df['name'].nunique():,}")
    print(f"Edges : {len(graph):,}")
    print(f"Output: {GRAPH.name}")


if __name__ == "__main__":
    main()