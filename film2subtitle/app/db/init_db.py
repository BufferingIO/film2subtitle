from sqlalchemy.orm import Session

from film2subtitle.app import crud, schemas
from film2subtitle.app.core.config import settings
from film2subtitle.app.db import base
from film2subtitle.app.db.session import engine


def init_db(db: Session, create_tables: bool = False) -> None:
    """Initialize database with first superuser data."""
    if create_tables is True:
        # You can create tables manually here if you want using tools like Alembic.
        base.Base.metadata.create_all(bind=engine)  # type: ignore
    user = crud.user.get_by_username(db, username=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
