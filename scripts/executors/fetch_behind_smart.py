
from __future__ import annotations

import sys
import pandas as pd
import json
from pathlib import Path
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from bs4 import BeautifulSoup
from scripts.lib.behind_client import fetch_html
from scripts.lib.behind_cache import get_cached, save_cache
from scripts.lib.behind_parser import parse_name_page
from scripts.lib.fetch_results import save_result

from scripts.lib.paths import EXECUTION, KNOWLEDGE

QUEUE = KNOWLEDGE / "execution_queue.parquet"
BATCHES = KNOWLEDGE / "execution_batches.parquet"

STATE = Path("data/outputs/fetch_state.json")

load_dotenv()

API_KEY = os.getenv("BEHIND_NAME_API_KEY")

if not API_KEY:
    raise RuntimeError("BEHIND_NAME_API_KEY not found in .env")


def fetch_name(name: str):

    url = "https://www.behindthename.com/api/lookup.json"

    params = {
        "name": name,
        "key": API_KEY,
    }

    r = requests.get(url, params=params, timeout=20)

    if r.status_code != 200:
        return {"api_status": f"HTTP_{r.status_code}"}

    data = r.json()

    # API повертає список
    if not data:
        return {
            "api_status": "not_found",
            "meaning": None,
            "origin": None,
            "pronunciation": None,
            "fetched_at": datetime.utcnow().isoformat(),
        }

    entry = data[0]

    # usages -> список об'єктів
    usages = ", ".join(
        u.get("usage", "")
        for u in entry.get("usages", [])
        if u.get("usage")
    )

    return {
        "meaning": entry.get("description"),
        "origin": usages,
        "pronunciation": entry.get("pronunciation"),
        "api_status": "ok",
        "fetched_at": datetime.utcnow().isoformat(),
    }

def fetch_family(name):

    cached = get_cached(name)

    if cached:

        from scripts.lib.etymology_writer import append_relations

        append_relations(name, cached)

        cached["cached"] = True

        return cached

    url, html = fetch_html(name)

    if html is None:

        return {
            "cached": False,
            "status": "not_found",
            "name": name,
        }

    parsed = parse_name_page(html)

    save_result(name, parsed)

    from scripts.lib.etymology_writer import append_relations

    append_relations(name, parsed)

    from scripts.builders.build_family_merge import main as family_merge_main

    family_merge_main()

    save_cache(
        name=name,
        url=url,
        html=html,
        parsed=parsed,
    )

    parsed["cached"] = False

    return parsed

def load_state():

    if not STATE.exists():

        STATE.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "last_batch": None,
            "completed_batches": [],
            "completed_families": 0,
        }

        STATE.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    return json.loads(STATE.read_text(encoding="utf-8"))


def save_state(state):

    STATE.write_text(
        json.dumps(state, indent=2),
        encoding="utf-8",
    )



def start_batch(batch_name, limit=None):

    queue = pd.read_parquet(QUEUE)

    rows = queue[
        (queue["executor"] == "behind")
        & (queue["batch_key"] == batch_name)
    ]

    if limit:
        rows = rows.head(limit)

    state = load_state()

    state["last_batch"] = batch_name
    save_state(state)

    print("=" * 55)
    print(f"STARTING BATCH — {batch_name}")
    print("=" * 55)
    print(f"Families : {len(rows):,}")
    print(f"Names    : {rows['estimated_gain'].sum():,}")
    print()

    completed = 0

    for family in rows.itertuples(index=False):

        print(f"[{completed+1}/{len(rows)}] {family.canonical_name}")

        result = fetch_family(family.canonical_name)

        status = result.get("status")

        if status == "not_found":
            print("    status : skipped (404)")
        elif result.get("cached"):
            print("    status : cached")
        else:
            print("    status : fetched")

        completed += 1

    state["completed_families"] += completed

    save_state(state)

    print()
    print("=" * 55)
    print("BATCH COMPLETE")
    print("=" * 55)
    print(f"Families processed : {completed}")


def preview():

    batches = pd.read_parquet(BATCHES)
    queue = pd.read_parquet(QUEUE)

    print("=" * 55)
    print("LENABA BEHIND EXECUTOR PREVIEW")
    print("=" * 55)

    print(f"Language batches : {len(batches):,}")
    print(f"Behind tasks     : {(queue['executor']=='behind').sum():,}")
    print()

    print("Top 10 batches")
    print("-" * 55)
    print(batches.head(10).to_string(index=False))


def preview_batch(batch_name: str):

    queue = pd.read_parquet(QUEUE)

    rows = queue[
        (queue["executor"] == "behind")
        & (queue["batch_key"] == batch_name)
    ]

    print("=" * 55)
    print(f"BATCH PREVIEW — {batch_name}")
    print("=" * 55)
    print(f"Families : {len(rows):,}")
    print(f"Names    : {rows['estimated_gain'].sum():,}")
    print()

    print(rows[["canonical_name", "family_size"]].head(20).to_string(index=False))



def main():

    args = sys.argv[1:]

    # fetch
    if not args:
        preview()
        return

    # fetch preview
    if args[0] == "preview":

        if len(args) == 1:
            preview()
            return

        preview_batch(args[1])
        return

    if args[0] == "test":

        from pprint import pprint

        pprint(fetch_family("Yamila"))

        return


    if args[0] == "batch":

        limit = None

        if "--limit" in args:
            limit = int(args[args.index("--limit") + 1])

        start_batch(args[1], limit)

        return

    if args[0] == "test":

        print(fetch_name("Yamila"))
        return

    print("Unknown command.")

if __name__ == "__main__":
    main()
