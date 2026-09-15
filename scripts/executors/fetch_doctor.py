from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib.normalization import normalize_key

QUEUE = ROOT / "data" / "knowledge" / "execution_queue.parquet"
FAMILIES = ROOT / "data" / "knowledge" / "canonical_families.parquet"
CACHE = ROOT / "data" / "cache" / "knowledge_cache.parquet"
BEHIND = ROOT / "data" / "outputs" / "behind_cache.parquet"
FETCH = ROOT / "data" / "outputs" / "fetch_results.parquet"


def build_family_map():
    fam = pd.read_parquet(FAMILIES)

    return (
        fam.assign(
            alias_key=fam["alias"].apply(normalize_key),
            canonical_key=fam["canonical_name"].apply(normalize_key),
        )[["alias_key", "canonical_key"]]
        .drop_duplicates()
    )


def run(name: str):

    key = normalize_key(name)

    queue = pd.read_parquet(QUEUE)
    family_map = build_family_map()

    queue["key"] = queue["canonical_name"].apply(normalize_key)

    canonical = family_map.loc[
        family_map["alias_key"] == key,
        "canonical_key",
    ]

    if canonical.empty:
        canonical = family_map.loc[
            family_map["canonical_key"] == key,
            "canonical_key",
        ]

    if len(canonical):
        key = canonical.iloc[0]

    if len(canonical):
        key = canonical.iloc[0]

    row = queue.loc[queue["key"] == key]

    print("=" * 36)
    print("FETCH DOCTOR")
    print("=" * 36)

    if row.empty:
        print(f"\n{name}: family not found.")
        return

    row = row.iloc[0]

    print(f"\nFamily        : {row['canonical_name']}")
    print(f"Status        : {row.get('status', 'pending')}")
    print(f"Priority      : {row['priority']}")
    print(f"Estimated gain: {row['estimated_gain']}")

    cache = False
    behind = False
    fetched = False

    if CACHE.exists():
        c = pd.read_parquet(CACHE)
        cache = key in set(
            c["name"].apply(normalize_key)
        )

    if BEHIND.exists():
        b = pd.read_parquet(BEHIND)
        behind = key in set(
            b["canonical_name"].apply(normalize_key)
        )

    if FETCH.exists():
        f = pd.read_parquet(FETCH)
        fetched = key in set(
            f["canonical_name"].apply(normalize_key)
        )

    print("\nSources")
    print(f"execution_queue : ✓")
    print(f"knowledge_cache : {'✓' if cache else '✗'}")
    print(f"behind_cache    : {'✓' if behind else '✗'}")
    print(f"fetch_results   : {'✓' if fetched else '✗'}")

    status = row.get("status", "pending")

    if status == "completed":
        next_step = "Nothing"
    elif status == "parsed":
        next_step = "Execution Engine"
    elif status == "fetched":
        next_step = "Knowledge Generator"
    else:
        next_step = "Queue Orchestrator"

    status = row.get("status", "pending")

    if status == "completed":
        next_step = "Nothing"
    elif status == "parsed":
        next_step = "Execution Engine"
    elif fetched:
        next_step = "Knowledge Generator"
    else:
        next_step = "Queue Orchestrator"

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("python scripts/executors/fetch_doctor.py LIAM")
        sys.exit(1)

    run(" ".join(sys.argv[1:]))
