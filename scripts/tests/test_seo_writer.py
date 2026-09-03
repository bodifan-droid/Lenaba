from scripts.lib.seo_writer import write_description

def test_write_description():
    text = write_description(
        "Amelia",
        "Industrious",
        "Germanic",
        ["classic"]
    )

    assert "Amelia" in text
    assert "Germanic" in text