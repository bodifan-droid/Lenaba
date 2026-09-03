from pathlib import Path

import pandas as pd

from lib.export import (
    build_supabase_dataset,
    build_seo_dataset,
    export_parquet,
)

BASE = Path(__file__).resolve().parent.parent

INPUT = BASE / "data" / "enriched" / "names_enriched.csv"

SUPABASE = BASE / "data" / "enriched" / "names_supabase.csv"
SEO = BASE / "data" / "enriched" / "names_seo.csv"
PARQUET = BASE / "data" / "enriched" / "names.parquet"

# -----------------------
# Load dataset
# -----------------------

df = pd.read_csv(INPUT)

# -----------------------
# Build exports
# -----------------------

supabase = build_supabase_dataset(df)
seo = build_seo_dataset(df)

# -----------------------
# Save outputs
# -----------------------

supabase.to_csv(SUPABASE, index=False)
seo.to_csv(SEO, index=False)
export_parquet(df, PARQUET)

# -----------------------
# Report
# -----------------------

print("=" * 40)
print("EXPORT REPORT")
print("=" * 40)
print(f"Supabase: {SUPABASE}")
print(f"SEO: {SEO}")
print(f"Parquet: {PARQUET}")
print(f"Records exported: {len(df):,}")