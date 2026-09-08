from __future__ import annotations

import ast
import numpy as np
import pandas as pd

from scripts.lib.paths import IMPORTS, KNOWLEDGE

SOURCE = IMPORTS / "behind_the_name" / "dataset3.csv"
MASTER = KNOWLEDGE / "knowledge_master.parquet"


def normalize(value):

    if isinstance(value, list):
        return value

    if isinstance(value, np.ndarray):
        return value.tolist()

    if pd.isna(value):
        return []

    if isinstance(value, str):

        value = value.strip()

        if value.startswith("["):
            try:
                return ast.literal_eval(value)
            except Exception:
                pass

        if value:
            return [value]

    return []


def count_filled(series):

    total = 0

    for value in series:

        if isinstance(value, list):
            if len(value):
                total += 1
            continue

        if isinstance(value, np.ndarray):
            if value.size:
                total += 1
            continue

        if pd.notna(value) and str(value).strip():
            total += 1

    return total


def main():

    src = pd.read_csv(SOURCE, low_memory=False)
    master = pd.read_parquet(MASTER)

    print("=" * 55)
    print("LENABA MAPPING AUDIT")
    print("=" * 55)

    print(f"Source rows : {len(src):,}")
    print(f"Master rows : {len(master):,}")

    print("\nCOLUMN COVERAGE")
    print("-" * 55)

    common = sorted(set(src.columns) & set(master.columns))

    report = []

    for col in common:

        src_count = count_filled(src[col])
        master_count = count_filled(master[col])

        report.append(
            (
                col,
                src_count,
                master_count,
                src_count - master_count,
            )
        )

    report = sorted(report, key=lambda x: x[3], reverse=True)

    for col, src_count, master_count, missing in report:

        status = "OK"

        if missing > 0:
            status = "MISSING"

        print(
            f"{col:<18}"
            f"{src_count:>8}"
            f"{master_count:>10}"
            f"{missing:>10}"
            f"   {status}"
        )

    print("\nSOURCE-ONLY COLUMNS")
    print("-" * 55)

    for col in sorted(set(src.columns) - set(master.columns)):
        print(col)

    print("\nMASTER-ONLY COLUMNS")
    print("-" * 55)

    for col in sorted(set(master.columns) - set(src.columns)):
        print(col)


if __name__ == "__main__":
    main()