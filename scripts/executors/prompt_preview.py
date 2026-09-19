from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.family_prompt_builder import build_prompt

QUEUE = ROOT / "data" / "knowledge" / "execution_queue.parquet"


def run(limit=5):

    print("=" * 50)
    print("LENABA PROMPT PREVIEW")
    print("=" * 50)

    queue = pd.read_parquet(QUEUE).head(limit)

    for i, (_, row) in enumerate(queue.iterrows(), start=1):

        prompt = build_prompt(row.to_dict())

        print()
        print("-" * 60)
        print(f"{i}. {row['canonical_name']}")
        print("-" * 60)

        print("\nSYSTEM\n")
        print(prompt["system"])

        print("\nUSER\n")
        print(prompt["user"])


if __name__ == "__main__":
    run()
