from pydantic import BaseModel, ConfigDict, Field
from app.schemas.categories_schemas import CategoryBase
from app.schemas.parameters_schemas import ParameterBase


class DatasetParameterPairLite(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    parameter_value: str
    parameter: ParameterBase


class DatasetParameterPairCreate(BaseModel):
    parameter_value: str
    parameter_id: int


class DatasetBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., description="Название набора параметров")
    description: str = Field(None, description="Описание набора параметров")
    category: CategoryBase
    pairs: list[DatasetParameterPairLite]


class DatasetCreate(BaseModel):
    name: str = Field(..., description="Название набора параметров")
    description: str = Field(None, description="Описание набора параметров")
    category_id: int = Field(..., description="ID категории набора параметров")
    pairs: list[DatasetParameterPairCreate]


class DatasetUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category_id: int | None = None
    pairs: list[DatasetParameterPairCreate] | None = None


class DatasetQuery(BaseModel):
    name: str | None = None
    description: str | None = None
    category_id: int | None = None
