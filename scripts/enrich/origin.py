from pathlib import Path
import pandas as pd
from lib.normalization import normalize_series

ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE = ROOT / "data" / "knowledge" / "knowledge_master.parquet"
FAMILIES = ROOT / "data" / "knowledge" / "canonical_families.parquet"

def enrich_origin(df: pd.DataFrame):

    print("Origin...")

    if "origin" not in df.columns:
        df["origin"] = None

    before = df["origin"].isna().sum()

    if not KNOWLEDGE.exists():
        print("  knowledge_master not found.")
        return df

    km = pd.read_parquet(KNOWLEDGE)

    if "origin" not in km.columns:
        print("  origin column missing in knowledge_master.")
        return df

    # ---------- Pass 1: direct name lookup ----------

    lookup = (
        km[["name", "origin"]]
        .dropna(subset=["origin"])
        .assign(name_key=normalize_series(km["name"]))
        [["name_key", "origin"]]
        .drop_duplicates("name_key")
    )

    merged = df.assign(name_key=normalize_series(df["name"]))

    merged = merged.merge(
        lookup,
        on="name_key",
        how="left",
        suffixes=("", "_km")
    )

    mask = merged["origin"].isna() & merged["origin_km"].notna()

    merged.loc[mask, "origin"] = merged.loc[mask, "origin_km"]

    merged = merged.drop(columns=["origin_km"])


    # ---------- Pass 2: etymology graph (variants only) ----------

    GRAPH = ROOT / "data" / "knowledge" / "etymology_graph.parquet"

    if GRAPH.exists():

        graph = pd.read_parquet(GRAPH)

        variants = graph[graph["relation"] == "variant"].copy()

        canonical_origin = (
            km[["name", "origin"]]
            .dropna(subset=["origin"])
            .assign(key=normalize_series(km["name"]))
            [["key", "origin"]]
            .drop_duplicates("key")
        )

        variant_lookup = (
            variants.assign(
                from_key=normalize_series(variants["from_name"]),
                to_key=normalize_series(variants["to_name"])
            )
            .merge(
                canonical_origin,
                left_on="from_key",
                right_on="key",
                how="inner"
            )
            [["to_key", "origin"]]
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
            merged["origin"].isna()
            & merged["origin_graph"].notna()
        )

        merged.loc[mask, "origin"] = merged.loc[mask, "origin_graph"]

        merged = merged.drop(columns=["origin_graph", "to_key", "name_key"])

    after = merged["origin"].isna().sum()

    print(f"  Filled: {before - after:,}")

    return merged
