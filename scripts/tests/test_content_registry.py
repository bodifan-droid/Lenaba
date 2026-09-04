from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def test_content_registry():

    df = pd.read_csv(
        ROOT / "data" / "content" / "content_registry.csv",
        low_memory=False,
    )

    assert "tier" in df.columns
    assert "status" in df.columns
    assert "content_hash" in df.columns
    assert "pipeline_version" in df.columns

    assert df["id"].is_unique
    assert not df[["name", "gender"]].duplicated().any()

    assert (df["tier"] == "golden").sum() == 500