from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

def test_content_factory_output():
    df = pd.read_parquet(ROOT / "data/content/content_registry.parquet")

    assert (df["status"] == "pending").sum() == 0

    assert "tags" in df.columns
    assert "seo_description" in df.columns

    assert df["tags"].notna().sum() > 0