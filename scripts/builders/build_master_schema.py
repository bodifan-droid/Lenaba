from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE
from scripts.lib.validate_master import run_integrity_gate

MASTER = KNOWLEDGE / "knowledge_master.parquet"

SCHEMA_DEFAULTS = {
    "confidence": 0.0,
    "verified": False,
    "stage": "raw",
    "meaning_done": False,
    "origin_done": False,
    "ipa_done": False,
    "seo_done": False,
    "reviewed": False,
    "published": False,
    "processed_at": "",
    "pipeline_version": "v0.6",
    "content_hash": "",
    "source": "global_dictionary",
}

BOOL_COLUMNS = [
    "verified",
    "meaning_done",
    "origin_done",
    "ipa_done",
    "seo_done",
    "reviewed",
    "published",
]

FLOAT_COLUMNS = ["confidence"]

STRING_COLUMNS = [
    "stage",
    "processed_at",
    "pipeline_version",
    "content_hash",
    "source",
]


def main():

    df = pd.read_parquet(MASTER)

    added = []
    normalized = []

    for col, default in SCHEMA_DEFAULTS.items():

        if col not in df.columns:
            df[col] = default
            added.append(col)

        else:
            df[col] = df[col].fillna(default)
            normalized.append(col)

    for col in BOOL_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(bool)

    for col in FLOAT_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(float)

    for col in STRING_COLUMNS:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str)

    run_integrity_gate(df)

    df.to_parquet(MASTER, index=False)

    print("=" * 45)
    print("MASTER SCHEMA NORMALIZED")
    print("=" * 45)
    print(f"Rows              : {len(df):,}")
    print(f"Columns           : {len(df.columns)}")
    print(f"Added columns     : {len(added)}")
    print(f"Normalized columns: {len(normalized)}")

    if added:
        print("\nAdded:")
        for col in added:
            print("  •", col)


if __name__ == "__main__":
    main()
