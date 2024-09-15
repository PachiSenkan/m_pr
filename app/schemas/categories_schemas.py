from pydantic import BaseModel, ConfigDict, Field


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
