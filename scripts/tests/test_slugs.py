from scripts.lib.slugs import slugify, name_length


def test_slugify_basic():
    assert slugify("Amelia") == "amelia"


def test_slugify_spaces():
    assert slugify("Mary Jane") == "mary-jane"


def test_name_length():
    assert name_length("Liam") == 4