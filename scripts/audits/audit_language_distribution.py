from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

QUEUE = KNOWLEDGE / "execution_queue.parquet"


def main():

    queue = pd.read_parquet(QUEUE)

    print("=" * 55)
    print("LANGUAGE DISTRIBUTION")
    print("=" * 55)

    print()
    print("Executors")
    print("-" * 20)
    print(queue["executor"].value_counts())

    print()
    print("Top 20 batches")
    print("-" * 20)
    print(
        queue["batch_key"]
        .value_counts()
        .head(20)
        .to_string()
    )


if __name__ == "__main__":
    main()
