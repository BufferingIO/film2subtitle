from sqlalchemy import Boolean, Column, Integer, String

from film2subtitle.app.db.base_class import Base


class User(Base):
    """Model representing a user in the database."""

    id_: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, index=True)
    email: str = Column(String, unique=True, index=True)
    password_hash: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean(), default=True)
    is_superuser: bool = Column(Boolean(), default=False)
