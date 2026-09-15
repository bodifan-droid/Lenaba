from pathlib import Path
from datetime import datetime
import sys
import pandas as pd
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib.normalization import normalize_key

QUEUE = ROOT / "data" / "outputs" / "next_batch.parquet"
CACHE = ROOT / "data" / "cache" / "knowledge_cache.parquet"
OUTPUT = ROOT / "data" / "outputs" / "generator_results.parquet"
JSONL = ROOT / "data" / "outputs" / "generator_batch.jsonl"


BATCH_SIZE = 100


def load_cache():

    if CACHE.exists():
        return pd.read_parquet(CACHE)

    return pd.DataFrame(
        columns=[
            "name",
            "meaning",
            "origin",
            "ipa",
            "pronunciation",
            "source",
            "verified",
        ]
    )

def json_safe(value):
    """Convert pandas/numpy objects into JSON-safe Python values."""

    # numpy arrays
    if isinstance(value, np.ndarray):
        return value.tolist()

    # lists and tuples
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]

    # numpy scalar types (int64, float64, bool_)
    if hasattr(value, "item") and not isinstance(value, (str, bytes)):
        try:
            return value.item()
        except Exception:
            pass

    # NaN / None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    return value

def build_prompt(row):

    payload = {
        "canonical_name": json_safe(row["canonical_name"]),
        "family_id": json_safe(row["family_id"]),
        "gender": json_safe(row.get("gender")),
        "language": json_safe(row.get("dominant_language")),
        "missing": json_safe(row.get("missing")),
    }

    prompt = (
        "Return ONLY valid JSON.\n"
        "Fill the missing baby-name fields.\n"
        "Fields:\n"
        "- origin\n"
        "- meaning\n"
        "- short_description\n"
        "- seo_title\n"
        "- seo_description\n"
        "- fun_fact\n"
        "- popularity_summary\n"
        "- confidence (0-1)\n"
        f"\nInput:\n{json.dumps(payload, ensure_ascii=False)}"
    )

    return prompt

def run(batch_size=BATCH_SIZE):

    print("=" * 50)
    print("LENABA KNOWLEDGE GENERATOR")
    print("=" * 50)

    queue = pd.read_parquet(QUEUE).head(batch_size)
    cache = load_cache()

    cache_keys = set(
        cache["name"].astype(str).apply(normalize_key)
    )

    results = []

    skipped = 0

    for _, row in queue.iterrows():

        key = normalize_key(row["canonical_name"])

        if key in cache_keys:
            skipped += 1
            continue


    jsonl_lines = []

    results = []

    for _, row in queue.iterrows():

        key = normalize_key(row["canonical_name"])

        if key in cache_keys:
            skipped += 1
            continue

        prompt = build_prompt(row)

        jsonl_lines.append(
            json.dumps(
                {
                    "custom_id": row["family_id"],
                    "prompt": prompt,
                },
                ensure_ascii=False,
            )
        )

        results.append(
            {
                "family_id": row["family_id"],
                "canonical_name": row["canonical_name"],
                "status": "ready",
                "generated_at": datetime.utcnow().isoformat(),
            }
        )

    pd.DataFrame(results).to_parquet(
        OUTPUT,
        index=False,
    )


    with open(JSONL, "w", encoding="utf-8") as f:
        f.write("\n".join(jsonl_lines))

    print()
    print("=" * 36)
    print("GENERATOR REPORT")
    print("=" * 36)
    print(f"Batch size : {batch_size}")
    print(f"Ready      : {len(results)}")
    print(f"Skipped    : {skipped}")
    print("Saved:")
    print(" - data/outputs/generator_results.parquet")


if __name__ == "__main__":
    run()
