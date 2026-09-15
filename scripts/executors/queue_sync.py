from pathlib import Path
from datetime import datetime
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib.normalization import normalize_series

QUEUE = ROOT / "data" / "knowledge" / "execution_queue.parquet"
FAMILIES = ROOT / "data" / "knowledge" / "canonical_families.parquet"
CACHE = ROOT / "data" / "cache" / "knowledge_cache.parquet"
BEHIND = ROOT / "data" / "outputs" / "behind_cache.parquet"
FETCH = ROOT / "data" / "outputs" / "fetch_results.parquet"


def run():

    print("=" * 50)
    print("LENABA QUEUE SYNC")
    print("=" * 50)

    queue = pd.read_parquet(QUEUE)
    families = pd.read_parquet(FAMILIES)

    queue["key"] = normalize_series(queue["canonical_name"])

    family_map = (
        families.assign(
            alias_key=normalize_series(families["alias"]),
            canonical_key=normalize_series(families["canonical_name"]),
        )[["alias_key", "canonical_key"]]
        .drop_duplicates()
    )

    if "status" not in queue.columns:
        queue["status"] = "pending"

    today = datetime.utcnow().strftime("%Y-%m-%d")

    if "status_updated_at" not in queue.columns:
        queue["status_updated_at"] = None

    if "completed_at" not in queue.columns:
        queue["completed_at"] = None

    # ---------- knowledge cache ----------

    completed = set()

    if CACHE.exists():
        cache = pd.read_parquet(CACHE)

        completed = set(
            cache.assign(alias_key=normalize_series(cache["name"]))
            .merge(family_map, on="alias_key", how="left")["canonical_key"]
            .dropna()
        )

    # ---------- behind cache ----------

    parsed = set()

    if BEHIND.exists():
        behind = pd.read_parquet(BEHIND)

        parsed = set(
            normalize_series(behind["canonical_name"])
        )

    # ---------- fetch results ----------

    fetched = set()

    if FETCH.exists():
        fetch = pd.read_parquet(FETCH)

        fetch = fetch.assign(
            alias_key=normalize_series(fetch["canonical_name"])
        )

        fetched = set(
            fetch.merge(
                family_map,
                left_on="alias_key",
                right_on="canonical_key",
                how="left",
            )["canonical_key"]
            .fillna(fetch["alias_key"])
        )

    completed_count = 0
    parsed_count = 0
    fetched_count = 0
    pending_count = 0

    for i in queue.index:

        key = queue.at[i, "key"]
        old = queue.at[i, "status"]

        if key in completed:
            new = "completed"

        elif key in parsed:
            new = "parsed"

        elif key in fetched:
            new = "fetched"

        else:
            new = "pending"

        queue.at[i, "status"] = new

        if new != old:
            queue.at[i, "status_updated_at"] = today

        if new == "completed":
            completed_count += 1

            if pd.isna(queue.at[i, "completed_at"]):
                queue.at[i, "completed_at"] = today

        elif new == "parsed":
            parsed_count += 1

        elif new == "fetched":
            fetched_count += 1

        else:
            pending_count += 1

    queue = queue.drop(columns=["key"])

    queue.to_parquet(QUEUE, index=False)

    print()
    print("=" * 36)
    print("QUEUE SYNC REPORT")
    print("=" * 36)
    print(f"Completed : {completed_count:,}")
    print(f"Parsed    : {parsed_count:,}")
    print(f"Fetched   : {fetched_count:,}")
    print(f"Pending   : {pending_count:,}")
    print("Saved: data/knowledge/execution_queue.parquet")


if __name__ == "__main__":
    run()
