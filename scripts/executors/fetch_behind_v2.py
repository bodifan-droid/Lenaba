from __future__ import annotations
import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

HTML_CACHE = ROOT / "data" / "outputs" / "behind_html"
HTML_CACHE.mkdir(parents=True, exist_ok=True)

from lib.behind_client import fetch_html
from lib.human_delay import HumanDelay
from lib.behind_parser import parse_name_page
from lib.behind_client import slugify
from lib.family_updater import update_family
from lib.pipeline_hooks import after_fetch
from lib.paths import KNOWLEDGE
from lib.completion_score import completion_score
from lib.new_name_candidates import collect_missing_family
from lib.schema_adapter import normalize_name_key
from lib.family_registry import is_done, mark_done

load_dotenv()
human = HumanDelay()

NAMES = ROOT / "data" / "enriched" / "names.parquet"

API_KEY = os.getenv("BEHIND_NAME_API_KEY")

if not API_KEY:
    raise RuntimeError("BEHIND_NAME_API_KEY not found")


def ensure_columns(df):

    defaults = {
        "family_processed": False,
        "canonical_family": None,
        "family_source": None,
        "completion_score": 0,
    }

    for col, value in defaults.items():

        if col not in df.columns:
            df[col] = value

    return df


def next_names(df, limit):

    pending = (
        df[df["family_processed"] == False]
        .sort_values("completion_score")
    )

    return pending.head(limit)


def process_name(df, idx):

    name = df.at[idx, "name"]

    print(f"\n{name}")

    cache_file = HTML_CACHE / f"{slugify(name)}.html"

    # -----------------------------
    # HTML cache
    # -----------------------------

    if cache_file.exists():

        html = cache_file.read_text(
            encoding="utf-8"
        )

        print("  html cache")

    else:

        canonical = df.at[idx, "canonical_family"]

        if isinstance(canonical, str) and is_done(canonical):

            print(f"  skipped (family already done: {canonical})")

            df.at[idx, "family_processed"] = True

            return df

        human.before_request()

        result = fetch_html(name)

        if result is None:
            html = None
        else:
            _, html = result

        human.after_request()

        human.after_request()

        if html is None:

            print("  404 skipped")

            df.at[idx, "family_processed"] = True

            if "family_source" in df.columns:
                df.at[idx, "family_source"] = "not_found"

            if "completion_score" in df.columns:
                df.at[idx, "completion_score"] = -1

            return df

        cache_file.write_text(
            html,
            encoding="utf-8",
        )

        print("  BTN")

    # -----------------------------
    # Parse every time
    # -----------------------------

    parsed = parse_name_page(
        html,
        current_name=name,
    )

    print("=" * 45)
    print(name)
    print("=" * 45)

    preview_fields = [
        "canonical_name",
        "origin_language",
        "usage",
        "pronunciation",
        "etymology_roots",
        "variants",
        "other_languages",
        "variant_languages",
        "diminutives",
        "feminine_forms",
        "masculine_forms",
        "script",
        "famous_people",
        "source_refs",
        "completion_score",
    ]

    for field in preview_fields:

        value = parsed.get(field)

        if value in (None, "", []):
            continue

        print(f"{field:18} {value}")

    # -----------------------------
    # Update family
    # -----------------------------

    df, family_id, members, updated, missing_names = update_family(
        df,
        name,
        parsed,
    )


    mark_done(family_id)

    after_fetch(name, parsed)

    btn_total = len(members)
    coverage = f"{updated}/{btn_total}"
    missing = len(missing_names)

    print(f"  family: {family_id}")
    print(f"  family members: {btn_total}")
    print(f"  updated rows: {updated}")
    print(f"  coverage: {coverage}")
    print(f"  missing: {missing}")

    if missing_names:
        print("  missing names:")
        for item in missing_names[:10]:
            print(f"    - {item}")

    collect_missing_family(
        family_id,
        parsed,
        missing_names,
    )

    parsed["completion_score"] = completion_score(parsed)

    members = sorted(set(members))
    preview = ", ".join(members[:8])

    if len(members) > 8:
        preview += ", ..."

    return df

def run(limit=10):

    print("=" * 50)
    print("LENABA FAMILY BUILDER V2")
    print("=" * 50)

    df = pd.read_parquet(NAMES)

    df = ensure_columns(df)

    completed = int(df["family_processed"].sum())
    remaining = len(df) - completed

    print(f"Completed : {completed:,}")
    print(f"Remaining : {remaining:,}")

    pending = next_names(df, limit)

    print(f"Processing: {len(pending)} names")

    for idx in pending.index:

        df = process_name(df, idx)

        df.to_parquet(NAMES, index=False)
        print("  saved checkpoint")

    print("\nDone.")


if __name__ == "__main__":

    limit = 10

    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    run(limit)
