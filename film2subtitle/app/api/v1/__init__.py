from fastapi import APIRouter

from film2subtitle.app.api.v1.endpoints import subtitles

api_router = APIRouter()
api_router.include_router(subtitles.router, prefix="/subs", tags=["Subtitles"])
