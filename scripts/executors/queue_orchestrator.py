from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib.normalization import normalize_series

QUEUE = ROOT / "data" / "knowledge" / "execution_queue.parquet"
CACHE = ROOT / "data" / "cache" / "knowledge_cache.parquet"
BEHIND = ROOT / "data" / "outputs" / "behind_cache.parquet"
OUTPUT = ROOT / "data" / "outputs" / "next_batch.parquet"
FAMILIES = ROOT / "data" / "knowledge" / "canonical_families.parquet"


def run():

    print("=" * 50)
    print("LENABA QUEUE ORCHESTRATOR")
    print("=" * 50)

    queue = pd.read_parquet(QUEUE)

    queue["key"] = normalize_series(queue["canonical_name"])

    total = len(queue)

    in_cache = 0
    in_behind = 0

    # ---------- canonical family map ----------

    families = pd.read_parquet(FAMILIES)

    family_map = (
        families.assign(
            alias_key=normalize_series(families["alias"]),
            canonical_key=normalize_series(families["canonical_name"]),
        )[["alias_key", "canonical_key"]]
        .drop_duplicates()
    )

    # ---------- knowledge cache ----------

    if CACHE.exists():

        cache = pd.read_parquet(CACHE)

        cache = cache.assign(
            alias_key=normalize_series(cache["name"])
        )

        cache_canonical = (
            cache.merge(
                family_map,
                on="alias_key",
                how="left",
            )["canonical_key"]
            .dropna()
        )

        cache_keys = set(cache_canonical)

        mask_cache = queue["key"].isin(cache_keys)

        in_cache = int(mask_cache.sum())

        queue = queue.loc[~mask_cache].copy()

    # ---------- behind cache ----------

    if BEHIND.exists():

        behind = pd.read_parquet(BEHIND)

        behind_keys = set(
            normalize_series(behind["canonical_name"])
        )

        mask_behind = queue["key"].isin(behind_keys)

        in_behind = int(mask_behind.sum())

        queue = queue.loc[~mask_behind].copy()

    queue = queue.sort_values(
        by=["priority", "estimated_gain"],
        ascending=[False, False]
    )

    queue = queue.drop(columns=["key"])

    queue.to_parquet(OUTPUT, index=False)

    families = pd.read_parquet(FAMILIES)

    family_map = (
        families.assign(
            alias_key=normalize_series(families["alias"]),
            canonical_key=normalize_series(families["canonical_name"]),
        )[["alias_key", "canonical_key"]]
    )

    print()
    print("=" * 36)
    print("QUEUE ORCHESTRATOR REPORT")
    print("=" * 36)
    print(f"Families total      : {total:,}")
    print(f"Already in cache    : {in_cache:,}")
    print(f"Already in behind   : {in_behind:,}")
    print(f"Ready for execution : {len(queue):,}")
    print("Saved: data/outputs/next_batch.parquet")


if __name__ == "__main__":
    run()
