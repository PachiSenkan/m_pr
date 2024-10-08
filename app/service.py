from typing import Any
from fastapi import HTTPException, status
from sqlalchemy import BinaryExpression
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base
from app.repository import DatabaseRepository


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
        offset: int,
        limit: int,
        order_by: Any,
        *expressions: BinaryExpression,
    ):
        return await self.repository.filter(offset, limit, order_by, *expressions)

    async def update(self, id: int, data: dict):
        result = await self.repository.get(id)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.repository.model.__name__} does not exist",
            )
        return await self.repository.update(result, data)

    async def delete(self, id: int):
        to_delete = await self.repository.get(id)
        if to_delete is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.repository.model.__name__} does not exist",
            )
        await self.repository.delete(to_delete)
        return to_delete
