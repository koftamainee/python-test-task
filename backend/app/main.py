import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import async_session, close_db, init_db
from app.elastic import close_es, create_index, es
from app.http_server.middleware import LoggerMiddleware, RequestIDMiddleware
from app.http_server.router import create_router
from app.service.document import DocumentService
from app.storage.esearch import ESDocumentStorage
from app.storage.postgres import PostgresDocumentStorage

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await create_index()
    app.state.document_service = DocumentService(
        db=PostgresDocumentStorage(async_session),
        es=ESDocumentStorage(es),
    )
    yield
    await close_db()
    await close_es()


app = FastAPI(title="Document Search Service", version="1.0.0", lifespan=lifespan)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggerMiddleware)

app.include_router(create_router())


@app.get("/health")
async def health():
    return {"status": "ok"}
