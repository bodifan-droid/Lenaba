from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

# ---- project paths ----

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.family_script_schema import FamilyScript
from lib.family_slug import family_slug

# ---- data files ----

QUEUE = ROOT / "data" / "knowledge" / "execution_queue.parquet"
OUTPUT = ROOT / "data" / "knowledge" / "family_scripts.parquet"

def run(limit: int = 100):

    print("=" * 50)
    print("LENABA FAMILY SCRIPT BUILDER")
    print("=" * 50)

    queue = pd.read_parquet(QUEUE)

    queue = queue.head(limit)

    existing = {}

    if OUTPUT.exists() and OUTPUT.stat().st_size > 0:
        old = pd.read_parquet(OUTPUT)
        existing = {
            row["family_id"]: row
            for _, row in old.iterrows()
        }

    rows = []

    skipped = 0

    for _, row in queue.iterrows():

        family_id = row["family_id"]

        if family_id in existing:
            rows.append(existing[family_id])
            skipped += 1
            continue

        script = FamilyScript(
            family_id=family_id,
            canonical_name=row["canonical_name"],
            family_slug=family_slug(row["canonical_name"]),
        )

        rows.append(script.to_dict())

    out = pd.DataFrame(rows)

    out.to_parquet(OUTPUT, index=False)

    print()
    print("=" * 36)
    print("FAMILY SCRIPT REPORT")
    print("=" * 36)
    print(f"Requested : {limit}")
    print(f"Created   : {len(out)-skipped}")
    print(f"Skipped   : {skipped}")
    print(f"Saved     : {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    run()
