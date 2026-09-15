
from pathlib import Path
import pandas as pd

from enrich.gender import enrich_gender
from enrich.origin import enrich_origin
from enrich.meaning import enrich_meaning
from enrich.ipa import enrich_ipa
from enrich.language import enrich_language
from enrich.country import enrich_country
from enrich.tags import enrich_tags
from enrich.slug import enrich_slug
from enrich.alt_spellings import enrich_alt_spellings
from enrich.related import enrich_related
from enrich.validator import validate_database

ROOT = Path(__file__).resolve().parents[1]

CANDIDATES = [
    ROOT / "data" / "enriched" / "names.parquet",
    ROOT / "data" / "enriched" / "names_enriched.parquet",
    ROOT / "data" / "enriched" / "names_enriched.csv",
    ROOT / "data" / "cleaned" / "names.parquet",
    ROOT / "data" / "cleaned" / "names_cleaned.parquet",
]

DB = next((p for p in CANDIDATES if p.exists()), None)

if DB is None:
    raise FileNotFoundError(
        "Could not find Lenaba database. Checked:\n"
        + "\n".join(str(p) for p in CANDIDATES)
    )


def run():

    print("=" * 50)
    print("LENABA DATABASE ENRICHMENT")
    print("=" * 50)
    print(f"Database: {DB.relative_to(ROOT)}")

    if DB.suffix == ".csv":
        df = pd.read_csv(DB)
    else:
        df = pd.read_parquet(DB)

    print(f"Loaded: {len(df):,} names")

    df = enrich_gender(df)
    df = enrich_origin(df)
    df = enrich_meaning(df)
    df = enrich_ipa(df)
    df = enrich_language(df)
    df = enrich_country(df)
    df = enrich_alt_spellings(df)
    df = enrich_related(df)
    df = enrich_tags(df)
    df = enrich_slug(df)

    report = validate_database(df)

    if DB.suffix == ".csv":
        df.to_csv(DB, index=False)
    else:
        df.to_parquet(DB, index=False)

    print("\nSaved.")
    print(report)


if __name__ == "__main__":
    run()
