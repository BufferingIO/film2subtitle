from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """Base class for all database models."""

    id_: Any
    __name__: str

    # Create table name automatically from class name
    @declared_attr
    def __tablename__(cls) -> str:  # noqa
        return cls.__name__.lower()
