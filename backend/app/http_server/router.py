from fastapi import APIRouter

from app.http_server.handlers import delete, search


def create_router() -> APIRouter:
    router = APIRouter()
    router.include_router(search.router)
    router.include_router(delete.router)
    return router
