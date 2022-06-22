from fastapi import APIRouter

from film2subtitle.app.api.v1.endpoints import auth, subtitles, users
from film2subtitle.app.core.config import settings

router = APIRouter(prefix=f"/{settings.API_V1_STR}")
router.include_router(subtitles.router, prefix="/subs", tags=["Subtitles"])
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(users.router, prefix="/users", tags=["Users"])
