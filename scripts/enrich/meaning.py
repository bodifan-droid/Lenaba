from pathlib import Path
import pandas as pd
from lib.normalization import normalize_series

ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE = ROOT / "data" / "knowledge" / "knowledge_master.parquet"
GRAPH = ROOT / "data" / "knowledge" / "etymology_graph.parquet"

def enrich_meaning(df: pd.DataFrame):

    print("Meaning...")

    if "meaning" not in df.columns:
        df["meaning"] = None

    before = df["meaning"].isna().sum()

    if not KNOWLEDGE.exists():
        print("  knowledge_master not found.")
        return df

    km = pd.read_parquet(KNOWLEDGE)

    if "meaning" not in km.columns:
        print("  meaning column missing in knowledge_master.")
        return df

    # ---------- Pass 1: direct lookup ----------

    lookup = (
        km[["name", "meaning"]]
        .dropna(subset=["meaning"])
        .assign(name_key=normalize_series(km["name"]))
        [["name_key", "meaning"]]
        .drop_duplicates("name_key")
    )

    merged = df.assign(name_key=normalize_series(df["name"]))

    merged = merged.merge(
        lookup,
        on="name_key",
        how="left",
        suffixes=("", "_km")
    )

    mask = merged["meaning"].isna() & merged["meaning_km"].notna()

    merged.loc[mask, "meaning"] = merged.loc[mask, "meaning_km"]

    merged = merged.drop(columns=["meaning_km"])

    # ---------- Pass 2: graph variants ----------

    if GRAPH.exists():

        graph = pd.read_parquet(GRAPH)

        variants = graph[graph["relation"] == "variant"].copy()

        canonical_meaning = (
            km[["name", "meaning"]]
            .dropna(subset=["meaning"])
            .assign(key=normalize_series(km["name"]))
            [["key", "meaning"]]
            .drop_duplicates("key")
        )

        variant_lookup = (
            variants.assign(
                from_key=normalize_series(variants["from_name"]),
                to_key=normalize_series(variants["to_name"])
            )
            .merge(
                canonical_meaning,
                left_on="from_key",
                right_on="key",
                how="inner"
            )
            [["to_key", "meaning"]]
            .drop_duplicates("to_key")
        )

        merged = merged.merge(
            variant_lookup,
            left_on="name_key",
            right_on="to_key",
            how="left",
            suffixes=("", "_graph")
        )

        mask = (
            merged["meaning"].isna()
            & merged["meaning_graph"].notna()
        )

        merged.loc[mask, "meaning"] = merged.loc[mask, "meaning_graph"]

        merged = merged.drop(columns=["meaning_graph", "to_key"])

    merged = merged.drop(columns=["name_key"])

    after = merged["meaning"].isna().sum()

    print(f"  Filled: {before - after:,}")

    return merged
