
from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE
from scripts.lib.validate_master import run_integrity_gate

MASTER = KNOWLEDGE / "knowledge_master.parquet"


def main():

    df = pd.read_parquet(MASTER)

    mask = (
        (df["source"] == "knowledge_seed_v1")
        & (df["confidence"] == 100)
    )

    updated = mask.sum()

    df.loc[mask, "confidence"] = 1.0

    run_integrity_gate(df)

    df.to_parquet(MASTER, index=False)

    print("=" * 45)
    print("CONFIDENCE SCALE FIXED")
    print("=" * 45)
    print(f"Updated rows : {updated}")


if __name__ == "__main__":
    main()
