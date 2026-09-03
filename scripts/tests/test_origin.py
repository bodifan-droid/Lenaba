from scripts.lib.origin import OriginResolver


def test_resolver_does_not_crash():
    resolver = OriginResolver()

    result = resolver.resolve("Amelia")

    assert result is None or isinstance(result, str)