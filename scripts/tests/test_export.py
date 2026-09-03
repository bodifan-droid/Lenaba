import pandas as pd

from scripts.lib.export import (
    build_supabase_dataset,
    build_seo_dataset,
)


def test_supabase_export():
    df = pd.DataFrame(
        {
            "id": [1],
            "name": ["Amelia"],
            "gender": ["Female"],
            "slug": ["amelia"],
        }
    )

    result = build_supabase_dataset(df)

    assert "slug" in result.columns


def test_seo_export():
    df = pd.DataFrame(
        {
            "name": ["Amelia"],
            "gender": ["Female"],
            "slug": ["amelia"],
            "origin": ["Germanic"],
            "meaning": ["Industrious"],
            "first_letter": ["A"],
        }
    )

    seo = build_seo_dataset(df)

    assert seo.iloc[0]["canonical"] == "https://lenaba.com/name/amelia"