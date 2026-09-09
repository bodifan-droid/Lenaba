
from __future__ import annotations

import re
import pandas as pd

from scripts.lib.paths import KNOWLEDGE

MASTER = KNOWLEDGE / "knowledge_master.parquet"

PATTERN = re.compile(r"([A-Z][A-Z\s]+?)\(")


def extract_languages(value):

    langs = set()

    if value is None:
        return langs

    text = str(value)

    for m in PATTERN.findall(text):
        langs.add(m.title().strip())

    return langs


def has_text(value):

    if value is None:
        return False

    if isinstance(value, str):
        return value.strip() != ""

    if isinstance(value, list):
        return len(value) > 0

    if hasattr(value, "size"):  # numpy array
        return value.size > 0

    return not pd.isna(value)


def main():

    df = pd.read_parquet(MASTER)

    stats = {
        "language_column": 0,
        "ipa": 0,
        "phonetic": 0,
        "taxonomy_hint": 0,
    }

    language_hits = {}

    for _, row in df.iterrows():

        if has_text(row.get("language")):
            stats["language_column"] += 1

        if has_text(row.get("ipa")):
            stats["ipa"] += 1

        if has_text(row.get("phonetic")):
            stats["phonetic"] += 1

        langs = set()

        for col in [
            "variants",
            "equivalents",
            "other_forms",
            "other_readings",
        ]:
            langs |= extract_languages(row.get(col))

        if langs:
            stats["taxonomy_hint"] += 1

            for lang in langs:
                language_hits[lang] = language_hits.get(lang, 0) + 1

    print("=" * 55)
    print("LENABA LOCAL PRON SOURCE AUDIT")
    print("=" * 55)

    for k, v in stats.items():
        print(f"{k:18}: {v:,}")

    print("\nTop detected languages")
    print("-" * 55)

    print(
        pd.Series(language_hits)
        .sort_values(ascending=False)
        .head(20)
    )


if __name__ == "__main__":
    main()
