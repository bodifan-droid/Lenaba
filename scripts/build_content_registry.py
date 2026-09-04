from __future__ import annotations

from pathlib import Path
from datetime import datetime
import hashlib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

SOURCE = ROOT / "data" / "enriched" / "names_enriched.csv"

CONTENT_DIR = ROOT / "data" / "content"

REGISTRY_CSV = CONTENT_DIR / "content_registry.csv"
REGISTRY_PARQUET = CONTENT_DIR / "content_registry.parquet"

GOLDEN_CSV = CONTENT_DIR / "golden_500.csv"

PIPELINE_VERSION = "0.2.0"


def content_hash(row: pd.Series) -> str:
    """Stable hash of content fields."""

    payload = "|".join(
        str(row.get(col, ""))
        for col in [
            "name",
            "meaning",
            "origin",
            "ipa",
            "pronunciation",
        ]
    )

    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def assign_tier(priority: int) -> str:
    if priority <= 500:
        return "golden"
    if priority <= 5000:
        return "silver"
    return "bronze"


def build_registry():

    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(
        SOURCE,
        low_memory=False,
    )

    # Keep unique name variants (name + gender + country), not just unique names.
    unique_cols = [c for c in ["name", "gender", "country"] if c in df.columns]
    df = df.drop_duplicates(subset=unique_cols).copy()

    if "popularity_score" in df.columns:
        df = df.sort_values("popularity_score", ascending=False)
    else:
        df = df.sort_values("name")

    df = df.reset_index(drop=True)

    df["priority"] = df.index + 1

    df["tier"] = df["priority"].apply(assign_tier)

    df["status"] = "pending"

    df["meaning_done"] = df["meaning"].fillna("").ne("") if "meaning" in df.columns else False
    df["origin_done"] = df["origin"].fillna("").ne("") if "origin" in df.columns else False
    df["ipa_done"] = df["ipa"].fillna("").ne("") if "ipa" in df.columns else False
    df["tags_done"] = False
    df["seo_done"] = False

    df["reviewed"] = False
    df["published"] = False

    df["processed_at"] = ""
    df["pipeline_version"] = PIPELINE_VERSION

    df["content_hash"] = df.apply(content_hash, axis=1)

    original = len(pd.read_csv(SOURCE, low_memory=False))
    final = len(df)

    print(f"Original rows: {original:,}")
    print(f"Registry rows: {final:,}")

    if final < original:
        print(f"WARNING: {original-final:,} rows removed")
    else:
        print("No rows lost.")

    df.to_csv(REGISTRY_CSV, index=False)
    df.to_parquet(REGISTRY_PARQUET, index=False)

    golden = df[df["tier"] == "golden"].copy()

    golden.to_csv(GOLDEN_CSV, index=False)

    print("[OK] Content Registry created")
    print(f"[OK] Total names: {len(df):,}")
    print(f"[OK] Golden: {len(golden)}")
    print(f"[OK] Silver: {(df['tier']=='silver').sum()}")
    print(f"[OK] Bronze: {(df['tier']=='bronze').sum()}")


if __name__ == "__main__":
    build_registry()