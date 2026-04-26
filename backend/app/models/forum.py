from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ForumPost(Base):
    __tablename__ = "forum_posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(300))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship(back_populates="forum_posts")
    replies: Mapped[list["ForumReply"]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )


class ForumReply(Base):
    __tablename__ = "forum_replies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    post_id: Mapped[int] = mapped_column(ForeignKey("forum_posts.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    post: Mapped["ForumPost"] = relationship(back_populates="replies")
    author: Mapped["User"] = relationship(back_populates="forum_replies")


from app.models.user import User  # noqa: E402
