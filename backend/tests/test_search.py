import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from app.domain.models import Document


class TestSearch:
    async def test_returns_documents_sorted_by_date(
        self, service, mock_db: AsyncMock, mock_es: AsyncMock
    ):
        id1 = uuid.uuid4()
        id2 = uuid.uuid4()
        mock_es.search.return_value = [str(id1), str(id2)]

        doc1 = Document(
            id=id1,
            text="older",
            rubrics=["a"],
            created_date=datetime(2020, 1, 1, tzinfo=timezone.utc),
        )
        doc2 = Document(
            id=id2,
            text="newer",
            rubrics=["b"],
            created_date=datetime(2021, 1, 1, tzinfo=timezone.utc),
        )
        mock_db.get_by_ids.return_value = [doc1, doc2]

        result = await service.search("test")

        assert len(result) == 2
        assert result[0].text == "newer"
        assert result[1].text == "older"

    async def test_returns_empty_when_no_matches(
        self, service, mock_db: AsyncMock, mock_es: AsyncMock
    ):
        mock_es.search.return_value = []

        result = await service.search("nothing")

        assert result == []
        mock_db.get_by_ids.assert_not_called()

    async def test_returns_only_documents_found_in_db(
        self, service, mock_db: AsyncMock, mock_es: AsyncMock
    ):
        existing_id = uuid.uuid4()
        missing_id = uuid.uuid4()
        mock_es.search.return_value = [str(existing_id), str(missing_id)]

        doc = Document(
            id=existing_id,
            text="exists",
            rubrics=["x"],
            created_date=datetime(2022, 1, 1, tzinfo=timezone.utc),
        )
        mock_db.get_by_ids.return_value = [doc]

        result = await service.search("test")

        assert len(result) == 1
        assert result[0].id == existing_id
