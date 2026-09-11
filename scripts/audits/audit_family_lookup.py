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
    print("LENABA FAMILY LOOKUP AUDIT")
    print("=" * 55)
    print(f"Master rows        : {len(master):,}")
    print(f"Lookup aliases     : {len(lookup):,}")
    print(f"Matched names      : {matched.sum():,}")
    print(f"Coverage           : {matched.mean()*100:.2f}%")
    print()

    print("Sample unmatched:")
    print(master.loc[~matched, "name"].head(20).to_string(index=False))


if __name__ == "__main__":
    main()
