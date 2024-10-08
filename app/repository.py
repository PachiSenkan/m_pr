from typing import Generic, TypeVar

from sqlalchemy import BinaryExpression, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base

Model = TypeVar("Model", bound=Base)


class DatabaseRepository(Generic[Model]):

    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def create(self, data: dict) -> Model:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get(self, id: int, for_update: bool = False) -> Model | None:
        return await self.session.get(self.model, id, with_for_update=for_update)

    async def get_by_parameter(self, expression: BinaryExpression) -> Model | None:
        return await self.session.scalar(select(self.model).where(expression))

    async def filter(
        self,
        offset: int,
        limit: int,
        order_by: str,
        *expressions: BinaryExpression,
    ) -> list[Model]:
        query = select(self.model)
        if expressions:
            query = query.where(*expressions)
        if order_by:
            query = query.order_by(order_by)
        query = query.offset(offset).limit(limit)
        return list(await self.session.scalars(query))

    async def update(self, instance: Model, data: dict) -> Model | None:
        for var, value in data.items():
            setattr(instance, var, value) if value else None
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: Model) -> None:
        await self.session.delete(instance)
        await self.session.commit()
