from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr
from app.database.config import settings


DATABASE_URL = settings.database_url
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


from collections.abc import AsyncGenerator

from sqlalchemy import exc
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.database.config import settings


class Base(DeclarativeBase):
    """Base database model."""

    id: Mapped[int] = mapped_column(primary_key=True)
