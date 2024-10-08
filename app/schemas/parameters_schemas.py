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
