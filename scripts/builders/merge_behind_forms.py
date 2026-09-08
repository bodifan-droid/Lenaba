from __future__ import annotations

import ast
import numpy as np
import pandas as pd

from scripts.lib.paths import IMPORTS, KNOWLEDGE
from scripts.lib.validate_master import run_integrity_gate

SOURCE = IMPORTS / "behind_the_name" / "dataset3.csv"
MASTER = KNOWLEDGE / "knowledge_master.parquet"


FORM_COLUMNS = [
    "short_forms",
    "full_forms",
    "feminine_forms",
    "masculine_forms",
    "other_forms",
    "other_readings",
]


def to_list(value):

    if isinstance(value, pd.Series):
        value = value.dropna()

        if value.empty:
            return []

        value = value.iloc[0]

    if isinstance(value, list):
        return value

    if isinstance(value, np.ndarray):
        return value.tolist()

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

    return []


def unique_keep_order(values):

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


def main():

    source = pd.read_csv(SOURCE, low_memory=False)

    master = pd.read_parquet(MASTER)

    run_integrity_gate(master)

    # виправляємо опечатку BehindTheName
    if "pronounciation" in source.columns:
        source = source.rename(
            columns={"pronounciation": "pronunciation"}
        )

# Скільки дублікатів у сирому BehindTheName
    duplicates = source["name"].duplicated().sum()
    print(f"Duplicate source names: {duplicates:,}")

# Беремо один канонічний запис на ім'я
    source_lookup = (
        source
        .sort_values("name")
        .drop_duplicates(subset=["name"], keep="first")
        .set_index("name")
    )

    added = 0

    for idx, row in master.iterrows():

        name = row["name"]

        if name not in source_lookup.index:
            continue

        src = source_lookup.loc[name]

        # ---------- pronunciation ----------

        current_pron = row.get("pronunciation")

        if (
            "pronunciation" in source.columns
            and (pd.isna(current_pron) or str(current_pron).strip() == "")
        ):
            master.at[idx, "pronunciation"] = src["pronunciation"]

        # ---------- new form columns ----------

        for col in FORM_COLUMNS:

            if col not in master.columns:
                master[col] = None

            if col in source.columns:

                values = to_list(src[col])

                if values:
                    master.at[idx, col] = values
                    added += len(values)

        # ---------- variants ----------

        merged = []

        merged.extend(to_list(row.get("variants")))

        for col in FORM_COLUMNS:

            merged.extend(
                to_list(master.at[idx, col])
            )

        master.at[idx, "variants"] = unique_keep_order(merged)

    master.to_parquet(MASTER, index=False)

    print("=" * 45)
    print("BEHIND FORMS MERGED")
    print("=" * 45)
    print(f"Names processed : {len(master):,}")
    print(f"Forms imported  : {added:,}")


if __name__ == "__main__":
    main()