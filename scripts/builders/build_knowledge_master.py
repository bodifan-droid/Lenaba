
from pathlib import Path
import ast
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

SEED = ROOT / "data/seed/knowledge_seed.parquet"
PACKS = ROOT / "data/content/packs"
OUT = ROOT / "data/knowledge/knowledge_master.parquet"


def normalize_list_column(value):

    # вже список
    if isinstance(value, list):
        return value

    # numpy array
    if isinstance(value, np.ndarray):
        return value.tolist()

    # тільки тепер перевіряємо NaN
    if pd.isna(value):
        return []

    # рядок
    if isinstance(value, str):

        value = value.strip()

        if value.startswith("["):
            try:
                return ast.literal_eval(value)
            except Exception:
                pass

        if value:
            return [value]

    return []

def main():

    OUT.parent.mkdir(parents=True, exist_ok=True)

    frames = []

    if SEED.exists():
        frames.append(pd.read_parquet(SEED))

    for pack in sorted(PACKS.glob("golden_pack_*.parquet")):
        frames.append(pd.read_parquet(pack))

    if not frames:
        raise FileNotFoundError("No knowledge sources found.")

    df = pd.concat(frames, ignore_index=True)

    from scripts.lib.schema import (
        LIST_COLUMNS,
        STRING_COLUMNS,
        BOOL_COLUMNS,
        FLOAT_COLUMNS,
    )

    def normalize_tags(value):
        return ",".join(normalize_list_column(value))

    for col in STRING_COLUMNS:
        if col in df.columns:
            df[col] = df[col].apply(normalize_tags)

    for col in LIST_COLUMNS:
        if col in df.columns:
            df[col] = df[col].apply(normalize_list_column)

    for col in STRING_COLUMNS:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: ",".join(normalize_list_column(x))
            )

    # ---------- Normalize string columns ----------

    STRING_FIELDS = [
        "tier",
        "status",
        "campaign",
        "source",
        "origin",
        "country",
        "meaning",
        "pronunciation",
        "seo_description",
        "content_hash",
        "pipeline_version",
    ]

    for col in STRING_FIELDS:
        if col in df.columns:
            df[col] = (
                df[col]
                .fillna("")
                .astype(str)
            )

    BOOL_FIELDS = [
        "verified",
        "meaning_done",
        "origin_done",
        "ipa_done",
        "tags_done",
        "seo_done",
        "reviewed",
        "published",
    ]

    for col in BOOL_FIELDS:
        if col in df.columns:
            df[col] = df[col].fillna(False).astype(bool)

    if "confidence" not in df.columns:
        df["confidence"] = 0.0

    if "source" not in df.columns:
        df["source"] = "unknown"

    if "verified" not in df.columns:
        df["verified"] = False

    df = (
        df.sort_values("confidence")
          .drop_duplicates("name", keep="last")
          .sort_values("name")
          .reset_index(drop=True)
    )

    df.to_parquet(OUT, index=False)

    print("=" * 40)
    print("KNOWLEDGE MASTER BUILT")
    print("=" * 40)
    print(f"Rows: {len(df):,}")
    print(f"Output: {OUT}")


if __name__ == "__main__":
    main()