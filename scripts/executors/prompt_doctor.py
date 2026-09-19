from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.normalization import normalize_key

QUEUE = ROOT / "data" / "knowledge" / "execution_queue.parquet"
NAMES = ROOT / "data" / "enriched" / "names.parquet"
FAMILIES = ROOT / "data" / "knowledge" / "canonical_families.parquet"


def run(name: str):

    key = normalize_key(name)

    queue = pd.read_parquet(QUEUE)
    names = pd.read_parquet(NAMES)
    families = pd.read_parquet(FAMILIES)

    q = queue[
        normalize_key(queue["canonical_name"]) == key
    ]

    if q.empty:
        print(f"{name}: family not found.")
        return

    row = q.iloc[0]

    aliases = families[
        normalize_key(families["canonical_name"]) == key
    ]

    ipa = names[
        normalize_key(names["name"]).isin(
            normalize_key(aliases["alias"])
        )
    ]["ipa"].notna().sum()

    print("="*36)
    print("PROMPT DOCTOR")
    print("="*36)
    print()
    print("Canonical :", row["canonical_name"])
    print("Family ID :", row["family_id"])
    print("Family size:", row["family_size"])
    print("Variants :", len(aliases))
    print("IPA filled:", ipa)
