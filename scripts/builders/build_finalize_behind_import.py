from __future__ import annotations

import ast
import numpy as np
import pandas as pd

from scripts.lib.paths import IMPORTS, KNOWLEDGE

SOURCE = IMPORTS / "behind_the_name" / "dataset3.csv"
MASTER = KNOWLEDGE / "knowledge_master.parquet"

FORM_COLUMNS = [
    "short_forms",
    "full_forms",
    "feminine_forms",
    "masculine_forms",
    "other_forms",
    "other_readings",
    "equivalents",
    "scripts",
]


def to_list(value):

    if isinstance(value, list):
        return value

    if isinstance(value, np.ndarray):
        return value.tolist()

    if isinstance(value, pd.Series):
        values = []
        for item in value:
            values.extend(to_list(item))
        return values

    if pd.isna(value):
        return []

    if isinstance(value, str):

        value = value.strip()

        if not value:
            return []

        if value.startswith("["):
            try:
                parsed = ast.literal_eval(value)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass

        return [value]

    return [str(value)]


def unique(values):

    seen = set()
    result = []

    for value in values:

        value = str(value).strip()

        if not value:
            continue

        key = value.lower()

        if key not in seen:
            seen.add(key)
            result.append(value)

    return result


def merge_group(group):

    row = group.iloc[0].copy()

    for col in FORM_COLUMNS:

        if col not in group.columns:
            continue

        merged = []

        for value in group[col]:
            merged.extend(to_list(value))

        row[col] = unique(merged)

    if "pronunciation" in group.columns:

        pron = (
            group["pronunciation"]
            .dropna()
            .astype(str)
            .str.strip()
        )

        if len(pron):
            row["pronunciation"] = pron.iloc[0]

    return row


def main():

    source = pd.read_csv(SOURCE, low_memory=False)

    if "pronounciation" in source.columns:
        source = source.rename(
            columns={"pronounciation": "pronunciation"}
        )

    duplicates = source["name"].duplicated().sum()

    canonical = (
        source
        .groupby("name", as_index=False)
        .apply(merge_group)
        .reset_index(drop=True)
    )

    lookup = canonical.set_index("name")

    master = pd.read_parquet(MASTER)

    imported = 0

    for idx, row in master.iterrows():

        name = row["name"]

        if name not in lookup.index:
            continue

        src = lookup.loc[name]

        # pronunciation
        current = row.get("pronunciation")

        if (
            (pd.isna(current) or str(current).strip() == "")
            and pd.notna(src.get("pronunciation"))
        ):
            master.at[idx, "pronunciation"] = src["pronunciation"]

        # forms
        for col in FORM_COLUMNS:

            if col not in master.columns:
                master[col] = None

            values = to_list(src.get(col))

            if values:
                master.at[idx, col] = values
                imported += len(values)

        # variants = агрегований список
        merged = []

        merged.extend(to_list(row.get("variants")))

        for col in FORM_COLUMNS:
            merged.extend(to_list(master.at[idx, col]))

        master.at[idx, "variants"] = unique(merged)

    master.to_parquet(MASTER, index=False)

    print("=" * 45)
    print("BEHINDTHENAME FINALIZED")
    print("=" * 45)
    print(f"Source rows      : {len(source):,}")
    print(f"Duplicate names  : {duplicates:,}")
    print(f"Canonical names  : {len(canonical):,}")
    print(f"Master rows      : {len(master):,}")
    print(f"Forms imported   : {imported:,}")


if __name__ == "__main__":
    main()