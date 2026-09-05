from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

SEED_DIR = ROOT / "data" / "seed"

CSV = SEED_DIR / "knowledge_seed.csv"
PARQUET = SEED_DIR / "knowledge_seed.parquet"
REQUIRED_COLUMNS = {
    "language",
    "tier",
    "confidence",
    "resolver",
    "updated_at",
}


def split_pipe(value):
    if pd.isna(value) or value == "":
        return []

    return [v.strip() for v in str(value).split("|")]


df = pd.read_csv(CSV)

missing_columns = REQUIRED_COLUMNS - set(df.columns)
if missing_columns:
    raise ValueError(f"Missing required seed columns: {sorted(missing_columns)}")

df["variants"] = df["variants"].apply(split_pipe)
df["tags"] = df["tags"].apply(split_pipe)

df.to_parquet(PARQUET, index=False)

print(f"Created {PARQUET}")
print(f"Rows: {len(df)}")
