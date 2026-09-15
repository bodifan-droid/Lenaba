from pathlib import Path
from datetime import datetime
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib.normalization import normalize_series

NAMES = ROOT / "data" / "enriched" / "names.parquet"
GRAPH = ROOT / "data" / "knowledge" / "etymology_graph.parquet"
FETCH = ROOT / "data" / "outputs" / "fetch_results.parquet"

def is_missing(series: pd.Series) -> pd.Series:
    return (
        series.isna()
        | (series.astype(str).str.strip() == "")
        | (series.astype(str).str.lower() == "nan")
    )


def build_family_lookup() -> pd.DataFrame:
    graph = pd.read_parquet(GRAPH)

    variants = graph.loc[
        graph["relation"] == "variant",
        ["from_name", "to_name"],
    ].copy()

    lookup = variants.assign(
        canonical=normalize_series(variants["from_name"]),
        variant=normalize_series(variants["to_name"]),
    )

    reverse = lookup.rename(
        columns={
            "canonical": "variant",
            "variant": "canonical",
        }
    )

    return (
        pd.concat([lookup, reverse], ignore_index=True)
        .drop_duplicates()
    )


def run():

    print("=" * 50)
    print("LENABA EXECUTION ENGINE V1")
    print("=" * 50)

    names = pd.read_parquet(NAMES)
    fetch = pd.read_parquet(FETCH)

    names["key"] = normalize_series(names["name"])
    fetch["key"] = normalize_series(fetch["canonical_name"])

    family_lookup = build_family_lookup()

    today = datetime.utcnow().strftime("%Y-%m-%d")

    families_processed = 0
    families_matched = 0
    rows_touched = 0
    fields_updated = 0

    for _, row in fetch.iterrows():

        families_processed += 1

        keys = {row["key"]}

        related = family_lookup.loc[
            family_lookup["canonical"] == row["key"],
            "variant",
        ]

        keys.update(related.tolist())

        mask = names["key"].isin(keys)

        if not mask.any():
            continue

        families_matched += 1
        rows_touched += int(mask.sum())

        updates = [
            ("origin", row.get("origin")),
            ("meaning", row.get("meaning")),
            ("pronunciation", row.get("pronunciation")),
            ("gender", row.get("gender")),
        ]

        for column, value in updates:

            if column not in names.columns:
                continue

            if pd.isna(value) or str(value).strip() == "":
                continue

            m = mask & is_missing(names[column])

            names.loc[m, column] = value
            fields_updated += int(m.sum())

        if "source" in names.columns:
            names.loc[mask, "source"] = "execution_engine"

        if "verified" in names.columns:
            names.loc[mask, "verified"] = True

        if "last_reviewed" in names.columns:
            names.loc[mask, "last_reviewed"] = today

    names = names.drop(columns=["key"])

    names.to_parquet(NAMES, index=False)

    print()
    print("=" * 36)
    print("EXECUTION ENGINE REPORT")
    print("=" * 36)
    print(f"Families processed : {families_processed:,}")
    print(f"Families matched   : {families_matched:,}")
    print(f"Rows touched       : {rows_touched:,}")
    print(f"Fields updated     : {fields_updated:,}")
    print("Saved: data/enriched/names.parquet")


if __name__ == "__main__":
    run()
