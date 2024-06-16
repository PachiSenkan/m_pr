from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class DatasetBase(BaseModel):
    name: str
    description: str


class DatasetCreate(DatasetBase):
    pass


class ParameterBase(BaseModel):
    name: str
    description: str
    datatype: str


class ParameterCreate(ParameterBase):
    pass


class Parameter(ParameterBase):
    id: int


class DatasetParameterPairBase(BaseModel):
    parameter_value: str


class DatasetParameterPairCreate(DatasetParameterPairBase):
    pass


class DatasetParameterPair(DatasetParameterPairBase):
    id: int
    dataset_id: int
    parameter_id: int

    class Config:
        orm_mode = True


class DatasetParameterPairView(DatasetParameterPairBase):
    parameter: ParameterBase


class Dataset(DatasetBase):
    id: int
    category: Category
    pairs: list[DatasetParameterPairView]

    class Config:
        orm_mode = True


class SubsetBase(BaseModel):
    pass


class SubsetCreate(SubsetBase):
    pass


class Subset(SubsetBase):
    id: int
    pair: DatasetParameterPairView
    data_subset_id: int


class SubsetView(SubsetBase):
    pair: DatasetParameterPairView


class DataSubsetBase(BaseModel):
    name: str
    description: str


class DataSubsetCreate(DataSubsetBase):
    pass


class DataSubset(DataSubsetBase):
    id: int
    category: Category
    subset_pairs: list[SubsetView]

    class Config:
        orm_mode = True
