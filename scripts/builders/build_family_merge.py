from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE
from scripts.lib.validate_master import run_integrity_gate

MASTER = KNOWLEDGE / "knowledge_master.parquet"
LOOKUP = KNOWLEDGE / "family_lookup.parquet"

SAFE_FIELDS = [
    "meaning",
    "origin",
    "pronunciation",
    "equivalents",
    "related",
    "root",
]


def empty(value):

    if pd.isna(value):
        return True

    if isinstance(value, str):
        return value.strip() == ""

    if isinstance(value, list):
        return len(value) == 0

    return False


def score(row):

    return sum(
        not empty(row.get(col))
        for col in SAFE_FIELDS
        if col in row.index
    )


def main():

    master = pd.read_parquet(MASTER)
    lookup = pd.read_parquet(LOOKUP)

    # Робимо повторний запуск безпечним
    master.drop(
        columns=["canonical_name", "alias"],
        inplace=True,
        errors="ignore",
    )

    master = master.merge(
        lookup[["alias", "canonical_name"]],
        left_on="name",
        right_on="alias",
        how="left",
    )

    master["canonical_name"] = (
        master["canonical_name"]
        .fillna(master["name"])
    )

    updated = 0

    for canonical, group in master.groupby("canonical_name"):

        best_idx = group.apply(score, axis=1).idxmax()

        best = master.loc[best_idx]

        for idx in group.index:

            if idx == best_idx:
                continue

            for col in SAFE_FIELDS:

                if col not in master.columns:
                    continue

                if empty(master.at[idx, col]) and not empty(best[col]):

                    master.at[idx, col] = best[col]
                    updated += 1

    master.drop(
        columns=["alias", "canonical_name"],
        inplace=True,
        errors="ignore",
    )

    run_integrity_gate(master)

    master.to_parquet(MASTER, index=False)

    print("=" * 45)
    print("FAMILY MERGE COMPLETE")
    print("=" * 45)
    print(f"Updated fields : {updated:,}")


if __name__ == "__main__":
    main()
