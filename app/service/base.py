from typing import Any
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import BinaryExpression, update, delete, CursorResult
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import Base, async_session_maker
from app.models.repository import DatabaseRepository, DatasetRepository
from app.models.models import Parameter


class BaseService:
    def __init__(self, model: type[Base], session: AsyncSession) -> None:
        self.repository = DatabaseRepository(model, session)

    async def create(self, data: dict):
        new_instance = await self.repository.create(data)
        return new_instance

    async def get(self, id: int):
        result = await self.repository.get(id)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.repository.model.__name__} does not exist",
            )
        return result

    async def filter(
        self,
        *expressions: BinaryExpression,
    ):
        return await self.repository.filter(*expressions)


class DatasetService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        self.repository = DatasetRepository(session)

    async def create(self, data: dict):
        parameter_repository = DatabaseRepository(Parameter, self.repository.session)
        for pair in data["pairs"]:
            if await parameter_repository.get(pair["parameter_id"]) is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Parameter with ID {pair["parameter_id"]} does not exist",
                )
        new_instance = await self.repository.create(data)
        return new_instance
