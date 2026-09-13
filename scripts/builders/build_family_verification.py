from __future__ import annotations

from datetime import datetime

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

GRAPH = KNOWLEDGE / "family_graph.parquet"
ETYMOLOGY = KNOWLEDGE / "etymology_graph.parquet"


VERIFIED_RELATIONS = [
    "variant",
    "language_variant",
    "feminine",
    "masculine",
    "diminutive",
]

def unique(values):

    seen = set()
    result = []

    for value in values:

        if not isinstance(value, str):
            continue

        value = value.strip()

        if not value or value in seen:
            continue

        seen.add(value)
        result.append(value)

    return result

def verify_family(name: str):

    family = pd.read_parquet(GRAPH)
    etymology = pd.read_parquet(ETYMOLOGY)

    if "family_status" not in family.columns:
        family["family_status"] = None

    if "family_source" not in family.columns:
        family["family_source"] = None

    if "family_last_verified" not in family.columns:
        family["family_last_verified"] = None

    group = etymology[etymology["from_name"] == name]

    if group.empty:
        return 0

    names = [name]

    for relation in VERIFIED_RELATIONS:

        names.extend(
            group.loc[
                group["relation"] == relation,
                "to_name",
            ].tolist()
        )

    if len(unique(names)) <= 1:
        return 0

    mask = family["name"] == name

    if not mask.any():
        return 0

    family.loc[mask, "family_status"] = "verified"
    family.loc[mask, "family_source"] = "behindthename"
    family.loc[
        mask,
        "family_last_verified",
    ] = datetime.utcnow().date().isoformat()

    family.to_parquet(GRAPH, index=False)

    return 1

def main():

    family = pd.read_parquet(GRAPH)
    etymology = pd.read_parquet(ETYMOLOGY)

    for col in [
        "family_status",
        "family_source",
        "family_last_verified",
    ]:
        if col not in family.columns:
            family[col] = None

    verified_lookup = {}

    for name, group in etymology.groupby("from_name"):

        names = [name]

        for relation in VERIFIED_RELATIONS:

            names.extend(
                group.loc[
                    group["relation"] == relation,
                    "to_name",
                ].tolist()
            )

        verified_lookup[name] = unique(names)

    verified = 0

    for idx, row in family.iterrows():

        name = row["name"]

        if name not in verified_lookup:
            continue

        # якщо для імені знайдено хоча б один підтверджений зв'язок
        if len(verified_lookup[name]) > 1:

            family.at[idx, "family_status"] = "verified"
            family.at[idx, "family_source"] = "behindthename"
            family.at[idx, "family_last_verified"] = (
                datetime.utcnow().date().isoformat()
            )

            verified += 1

    family.to_parquet(GRAPH, index=False)

    print("=" * 45)
    print("FAMILY VERIFICATION COMPLETE")
    print("=" * 45)
    print(f"Verified families : {verified:,}")


if __name__ == "__main__":
    main()
