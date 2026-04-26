import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.auth import get_current_user
from app.config import settings
from app.models.user import User

router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=8000)


class ChatResponse(BaseModel):
    reply: str
    model: str


SYSTEM_PROMPT = (
    "Tu es un assistant santé pour Healthy-AZ, une encyclopédie médicale grand public. "
    "Tu donnes des informations générales et éducatives, jamais un diagnostic ni des conseils "
    "qui remplacent un professionnel. Rappelle souvent de consulter un médecin. Réponds en français, "
    "de façon claire et concise."
)


@router.post("/assistant", response_model=ChatResponse)
async def assistant_chat(
    payload: ChatRequest,
    user: User = Depends(get_current_user),
):
    _ = user
    url = f"{settings.ollama_host.rstrip('/')}/api/chat"
    body = {
        "model": settings.ollama_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": payload.message},
        ],
        "stream": False,
    }
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            r = await client.post(url, json=body)
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Ollama inaccessible ({settings.ollama_host}). Lancez Ollama et le modèle {settings.ollama_model}. Erreur: {e!s}",
        )
    if r.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama a répondu {r.status_code}: {r.text[:500]}",
        )
    data = r.json()
    msg = data.get("message", {}) or {}
    content = msg.get("content") or data.get("response") or ""
    if not content.strip():
        raise HTTPException(status_code=502, detail="Réponse vide du modèle")
    return ChatResponse(reply=content.strip(), model=settings.ollama_model)
