from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.family_context import build_context


def run(name: str):

    print("=" * 50)
    print("LENABA FAMILY CONTEXT")
    print("=" * 50)
    print()

    context = build_context(name)

    print(
        json.dumps(
            context.to_dict(),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: context_preview.py NAME")
        raise SystemExit(1)

    run(sys.argv[1])
