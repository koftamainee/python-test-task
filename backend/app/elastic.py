from elasticsearch import AsyncElasticsearch

from app.config import settings

es = AsyncElasticsearch(
    settings.elasticsearch_url,
    basic_auth=(settings.elasticsearch_user, settings.elasticsearch_password),
)


async def create_index():
    if not await es.indices.exists(index=settings.elasticsearch_index):
        await es.indices.create(
            index=settings.elasticsearch_index,
            mappings={
                "properties": {
                    "id": {"type": "keyword"},
                    "text": {"type": "text"},
                }
            },
        )


async def close_es():
    await es.close()
