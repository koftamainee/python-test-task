import uuid
from unittest.mock import AsyncMock

import pytest


class TestDelete:
    async def test_deletes_from_both_stores(
        self, service, mock_db: AsyncMock, mock_es: AsyncMock
    ):
        doc_id = uuid.uuid4()
        mock_db.delete.return_value = True

        result = await service.delete(doc_id)

        assert result is True
        mock_db.delete.assert_awaited_once_with(doc_id)
        mock_es.delete.assert_awaited_once_with(doc_id)

    async def test_skips_es_when_not_in_db(
        self, service, mock_db: AsyncMock, mock_es: AsyncMock
    ):
        doc_id = uuid.uuid4()
        mock_db.delete.return_value = False

        result = await service.delete(doc_id)

        assert result is False
        mock_db.delete.assert_awaited_once_with(doc_id)
        mock_es.delete.assert_not_called()
