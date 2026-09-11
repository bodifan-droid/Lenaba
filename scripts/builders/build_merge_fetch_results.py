
from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE, OUTPUTS
from scripts.lib.validate_master import run_integrity_gate

MASTER = KNOWLEDGE / "knowledge_master.parquet"
FETCH = OUTPUTS / "fetch_results.parquet"


def fill_if_empty(current, new):

    if pd.isna(current):
        return new

    if isinstance(current, str) and current.strip() == "":
        return new

    if isinstance(current, list) and len(current) == 0:
        return new

    return current


def main():

    master = pd.read_parquet(MASTER)

    if not FETCH.exists():
        print("No fetch_results.parquet found.")
        return

    fetched = pd.read_parquet(FETCH)

    lookup = fetched.set_index("canonical_name")

    updated = 0

    for idx, row in master.iterrows():

        name = row["name"]

        if name not in lookup.index:
            continue

        src = lookup.loc[name]

        before = (
            row.get("meaning"),
            row.get("origin"),
            row.get("pronunciation"),
        )

        master.at[idx, "meaning"] = fill_if_empty(
            row.get("meaning"),
            src.get("meaning"),
        )

        master.at[idx, "origin"] = fill_if_empty(
            row.get("origin"),
            src.get("usage"),
        )

        master.at[idx, "pronunciation"] = fill_if_empty(
            row.get("pronunciation"),
            src.get("pronunciation"),
        )

        after = (
            master.at[idx, "meaning"],
            master.at[idx, "origin"],
            master.at[idx, "pronunciation"],
        )

        if before != after:
            updated += 1

    run_integrity_gate(master)

    master.to_parquet(MASTER, index=False)

    print("=" * 45)
    print("FETCH RESULTS MERGED")
    print("=" * 45)
    print(f"Updated rows : {updated}")

if __name__ == "__main__":
    main()
