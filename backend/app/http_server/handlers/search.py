from fastapi import APIRouter, Depends, Query

from app.domain.schemas import DocumentResponse
from app.http_server.dependencies import get_document_service
from app.service.document import DocumentService

router = APIRouter(tags=["documents"])


@router.get("/api/documents")
async def search(
    q: str = Query(..., description="Search query"),
    service: DocumentService = Depends(get_document_service),
) -> list[DocumentResponse]:
    return await service.search(q)
