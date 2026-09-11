from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

MASTER = KNOWLEDGE / "knowledge_master.parquet"
LOOKUP = KNOWLEDGE / "family_lookup.parquet"


def main():

    master = pd.read_parquet(MASTER)
    lookup = pd.read_parquet(LOOKUP)

    matched = master["name"].isin(lookup["alias"])

    print("=" * 55)
    print("LENABA DATA PLATFORM")
    print("=" * 55)

    print(f"Rows            : {len(master):,}")
    print(f"Columns         : {len(master.columns)}")
    print(f"Family coverage : {matched.mean()*100:.2f}%")
    print()

    print("Completion")
    print("-" * 55)

    for col in ["meaning", "origin", "pronunciation"]:

        filled = master[col].fillna("").astype(str).str.strip().ne("").sum()

        print(f"{col:<15}{filled:>8,}")

    print()

    print("Confidence")
    print("-" * 55)

    invalid = ((master["confidence"] < 0) | (master["confidence"] > 1)).sum()

    print(f"Outside range : {invalid}")

if __name__ == "__main__":
    main()
