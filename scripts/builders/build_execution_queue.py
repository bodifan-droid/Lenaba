from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE
from scripts.lib.validate_master import run_integrity_gate

SMART_QUEUE = KNOWLEDGE / "smart_queue_v3.parquet"
OUT = KNOWLEDGE / "execution_queue.parquet"

REQUIRED_COLUMNS = [
    "family_id",
    "canonical_name",
    "family_size",
    "dominant_language",
    "missing",
    "priority",
    "estimated_gain",
    "api_needed",
]


def classify(language, api_needed):

    if not api_needed:
        return "local_ipa"

    if language is None or pd.isna(language):
        return "manual_review"

    language = str(language)

    behind_languages = {
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
        "Latin",
        "Greek",
        "Finnish",
        "Hawaiian",
        "Maori",
        "Sanskrit",
        "Indian",
    }

    if language in behind_languages:
        return "behind"

    if language.startswith("Ancient"):
        return "behind"

    if language.startswith("Biblical"):
        return "behind"

    if "Mythology" in language:
        return "manual_review"

    if "Fiction" in language:
        return "manual_review"

    return "behind"


def build_execution(queue: pd.DataFrame) -> pd.DataFrame:

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
            ["executor", "priority", "estimated_gain"],
            ascending=[True, False, False],
        )
        .reset_index(drop=True)
    )

    return execution


def empty_execution():

    return pd.DataFrame(columns=[
        "family_id",
        "canonical_name",
        "family_size",
        "executor",
        "batch_key",
        "dominant_language",
        "missing",
        "priority",
        "estimated_gain",
    ])


def main():

    queue = pd.read_parquet(SMART_QUEUE)

    missing_cols = [
        c for c in REQUIRED_COLUMNS
        if c not in queue.columns
    ]

    if queue.empty or missing_cols:

        execution = empty_execution()

        execution.to_parquet(OUT, index=False)

        print("=" * 45)
        print("EXECUTION QUEUE BUILT")
        print("=" * 45)
        print("Tasks        : 0")

        if queue.empty:
            print("Reason       : Smart Queue is empty.")

        if missing_cols:
            print(f"Missing cols : {missing_cols}")

        print(f"Output       : {OUT.name}")

        return

    execution = build_execution(queue)

    execution.to_parquet(OUT, index=False)

    run_integrity_gate(
        pd.DataFrame({
            "name": execution["canonical_name"]
        })
    )

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
