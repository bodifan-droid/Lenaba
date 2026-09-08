from __future__ import annotations

import re
import ast
import pandas as pd

from scripts.lib.paths import KNOWLEDGE

MASTER = KNOWLEDGE / "knowledge_master.parquet"

PATTERN = re.compile(r"[A-Z][A-Z\s]+?\(.*?\)")

FIELDS = [
    "variants",
    "equivalents",
    "scripts",
    "other_forms",
    "other_readings",
]

def to_list(value):

    if value is None:
        return []

    if isinstance(value, list):
        return value

    if hasattr(value, "tolist"):
        return value.tolist()

    if pd.isna(value):
        return []

    if isinstance(value, str):

        value = value.strip()

        if not value:
            return []

        if value.startswith("[") and value.endswith("]"):
            try:
                parsed = ast.literal_eval(value)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass

        return [value]

    return [str(value)]

def main():

    df = pd.read_parquet(MASTER)

    print("="*60)
    print("LENABA TAXONOMY SOURCE AUDIT")
    print("="*60)

    for field in FIELDS:

        if field not in df.columns:
            continue

        matches = []

        for value in df[field]:

            for item in to_list(value):

                if PATTERN.search(str(item)):
                    matches.append(str(item))

        print(f"\n{field}")
        print("-"*40)
        print(f"Matches: {len(matches):,}")

        for sample in matches[:5]:
            print(sample)

if __name__ == "__main__":
    main()