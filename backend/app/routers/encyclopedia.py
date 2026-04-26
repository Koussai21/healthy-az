from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.encyclopedia import EncyclopediaEntry, EntryKind
from app.models.user import User
from app.schemas.encyclopedia import EncyclopediaCreate, EncyclopediaOut, EncyclopediaUpdate
from app.utils.slug import slugify

router = APIRouter()


def _unique_slug(db: Session, base: str, exclude_id: int | None = None) -> str:
    slug = base
    n = 1
    while True:
        q = db.query(EncyclopediaEntry).filter(EncyclopediaEntry.slug == slug)
        if exclude_id is not None:
            q = q.filter(EncyclopediaEntry.id != exclude_id)
        if q.first() is None:
            return slug
        slug = f"{base}-{n}"
        n += 1


@router.get("", response_model=list[EncyclopediaOut])
def list_entries(
    db: Session = Depends(get_db),
    q: str | None = Query(None, description="Recherche libre (titre, résumé, contenu)"),
    kind: EntryKind | None = None,
    limit: int = Query(100, le=200),
    offset: int = 0,
):
    query = db.query(EncyclopediaEntry)
    if kind:
        query = query.filter(EncyclopediaEntry.kind == kind.value)
    if q and q.strip():
        term = f"%{q.strip()}%"
        query = query.filter(
            or_(
                EncyclopediaEntry.title.ilike(term),
                EncyclopediaEntry.summary.ilike(term),
                EncyclopediaEntry.content.ilike(term),
            )
        )
    rows = query.order_by(EncyclopediaEntry.title.asc()).offset(offset).limit(limit).all()
    return rows


@router.get("/{slug}", response_model=EncyclopediaOut)
def get_entry(slug: str, db: Session = Depends(get_db)):
    row = db.query(EncyclopediaEntry).filter(EncyclopediaEntry.slug == slug).first()
    if not row:
        raise HTTPException(status_code=404, detail="Fiche introuvable")
    return row


@router.post("", response_model=EncyclopediaOut, status_code=201)
def create_entry(
    payload: EncyclopediaCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    base = slugify(payload.title)
    slug = _unique_slug(db, base)
    entry = EncyclopediaEntry(
        kind=payload.kind.value,
        title=payload.title.strip(),
        slug=slug,
        summary=payload.summary,
        content=payload.content.strip(),
        author_id=user.id,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.patch("/{slug}", response_model=EncyclopediaOut)
def update_entry(
    slug: str,
    payload: EncyclopediaUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    row = db.query(EncyclopediaEntry).filter(EncyclopediaEntry.slug == slug).first()
    if not row:
        raise HTTPException(status_code=404, detail="Fiche introuvable")
    if row.author_id != user.id:
        raise HTTPException(status_code=403, detail="Modification réservée à l'auteur")
    if payload.title is not None:
        row.title = payload.title.strip()
        row.slug = _unique_slug(db, slugify(row.title), exclude_id=row.id)
    if payload.summary is not None:
        row.summary = payload.summary
    if payload.content is not None:
        row.content = payload.content.strip()
    row.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(row)
    return row
