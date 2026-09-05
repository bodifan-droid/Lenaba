
from scripts.lib.providers.behind_name import BehindTheNameProvider


def test_provider_runs():

    provider = BehindTheNameProvider()

    result = provider.resolve("Amelia")

    assert result is None or hasattr(result, "meaning")