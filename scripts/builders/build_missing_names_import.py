
from pathlib import Path
import pandas as pd

NAMES = Path("data/enriched/names.parquet")
MISSING = Path("data/editorial/missing_btn_names.parquet")


def normalize(name):
    return (
        str(name)
        .strip()
        .upper()
        .replace("’", "'")
    )


def main():

    if not MISSING.exists():
        print("No missing names found.")
        return

    names = pd.read_parquet(NAMES)
    missing = pd.read_parquet(MISSING)

    existing = {
        normalize(n)
        for n in names["name"]
    }

    rows = []

    for _, row in missing.iterrows():

        key = normalize(row["name"])

        if key in existing:
            continue

        rows.append({
            "name": row["name"].title(),
            "gender": None,
            "family_processed": True,
            "family_id": row["family"],
            "canonical_family": row["family"],
            "family_slug": row["family"].lower(),
            "family_source": "behindthename",
        })

        existing.add(key)

    if not rows:
        print("Nothing new to import.")
        return

    new_df = pd.DataFrame(rows)

    names = pd.concat(
        [names, new_df],
        ignore_index=True,
    )

    names.to_parquet(NAMES, index=False)

    print("=" * 45)
    print("MISSING NAMES IMPORT")
    print("=" * 45)
    print(f"Imported: {len(rows)}")
    print(f"Total names: {len(names):,}")


if __name__ == "__main__":
    main()
