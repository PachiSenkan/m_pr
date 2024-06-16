from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from .database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="datasets")
    pairs = relationship("DatasetParameterPair", back_populates="dataset")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)

    datasets = relationship("Dataset", back_populates="category")
    datasubsets = relationship("DataSubset", back_populates="category")


class Parameter(Base):
    __tablename__ = "parameters"

    TYPES = [("str", "String"), ("int", "Integer"), ("float", "Float")]

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    datatype = Column(String)


class DatasetParameterPair(Base):
    __tablename__ = "pairs"

    id = Column(Integer, primary_key=True)
    parameter_value = Column(String)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    parameter_id = Column(Integer, ForeignKey("parameters.id"))

    dataset = relationship("Dataset", back_populates="pairs")
    parameter = relationship("Parameter")
    subset = relationship("Subset", back_populates="pair")


class Subset(Base):
    __tablename__ = "subsets"

    id = Column(Integer, primary_key=True)
    pair_id = Column(Integer, ForeignKey("pairs.id"))
    data_subset_id = Column(Integer, ForeignKey("datasubsets.id"))

    pair = relationship("DatasetParameterPair", back_populates="subset")
    datasubset = relationship("DataSubset", back_populates="subset_pairs")


class DataSubset(Base):
    __tablename__ = "datasubsets"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="datasubsets")
    subset_pairs = relationship("Subset", back_populates="datasubset")
