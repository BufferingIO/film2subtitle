from fastapi import APIRouter

from film2subtitle.app.api import health
from film2subtitle.app.api.v1 import router as v1_router

router = APIRouter(prefix="/api")
router.include_router(health.router)
router.include_router(v1_router)
