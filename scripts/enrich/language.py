from lib.normalization import normalize_series
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

RESOLVER = ROOT / "data" / "knowledge" / "language_resolver.parquet"


def enrich_language(df):

    print("Language...")

    if "language" not in df.columns:
        df["language"] = None

    if "language_confidence" not in df.columns:
        df["language_confidence"] = None

    before = df["language"].isna().sum()

    if not RESOLVER.exists():
        print("  language_resolver not found.")
        return df

    lr = pd.read_parquet(RESOLVER)

    lookup = (
        lr.assign(name_key=normalize_series(lr["name"]))
        [["name_key", "dominant_language", "confidence"]]
        .rename(
            columns={
                "dominant_language": "resolver_language",
                "confidence": "resolver_confidence",
            }
        )
        .drop_duplicates("name_key")
    )

    merged = df.assign(name_key=normalize_series(df["name"]))

    merged = merged.merge(
        lookup,
        on="name_key",
        how="left",
    )

    mask = (
        merged["language"].isna()
        & merged["resolver_language"].notna()
    )

    merged.loc[mask, "language"] = merged.loc[mask, "resolver_language"]
    merged.loc[mask, "language_confidence"] = merged.loc[
        mask, "resolver_confidence"
    ]

    merged = merged.drop(
        columns=[
            "resolver_language",
            "resolver_confidence",
            "name_key",
        ]
    )

    after = merged["language"].isna().sum()

    print(f"  Filled: {before-after:,}")

    return merged
