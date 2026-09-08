from __future__ import annotations

import ast
import re

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

MASTER = KNOWLEDGE / "knowledge_master.parquet"
OUT = KNOWLEDGE / "name_taxonomy.parquet"

PATTERN = re.compile(r"([A-Z][A-Z\s]+?)\((.*?)\)")

FIELDS = [
    "variants",
    "equivalents",
    "scripts",
    "other_forms",
    "other_readings",
]


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

        if not value:
            return []

        if value.startswith("[") and value.endswith("]"):
            try:
                parsed = ast.literal_eval(value)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass

        return [value]

    return [str(value)]


def parse_taxonomy(text):

    rows = []

    for category, content in PATTERN.findall(str(text)):

        category = category.strip().title()

        for value in content.split(","):

            value = value.strip()

            if value:
                rows.append((category, value))

    return rows


def main():

    df = pd.read_parquet(MASTER)

    taxonomy_rows = []

    for _, row in df.iterrows():

        name = row["name"]

        if pd.isna(name):
            continue

        name = str(name).strip()

        for field in FIELDS:

            if field not in df.columns:
                continue

            for item in to_list(row[field]):

                for category, value in parse_taxonomy(item):

                    taxonomy_rows.append({
                        "name": name,
                        "taxonomy_type": category,
                        "taxonomy_value": value,
                        "source_field": field,
                    })

    taxonomy = pd.DataFrame(taxonomy_rows)

    taxonomy = (
        taxonomy
        .sort_values(["name", "taxonomy_type", "taxonomy_value"])
        .drop_duplicates(
            subset=[
                "name",
                "taxonomy_type",
                "taxonomy_value",
            ],
            keep="first",
        )
        .reset_index(drop=True)
    )

    taxonomy.to_parquet(OUT, index=False)

    print("=" * 45)
    print("TAXONOMY BUILT")
    print("=" * 45)
    print(f"Entries : {len(taxonomy):,}")
    print(f"Names   : {taxonomy['name'].nunique():,}")
    print(f"Output  : {OUT.name}")


if __name__ == "__main__":
    main()