from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

SOURCE = ROOT / "data/imports/behind_the_name/dataset3.csv"
if not SOURCE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {SOURCE}"
    )
MASTER = ROOT / "data/knowledge/knowledge_master.parquet"


def main():

    incoming = pd.read_csv(SOURCE, low_memory=False)

    incoming.columns = (
        incoming.columns
        .str.lower()
        .str.strip()
    )

    rename = {
        "pronounciation": "pronunciation"
    }

    incoming = incoming.rename(columns=rename)

    keep = [
        "name",
        "gender",
        "meaning",
        "origin",
        "pronunciation",
        "equivalents",
        "scripts",
    ]

    keep = [c for c in keep if c in incoming.columns]

    incoming = incoming[keep].copy()

    incoming["source"] = "behindthename_dataset"
    incoming["confidence"] = 0.95
    incoming["verified"] = True

    if MASTER.exists():
        master = pd.read_parquet(MASTER)
    else:
        master = pd.DataFrame()

    merged = pd.concat([master, incoming], ignore_index=True)

    merged = (
        merged
        .sort_values("confidence")
        .drop_duplicates("name", keep="last")
        .sort_values("name")
        .reset_index(drop=True)
    )

    merged.to_parquet(MASTER, index=False)

    print("=" * 40)
    print("BEHINDTHENAME IMPORT COMPLETE")
    print("=" * 40)
    print(f"Imported : {len(incoming):,}")
    print(f"Master   : {len(merged):,}")


if __name__ == "__main__":
    main()