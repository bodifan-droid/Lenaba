from pathlib import Path

from scripts.lib.knowledge import KnowledgeCache, KnowledgeRecord


def test_save_and_load(tmp_path: Path):
    cache_path = tmp_path / "knowledge_cache.parquet"

    cache = KnowledgeCache(cache_path)

    cache.save(
        KnowledgeRecord(
            name="Amelia",
            meaning="Industrious",
            origin="Germanic",
            ipa="/əˈmiːliə/",
            pronunciation="uh-MEE-lee-uh",
            source="test",
            verified=True,
        )
    )

    record = cache.get("Amelia")

    assert record is not None
    assert record.name == "Amelia"
    assert record.origin == "Germanic"
    assert record.verified is True