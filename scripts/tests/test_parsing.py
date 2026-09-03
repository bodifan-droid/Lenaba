from scripts.lib.parsing import (
    normalize_variants,
    normalize_phonetics,
    normalize_stresses,
)


def test_variants():
    assert normalize_variants("Emilia; Amelie") == [
        "Emilia",
        "Amelie",
    ]


def test_phonetic():
    assert normalize_phonetics(" AH M EE ") == [
        "AH",
        "M",
        "EE",
    ]


def test_stresses():
    assert normalize_stresses("a|me|lia") == [
        "a|me|lia",
    ]