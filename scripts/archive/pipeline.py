from scripts.lib.origin import OriginResolver
from scripts.lib.pronunciation import enrich_pronunciation
from scripts.lib.tagger import generate_tags
from scripts.lib.seo_writer import write_description

resolver = OriginResolver()

def enrich_record(record, phonetic=None):
    record.origin = resolver.resolve(record.name)

    enrich_pronunciation(record, phonetic)

    tags = generate_tags(record.name, record.meaning, record.origin)

    seo = write_description(
        record.name,
        record.meaning,
        record.origin,
        tags,
    )

    return record, tags, seo