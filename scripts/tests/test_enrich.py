import pandas as pd

from scripts.lib.enrich import merge_lookup


def test_merge_lookup():
    names = pd.DataFrame(
        {
            "name": ["Amelia"],
            "gender": ["Female"],
        }
    )

    lookup = pd.DataFrame(
        {
            "name": ["Amelia"],
            "gender": ["Female"],
            "origin": ["Germanic"],
            "country": ["GB"],
            "meaning": ["Industrious"],
            "pronunciation": ["uh-MEE-lee-uh"],
            "variants": ["Emilia"],
            "verified": [True],
            "confidence": [99],
            "source": ["Wikidata"],
            "source_url": [""],
            "last_reviewed": ["2026-09-03"],
            "notes": [""],
        }
    )

    merged = merge_lookup(names, lookup)

    assert merged.iloc[0]["origin"] == "Germanic"
    assert merged.iloc[0]["meaning"] == "Industrious"