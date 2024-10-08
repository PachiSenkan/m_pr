from typing import Optional
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(unique=True, index=True)

    datasets: Mapped[list["Dataset"]] = relationship(
        "Dataset", back_populates="category"
    )


class Dataset(Base):
    __tablename__ = "datasets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True)
    parent_dataset_id: Mapped[Optional[int]] = mapped_column(ForeignKey("datasets.id"))

    children_datasets: Mapped[list["Dataset"]] = relationship(
        "Dataset", back_populates="parent_dataset", lazy="joined", join_depth=1
    )
    parent_dataset: Mapped[Optional["Dataset"]] = relationship(
        "Dataset",
        back_populates="children_datasets",
        remote_side=id,
        lazy="joined",
        join_depth=1,
    )

    category: Mapped["Category"] = relationship(
        "Category", back_populates="datasets", lazy="subquery"
    )
    pairs: Mapped[list["DatasetParameterPair"]] = relationship(
        "DatasetParameterPair",
        back_populates="dataset",
        lazy="subquery",
        cascade="all, delete-orphan",
    )

    parameters: AssociationProxy[list["Parameter"]] = association_proxy(
        "pairs", "parameter"
    )

    def __str__(self) -> str:
        return f"{self.id} - {self.name}: {self.description}. category: {self.category}, parent: {self.parent_dataset} pairs: {self.pairs}"


class DatasetParameterPair(Base):
    __tablename__ = "datasetparameterpairs"

    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id"))
    parameter_id: Mapped[int] = mapped_column(ForeignKey("parameters.id"))
    parameter_value: Mapped[str] = mapped_column(nullable=False)

    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="pairs")
    parameter: Mapped["Parameter"] = relationship(
        "Parameter",
        lazy="subquery",
        back_populates="pairs",
    )


class Parameter(Base):
    __tablename__ = "parameters"

    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    datatype: Mapped[str] = mapped_column(nullable=False)
    pairs: Mapped[list["DatasetParameterPair"]] = relationship(
        "DatasetParameterPair", back_populates="parameter", cascade="all, delete-orphan"
    )
