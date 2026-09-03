from pathlib import Path

from scripts.lib.knowledge import KnowledgeCache
from scripts.lib.origin import OriginResolver


class OfflineProvider:
    def search(self, name: str):
        raise AssertionError("Seed-backed resolution must not call Wikidata")


def test_resolver_resolves_amelia_from_seed(tmp_path: Path):
    resolver = OriginResolver(
        cache=KnowledgeCache(tmp_path / "knowledge_cache.parquet"),
        provider=OfflineProvider(),
    )

    result = resolver.resolve("Amelia")

    assert result == "Germanic"
