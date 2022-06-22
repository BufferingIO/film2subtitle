from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from film2subtitle.app import crud, schemas
from film2subtitle.app.api.dependency import get_db
from film2subtitle.app.core import security
from film2subtitle.app.core.config import settings

router = APIRouter(
    responses={
        401: {
            "description": "Unauthorized, invalid credentials or no access token",
        },
    },
)


@router.post(
    "/access-token",
    response_model=schemas.Token,
    summary="Generate access token",
    description="Retrieve an access token for the given username and password",
    status_code=200,
)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    """Get an access token for future requests."""
    user = crud.user.authenticate(
        db,
        username=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    expires_in = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id_,
            expires_delta=expires_in,
        ),
        "token_type": "bearer",
    }
