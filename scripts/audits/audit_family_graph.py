from __future__ import annotations

import pandas as pd
import numpy as np

from scripts.lib.paths import KNOWLEDGE

GRAPH = KNOWLEDGE / "family_graph.parquet"


def count_items(series):

    total = 0

    for value in series:

        if isinstance(value, np.ndarray):
            total += len(value)

        elif isinstance(value, list):
            total += len(value)

        elif isinstance(value, str) and value.strip():
            total += 1

    return total


def main():

    df = pd.read_parquet(GRAPH)

    print("=" * 55)
    print("LENABA FAMILY GRAPH")
    print("=" * 55)

    print(f"Names            : {len(df):,}")
    print(f"Roots            : {count_items(df['root']):,}")
    print(f"Variants         : {count_items(df['variant']):,}")
    print(f"Language forms   : {count_items(df['language_variant']):,}")
    print(f"Equivalents      : {count_items(df['equivalent']):,}")
    print(f"Related          : {count_items(df['related']):,}")

if __name__ == "__main__":
    main()
