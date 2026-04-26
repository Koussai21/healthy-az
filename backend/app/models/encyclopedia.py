import enum
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EntryKind(str, enum.Enum):
    maladie = "maladie"
    symptome = "symptome"
    diagnostic = "diagnostic"


class EncyclopediaEntry(Base):
    __tablename__ = "encyclopedia_entries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # VARCHAR uniquement : aucun CREATE TYPE PostgreSQL (compatible droits restreints sur public)
    kind: Mapped[str] = mapped_column(String(32), index=True)
    title: Mapped[str] = mapped_column(String(300), index=True)
    slug: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    author_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    author: Mapped["User | None"] = relationship("User")
