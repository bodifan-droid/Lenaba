
from pathlib import Path
import pandas as pd

NAMES = Path("data/enriched/names.parquet")
MASTER = Path("data/knowledge/knowledge_master.parquet")

FIELDS = [
    "pronunciation",
    "ipa",
    "usage",
    "origin_language",
    "script",
    "etymology_roots",
    "variants",
    "other_languages",
    "variant_languages",
    "masculine_forms",
    "feminine_forms",
    "diminutives",
]


def normalize(value):
    return str(value).strip().upper()


def empty(value):
    if value is None:
        return True
    if isinstance(value, float) and pd.isna(value):
        return True
    if value == "":
        return True
    if isinstance(value, list) and len(value) == 0:
        return True
    return False


def main():

    names = pd.read_parquet(NAMES)
    master = pd.read_parquet(MASTER)

    names["_key"] = names["name"].map(normalize)
    master["_key"] = master["name"].map(normalize)

    lookup = (
        master
        .drop_duplicates("_key")
        .set_index("_key")
    )

    updated = {field: 0 for field in FIELDS}

    for idx, row in names.iterrows():

        key = row["_key"]

        if key not in lookup.index:
            continue

        source = lookup.loc[key]

        for field in FIELDS:

            if field not in names.columns:
                continue

            if field not in lookup.columns:
                continue

            if not empty(names.at[idx, field]):
                continue

            value = source[field]

            if empty(value):
                continue

            names.at[idx, field] = value
            updated[field] += 1

    names.drop(columns="_key", inplace=True)

    names.to_parquet(NAMES, index=False)

    print("=" * 50)
    print("DATA COMPLETION ENGINE")
    print("=" * 50)

    total = sum(updated.values())

    for field, count in updated.items():
        print(f"{field:20} +{count}")

    print("-" * 50)
    print(f"Total updates: {total}")


if __name__ == "__main__":
    main()
