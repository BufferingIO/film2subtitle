from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from film2subtitle.app import schemas
from film2subtitle.app.api.dependency import get_db

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "/",
    tags=["Health"],
    response_model=schemas.HealthCheck,
    response_description="Health check response.",
)
async def health_check(db: Session = Depends(get_db)) -> JSONResponse:
    """A simple health check endpoint to check the service status."""
    # Query the database to check if the service is up and running correctly.
    try:
        db.execute("SELECT 1")
    except SQLAlchemyError:
        return JSONResponse(
            content={"status": "unavailable"},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    return JSONResponse(
        content={"status": "available"},
    )
