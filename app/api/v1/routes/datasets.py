from typing import Annotated, Any
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.models.repository import DatabaseRepository, DatasetRepository
from app.api.dependencies import get_dataset_repository, get_repository
from app.models.models import Dataset, DatasetParameterPair
from app.database.session import get_db_session
from app.service.base import BaseService, DatasetService
from app.schemas.datasets_schemas import (
    DatasetBase,
    DatasetCreate,
    DatasetQuery,
    DatasetUpdate,
)

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
    session: AsyncSession = Depends(get_db_session),
) -> list[DatasetBase]:
    service = DatasetService(session)
    datasets = await service.filter()
    return [DatasetBase.model_validate(dataset) for dataset in datasets]


@router_datasets.get("/{dataset_id}", status_code=status.HTTP_200_OK)
async def get_dataset(
    dataset_id: int, session: AsyncSession = Depends(get_db_session)
) -> DatasetBase:
    service = DatasetService(session)
    dataset = await service.get(dataset_id)
    return DatasetBase.model_validate(dataset)
