from __future__ import annotations
from scripts.lib.schema_adapter import normalize_columns

import pandas as pd

from scripts.lib.paths import (
    ENRICHED,
    KNOWLEDGE,
    CONTENT,
    OUTPUTS,
)
from scripts.lib.validate_master import run_integrity_gate

BASE = ENRICHED / "names.parquet"
MASTER = KNOWLEDGE / "knowledge_master.parquet"
PACKS = CONTENT / "packs"
FETCH = OUTPUTS / "fetch_results.parquet"
LEGACY = OUTPUTS / "legacy_patch.parquet"


def fill_if_empty(current, new):

    if pd.isna(current):
        return new

    if isinstance(current, str) and current.strip() == "":
        return new

    if isinstance(current, list) and len(current) == 0:
        return new

    return current


def apply_patch(master, patch):

    # визначаємо ключ автоматично
    from scripts.lib.schema_adapter import normalize_name_key

    patch = patch.copy()

    master["_merge_key"] = master["name"].apply(normalize_name_key)
    patch["_merge_key"] = patch["name"].apply(normalize_name_key)

    # -------------------------------------------------
    # залишаємо найповніший запис для кожного merge_key
    # -------------------------------------------------

    patch["_score"] = (
        patch[["meaning", "origin", "pronunciation"]]
        .fillna("")
        .astype(str)
        .ne("")
        .sum(axis=1)
    )

    patch = (
        patch.sort_values("_score", ascending=False)
            .drop_duplicates("_merge_key", keep="first")
    )

    lookup = patch.set_index("_merge_key")

    updated = 0

    for idx, row in master.iterrows():

        key = row["_merge_key"]

        if key not in lookup.index:
            continue

        src = lookup.loc[key]

        before = row.to_dict()

        for col in patch.columns:

            if col == "name":
                continue

            if col not in master.columns:
                master[col] = None

            master.at[idx, col] = fill_if_empty(
                row.get(col),
                src.get(col),
            )

        if before != master.loc[idx].to_dict():
            updated += 1

    master.drop(
        columns=["_merge_key"],
        inplace=True,
        errors="ignore",
    )

    patch.drop(
        columns=["_score"],
        inplace=True,
        errors="ignore",
    )

    return master, updated


def main():

    master = pd.read_parquet(BASE)

    print("=" * 45)
    print("MASTER V2")
    print("=" * 45)
    print(f"Base rows : {len(master):,}")

    total_updates = 0

    if LEGACY.exists():

        patch = normalize_columns(pd.read_parquet(LEGACY))

        master, updated = apply_patch(master, patch)
        total_updates += updated

        print(f"Applied {LEGACY.name}")

    for pack in sorted(PACKS.glob("golden_pack_*.parquet")):

        patch = normalize_columns(pd.read_parquet(pack))

        master, updated = apply_patch(master, patch)
        total_updates += updated

        print(f"Applied {pack.name}")

    if FETCH.exists():

        patch = normalize_columns(pd.read_parquet(FETCH))

        master, updated = apply_patch(master, patch)
        total_updates += updated

        print("Applied fetch_results.parquet")

    run_integrity_gate(master)

    master.to_parquet(MASTER, index=False)

    print()
    print(f"Rows        : {len(master):,}")
    print(f"Patched rows: {total_updates:,}")


if __name__ == "__main__":
    main()
