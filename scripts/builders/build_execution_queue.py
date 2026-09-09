
from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE
from scripts.lib.validate_master import run_integrity_gate

QUEUE = KNOWLEDGE / "smart_queue_v3.parquet"
OUT = KNOWLEDGE / "execution_queue.parquet"


def classify(language, api_needed):

    if not api_needed:
        return "local_ipa"

    if language is None or pd.isna(language):
        return "manual_review"

    language = str(language)

    if language in {
        "Arabic",
        "Hebrew",
        "Persian",
        "Hindi",
        "Bengali",
        "Gujarati",
        "Armenian",
        "Igbo",
        "Yoruba",
        "Akan",
        "Chechen",
        "Georgian",
        "Turkish",
        "Uzbek",
        "Vietnamese",
        "Yiddish",
    }:
        return "behind"

    if language.startswith("Ancient"):
        return "behind"

    if language.startswith("Biblical"):
        return "behind"

    if "Mythology" in language:
        return "manual_review"

    return "behind"


def main():

    queue = pd.read_parquet(QUEUE)

    rows = []

    for row in queue.itertuples(index=False):

        executor = classify(
            row.dominant_language,
            row.api_needed,
        )

        batch_key = (
            row.dominant_language
            if executor == "behind"
            else executor
        )

        rows.append({
            "family_id": row.family_id,
            "canonical_name": row.canonical_name,
            "family_size": row.family_size,
            "executor": executor,
            "batch_key": batch_key,
            "dominant_language": row.dominant_language,
            "missing": row.missing,
            "priority": row.priority,
            "estimated_gain": row.estimated_gain,
        })

    execution = (
        pd.DataFrame(rows)
        .sort_values(
            ["executor", "priority"],
            ascending=[True, False],
        )
        .reset_index(drop=True)
    )

    execution.to_parquet(OUT, index=False)

    run_integrity_gate(pd.DataFrame({"name": execution["canonical_name"]}))

    print("=" * 45)
    print("EXECUTION QUEUE BUILT")
    print("=" * 45)
    print(f"Tasks        : {len(execution):,}")
    print(f"Behind       : {(execution['executor']=='behind').sum():,}")
    print(f"Local IPA    : {(execution['executor']=='local_ipa').sum():,}")
    print(f"Manual       : {(execution['executor']=='manual_review').sum():,}")
    print(f"Output       : {OUT.name}")


if __name__ == "__main__":
    main()
