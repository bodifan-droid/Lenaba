from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_parquet(ROOT / "data/content/content_registry.parquet")

fields = [
    "meaning",
    "origin",
    "ipa",
    "pronunciation",
    "tags",
    "seo_description",
]

print("\nLENABA CONTENT AUDIT\n")

for col in fields:
    filled = df[col].notna().sum() if col in df.columns else 0
    pct = filled / len(df) * 100
    print(f"{col:20} {filled:>7,} ({pct:5.1f}%)")

print("\nStatus distribution:\n")
print(df["status"].value_counts())

print("\nTier distribution:\n")
print(df["tier"].value_counts())