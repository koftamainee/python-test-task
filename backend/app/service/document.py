from uuid import UUID

from app.domain.schemas import DocumentResponse
from app.storage.esearch import ESDocumentStorage
from app.storage.postgres import PostgresDocumentStorage


class DocumentService:
    def __init__(self, db: PostgresDocumentStorage, es: ESDocumentStorage):
        self._db = db
        self._es = es

    async def search(self, query: str) -> list[DocumentResponse]:
        ids = await self._es.search(query)
        if not ids:
            return []

        uuids = [UUID(id_) for id_ in ids]
        documents = await self._db.get_by_ids(uuids)
        documents.sort(key=lambda d: d.created_date, reverse=True)
        return [DocumentResponse.model_validate(d) for d in documents]

    async def delete(self, document_id: UUID) -> bool:
        ok = await self._db.delete(document_id)
        if ok:
            await self._es.delete(document_id)
        return ok


