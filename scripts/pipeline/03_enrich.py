from pathlib import Path

import pandas as pd

from lib.enrich import (
    load_lookup,
    merge_lookup,
    save_missing_meanings,
)

BASE = Path(__file__).resolve().parent.parent

INPUT = BASE / "data" / "cleaned" / "names_cleaned.csv"
LOOKUP = BASE / "data" / "enriched" / "lookup.csv"
OUTPUT = BASE / "data" / "enriched" / "names_enriched.csv"
MISSING = BASE / "data" / "reports" / "missing_meanings.csv"

# -----------------------
# Load datasets
# -----------------------

df = pd.read_csv(INPUT)
lookup = load_lookup(LOOKUP)

# -----------------------
# Merge enrichment
# -----------------------

df = merge_lookup(df, lookup)

# -----------------------
# Save outputs
# -----------------------

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT, index=False)

missing = save_missing_meanings(df, MISSING)

# -----------------------
# Report
# -----------------------

filled = len(df) - len(missing)

print("=" * 40)
print("ENRICH REPORT")
print("=" * 40)
print(f"Total records: {len(df):,}")
print(f"Enriched names: {filled:,}")
print(f"Missing meanings: {len(missing):,}")
print(f"Output: {OUTPUT}")
print(f"Missing report: {MISSING}")