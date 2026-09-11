from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE
from scripts.lib.validate_master import run_integrity_gate

MASTER = KNOWLEDGE / "knowledge_master.parquet"


def main():

    df = pd.read_parquet(MASTER)

    before = (
        (df["confidence"] > 1)
        | (df["confidence"] < 0)
    ).sum()

    df["confidence"] = (
        df["confidence"]
        .clip(lower=0, upper=1)
    )

    run_integrity_gate(df)

    df.to_parquet(MASTER, index=False)

    print("=" * 45)
    print("CONFIDENCE V3")
    print("=" * 45)
    print(f"Fixed rows : {before}")


if __name__ == "__main__":
    main()
