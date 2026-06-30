from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.domain.schemas import DeleteResponse
from app.http_server.dependencies import get_document_service
from app.service.document import DocumentService

router = APIRouter(tags=["documents"])


@router.delete("/api/documents/{document_id}")
async def delete(
    document_id: UUID,
    service: DocumentService = Depends(get_document_service),
) -> DeleteResponse:
    ok = await service.delete(document_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Document not found")
    return DeleteResponse(ok=True)
