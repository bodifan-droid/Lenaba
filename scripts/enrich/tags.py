import numpy as np
import pandas as pd


def _is_empty_tags(value):
    """Безпечна перевірка порожнього списку/масиву."""

    if value is None:
        return True

    if isinstance(value, float) and pd.isna(value):
        return True

    if isinstance(value, (list, tuple, np.ndarray)):
        return len(value) == 0

    if isinstance(value, str):
        return value.strip() == ""

    return False


def enrich_tags(df: pd.DataFrame):

    print("Tags...")

    if "tags" not in df.columns:
        df["tags"] = None

    filled = 0

    for i, row in df.iterrows():

        if not _is_empty_tags(row["tags"]):
            continue

        tags = []

        origin = str(row.get("origin", "")).lower()
        meaning = str(row.get("meaning", "")).lower()

        if "hebrew" in origin:
            tags.append("biblical")

        if "greek" in origin:
            tags.append("classic")

        if "latin" in origin:
            tags.append("traditional")

        if "light" in meaning:
            tags.append("light")

        if "strong" in meaning:
            tags.append("strength")

        if tags:
            filled += 1

        df.at[i, "tags"] = tags

    print(f"  Filled: {filled:,}")

    return df
