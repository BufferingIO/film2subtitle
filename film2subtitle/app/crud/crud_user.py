from typing import Optional, Union

from sqlalchemy.orm import Session

from film2subtitle.app.core.security import get_password_hash, verify_password
from film2subtitle.app.crud.base import CRUDBase
from film2subtitle.app.models import User
from film2subtitle.app.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD operations for User."""

    # noinspection PyMethodMayBeStatic
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    # noinspection PyMethodMayBeStatic
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        # noinspection PyArgumentList
        db_obj = User(
            username=obj_in.username,  # type: ignore
            email=obj_in.email,  # type: ignore
            password_hash=get_password_hash(obj_in.password),  # type: ignore
            is_superuser=obj_in.is_superuser,  # type: ignore
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # noinspection PyMethodMayBeStatic
    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, dict],
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if pwd := update_data.pop("password", None):
            update_data["hashed_password"] = get_password_hash(pwd)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    # noinspection PyMethodMayBeStatic
    def authenticate(
        self,
        db: Session,
        *,
        username: str,
        password: str,
    ) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    # noinspection PyMethodMayBeStatic
    def is_active(self, user: User) -> bool:
        return user.is_active

    # noinspection PyMethodMayBeStatic
    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
