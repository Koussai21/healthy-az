from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.message import Message
from app.models.user import User
from app.schemas.message import ConversationPartner, MessageCreate, MessageOut

router = APIRouter()


def _msg_out(m: Message) -> MessageOut:
    return MessageOut(
        id=m.id,
        content=m.content,
        read=m.read,
        created_at=m.created_at,
        sender_id=m.sender_id,
        recipient_id=m.recipient_id,
        sender_username=m.sender.username,
        recipient_username=m.recipient.username,
    )


@router.get("/conversations", response_model=list[ConversationPartner])
def conversations(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    msgs = (
        db.query(Message)
        .filter(or_(Message.sender_id == user.id, Message.recipient_id == user.id))
        .order_by(Message.created_at.desc())
        .all()
    )
    latest_by_peer: dict[int, Message] = {}
    for m in msgs:
        other = m.recipient_id if m.sender_id == user.id else m.sender_id
        if other not in latest_by_peer:
            latest_by_peer[other] = m
    result: list[ConversationPartner] = []
    for other_id, last_msg in sorted(
        latest_by_peer.items(), key=lambda x: x[1].created_at, reverse=True
    ):
        other = db.query(User).filter(User.id == other_id).first()
        if not other:
            continue
        unread = (
            db.query(func.count(Message.id))
            .filter(
                Message.sender_id == other_id,
                Message.recipient_id == user.id,
                Message.read.is_(False),
            )
            .scalar()
            or 0
        )
        preview = last_msg.content
        if preview and len(preview) > 120:
            preview = preview[:120] + "…"
        result.append(
            ConversationPartner(
                user_id=other.id,
                username=other.username,
                last_message_at=last_msg.created_at,
                last_preview=preview,
                unread_count=int(unread),
            )
        )
    return result


@router.get("/with/{peer_id}", response_model=list[MessageOut])
def thread(
    peer_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    limit: int = Query(200, le=500),
):
    if peer_id == user.id:
        raise HTTPException(status_code=400, detail="Impossible de chatter avec soi-même")
    peer = db.query(User).filter(User.id == peer_id).first()
    if not peer:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    msgs = (
        db.query(Message)
        .filter(
            or_(
                and_(Message.sender_id == user.id, Message.recipient_id == peer_id),
                and_(Message.sender_id == peer_id, Message.recipient_id == user.id),
            )
        )
        .order_by(Message.created_at.asc())
        .limit(limit)
        .all()
    )
    db.query(Message).filter(
        Message.sender_id == peer_id,
        Message.recipient_id == user.id,
        Message.read.is_(False),
    ).update({Message.read: True}, synchronize_session=False)
    db.commit()
    refreshed = (
        db.query(Message)
        .filter(
            or_(
                and_(Message.sender_id == user.id, Message.recipient_id == peer_id),
                and_(Message.sender_id == peer_id, Message.recipient_id == user.id),
            )
        )
        .order_by(Message.created_at.asc())
        .limit(limit)
        .all()
    )
    return [_msg_out(m) for m in refreshed]


@router.post("", response_model=MessageOut, status_code=201)
def send_message(
    payload: MessageCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if payload.recipient_id == user.id:
        raise HTTPException(status_code=400, detail="Destinataire invalide")
    peer = db.query(User).filter(User.id == payload.recipient_id).first()
    if not peer:
        raise HTTPException(status_code=404, detail="Destinataire introuvable")
    msg = Message(
        content=payload.content.strip(),
        sender_id=user.id,
        recipient_id=payload.recipient_id,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    m = db.query(Message).filter(Message.id == msg.id).first()
    return _msg_out(m)


@router.get("/users", response_model=list[dict])
def list_users_for_dm(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    q: str | None = None,
):
    query = db.query(User).filter(User.id != user.id)
    if q and q.strip():
        term = f"%{q.strip()}%"
        query = query.filter(
            or_(User.username.ilike(term), User.first_name.ilike(term), User.last_name.ilike(term))
        )
    users = query.order_by(User.username).limit(50).all()
    return [{"id": u.id, "username": u.username, "display": f"{u.first_name} {u.last_name}"} for u in users]
