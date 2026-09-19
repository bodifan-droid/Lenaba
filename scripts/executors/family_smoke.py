from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

GOLDEN = ROOT / "data" / "tests" / "golden_families.json"
FAMILIES = ROOT / "data" / "knowledge" / "canonical_families_v2.parquet"


def run():

    golden = json.loads(GOLDEN.read_text(encoding="utf-8"))

    df = pd.read_parquet(FAMILIES)

    if df.empty:
        print("canonical_families_v2.parquet is empty.")
        return

    required = {"canonical_name", "alias"}

    missing = required - set(df.columns)

    if missing:
        print(f"Missing columns: {missing}")
        return

    ok = True

    for family, rules in golden.items():

        aliases = set(
            df[df["canonical_name"] == family]["alias"]
        )

        missing = [
            x
            for x in rules["must_include"]
            if x not in aliases
        ]

        leaked = [
            x
            for x in rules["must_exclude"]
            if x in aliases
        ]

        print()
        print("=" * 40)
        print(family)
        print("=" * 40)

        print("Missing :", missing or "OK")
        print("Leaked  :", leaked or "OK")

        if missing or leaked:
            ok = False

    print()
    print("=" * 40)

    if ok:
        print("GOLDEN TEST PASSED")
    else:
        print("GOLDEN TEST FAILED")


if __name__ == "__main__":
    run()
