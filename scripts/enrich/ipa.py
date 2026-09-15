
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

PHONETICS = ROOT / "data" / "cleaned" / "phonetics.parquet"


def _norm(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.strip()
        .str.strip("'")
        .str.upper()
    )


def enrich_ipa(df: pd.DataFrame):

    print("IPA...")

    if "ipa" not in df.columns:
        df["ipa"] = None

    before = df["ipa"].isna().sum()

    if not PHONETICS.exists():
        print("  phonetics.parquet not found.")
        return df

    phon = pd.read_parquet(PHONETICS)

    if not {"name", "phonetic"}.issubset(phon.columns):
        print("  required columns missing.")
        return df

    lookup = (
        phon[["name", "phonetic"]]
        .dropna(subset=["phonetic"])
        .assign(name_key=_norm(phon["name"]))
        [["name_key", "phonetic"]]
        .drop_duplicates("name_key")
    )

    merged = df.assign(name_key=_norm(df["name"]))

    merged = merged.merge(
        lookup,
        on="name_key",
        how="left",
        suffixes=("", "_lookup")
    )

    mask = merged["ipa"].isna() & merged["phonetic"].notna()

    merged.loc[mask, "ipa"] = merged.loc[mask, "phonetic"]

    merged = merged.drop(columns=["phonetic", "name_key"])

    after = merged["ipa"].isna().sum()

    print(f"  Filled: {before-after:,}")

    return merged
