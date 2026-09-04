
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.knowledge import KnowledgeCache, KnowledgeRecord
from scripts.lib.origin import OriginResolver
from scripts.lib.pronunciation import (
    cmu_to_ipa,
    human_pronunciation,
)
from scripts.lib.providers.wikipedia import WikipediaProvider

GOLDEN = ROOT / "data" / "content" / "golden_500.csv"

BATCH_SIZE = 100

resolver = OriginResolver()
wiki = WikipediaProvider()
cache = KnowledgeCache()


def build_record(row):

    name = row["name"]

    phonetic = row.get("phonetic")

    if isinstance(phonetic, list):
        phonetic = " ".join(phonetic)

    ipa = cmu_to_ipa(str(phonetic)) if pd.notna(phonetic) else ""

    origin = resolver.resolve(name)

    wiki_data = wiki.resolve(name)

    meaning = ""
    description = ""

    if wiki_data:
        description = wiki_data["description"]

        if description:
            meaning = description.split(".")[0].strip()

    return KnowledgeRecord(
        name=name,
        meaning=meaning,
        origin=origin or "",
        ipa=ipa,
        pronunciation=human_pronunciation(name),
        source="wikipedia+resolver",
        verified=bool(origin or meaning),
    )


def main():

    df = pd.read_csv(GOLDEN, low_memory=False)

    processed = 0
    skipped = 0

    for _, row in df.iterrows():

        if processed >= BATCH_SIZE:
            break

        name = row["name"]

        if cache.get(name):
            skipped += 1
            continue

        cache.save(build_record(row))

        processed += 1

    print("=" * 45)
    print("LENABA KNOWLEDGE BATCH V2")
    print("=" * 45)
    print(f"Processed : {processed}")
    print(f"Skipped   : {skipped}")
    print(f"Finished  : {datetime.utcnow().isoformat()}Z")


if __name__ == "__main__":
    main()