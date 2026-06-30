import uuid

from sqlalchemy import Column, DateTime, Text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import JSON, Uuid


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(Text, nullable=False)
    rubrics = Column(JSON, nullable=False)
    created_date = Column(DateTime(timezone=True), nullable=False)
