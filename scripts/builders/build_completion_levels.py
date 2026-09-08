from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE
from scripts.lib.validate_master import run_integrity_gate

MASTER = KNOWLEDGE / "knowledge_master.parquet"



def has_text(value):

    if value is None:
        return False

    # список
    if isinstance(value, list):
        return len(value) > 0

    # numpy масив
    if hasattr(value, "shape") and hasattr(value, "size"):
        return value.size > 0

    # NaN
    if pd.isna(value):
        return False

    # текст
    if isinstance(value, str):
        return value.strip() != ""

    return True


def level(row):

    has_meaning = has_text(row.get("meaning"))
    has_origin = has_text(row.get("origin"))
    has_pron = has_text(row.get("pronunciation"))

    has_forms = (
        has_text(row.get("variants"))
        or has_text(row.get("equivalents"))
        or has_text(row.get("short_forms"))
        or has_text(row.get("full_forms"))
        or has_text(row.get("feminine_forms"))
        or has_text(row.get("masculine_forms"))
        or has_text(row.get("other_forms"))
    )

    has_scripts = has_text(row.get("scripts"))

    if has_meaning and has_origin and has_pron and has_forms and has_scripts:
        return "platinum"

    if has_meaning and has_origin and has_pron and has_forms:
        return "gold"

    if has_meaning and has_origin and has_pron:
        return "silver"

    if has_meaning and has_origin:
        return "bronze"

    return "empty"


def main():

    df = pd.read_parquet(MASTER)

    run_integrity_gate(df)

    df["completion_level"] = df.apply(level, axis=1)

    df.to_parquet(MASTER, index=False)

    print("=" * 45)
    print("KNOWLEDGE LEVELS")
    print("=" * 45)

    for lvl in [
        "platinum",
        "gold",
        "silver",
        "bronze",
        "empty",
    ]:
        print(
            f"{lvl:10}: "
            f"{(df['completion_level']==lvl).sum():,}"
        )


if __name__ == "__main__":
    main()