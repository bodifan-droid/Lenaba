from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

NAMES = ROOT / "data" / "enriched" / "names.parquet"
LOG = ROOT / "data" / "outputs" / "slug_changes.parquet"

GENDER_SUFFIX = {
    "female": "f",
    "male": "m",
    "unisex": "u",
}


def clean(value):
    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    return value if value else None


def resolve():

    print("=" * 50)
    print("LENABA SLUG RESOLVER")
    print("=" * 50)

    df = pd.read_parquet(NAMES)

    original = df["slug"].copy()

    duplicates = df[df["slug"].duplicated(keep=False)]["slug"].unique()

    changes = []

    for slug in duplicates:

        group = df[df["slug"] == slug].copy()

        used = set()

        for idx, row in group.iterrows():

            gender = GENDER_SUFFIX.get(clean(row["gender"]), "u")

            candidate = f"{slug}-{gender}"

            origin = clean(row.get("origin"))

            if candidate in used:

                if origin:
                    candidate = f"{candidate}-{origin.replace(' ', '-')}"

            counter = 2

            final = candidate

            while final in used:

                final = f"{candidate}-{counter}"
                counter += 1

            used.add(final)

            df.at[idx, "slug"] = final

            changes.append(
                {
                    "name": row["name"],
                    "old_slug": slug,
                    "new_slug": final,
                    "gender": row["gender"],
                    "origin": row.get("origin"),
                }
            )

    df.to_parquet(NAMES, index=False)

    pd.DataFrame(changes).to_parquet(LOG, index=False)

    remaining = int(df["slug"].duplicated().sum())

    print()
    print("=" * 36)
    print("SLUG RESOLVER REPORT")
    print("=" * 36)
    print(f"Duplicate groups : {len(duplicates):,}")
    print(f"Slugs changed    : {len(changes):,}")
    print(f"Remaining dupes  : {remaining:,}")
    print("Saved:")
    print(" - data/enriched/names.parquet")
    print(" - data/outputs/slug_changes.parquet")


if __name__ == "__main__":
    resolve()
