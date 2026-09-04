
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_parquet(
    ROOT / "data/content/content_registry.parquet"
)

golden = df[df["tier"] == "golden"]

print("=" * 40)
print("LENABA KNOWLEDGE AUDIT")
print("=" * 40)

metrics = {
    "Meaning": golden["meaning_done"].sum(),
    "Origin": golden["origin_done"].sum(),
    "IPA": golden["ipa_done"].sum(),
    "Tags": golden["tags_done"].sum(),
    "SEO": golden["seo_done"].sum(),
}

print(f"Golden total : {len(golden)}")
for k, v in metrics.items():
    print(f"{k:<12}: {v}")