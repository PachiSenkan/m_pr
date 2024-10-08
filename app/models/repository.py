from typing import Generic, TypeVar

from sqlalchemy import BinaryExpression, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import Base
from app.models.models import Dataset, DatasetParameterPair

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

    async def get(self, id: int) -> Model | None:
        return await self.session.get(self.model, id)

    async def filter(
        self,
        *expressions: BinaryExpression,
    ) -> list[Model]:
        query = select(self.model)
        if expressions:
            query = query.where(*expressions)
        return list(await self.session.scalars(query))

    async def update(self, id: int, data: dict) -> Model | None:
        pass

    async def delete(self, id: int) -> None:
        await self.session.delete(self.get(id))
        await self.session.commit()


class DatasetRepository(DatabaseRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Dataset, session)
        self.session = session

    async def create(self, data: dict) -> Dataset:
        pairs = data.pop("pairs")
        dataset = Dataset(**data)
        for pair in pairs:
            dataset.pairs.append(
                DatasetParameterPair(
                    dataset=dataset,
                    parameter_id=pair["parameter_id"],
                    parameter_value=pair["parameter_value"],
                )
            )
        self.session.add(dataset)
        await self.session.commit()
        await self.session.refresh(dataset)
        return dataset
