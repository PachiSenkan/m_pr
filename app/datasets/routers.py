from typing import Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.datasets.models import Category, Parameter
from app.datasets.schemas import (
    CategoryBase,
    CategoryQuery,
    CategoryCreate,
    CategoriesOrderBy,
    CategoriesOrder,
    DataSubsetBase,
    DataSubsetCreate,
    DatasetBase,
    DatasetCreate,
    DatasetQuery,
    DatasetUpdate,
    ParameterBase,
    ParameterCreate,
    ParameterQuery,
)
from app.service import BaseService
from app.datasets.service import CategoryService
from app.core.session import get_db_session
from app.service import BaseService
from app.datasets.service import DatasetService


router_categories = APIRouter(prefix="/categories", tags=["Категории наборов данных"])


@router_categories.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate, session: AsyncSession = Depends(get_db_session)
) -> CategoryBase:
    service = CategoryService(session)
    new_category = await service.create(data.model_dump())
    return CategoryBase.model_validate(new_category)


@router_categories.get("/", status_code=status.HTTP_200_OK)
async def get_categories(
    order_by: CategoriesOrderBy = Depends(),
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db_session),
) -> list[CategoryBase]:
    service = CategoryService(session)
    if order_by.order_by:
        order: str | Any = CategoriesOrder[order_by.order_by.name]
    else:
        order = ""
    categories = await service.filter(offset, limit, order)
    return [CategoryBase.model_validate(category) for category in categories]


@router_categories.get("/filter", status_code=status.HTTP_200_OK)
async def get_category_by_name(
    name: str = "",
    session: AsyncSession = Depends(get_db_session),
) -> CategoryBase:
    service = CategoryService(session)
    category = await service.get_by_name(name)
    return CategoryBase.model_validate(category)


@router_categories.get("/{category_id}", status_code=status.HTTP_200_OK)
async def get_category(
    category_id: int, session: AsyncSession = Depends(get_db_session)
) -> CategoryBase:
    service = CategoryService(session)
    category = await service.get(category_id)
    return CategoryBase.model_validate(category)


@router_categories.put("/{category_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_category(
    category_id: int,
    new_data: CategoryQuery,
    session: AsyncSession = Depends(get_db_session),
) -> CategoryBase:
    service = CategoryService(session)
    category = await service.update(category_id, new_data.model_dump(exclude_none=True))
    return category


@router_categories.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(
    category_id: int, session: AsyncSession = Depends(get_db_session)
) -> CategoryBase:
    service = CategoryService(session)
    result = await service.delete(category_id)
    return result


router_parameters = APIRouter(prefix="/parameters", tags=["Параметры"])


@router_parameters.post("/", status_code=status.HTTP_201_CREATED)
async def create_parameter(
    data: ParameterCreate, session: AsyncSession = Depends(get_db_session)
) -> ParameterBase:
    service = BaseService(Parameter, session)
    new_category = await service.create(data.model_dump())
    return ParameterBase.model_validate(new_category)


@router_parameters.get("/", status_code=status.HTTP_200_OK)
async def get_parameter(
    offset: int = 0,
    limit: int = 100,
    order_by: str = "",
    session: AsyncSession = Depends(get_db_session),
) -> list[ParameterBase]:
    service = BaseService(Parameter, session)
    parameters = await service.filter(offset, limit, order_by)
    return [ParameterBase.model_validate(parameter) for parameter in parameters]


@router_parameters.get("/{parameter_id}", status_code=status.HTTP_200_OK)
async def get_category(
    parameter_id: int, session: AsyncSession = Depends(get_db_session)
) -> ParameterBase:
    service = BaseService(Parameter, session)
    category = await service.get(parameter_id)
    return ParameterBase.model_validate(category)


@router_parameters.put("/{parameter_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_parameter(
    parameter_id: int,
    new_data: ParameterQuery,
    session: AsyncSession = Depends(get_db_session),
) -> ParameterBase:
    service = BaseService(Parameter, session)
    parameter = await service.update(
        parameter_id, new_data.model_dump(exclude_none=True)
    )
    return parameter


@router_parameters.delete("/{parameter_id}", status_code=status.HTTP_200_OK)
async def delete_parameter(
    parameter_id: int, session: AsyncSession = Depends(get_db_session)
) -> ParameterBase:
    service = BaseService(Parameter, session)
    result = await service.delete(parameter_id)
    return result


router_datasets = APIRouter(prefix="/datasets", tags=["Наборы данных"])


@router_datasets.post("/", status_code=status.HTTP_201_CREATED)
async def create_dataset(
    data: DatasetCreate, session: AsyncSession = Depends(get_db_session)
) -> DatasetBase:
    data_dict = data.model_dump()
    service = DatasetService(session)
    dataset = await service.create(data_dict)
    return DatasetBase.model_validate(dataset)


@router_datasets.get("/", status_code=status.HTTP_200_OK)
async def get_datasets(
    offset: int = 0,
    limit: int = 100,
    order_by: str = "",
    session: AsyncSession = Depends(get_db_session),
) -> list[DatasetBase]:
    service = DatasetService(session)
    datasets = await service.filter(offset, limit, order_by)
    return [DatasetBase.model_validate(dataset) for dataset in datasets]


@router_datasets.get("/{dataset_id}", status_code=status.HTTP_200_OK)
async def get_dataset(
    dataset_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> DatasetBase:
    service = DatasetService(session)
    dataset = await service.get(dataset_id)
    print(dataset)
    return DatasetBase.model_validate(dataset)


@router_datasets.put("/{dataset_id}", status_code=status.HTTP_200_OK)
async def update_dataset(
    dataset_id: int,
    new_data: DatasetUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> DatasetBase:
    service = DatasetService(session)
    result = await service.update(dataset_id, new_data.model_dump(exclude_none=True))
    return result


@router_datasets.delete("/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dataset(
    dataset_id: int, session: AsyncSession = Depends(get_db_session)
) -> None:
    service = DatasetService(session)
    await service.delete(dataset_id)
    return None
