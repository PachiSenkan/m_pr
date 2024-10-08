from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from app.database.database import Base


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(unique=True, index=True)

    datasets: Mapped[list["Dataset"]] = relationship(
        "Dataset", back_populates="category"
    )
    datasubsets: Mapped[list["DataSubset"]] = relationship(
        "DataSubset", back_populates="category"
    )


class Dataset(Base):
    __tablename__ = "datasets"

    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )

    category: Mapped["Category"] = relationship(  # type: ignore
        "Category", back_populates="datasets", lazy="subquery"
    )  # type: ignore
    pairs: Mapped[list["DatasetParameterPair"]] = relationship(
        "DatasetParameterPair", back_populates="dataset", lazy="subquery"
    )

    parameters: AssociationProxy[list["Parameter"]] = association_proxy(
        "pairs",
        "parameter",
        # creator=lambda param, value: DatasetParameterPair(
        #     parameter_id=param, parameter_value=value
        # ),
    )

    def __str__(self) -> str:
        return f"{self.id} - {self.name}: {self.description}. category: {self.category}, pairs: {self.pairs}"


class DatasetParameterPair(Base):
    __tablename__ = "datasetparameterpairs"

    dataset_id: Mapped[int] = mapped_column(ForeignKey("datasets.id"))
    parameter_id: Mapped[int] = mapped_column(ForeignKey("parameters.id"))
    parameter_value: Mapped[str] = mapped_column(nullable=False)

    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="pairs")
    parameter: Mapped["Parameter"] = relationship(  # type: ignore
        "Parameter", lazy="subquery"
    )
    subset: Mapped["Subset"] = relationship("Subset", back_populates="pair")  # type: ignore


class Subset(Base):
    __tablename__ = "subsets"

    pair_id: Mapped[int] = mapped_column(
        ForeignKey("datasetparameterpairs.id"), nullable=False
    )
    data_subset_id: Mapped[int] = mapped_column(
        ForeignKey("datasubsets.id"), nullable=False
    )

    pair: Mapped["DatasetParameterPair"] = relationship(  # type: ignore
        "DatasetParameterPair", back_populates="subset"
    )
    data_subset: Mapped["DataSubset"] = relationship(
        "DataSubset", back_populates="subset_pairs"
    )


class DataSubset(Base):
    __tablename__ = "datasubsets"

    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )

    category: Mapped["Category"] = relationship(  # type: ignore
        "Category", back_populates="datasubsets"
    )
    subset_pairs: Mapped[list["Subset"]] = relationship(
        "Subset", back_populates="data_subset"
    )


class Parameter(Base):
    __tablename__ = "parameters"

    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    datatype: Mapped[str] = mapped_column(nullable=False)
