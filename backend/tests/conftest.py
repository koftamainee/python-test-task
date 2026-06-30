import os

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://u:p@localhost/db")
os.environ.setdefault("ELASTICSEARCH_URL", "http://localhost:9200")
os.environ.setdefault("ELASTICSEARCH_PASSWORD", "test")

from unittest.mock import AsyncMock

import pytest

from app.service.document import DocumentService
from app.storage.esearch import ESDocumentStorage
from app.storage.postgres import PostgresDocumentStorage


@pytest.fixture
def mock_db() -> AsyncMock:
    return AsyncMock(spec=PostgresDocumentStorage)


@pytest.fixture
def mock_es() -> AsyncMock:
    return AsyncMock(spec=ESDocumentStorage)


@pytest.fixture
def service(mock_db: AsyncMock, mock_es: AsyncMock) -> DocumentService:
    return DocumentService(db=mock_db, es=mock_es)
