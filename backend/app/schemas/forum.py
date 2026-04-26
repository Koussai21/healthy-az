from datetime import datetime

from pydantic import BaseModel, Field


class ForumReplyCreate(BaseModel):
    content: str = Field(..., min_length=1)


class ForumReplyOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    author_id: int
    author_username: str

    model_config = {"from_attributes": True}


class ForumPostCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=300)
    content: str = Field(..., min_length=1)


class ForumPostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author_id: int
    author_username: str
    replies: list[ForumReplyOut] = []

    model_config = {"from_attributes": True}
