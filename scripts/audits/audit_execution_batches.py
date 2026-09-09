
from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

BATCHES = KNOWLEDGE / "execution_batches.parquet"


def main():

    df = pd.read_parquet(BATCHES)

    print("=" * 55)
    print("LENABA EXECUTION BATCHES")
    print("=" * 55)

    print(f"Language batches : {len(df):,}")

    print("\nTop batches")
    print("-" * 55)

    print(df.head(20))


if __name__ == "__main__":
    main()
