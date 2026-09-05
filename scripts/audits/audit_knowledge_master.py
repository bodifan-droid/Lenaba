from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "data/knowledge/knowledge_master.parquet"

df = pd.read_parquet(MASTER)

print("=" * 40)
print("KNOWLEDGE MASTER AUDIT")
print("=" * 40)

print(f"Rows         : {len(df):,}")
print(f"Unique names : {df['name'].is_unique}")

if "verified" in df.columns:
    print(f"Verified     : {df['verified'].fillna(False).sum():,}")

for col in ["meaning", "origin", "pronunciation"]:
    if col in df.columns:
        print(f"{col.capitalize():13}: {df[col].notna().sum():,}")