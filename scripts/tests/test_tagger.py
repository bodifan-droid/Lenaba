from scripts.lib.tagger import generate_tags

def test_generate_tags():
    tags = generate_tags("Noah", "Peace", "Hebrew")

    assert "hebrew" in tags
    assert "peace" in tags
    assert "short" in tags