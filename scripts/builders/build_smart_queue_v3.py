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

FIELD_WEIGHTS = {
    "meaning": 3,
    "origin": 2,
    "pronunciation": 2,
    "root": 2,
    "other_languages": 2,
    "equivalents": 1,
    "related": 1,
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

    # статус уже перевірених сімей
    family_status = pd.read_parquet(
        KNOWLEDGE / "family_graph.parquet"
    )

    rows = []

    order = {
        "empty":0,
        "bronze":1,
        "silver":2,
        "gold":3,
        "platinum":4,
    }

    for family_id, group in families.groupby("family_id"):

        aliases = group["alias"].tolist()
        canonical = group.loc[group["is_canonical"], "canonical_name"].iloc[0]

        has_meaning = False
        has_origin = False
        has_pron = False
        has_root = False
        has_other_languages = False
        has_equivalents = False
        has_related = False

        best_level = "empty"
        dominant_lang = None
        lang_conf = 0

        for alias in aliases:

            if alias not in master_lookup.index:
                continue

            row = master_lookup.loc[alias]

            has_meaning |= has_text(row.get("meaning"))
            has_origin |= has_text(row.get("origin"))
            has_pron |= has_text(row.get("pronunciation"))
            has_root |= has_text(row.get("root"))
            has_other_languages |= has_text(row.get("other_languages"))
            has_equivalents |= has_text(row.get("equivalents"))
            has_related |= has_text(row.get("related"))

            lvl = str(row.get("completion_level", "empty"))

            if order.get(lvl, 0) > order[best_level]:
                best_level = lvl

            if alias in lang_lookup.index:

                lang = lang_lookup.at[alias, "dominant_language"]
                conf = lang_lookup.at[alias, "confidence"]

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

        if not has_root:
            missing.append("root")

        if not has_other_languages:
            missing.append("other_languages")

        if not has_equivalents:
            missing.append("equivalents")

        if not has_related:
            missing.append("related")

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

        estimated_gain = (
            len(aliases)
            * sum(FIELD_WEIGHTS[f] for f in missing)
        )

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
            "estimated_gain": estimated_gain,
            "priority": estimated_gain,
        })

    queue = pd.DataFrame(rows)

    family_status = family_status[
        ["name", "family_status"]
    ].copy()

    family_status["_key"] = (
        family_status["name"]
        .astype(str)
        .str.upper()
    )

    queue["_key"] = (
        queue["canonical_name"]
        .astype(str)
        .str.upper()
    )

    queue = queue.merge(
        family_status[["_key", "family_status"]],
        on="_key",
        how="left",
    )

    queue.drop(columns="_key", inplace=True)

    queue = queue[
        ~queue["family_status"].isin(
            ["verified", "completed"]
        )
    ]

    queue = (
        queue
        .sort_values(
            ["estimated_gain", "family_size"],
            ascending=False,
        )
        .reset_index(drop=True)
    )

    queue.to_parquet(OUT, index=False)

    if len(families) and queue.empty:
        raise RuntimeError(
            f"Queue sanity check failed: {len(families)} families found but 0 queued."
        )

    print("=" * 45)
    print("SMART QUEUE V3 BUILT")
    print("=" * 45)
    print(f"Families queued : {len(queue):,}")

    if not queue.empty:
        print(f"API needed      : {queue['api_needed'].sum():,}")
        print(f"Local IPA       : {(~queue['api_needed']).sum():,}")
    else:
        print("API needed      : 0")
        print("Local IPA       : 0")


if __name__ == "__main__":
    main()
