from sqlalchemy.orm import Session

from . import models, schemas


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_category_by_name(db: Session, name: int):
    return db.query(models.Category).filter(models.Category.name == name).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def get_dataset(db: Session, dataset_id: int):
    return db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()


def get_datasets(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.Dataset).offset(skip).limit(limit).all()


def get_dataset_by_name(db: Session, name: int):
    return db.query(models.Dataset).filter(models.Dataset.name == name).first()


def get_parameter(db: Session, parameter_id: int):
    return (
        db.query(models.Parameter).filter(models.Parameter.id == parameter_id).first()
    )


def get_parameters(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.Parameter).offset(skip).limit(limit).all()


def get_parameter(db: Session, parameter_id: int):
    return (
        db.query(models.Parameter).filter(models.Parameter.id == parameter_id).first()
    )


def get_parameters(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.Parameter).offset(skip).limit(limit).all()


def get_parameter_by_name(db: Session, name: int):
    return db.query(models.Parameter).filter(models.Parameter.name == name).first()


def get_pair(db: Session, pair_id: int):
    return (
        db.query(models.DatasetParameterPair)
        .filter(models.DatasetParameterPair.id == pair_id)
        .first()
    )


def get_pairs(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.DatasetParameterPair).offset(skip).limit(limit).all()


def get_subset(db: Session, subset_id: int):
    return db.query(models.Subset).filter(models.Subset.id == subset_id).first()


def get_subsets(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.Subset).offset(skip).limit(limit).all()


def get_subset_by_name(db: Session, name: int):
    return db.query(models.Subset).filter(models.Subset.name == name).first()


def get_datasubset(db: Session, datasubset_id: int):
    return (
        db.query(models.DataSubset)
        .filter(models.DataSubset.id == datasubset_id)
        .first()
    )


def get_datasubsets(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.DataSubset).offset(skip).limit(limit).all()


def get_datasubset_by_name(db: Session, name: int):
    return db.query(models.DataSubset).filter(models.DataSubset.name == name).first()


def create_subsets(db: Session, pair_ids: list[int], data_subset_id: int):
    for pair_id in pair_ids:
        db_subset = models.Subset(data_subset_id=data_subset_id, pair_id=pair_id)
        print(db_subset)
        db.add(db_subset)
        db.commit()
    # return db_subsets


def create_datasubset(
    db: Session, datasubset: schemas.DataSubsetCreate, category_id: int
):
    db_datasubset = models.DataSubset(
        **datasubset.model_dump(), category_id=category_id
    )
    db.add(db_datasubset)
    db.commit()
    db.refresh(db_datasubset)
    return db_datasubset


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def create_dataset(db: Session, dataset: schemas.DatasetCreate, category_id: int):
    db_dataset = models.Dataset(**dataset.model_dump(), category_id=category_id)
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset


def create_parameter(db: Session, parameter: schemas.ParameterCreate):
    db_parameter = models.Parameter(**parameter.model_dump())
    db.add(db_parameter)
    db.commit()
    db.refresh(db_parameter)
    return db_parameter


def create_pair(
    db: Session,
    pair: schemas.DatasetParameterPairCreate,
    dataset_id: int,
    parameter_id: int,
):
    db_pair = models.DatasetParameterPair(
        **pair.model_dump(), dataset_id=dataset_id, parameter_id=parameter_id
    )
    db.add(db_pair)
    db.commit()
    db.refresh(db_pair)
    return db_pair
