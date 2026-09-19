import json
from pathlib import Path


def test_golden_file_exists():
    assert Path("data/tests/golden_families.json").exists()


def test_golden_schema():

    data = json.loads(
        Path("data/tests/golden_families.json").read_text(
            encoding="utf-8"
        )
    )

    assert "ALISA" in data
