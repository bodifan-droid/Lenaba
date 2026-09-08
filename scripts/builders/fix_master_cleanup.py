
from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

MASTER = KNOWLEDGE / "knowledge_master.parquet"


def main():

    df = pd.read_parquet(MASTER)

    before = len(df)

    df = df[df["name"].notna()].copy()
    df = df[df["name"].astype(str).str.strip() != ""].copy()

    after = len(df)

    df.to_parquet(MASTER, index=False)

    print("=" * 40)
    print("MASTER CLEANUP")
    print("=" * 40)
    print(f"Rows before : {before:,}")
    print(f"Rows after  : {after:,}")
    print(f"Removed     : {before-after}")


if __name__ == "__main__":
    main()