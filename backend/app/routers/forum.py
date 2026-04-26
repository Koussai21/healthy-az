from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.forum import ForumPost, ForumReply
from app.models.user import User
from app.schemas.forum import ForumPostCreate, ForumPostOut, ForumReplyCreate, ForumReplyOut

router = APIRouter()


def _post_out(post: ForumPost) -> ForumPostOut:
    return ForumPostOut(
        id=post.id,
        title=post.title,
        content=post.content,
        created_at=post.created_at,
        author_id=post.author_id,
        author_username=post.author.username,
        replies=[
            ForumReplyOut(
                id=r.id,
                content=r.content,
                created_at=r.created_at,
                author_id=r.author_id,
                author_username=r.author.username,
            )
            for r in sorted(post.replies, key=lambda x: x.created_at)
        ],
    )


@router.get("/posts", response_model=list[ForumPostOut])
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(ForumPost).order_by(ForumPost.created_at.desc()).all()
    return [_post_out(p) for p in posts]


@router.get("/posts/{post_id}", response_model=ForumPostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Sujet introuvable")
    return _post_out(post)


@router.post("/posts", response_model=ForumPostOut, status_code=201)
def create_post(
    payload: ForumPostCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post = ForumPost(title=payload.title.strip(), content=payload.content.strip(), author_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    post = db.query(ForumPost).filter(ForumPost.id == post.id).first()
    return _post_out(post)


@router.post("/posts/{post_id}/replies", response_model=ForumReplyOut, status_code=201)
def add_reply(
    post_id: int,
    payload: ForumReplyCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Sujet introuvable")
    reply = ForumReply(content=payload.content.strip(), post_id=post_id, author_id=user.id)
    db.add(reply)
    db.commit()
    db.refresh(reply)
    r = db.query(ForumReply).filter(ForumReply.id == reply.id).first()
    return ForumReplyOut(
        id=r.id,
        content=r.content,
        created_at=r.created_at,
        author_id=r.author_id,
        author_username=r.author.username,
    )
