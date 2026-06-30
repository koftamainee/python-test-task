from fastapi import Request

from app.service.document import DocumentService


async def get_document_service(request: Request) -> DocumentService:
    return request.app.state.document_service
