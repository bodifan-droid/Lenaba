from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

MASTER = KNOWLEDGE / "knowledge_master.parquet"


def has_text(value):

    if value is None:
        return False

    if isinstance(value, list):
        return len(value) > 0

    if hasattr(value, "size"):
        return value.size > 0

    if pd.isna(value):
        return False

    if isinstance(value, str):
        return value.strip() != ""

    return True


def main():

    df = pd.read_parquet(MASTER)

    # Meaning відсутній
    no_meaning = ~df["meaning"].apply(has_text)

    # Є хоча б одна корисна підказка
    taxonomy_source = (
        df["equivalents"].apply(has_text)
        | df["scripts"].apply(has_text)
        | df["variants"].apply(has_text)
        | df["short_forms"].apply(has_text)
        | df["full_forms"].apply(has_text)
        | df["feminine_forms"].apply(has_text)
        | df["masculine_forms"].apply(has_text)
        | df["other_forms"].apply(has_text)
        | df["other_readings"].apply(has_text)
    )

    candidates = df[no_meaning & taxonomy_source].copy()

    print("=" * 55)
    print("LENABA TEMPLATE CANDIDATES AUDIT")
    print("=" * 55)
    print(f"Total names                : {len(df):,}")
    print(f"Without meaning            : {no_meaning.sum():,}")
    print(f"Template candidates        : {len(candidates):,}")
    print()

    print("Top sample:")
    print("-" * 55)

    cols = [
        "name",
        "origin",
        "equivalents",
        "scripts",
        "short_forms",
        "variants",
    ]

    print(candidates[cols].head(20))

    candidates.to_csv(
        KNOWLEDGE / "template_candidates.csv",
        index=False,
    )

    print()
    print("Saved:")
    print(KNOWLEDGE / "template_candidates.csv")


if __name__ == "__main__":
    main()