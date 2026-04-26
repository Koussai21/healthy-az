from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class KindEnum(str, Enum):
    maladie = "maladie"
    symptome = "symptome"
    diagnostic = "diagnostic"


class EncyclopediaCreate(BaseModel):
    kind: KindEnum
    title: str = Field(..., min_length=2, max_length=300)
    summary: str | None = None
    content: str = Field(..., min_length=10)


class EncyclopediaUpdate(BaseModel):
    title: str | None = Field(None, min_length=2, max_length=300)
    summary: str | None = None
    content: str | None = Field(None, min_length=10)


class EncyclopediaOut(BaseModel):
    id: int
    kind: KindEnum
    title: str
    slug: str
    summary: str | None
    content: str
    created_at: datetime
    updated_at: datetime
    author_id: int | None

    model_config = {"from_attributes": True}
