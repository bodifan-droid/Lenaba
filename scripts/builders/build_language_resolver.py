
from __future__ import annotations

import re
from collections import Counter

import pandas as pd

from scripts.lib.paths import KNOWLEDGE
from scripts.lib.validate_master import run_integrity_gate

MASTER = KNOWLEDGE / "knowledge_master.parquet"
OUT = KNOWLEDGE / "language_resolver.parquet"

PATTERN = re.compile(r"([A-Z][A-Z\s]+?)\(")


def extract_languages(value):

    if value is None:
        return []

    text = str(value)

    return [
        lang.title().strip()
        for lang in PATTERN.findall(text)
    ]


def main():

    master = pd.read_parquet(MASTER)

    rows = []

    for row in master.itertuples(index=False):

        counter = Counter()

        # 1. Existing language field gets extra weight
        language = getattr(row, "language", None)

        if isinstance(language, str) and language.strip():
            counter[language.strip()] += 3

        # 2. Parse taxonomy hints
        for col in [
            "variants",
            "equivalents",
            "other_forms",
            "other_readings",
        ]:

            if hasattr(row, col):
                for lang in extract_languages(getattr(row, col)):
                    counter[lang] += 1

        if counter:
            dominant, votes = counter.most_common(1)[0]
            confidence = votes / sum(counter.values())

            rows.append({
                "name": row.name,
                "dominant_language": dominant,
                "confidence": round(confidence, 3),
                "sources_found": sum(counter.values()),
                "languages": sorted(counter.keys()),
            })

    resolver = pd.DataFrame(rows)

    resolver.to_parquet(OUT, index=False)

    run_integrity_gate(master)

    print("=" * 45)
    print("LANGUAGE RESOLVER BUILT")
    print("=" * 45)
    print(f"Resolved names : {len(resolver):,}")
    print(f"Output         : {OUT.name}")


if __name__ == "__main__":
    main()
