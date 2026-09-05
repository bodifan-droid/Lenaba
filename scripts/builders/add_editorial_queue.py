
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

FILE = ROOT / "data/content/content_registry.parquet"

df = pd.read_parquet(FILE)

if "campaign" not in df.columns:
    df["campaign"] = ""

if "stage" not in df.columns:
    df["stage"] = "queued"

df.loc[df["tier"] == "golden", "campaign"] = "golden_500"

import os

csv_file = ROOT / "data/content/content_registry.csv"
tmp_file = csv_file.with_suffix(".tmp.csv")

df.to_parquet(FILE, index=False)

try:
    df.to_csv(tmp_file, index=False)

    os.replace(tmp_file, csv_file)

    print("[OK] Editorial Queue added.")

except PermissionError:

    if tmp_file.exists():
        tmp_file.unlink()

    print("[ERROR] content_registry.csv is open.")
    print("Close Excel/VS Code and run the script again.")