
from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

MASTER = KNOWLEDGE / "knowledge_master.parquet"
FAMILIES = KNOWLEDGE / "canonical_families.parquet"
OUT = KNOWLEDGE / "smart_queue.parquet"



def missing_fields(row):

    missing = []

    for field in [
        "meaning",
        "origin",
        "pronunciation",
    ]:
        value = row.get(field)

        if pd.isna(value) or value == "":
            missing.append(field)

    return missing


def priority(row):

    score = 0

    score += row["family_size"]

    score += (5 - len(row["missing"]))

    if row["completion_level"] == "platinum":
        score += 20
    elif row["completion_level"] == "gold":
        score += 15
    elif row["completion_level"] == "silver":
        score += 8

    return score


def main():

    master = pd.read_parquet(MASTER)
    families = pd.read_parquet(FAMILIES)

    canonical = families[families["is_canonical"]].copy()

    family_sizes = (
        families.groupby("family_id")
        .size()
        .rename("family_size")
    )

    canonical = canonical.merge(
        family_sizes,
        on="family_id",
        how="left",
    )

    master_lookup = master.set_index("name")

    rows = []

    for row in canonical.itertuples(index=False):

        name = row.canonical_name

        if name not in master_lookup.index:
            continue

        data = master_lookup.loc[name]

        missing = missing_fields(data)

        if not missing:
            continue

        rows.append({
            "family_id": row.family_id,
            "canonical_name": name,
            "family_size": row.family_size,
            "completion_level": data.get("completion_level"),
            "missing": missing,
        })

    queue = pd.DataFrame(rows)

    if not queue.empty:
        queue["priority"] = queue.apply(priority, axis=1)
        queue = (
            queue
            .sort_values("priority", ascending=False)
            .reset_index(drop=True)
        )

    queue.to_parquet(OUT, index=False)

    print("=" * 45)
    print("SMART QUEUE BUILT")
    print("=" * 45)
    print(f"Families queued : {len(queue):,}")
    print(f"Output          : {OUT.name}")


if __name__ == "__main__":
    main()
