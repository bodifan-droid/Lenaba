
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "data/content/packs/golden_pack_001.parquet"

df = pd.read_parquet(PACK)

print("=" * 45)
print("GOLDEN PACK AUDIT")
print("=" * 45)

print(f"Rows         : {len(df)}")
print(f"Meaning      : {df['meaning'].notna().sum()}")
print(f"Origin       : {df['origin'].notna().sum()}")
print(f"Pronunciation: {df['pronunciation'].notna().sum()}")
print(f"Verified     : {(df['stage']=='verified').sum()}")
print(f"Confidence≥.9: {(df['confidence']>=0.9).sum()}")