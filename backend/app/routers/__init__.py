from fastapi import APIRouter

from app.routers import auth, chat, encyclopedia, forum, messages, users

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(encyclopedia.router, prefix="/encyclopedia", tags=["encyclopedia"])
api_router.include_router(forum.router, prefix="/forum", tags=["forum"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
