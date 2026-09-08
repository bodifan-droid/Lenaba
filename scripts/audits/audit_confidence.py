from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

MASTER = KNOWLEDGE / "knowledge_master.parquet"


def main():

    df = pd.read_parquet(MASTER)

    bad = df[(df["confidence"] < 0) | (df["confidence"] > 1)]

    print("=" * 45)
    print("CONFIDENCE AUDIT")
    print("=" * 45)
    print(f"Invalid rows: {len(bad)}")

    if len(bad):
        print("\nValue counts:")
        print(bad["confidence"].value_counts().sort_index())

        print("\nSample:")
        print(bad[["name", "confidence", "source"]].head(20))


if __name__ == "__main__":
    main()