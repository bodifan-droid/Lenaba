from scripts.lib.paths import KNOWLEDGE
import pandas as pd

MASTER = KNOWLEDGE / "knowledge_master.parquet"

df = pd.read_parquet(MASTER)

def filled(col):
    if col not in df.columns:
        return 0
    return (
        df[col]
        .fillna("")
        .astype(str)
        .str.strip()
        .ne("")
        .sum()
    )

print("="*45)
print("LENABA COMPLETION AUDIT")
print("="*45)
print(f"Total names      : {len(df):,}")
print(f"Meaning          : {filled('meaning'):,}")
print(f"Origin           : {filled('origin'):,}")
print(f"Pronunciation    : {filled('pronunciation'):,}")
print(f"Variants         : {filled('variants'):,}")
print(f"Equivalents      : {filled('equivalents'):,}")
print(f"Related          : {filled('related'):,}")
print(f"Scripts          : {filled('scripts'):,}")