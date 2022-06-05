from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.orm import Session

from film2subtitle.app import crud, models, schemas
from film2subtitle.app.api.dependency import (
    get_current_active_superuser,
    get_current_active_user,
    get_db,
)

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def get_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # whether the user has superuser privileges
    _=Depends(get_current_active_superuser),
):
    return crud.user.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_superuser),
) -> models.User:
    """Create new user in the database."""
    user = crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user associated with this username already exists",
        )
    user = crud.user.create(db, obj_in=user_in)
    # NOTE: You can also send email to the user with a confirmation link.
    return user


@router.get("/me", response_model=schemas.User, summary="Get current user")
def get_user_me(user: models.User = Depends(get_current_active_user)) -> models.User:
    """Get current active user details."""
    return user


@router.put("/me", response_model=schemas.User, summary="Update current user")
def update_user_me(
    db: Session = Depends(get_db),
    password: str = Body(None),
    email: EmailStr = Body(None),
    user: models.User = Depends(get_current_active_user),
) -> models.User:
    """Update current user using provided data."""
    user_in = schemas.UserUpdate(**jsonable_encoder(user))
    if password is not None:
        user_in.password = password
    if email is not None:
        user_in.email = email
    return crud.user.update(db, db_obj=user, obj_in=user_in)


@router.get("/{user_id}", response_model=schemas.User, summary="Get user by ID")
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_superuser),
) -> models.User:
    """Get a specific user by ID."""
    return crud.user.get(db, id_=user_id)


@router.put("/{user_id}", response_model=schemas.User, summary="Update user by ID")
def update_user_by_id(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_superuser),
) -> models.User:
    """Update a specific user by ID."""
    user = crud.user.get(db, id_=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this ID does not exist",
        )
    return crud.user.update(db, db_obj=user, obj_in=user_in)
