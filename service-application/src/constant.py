import uuid
from pydantic import BaseModel
from enum import Enum
from sqlalchemy import Column, String, DateTime
from sqlalchemy import func
from fastapi_utils.guid_type import GUID
from .db import Base


class ApplicationStatusEnum(Enum):
    pending = "pending"
    complete = "completed"
    rejected = "rejected"


class ApplicationIn(BaseModel):
    first_name: str
    last_name: str


class ApplicationOut(BaseModel):
    id: str
    first_name: str
    last_name: str
    status: ApplicationStatusEnum


class ApplicationStatus(BaseModel):
    id: str
    application_id: str
    status: ApplicationStatusEnum


class ApplicationModel(Base):
    __tablename__ = "applications"

    id = Column(GUID, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
