from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.base import BaseService
from app.api.dependencies import get_db_session
from app.models.models import Parameter
from app.schemas.parameters_schemas import (
    ParameterBase,
    ParameterCreate,
    ParameterQuery,
)

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
    session: AsyncSession = Depends(get_db_session),
) -> list[ParameterBase]:
    service = BaseService(Parameter, session)
    parameters = await service.filter()
    return [ParameterBase.model_validate(parameter) for parameter in parameters]


@router_parameters.get("/{parameter_id}", status_code=status.HTTP_200_OK)
async def get_category(
    parameter_id: int, session: AsyncSession = Depends(get_db_session)
) -> ParameterBase:
    service = BaseService(Parameter, session)
    category = await service.get(parameter_id)
    return ParameterBase.model_validate(category)
