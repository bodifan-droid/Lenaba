from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

MASTER = KNOWLEDGE / "knowledge_master.parquet"

REQUIRED = [
    "name",
    "gender",
    "meaning",
    "origin",
    "pronunciation",
    "variants",
    "equivalents",
    "script",
    "confidence",
    "verified",
    "stage",
    "meaning_done",
    "origin_done",
    "ipa_done",
    "seo_done",
    "reviewed",
    "published",
    "processed_at",
    "pipeline_version",
    "content_hash",
    "source",
]


def main():

    df = pd.read_parquet(MASTER)

    print("=" * 55)
    print("LENABA MASTER SCHEMA AUDIT")
    print("=" * 55)
    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")
    print()

    rows = []

    for col in REQUIRED:

        rows.append({
            "column": col,
            "exists": col in df.columns,
            "dtype": str(df[col].dtype) if col in df.columns else "—",
            "missing": int(df[col].isna().sum()) if col in df.columns else "—",
        })

    report = pd.DataFrame(rows)

    print(report.to_string(index=False))

    missing_cols = report[~report["exists"]]

    print()

    if len(missing_cols) == 0:
        print("✓ Schema contract satisfied.")
    else:
        print("Missing columns:")
        print(missing_cols["column"].tolist())


if __name__ == "__main__":
    main()
