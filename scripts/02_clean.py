
from pathlib import Path

import pandas as pd

from lib.parsing import (
    normalize_variants,
    normalize_phonetics,
    normalize_stresses,
)
from lib.slugs import slugify, name_length
from lib.reports import save_json

ROOT = Path(__file__).resolve().parent.parent

RAW = ROOT / "data" / "raw" / "all-names.csv"
OUT = ROOT / "data" / "cleaned"

OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW)

df = df.rename(columns={
    "sex": "gender",
    "alt_spellings": "variants",
    "n_sum": "popularity_score",
    "year_min": "first_seen_year",
    "year_max": "last_seen_year",
    "year_pop": "peak_year",
    "biblical": "is_biblical",
    "palindrome": "is_palindrome",
    "phones": "phonetic",
    "alliteration_first": "alliteration",
    "unisex": "is_unisex",
})

df["gender"] = df["gender"].replace({"F":"Female","M":"Male"})
df["name"] = df["name"].str.strip().str.title()

df["variants"] = df["variants"].apply(normalize_variants)
df["phonetic"] = df["phonetic"].apply(normalize_phonetics)
df["stresses"] = df["stresses"].apply(normalize_stresses)

df["slug"] = df["name"].apply(slugify)
df["length"] = df["name"].apply(name_length)

df.insert(0, "id", range(1, len(df)+1))

for col in ["is_biblical","is_palindrome","is_unisex"]:
    df[col] = df[col].fillna(False).astype(bool)

df.to_parquet(OUT/"names_cleaned.parquet", index=False)
df.to_csv(OUT/"names_cleaned.csv", index=False)

save_json(
    {
        "rows": len(df),
        "columns": len(df.columns),
        "output": "names_cleaned.parquet",
    },
    OUT/"cleaning_report.json",
)

print("Cleaning complete.")