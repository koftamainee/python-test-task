from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.domain.models import Document


class PostgresDocumentStorage:
    def __init__(self, session_factory: async_sessionmaker):
        self._session_factory = session_factory

    async def get_by_ids(self, ids: list[UUID]) -> list[Document]:
        async with self._session_factory() as session:
            result = await session.execute(
                select(Document).where(Document.id.in_(ids))
            )
            return list(result.scalars().all())

    async def delete(self, document_id: UUID) -> bool:
        async with self._session_factory() as session:
            result = await session.execute(
                select(Document).where(Document.id == document_id)
            )
            doc = result.scalar_one_or_none()
            if not doc:
                return False
            await session.delete(doc)
            await session.commit()
            return True
