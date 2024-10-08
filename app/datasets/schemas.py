from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from app.datasets.models import Category

CategoriesOrder = {"name": Category.name, "id": Category.id}


class CategoriesOrderByEnum(str, Enum):
    name = "name"
    id = "id"


class CategoriesOrderBy(BaseModel):
    order_by: CategoriesOrderByEnum | None = None


class CategoryBase(BaseModel):
    id: int
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Название категории, от 1 до 50 символов",
    )
    model_config = ConfigDict(from_attributes=True)


class CategoryQuery(BaseModel):
    id: int | None = Field(None)
    name: str | None = Field(None)


class CategoryCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Название категории, от 1 до 50 символов",
    )


from pydantic import BaseModel, ConfigDict, Field


class ParameterBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Название параметра, от 1 до 50 символов",
    )
    description: str = Field(None, description="Описание параметра")
    datatype: str = Field(..., description="Тип данных параметра")


class ParameterCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Название параметра, от 1 до 50 символов",
    )
    description: str = Field(None, description="Описание параметра")
    datatype: str = Field(..., description="Тип данных параметра")


class ParameterQuery(BaseModel):
    name: str | None = None
    description: str | None = None
    datatype: str | None = None


class DatasetParameterPairLite(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    parameter_value: str
    parameter: ParameterBase


class DatasetParameterPairCreate(BaseModel):
    parameter_value: str
    parameter_id: int


class DatasetParameterPairUpdate(BaseModel):
    parameter_value: str | None = None
    parameter_id: int | None = None


class DatasetLite(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class DatasetBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., description="Название набора параметров")
    description: str = Field(None, description="Описание набора параметров")
    category: CategoryBase | None
    parent_dataset_id: int | None = Field(None, description="ID родительского набора")
    children_datasets: list[DatasetLite | None]
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
    pairs: list[DatasetParameterPairUpdate] | None = None


class DatasetQuery(BaseModel):
    name: str | None = None
    description: str | None = None
    category_id: int | None = None


class DataSubsetBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., description="Название поднабора параметров")
    description: str = Field(None, description="Описание поднабора параметров")
    dataset_id: int = Field(..., description="ID родительского набора данных")
    category: CategoryBase | None
    pairs: list[DatasetParameterPairLite]


class DataSubsetCreate(BaseModel):
    name: str = Field(..., description="Название набора параметров")
    description: str = Field(None, description="Описание набора параметров")
    category_id: int = Field(..., description="ID категории набора параметров")
    dataset_id: int = Field(..., description="ID родительского набора данных")
    pairs: list[int]


class DataSubsetUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category_id: int | None = None
    pairs: list[DatasetParameterPairUpdate] | None = None


class DataSubsetQuery(BaseModel):
    name: str | None = None
    description: str | None = None
    category_id: int | None = None
    dataset_id: int | None = None
