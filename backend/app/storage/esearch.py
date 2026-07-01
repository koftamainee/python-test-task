from uuid import UUID

from elasticsearch import AsyncElasticsearch, NotFoundError

from app.config import settings


class ESDocumentStorage:
    def __init__(self, client: AsyncElasticsearch):
        self._client = client

    async def search(self, query: str, size: int = 20) -> list[str]:
        response = await self._client.search(
            index=settings.elasticsearch_index,
            query={"match": {"text": query}},
            size=size,
        )
        return [hit["_id"] for hit in response["hits"]["hits"]]

    async def delete(self, document_id: UUID):
        try:
            await self._client.delete(
                index=settings.elasticsearch_index,
                id=str(document_id),
            )
        except NotFoundError:
            pass
