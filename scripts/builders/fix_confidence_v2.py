from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE
from scripts.lib.validate_master import run_integrity_gate

MASTER = KNOWLEDGE / "knowledge_master.parquet"


def normalize(value):

    if pd.isna(value):
        return value

    if value > 1:
        return value / 100

    return value


def main():

    df = pd.read_parquet(MASTER)

    before = (df["confidence"] > 1).sum()

    df["confidence"] = df["confidence"].apply(normalize)

    run_integrity_gate(df)

    df.to_parquet(MASTER, index=False)

    print("=" * 45)
    print("CONFIDENCE V2 FIX")
    print("=" * 45)
    print(f"Updated rows : {before}")


if __name__ == "__main__":
    main()
