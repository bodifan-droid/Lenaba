from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

QUEUE = KNOWLEDGE / "smart_queue_v3.parquet"


def main():

    df = pd.read_parquet(QUEUE)

    print("=" * 55)
    print("LENABA SMART QUEUE V3 AUDIT")
    print("=" * 55)

    print(f"Families queued : {len(df):,}")
    print(f"API needed      : {df['api_needed'].sum():,}")
    print(f"Local IPA       : {(~df['api_needed']).sum():,}")

    print("\nMissing fields")
    print("-" * 55)

    counter = {}

    for missing in df["missing"]:
        for field in missing:
            counter[field] = counter.get(field, 0) + 1

    print(pd.Series(counter).sort_values(ascending=False))

    print("\nTop API languages")
    print("-" * 55)

    print(
        df[df["api_needed"]]
        ["dominant_language"]
        .fillna("Unknown")
        .value_counts()
        .head(20)
    )

    print("\nLargest API families")
    print("-" * 55)

    print(
        df[df["api_needed"]]
        .sort_values("family_size", ascending=False)
        .head(20)
        [
            [
                "canonical_name",
                "family_size",
                "dominant_language",
                "missing",
            ]
        ]
    )


if __name__ == "__main__":
    main()
