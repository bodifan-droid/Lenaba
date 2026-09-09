
from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

MASTER = KNOWLEDGE / "knowledge_master.parquet"
FAMILIES = KNOWLEDGE / "canonical_families.parquet"
OUT = KNOWLEDGE / "smart_queue_v2.parquet"

# Мови, для яких ми потенційно можемо генерувати вимову локально
LATIN_LANGUAGES = {
    "English",
    "French",
    "German",
    "Spanish",
    "Italian",
    "Portuguese",
    "Dutch",
    "Polish",
    "Czech",
    "Slovak",
    "Croatian",
    "Slovene",
    "Romanian",
    "Hungarian",
    "Swedish",
    "Norwegian",
    "Danish",
    "Finnish",
}


def has_text(value):

    if value is None:
        return False

    if isinstance(value, str):
        return value.strip() != ""

    if isinstance(value, list):
        return len(value) > 0

    if hasattr(value, "size"):
        return value.size > 0

    return not pd.isna(value)


def main():

    master = pd.read_parquet(MASTER)
    families = pd.read_parquet(FAMILIES)

    lookup = master.set_index("name")

    rows = []

    for family_id, group in families.groupby("family_id"):

        aliases = group["alias"].tolist()
        canonical = group.loc[group["is_canonical"], "canonical_name"].iloc[0]

        coverage = {
            "meaning": False,
            "origin": False,
            "pronunciation": False,
        }

        local_pron_possible = False
        best_level = "empty"

        for alias in aliases:

            if alias not in lookup.index:
                continue

            row = lookup.loc[alias]

            # Покриття сім'ї
            for field in coverage:
                if has_text(row.get(field)):
                    coverage[field] = True

            # Локальна генерація вимови
            if (
                has_text(row.get("ipa"))
                or has_text(row.get("phonetic"))
                or str(row.get("language", "")) in LATIN_LANGUAGES
            ):
                local_pron_possible = True

            level = str(row.get("completion_level", "empty"))

            order = {
                "empty": 0,
                "bronze": 1,
                "silver": 2,
                "gold": 3,
                "platinum": 4,
            }

            if order[level] > order[best_level]:
                best_level = level

        missing = [
            f
            for f, ok in coverage.items()
            if not ok
        ]

        if not missing:
            continue

        api_needed = True
        reason = ", ".join(missing)

        # Якщо бракує лише вимови і можемо зробити локально
        if (
            missing == ["pronunciation"]
            and local_pron_possible
        ):
            api_needed = False
            reason = "local_pronunciation"

        rows.append({
            "family_id": family_id,
            "canonical_name": canonical,
            "family_size": len(aliases),
            "completion_level": best_level,
            "missing": missing,
            "reason": reason,
            "can_generate_local": local_pron_possible,
            "api_needed": api_needed,
            "estimated_gain": len(aliases),
        })

    queue = pd.DataFrame(rows)

    if not queue.empty:

        queue["priority"] = (
            queue["estimated_gain"] * 10
            + queue["api_needed"].astype(int) * 100
        )

        queue = (
            queue
            .sort_values("priority", ascending=False)
            .reset_index(drop=True)
        )

    queue.to_parquet(OUT, index=False)

    print("=" * 45)
    print("SMART QUEUE V2 BUILT")
    print("=" * 45)
    print(f"Families queued : {len(queue):,}")

    if not queue.empty:
        print(f"API needed      : {queue['api_needed'].sum():,}")
        print(f"Local possible  : {(~queue['api_needed']).sum():,}")

    print(f"Output          : {OUT.name}")


if __name__ == "__main__":
    main()
