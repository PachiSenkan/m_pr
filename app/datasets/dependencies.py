from collections.abc import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base
from app.repository import DatabaseRepository, DatasetRepository
from app.core.session import get_db_session


def get_repository(
    model: type[Base],
) -> Callable[[AsyncSession], DatabaseRepository]:
    def func(session: AsyncSession = Depends(get_db_session)):
        return DatabaseRepository(model, session)

    return func


def get_dataset_repository() -> Callable[[AsyncSession], DatasetRepository]:
    def func(session: AsyncSession = Depends(get_db_session)):
        return DatasetRepository(session)

    return func
