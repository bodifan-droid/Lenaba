
from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

QUEUE = KNOWLEDGE / "execution_queue.parquet"


def main():

    df = pd.read_parquet(QUEUE)

    print("=" * 55)
    print("LENABA EXECUTION QUEUE AUDIT")
    print("=" * 55)

    print(f"Tasks : {len(df):,}")

    print("\nExecutors")
    print("-" * 55)
    print(df["executor"].value_counts())

    print("\nLargest batches")
    print("-" * 55)

    print(
        df.groupby("batch_key")
        .agg(
            tasks=("family_id", "count"),
            names=("estimated_gain", "sum"),
        )
        .sort_values("tasks", ascending=False)
        .head(20)
    )

    print("\nTop tasks")
    print("-" * 55)

    print(
        df.head(20)[
            [
                "canonical_name",
                "executor",
                "batch_key",
                "estimated_gain",
            ]
        ]
    )


if __name__ == "__main__":
    main()
