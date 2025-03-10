from sqlalchemy import Column, String, JSON, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.db import Base

class ClientDummy(Base):
    __tablename__ = "client_dummy"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nama = Column(String(255), nullable=False)
    alamat = Column(String(255))
    created_time = Column(TIMESTAMP, server_default=func.now())

class ApiLogs(Base):
    __tablename__ = "api_logs"

    api_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_payload = Column(JSON, nullable=False)
    response_payloads = Column(JSON, nullable=False)
    created_time = Column(TIMESTAMP, server_default=func.now())
