from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import DatabaseRepository
from app.datasets.models import Dataset, DatasetParameterPair


class DatasetRepository(DatabaseRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Dataset, session)
        self.session = session

    async def update(self, dataset: Dataset, data: dict) -> Dataset | None:
        pairs = data.pop("pairs")
        for var, value in data.items():
            setattr(dataset, var, value) if value else None
        for pair in pairs:
            existing_pair = await self.session.scalar(
                select(DatasetParameterPair)
                .where(DatasetParameterPair.dataset_id == dataset.id)
                .where(DatasetParameterPair.parameter_id == pair["parameter_id"])
            )
            if existing_pair is None:
                dataset.pairs.append(
                    DatasetParameterPair(
                        dataset=dataset,
                        parameter_id=pair["parameter_id"],
                        parameter_value=pair["parameter_value"],
                    )
                )
            else:
                print(existing_pair)
                existing_pair.parameter_value = pair["parameter_value"]
        await self.session.commit()
        await self.session.refresh(dataset)
        return dataset

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
