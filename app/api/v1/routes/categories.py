from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Category
from app.schemas.categories_schemas import CategoryBase, CategoryQuery, CategoryCreate
from app.service.base import BaseService
from app.api.dependencies import get_db_session


router_categories = APIRouter(prefix="/categories", tags=["Категории наборов данных"])


@router_categories.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate, session: AsyncSession = Depends(get_db_session)
) -> CategoryBase:
    service = BaseService(Category, session)
    new_category = await service.create(data.model_dump())
    return CategoryBase.model_validate(new_category)


@router_categories.get("/", status_code=status.HTTP_200_OK)
async def get_categories(
    session: AsyncSession = Depends(get_db_session),
) -> list[CategoryBase]:
    service = BaseService(Category, session)
    categories = await service.filter()
    return [CategoryBase.model_validate(category) for category in categories]


@router_categories.get("/{category_id}", status_code=status.HTTP_200_OK)
async def get_category(
    category_id: int, session: AsyncSession = Depends(get_db_session)
) -> CategoryBase:
    service = BaseService(Category, session)
    category = await service.get(category_id)
    return CategoryBase.model_validate(category)
