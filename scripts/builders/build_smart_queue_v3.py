
from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

MASTER = KNOWLEDGE / "knowledge_master.parquet"
FAMILIES = KNOWLEDGE / "canonical_families.parquet"
LANG = KNOWLEDGE / "language_resolver.parquet"
OUT = KNOWLEDGE / "smart_queue_v3.parquet"

LOCAL_IPA_LANGUAGES = {
    "English","French","German","Spanish","Italian",
    "Portuguese","Dutch","Polish","Czech","Slovak",
    "Croatian","Slovene","Romanian","Hungarian",
    "Swedish","Norwegian","Danish","Finnish",
    "Irish","Scottish"
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
    resolver = pd.read_parquet(LANG)

    master_lookup = master.set_index("name")
    lang_lookup = resolver.set_index("name")

    rows = []

    for family_id, group in families.groupby("family_id"):

        aliases = group["alias"].tolist()
        canonical = group.loc[group["is_canonical"], "canonical_name"].iloc[0]

        has_meaning = False
        has_origin = False
        has_pron = False

        best_level = "empty"
        dominant_lang = None
        lang_conf = 0

        order = {
            "empty":0,
            "bronze":1,
            "silver":2,
            "gold":3,
            "platinum":4,
        }

        for alias in aliases:

            if alias not in master_lookup.index:
                continue

            row = master_lookup.loc[alias]

            has_meaning |= has_text(row.get("meaning"))
            has_origin |= has_text(row.get("origin"))
            has_pron |= has_text(row.get("pronunciation"))

            lvl = str(row.get("completion_level","empty"))

            if order[lvl] > order[best_level]:
                best_level = lvl

            if alias in lang_lookup.index:

                lang = lang_lookup.at[alias,"dominant_language"]
                conf = lang_lookup.at[alias,"confidence"]

                if conf > lang_conf:
                    dominant_lang = lang
                    lang_conf = conf

        missing = []

        if not has_meaning:
            missing.append("meaning")

        if not has_origin:
            missing.append("origin")

        if not has_pron:
            missing.append("pronunciation")

        if not missing:
            continue

        api_needed = True
        route = "behind"

        if (
            missing == ["pronunciation"]
            and dominant_lang in LOCAL_IPA_LANGUAGES
        ):
            api_needed = False
            route = "local_ipa"

        rows.append({
            "family_id": family_id,
            "canonical_name": canonical,
            "family_size": len(aliases),
            "dominant_language": dominant_lang,
            "language_confidence": lang_conf,
            "completion_level": best_level,
            "missing": missing,
            "route": route,
            "api_needed": api_needed,
            "estimated_gain": len(aliases),
        })

    queue = pd.DataFrame(rows)

    if not queue.empty:

        queue["priority"] = (
            queue["api_needed"].astype(int) * 100
            + queue["estimated_gain"] * 10
            + queue["language_confidence"] * 5
        )

        queue = queue.sort_values(
            "priority",
            ascending=False,
        ).reset_index(drop=True)

    queue.to_parquet(OUT,index=False)

    print("="*45)
    print("SMART QUEUE V3 BUILT")
    print("="*45)
    print(f"Families queued : {len(queue):,}")
    print(f"API needed      : {queue['api_needed'].sum():,}")
    print(f"Local IPA       : {(~queue['api_needed']).sum():,}")
    print(f"Output          : {OUT.name}")


if __name__=="__main__":
    main()
