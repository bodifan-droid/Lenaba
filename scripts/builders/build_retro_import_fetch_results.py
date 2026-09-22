
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.master_writer import write_to_master

FETCH = ROOT / "data" / "outputs" / "fetch_results.parquet"


def empty(value):
    if value is None:
        return True
    if isinstance(value, float) and pd.isna(value):
        return True
    if isinstance(value, list):
        return len(value) == 0
    if isinstance(value, str):
        return value.strip() == ""
    return False


def main():

    df = pd.read_parquet(FETCH)

    print("=" * 50)
    print("RETRO IMPORT FROM FETCH RESULTS")
    print("=" * 50)
    print(f"Parsed families: {len(df):,}")

    pages = 0
    fields = 0

    for _, row in df.iterrows():

        parsed = {}

        for col in df.columns:

            value = row[col]

            if empty(value):
                continue

            parsed[col] = value

        name = (
            row["canonical_name"]
            if not empty(row["canonical_name"])
            else row["family_id"]
        )

        updated = write_to_master(name, parsed)

        if updated:
            pages += 1
            fields += updated

    print("-" * 50)
    print(f"Families updated : {pages}")
    print(f"Fields written   : {fields}")
    print("=" * 50)


if __name__ == "__main__":
    main()
