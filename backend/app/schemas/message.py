from datetime import datetime

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    recipient_id: int
    content: str = Field(..., min_length=1, max_length=8000)


class MessageOut(BaseModel):
    id: int
    content: str
    read: bool
    created_at: datetime
    sender_id: int
    recipient_id: int
    sender_username: str
    recipient_username: str

    model_config = {"from_attributes": True}


class ConversationPartner(BaseModel):
    user_id: int
    username: str
    last_message_at: datetime | None
    last_preview: str | None
    unread_count: int
