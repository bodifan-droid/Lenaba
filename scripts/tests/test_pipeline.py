from scripts.lib.pipeline import EnrichmentPipeline
from scripts.lib.knowledge import KnowledgeRecord


def test_pipeline_enrich():
    pipeline = EnrichmentPipeline()

    record = KnowledgeRecord(
        name="Amelia",
        meaning="Industrious",
        origin="",
        ipa="",
        pronunciation="",
        source="test",
        verified=True,
    )

    result = pipeline.enrich(record)

    assert result["record"].name == "Amelia"
    assert "germanic" in result["tags"]
    assert "Amelia" in result["seo"]