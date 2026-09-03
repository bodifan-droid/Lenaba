from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def test_golden_queue():
    df = pd.read_csv(ROOT / "data" / "seed" / "golden_500.csv")

    assert len(df) == 500
    assert df["priority"].is_unique
    assert df["priority"].min() == 1
    assert df["status"].eq("pending").all()