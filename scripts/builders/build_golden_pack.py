
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd

from scripts.lib.providers.behind_name import BehindTheNameProvider
from scripts.lib.confidence import can_verify

REGISTRY = ROOT / "data/content/content_registry.parquet"
PACKS_DIR = ROOT / "data/content/packs"

PACK_SIZE = 100


def next_pack_number():
    PACKS_DIR.mkdir(parents=True, exist_ok=True)

    packs = sorted(PACKS_DIR.glob("golden_pack_*.parquet"))

    if not packs:
        return 1

    last = packs[-1].stem.split("_")[-1]

    return int(last) + 1


def main():

    provider = BehindTheNameProvider()

    df = pd.read_parquet(REGISTRY)

    queued = (
        df[
            (df["campaign"] == "golden_500")
            & (df["stage"].isin(["queued", "processing"]))
        ]
        .sort_values("priority")
        .head(PACK_SIZE)
        .copy()
    )

    if queued.empty:
        print("No queued names found.")
        return

    pack_number = next_pack_number()

    processed = 0

    for idx, row in queued.iterrows():

        if df.at[idx, "stage"] == "queued":
            df.at[idx, "stage"] = "processing"

        result = provider.resolve(row["name"])

        if result:

            if result.meaning:
                df.at[idx, "meaning"] = result.meaning
                df.at[idx, "meaning_done"] = True

            if result.origin:
                df.at[idx, "origin"] = result.origin
                df.at[idx, "origin_done"] = True

            if result.pronunciation:
                df.at[idx, "pronunciation"] = result.pronunciation

            df.at[idx, "source"] = result.source
            df.at[idx, "confidence"] = result.confidence

            if can_verify(result.confidence):

                df.at[idx, "verified"] = True
                df.at[idx, "stage"] = "verified"

            processed += 1

    pack = (
        df[
            (df["campaign"] == "golden_500")
            & (df["stage"] == "verified")
        ]
        .sort_values("priority")
        .head(pack_number * PACK_SIZE)
    )

    output = PACKS_DIR / f"golden_pack_{pack_number:03}.parquet"

    pack.to_parquet(output, index=False)

    df.to_parquet(REGISTRY, index=False)

    df.to_csv(
        ROOT / "data/content/content_registry.csv",
        index=False,
    )

    print("=" * 45)
    print("LENABA GOLDEN PACK")
    print("=" * 45)
    print(f"Pack      : {pack_number:03}")
    print(f"Queued    : {len(queued)}")
    print(f"Processed : {processed}")
    print(f"Saved     : {output.name}")
    print(f"Time      : {datetime.utcnow().isoformat()}Z")


if __name__ == "__main__":
    main()