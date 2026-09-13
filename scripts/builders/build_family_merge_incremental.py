from __future__ import annotations

import pandas as pd
import numpy as np

from scripts.lib.paths import KNOWLEDGE

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

    if value is None:
        return True

    if isinstance(value, str):
        return value.strip() == ""

    if isinstance(value, list):
        return len(value) == 0

    if isinstance(value, np.ndarray):
        return value.size == 0

    try:
        return bool(pd.isna(value))
    except (ValueError, TypeError):
        return False


def score(row):

    return sum(
        not empty(row.get(col))
        for col in SAFE_FIELDS
    )


def merge_family(canonical_name: str):

    master = pd.read_parquet(MASTER)
    lookup = pd.read_parquet(LOOKUP)

    aliases = lookup.loc[
        lookup["canonical_name"] == canonical_name,
        "alias",
    ].tolist()

    if not aliases:
        aliases = [canonical_name]

    mask = master["name"].isin(aliases)

    family = master.loc[mask].copy()

    if family.empty:
        return 0

    best_idx = family.apply(score, axis=1).idxmax()

    best = master.loc[best_idx]

    updated = 0

    for idx in family.index:

        if idx == best_idx:
            continue

        for col in SAFE_FIELDS:

            if col not in master.columns:
                continue

            if empty(master.at[idx, col]) and not empty(best[col]):

                master.at[idx, col] = best[col]
                updated += 1

    master.to_parquet(MASTER, index=False)

    return updated


if __name__ == "__main__":

    print("Use merge_family(canonical_name)")
