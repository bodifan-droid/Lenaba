from __future__ import annotations

import subprocess
from io import BytesIO

import pandas as pd

from scripts.lib.paths import OUTPUTS

TAG = "v0.4.5-smart-knowledge"
FILE = "data/knowledge/knowledge_master.parquet"
OUT = OUTPUTS / "legacy_patch.parquet"


def main():

    print("=" * 45)
    print("LEGACY KNOWLEDGE PATCH")
    print("=" * 45)

    blob = subprocess.check_output(
        ["git", "show", f"{TAG}:{FILE}"]
    )

    legacy = pd.read_parquet(BytesIO(blob))

    keep = [
        "name",
        "meaning",
        "origin",
        "pronunciation",
        "variants",
        "equivalents",
        "related",
        "script",
        "confidence",
        "verified",
        "source",
    ]

    keep = [c for c in keep if c in legacy.columns]

    legacy = legacy[keep].drop_duplicates("name")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    legacy.to_parquet(OUT, index=False)

    print(f"Rows   : {len(legacy):,}")
    print(f"Fields : {len(legacy.columns)}")
    print(f"Saved  : {OUT}")


if __name__ == "__main__":
    main()
