from __future__ import annotations
import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
import time
from collections import deque

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
        df[~df["family_processed"].fillna(False).astype(bool)]
        .sort_values("completion_score")
    )

    return pending.head(limit)


def process_name(df, idx, force=False):

    name = df.at[idx, "name"]

    # Skip only in production mode
    if not force and bool(df.at[idx, "family_processed"]):
        family = (
            df.at[idx, "canonical_family"]
            or df.at[idx, "family_id"]
            or "UNKNOWN"
        )
        print(f"\n{name}")
        print(f"  skipped (family already done: {family})")
        return df

    print(f"\n{name}")

    family = (
        df.at[idx, "canonical_family"]
        or df.at[idx, "family_id"]
    )

    if not force and isinstance(family, str) and is_done(family):
        print(f"  skipped (family already completed: {family})")
        df.at[idx, "family_processed"] = True
        return df

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

        human.before_request()

        result = fetch_html(name)

        if result is None:
            html = None
        else:
            _, html = result

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

    parsed["completion_score"] = completion_score(parsed)

    mark_done(family_id)

    after_fetch(
        name,
        parsed,
        family_id,
        members,
        missing_names,
    )

    btn_total = len(members)
    coverage = f"{updated}/{btn_total}"
    missing = len(missing_names)

    print(f"  family: {family_id}")
    print(f"  family members: {btn_total}")
    print(f"  Lenaba rows updated: {updated}")
    print(f"  BTN family members : {btn_total}")
    print(f"  Missing BTN names  : {missing}")

    if missing_names:
        print("  missing names:")
        for item in missing_names[:10]:
            print(f"    - {item}")

    collect_missing_family(
        family_id,
        parsed,
        missing_names,
    )

    preview = ", ".join(members[:8])

    if len(members) > 8:
        preview += ", ..."

    return df

def run(limit=10, target_name=None):

    print("=" * 50)
    print("LENABA FAMILY BUILDER V2")
    print("=" * 50)

    df = pd.read_parquet(NAMES)

    df = ensure_columns(df)

    completed = int(df["family_processed"].sum())
    remaining = len(df) - completed

    start_time = time.time()
    last_times = deque(maxlen=20)

    rows_updated_total = 0
    families_processed = 0

    print(f"Completed : {completed:,}")
    print(f"Remaining : {remaining:,}")

    pending = next_names(df, limit)

    print(f"Processing: {len(pending)} names")

    processed = 0

    # ---------------------------------------------
    # Single Family Mode (--name)
    # ---------------------------------------------

    if target_name:

        match = df[
            df["name"].str.upper() == target_name.upper()
        ]

        if match.empty:
            print(f"Name '{target_name}' not found.")
            return

        idx = match.index[0]

        print("=" * 50)
        print("LENABA SINGLE FAMILY MODE")
        print("=" * 50)
        print(f"Target: {target_name}")
        print()

        df = process_name(df, idx, force=True)

        df.to_parquet(NAMES, index=False)

        print("\nDone.")
        return

    while processed < limit:

        pending = next_names(df, 1)

        if pending.empty:
            break

        idx = pending.index[0]

        family_start = time.time()

        df = process_name(df, idx, force=True)

        df.to_parquet(NAMES, index=False)
        print("  saved checkpoint")

        families_processed += 1

        family_time = time.time() - family_start
        last_times.append(family_time)

        elapsed = time.time() - start_time
        avg_time = sum(last_times) / len(last_times)

        current_completed = int(df["family_processed"].sum())
        current_remaining = len(df) - current_completed

        families_per_hour = 3600 / avg_time if avg_time else 0
        eta_hours = current_remaining / families_per_hour if families_per_hour else 0

        print(f"  progress: {current_completed:,}/{len(df):,}")
        print(f"  speed   : {families_per_hour:.1f} families/hour")
        print(f"  ETA     : {eta_hours:.1f} hours ({eta_hours/24:.1f} days)")

        processed += 1

    elapsed = time.time() - start_time

    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)

    avg_speed = (
        families_processed / (elapsed / 3600)
        if elapsed else 0
    )

    completed_now = int(df["family_processed"].sum())
    remaining_now = len(df) - completed_now

    eta_hours = (
        remaining_now / avg_speed
        if avg_speed else 0
    )

    print("\n" + "="*50)
    print("RUN SUMMARY")
    print("="*50)

    print(f"Families processed : {families_processed}")
    print(f"Elapsed            : {hours:02}:{minutes:02}:{seconds:02}")
    print(f"Average speed      : {avg_speed:.1f} families/hour")

    print("\nProgress")
    print(f"Completed          : {completed_now:,}/{len(df):,}")
    print(f"Remaining          : {remaining_now:,}")

    print(f"\nETA remaining      : {eta_hours/24:.1f} days")

    print("\nDone.")


if __name__ == "__main__":

    limit = 10
    name = None

    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    if "--name" in sys.argv:
        name = sys.argv[sys.argv.index("--name") + 1]

    run(limit, name)
