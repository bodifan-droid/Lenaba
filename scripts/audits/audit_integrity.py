from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

MASTER = KNOWLEDGE / "knowledge_master.parquet"


def main():

    df = pd.read_parquet(MASTER)

    print("=" * 55)
    print("LENABA DATA INTEGRITY AUDIT")
    print("=" * 55)

    # Missing names
    missing = df[df["name"].isna() | (df["name"].astype(str).str.strip() == "")]
    print(f"Missing names : {len(missing)}")

    if len(missing):
        print("\nMissing name rows:")
        print(missing[["id", "name"]].head(20))

    # Duplicate IDs
    dup = df[df["id"].duplicated(keep=False)]
    print(f"\nDuplicate IDs : {dup['id'].nunique()}")

    if len(dup):
        print("\nDuplicate samples:")
        print(
            dup[["id", "name"]]
            .sort_values("id")
            .head(30)
        )

    # Save reports
    OUT = KNOWLEDGE / "integrity_reports"
    OUT.mkdir(exist_ok=True)

    missing.to_csv(OUT / "missing_names.csv", index=False)
    dup.to_csv(OUT / "duplicate_ids.csv", index=False)

    print("\nReports saved:")
    print(OUT)


if __name__ == "__main__":
    main()