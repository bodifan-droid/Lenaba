
from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

QUEUE = KNOWLEDGE / "execution_queue.parquet"
OUT = KNOWLEDGE / "execution_batches.parquet"


def main():

    queue = pd.read_parquet(QUEUE)

    behind = queue[
        queue["executor"] == "behind"
    ].copy()

    batches = (
        behind.groupby("batch_key")
        .agg(
            tasks=("family_id", "count"),
            names=("estimated_gain", "sum"),
            avg_gain=("estimated_gain", "mean"),
        )
        .sort_values("tasks", ascending=False)
        .reset_index()
    )

    batches.to_parquet(OUT, index=False)

    print("=" * 45)
    print("EXECUTION BATCHES BUILT")
    print("=" * 45)
    print(f"Batches : {len(batches):,}")
    print(f"Output  : {OUT.name}")


if __name__ == "__main__":
    main()
