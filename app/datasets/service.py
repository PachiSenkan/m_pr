from sqlalchemy import BinaryExpression
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.datasets.models import Parameter, Category
from app.datasets.repository import DatasetRepository
from app.repository import DatabaseRepository
from app.service import BaseService


class CategoryService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        self.repository = DatabaseRepository(Category, session)

    async def get_by_name(self, name: str):
        result = await self.repository.get_by_parameter(
            Category.name == name  # type: ignore
        )
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.repository.model.__name__} does not exist",
            )
        return result



class DatasetService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        self.repository = DatasetRepository(session)

    async def create(self, data: dict):
        parameter_repository = DatabaseRepository(Parameter, self.repository.session)
        category_repository = DatabaseRepository(Category, self.repository.session)
        if await category_repository.get(data["category_id"]) is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with ID {data["category_id"]} does not exist",
                )
        for pair in data["pairs"]:
            if await parameter_repository.get(pair["parameter_id"]) is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Parameter with ID {pair["parameter_id"]} does not exist",
                )
        new_instance = await self.repository.create(data)
        return new_instance

    async def update(self, id: int, data: dict):
        parameter_repository = DatabaseRepository(Parameter, self.repository.session)
        category_repository = DatabaseRepository(Category, self.repository.session)
        result = await self.repository.get(id, for_update=True)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dataset does not exist",
            )
        if data.get("category_id"):
            if await category_repository.get(data["category_id"]) is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category does not exist",
                )
        if data.get("pairs"):
            for pair in data["pairs"]:
                if await parameter_repository.get(pair["parameter_id"]) is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Parameter with ID {pair["parameter_id"]} does not exist",
                    )
        return await self.repository.update(result, data)

