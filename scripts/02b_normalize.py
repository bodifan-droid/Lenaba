
from pathlib import Path
import pandas as pd

from lib.parsing import (
    normalize_variants,
    normalize_phonetics,
    normalize_stresses,
)
from lib.reports import save_json

ROOT = Path(__file__).resolve().parent.parent
CLEAN = ROOT / "data" / "cleaned"

df = pd.read_parquet(CLEAN/"names_cleaned.parquet")

df["variants"] = df["variants"].apply(normalize_variants)
df["phonetic"] = df["phonetic"].apply(normalize_phonetics)
df["stresses"] = df["stresses"].apply(normalize_stresses)

# ---------- Main table ----------

names = df[
    [
        "id","name","gender","slug",
        "first_letter","length","syllables",
        "is_biblical","is_palindrome","is_unisex",
    ]
]

# ---------- Variants ----------

variant_rows = []

for _, row in df.iterrows():
    for variant in row["variants"]:
        variant_rows.append(
            {
                "canonical_id": row["id"],
                "canonical_name": row["name"],
                "variant": variant,
            }
        )

name_variants = pd.DataFrame(variant_rows)

# ---------- Phonetics ----------

phonetic_rows = []

for _, row in df.iterrows():
    for i, phone in enumerate(row["phonetic"]):

        stress = row["stresses"][i] if i < len(row["stresses"]) else None

        phonetic_rows.append(
            {
                "name_id": row["id"],
                "name": row["name"],
                "phonetic": phone,
                "stress_pattern": stress,
            }
        )

phonetics = pd.DataFrame(phonetic_rows)

# ---------- Stats ----------

stats = df[
    [
        "id",
        "name",
        "popularity_score",
        "first_seen_year",
        "last_seen_year",
        "peak_year",
    ]
]

# ---------- Save ----------

names.to_parquet(CLEAN/"names.parquet", index=False)
name_variants.to_parquet(CLEAN/"name_variants.parquet", index=False)
phonetics.to_parquet(CLEAN/"phonetics.parquet", index=False)
stats.to_parquet(CLEAN/"name_stats.parquet", index=False)

save_json(
    {
        "names": len(names),
        "variants": len(name_variants),
        "phonetics": len(phonetics),
        "stats": len(stats),
    },
    CLEAN/"normalization_report.json",
)

print("Normalization complete.")