from __future__ import annotations

from datetime import datetime
import sys

from scripts.lib.paths import ROOT, CONTENT, KNOWLEDGE

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd

from scripts.lib.providers.behind_name import BehindTheNameProvider
from scripts.lib.confidence import can_verify

REGISTRY = CONTENT / "content_registry.parquet"
PACKS_DIR = CONTENT / "packs"
MASTER = KNOWLEDGE / "knowledge_master.parquet"

PACK_SIZE = 100


def next_pack_number():
    PACKS_DIR.mkdir(parents=True, exist_ok=True)

    packs = sorted(PACKS_DIR.glob("golden_pack_*.parquet"))

    if not packs:
        return 1

    last = packs[-1].stem.split("_")[-1]

    return int(last) + 1

def has_value(value):
    """Array-safe check for meaningful values."""

    if isinstance(value, list):
        return len(value) > 0

    if hasattr(value, "size"):   # numpy array
        return value.size > 0

    if pd.isna(value):
        return False

    if isinstance(value, str):
        return value.strip() != ""

    return True

def main():

    provider = BehindTheNameProvider()

    df = pd.read_parquet(REGISTRY)

    master = pd.read_parquet(MASTER)

    master = (
        master
        .sort_values("confidence")
        .drop_duplicates("name", keep="last")
    )

    lookup = master.set_index("name")

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

        name = row["name"]

# ---------- 1. Спочатку беремо з Knowledge Master ----------

        if name in lookup.index:

            kb = lookup.loc[name]

            for field in [
                "meaning",
                "origin",
                "pronunciation",
                "gender",
                "variants",
                "equivalents",
                "scripts",
            ]:
                if field in kb.index:
                    value = kb[field]

                    if has_value(value):
                        df.at[idx, field] = value

            confidence = kb.get("confidence", 0)
            source = kb.get("source", "knowledge_master")

# ---------- 2. Якщо нема — звертаємось до Provider ----------

        else:

            result = provider.resolve(name)

            if result is None:
                continue

            if result.meaning:
                df.at[idx, "meaning"] = result.meaning

            if result.origin:
                df.at[idx, "origin"] = result.origin

            if result.pronunciation:
                df.at[idx, "pronunciation"] = result.pronunciation

            confidence = result.confidence
            source = result.source

# ---------- Common ----------

        df.at[idx, "source"] = source
        df.at[idx, "confidence"] = confidence

        df.at[idx, "meaning_done"] = bool(df.at[idx, "meaning"])
        df.at[idx, "origin_done"] = bool(df.at[idx, "origin"])

        if can_verify(confidence):
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