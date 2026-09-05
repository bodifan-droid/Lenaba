from pathlib import Path
import subprocess
import sys

import pandas as pd

from scripts.lib.seed import SeedProvider

V2_COLUMNS = {"language", "tier", "confidence", "resolver", "updated_at"}


def test_reads_amelia_from_seed():
    record = SeedProvider().get("Amelia")

    assert record is not None
    assert record.origin == "Germanic"
    assert record.meaning == "Industrious"


def test_returns_none_for_unknown_name():
    assert SeedProvider().get("NotARealLenabaName") is None


def test_seed_has_v2_metadata_columns():
    columns = set(pd.read_csv("data/seed/knowledge_seed.csv", nrows=0).columns)

    assert V2_COLUMNS <= columns


def test_parquet_preserves_v2_metadata_columns():
    subprocess.run(
        [sys.executable, "scripts/builders/build_seed.py"],
        check=True,
    )

    columns = set(pd.read_parquet("data/seed/knowledge_seed.parquet").columns)
    assert V2_COLUMNS <= columns
