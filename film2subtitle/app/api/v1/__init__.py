from fastapi import APIRouter

from film2subtitle.app.api.v1.endpoints import login, subtitles, users

api_router = APIRouter()
api_router.include_router(subtitles.router, prefix="/subs", tags=["Subtitles"])
api_router.include_router(login.router, prefix="/login", tags=["Login"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
