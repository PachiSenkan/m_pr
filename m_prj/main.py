from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/categories/", response_model=list[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories


@app.get("/categories/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@app.post("/categories/", response_model=schemas.Category)
def create_category(
    category: Annotated[schemas.CategoryCreate, Depends()],
    db: Session = Depends(get_db),
):
    db_category = crud.get_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    return crud.create_category(db=db, category=category)


@app.get("/datasets/", response_model=list[schemas.Dataset])
def read_datasets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    datasets = crud.get_datasets(db, skip=skip, limit=limit)
    return datasets


@app.get("/datasets/{dataset_id}", response_model=schemas.Dataset)
def read_dataset(dataset_id: int, db: Session = Depends(get_db)):
    db_dataset = crud.get_dataset(db, dataset_id=dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return db_dataset


@app.post("/datasets/", response_model=schemas.Dataset)
def create_dataset(
    category_id: int,
    dataset: Annotated[schemas.DatasetCreate, Depends()],
    db: Session = Depends(get_db),
):
    db_dataset = crud.get_dataset_by_name(db, name=dataset.name)
    if db_dataset:
        raise HTTPException(status_code=400, detail="Dataset already exists")

    return crud.create_dataset(db=db, dataset=dataset, category_id=category_id)


@app.get("/parameters/", response_model=list[schemas.Parameter])
def read_parameters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    parameters = crud.get_parameters(db, skip=skip, limit=limit)
    return parameters


@app.get("/parameters/{dataset_id}", response_model=schemas.Parameter)
def read_parameter(parameter_id: int, db: Session = Depends(get_db)):
    db_parameter = crud.get_parameter(db, parameter_id=parameter_id)
    if db_parameter is None:
        raise HTTPException(status_code=404, detail="Parameter not found")
    return db_parameter


@app.post("/parameters/", response_model=schemas.Parameter)
def create_dataset(
    parameter: Annotated[schemas.ParameterCreate, Depends()],
    db: Session = Depends(get_db),
):
    db_parameter = crud.get_parameter_by_name(db, name=parameter.name)
    if db_parameter:
        raise HTTPException(status_code=400, detail="Parameter already exists")

    return crud.create_parameter(db=db, parameter=parameter)


@app.get("/pairs/", response_model=list[schemas.DatasetParameterPair])
def read_pairs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pairs = crud.get_pairs(db, skip=skip, limit=limit)
    return pairs


@app.get("/pairs/{pair_id}", response_model=schemas.DatasetParameterPair)
def read_pair(pair_id: int, db: Session = Depends(get_db)):
    db_pair = crud.get_pair(db, pair_id=pair_id)
    if db_pair is None:
        raise HTTPException(status_code=404, detail="Pair not found")
    return db_pair


@app.post("/pairs/", response_model=schemas.DatasetParameterPair)
def create_dataset(
    dataset_id: int,
    parameter_id: int,
    pair: Annotated[schemas.DatasetParameterPairCreate, Depends()],
    db: Session = Depends(get_db),
):
    return crud.create_pair(
        db=db, pair=pair, dataset_id=dataset_id, parameter_id=parameter_id
    )


@app.get("/subsets/", response_model=list[schemas.Subset])
def read_subsets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subsets = crud.get_subsets(db, skip=skip, limit=limit)
    return subsets


@app.get("/subsets/{subset_id}", response_model=schemas.Subset)
def read_pair(subset_id: int, db: Session = Depends(get_db)):
    db_subset = crud.get_subset(db, subset_id=subset_id)
    if db_subset is None:
        raise HTTPException(status_code=404, detail="Subset not found")
    return db_subset


@app.post("/subsets/")  # , response_model=list[schemas.Subset])
def create_subset(
    pair_ids: list[int],
    data_subset_id: int,
    db: Session = Depends(get_db),
):
    crud.create_subsets(db=db, data_subset_id=data_subset_id, pair_ids=pair_ids)
    return {"GOD": "WORKS"}


@app.get("/datasubsets/", response_model=list[schemas.DataSubset])
def read_datasubsets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    datasubsets = crud.get_datasubsets(db, skip=skip, limit=limit)
    return datasubsets


@app.get("/datasubsets/{datasubset_id}", response_model=schemas.Dataset)
def read_datasubset(datasubset_id: int, db: Session = Depends(get_db)):
    db_datasubset = crud.get_datasubset(db, datasubset_id == datasubset_id)
    if db_datasubset is None:
        raise HTTPException(status_code=404, detail="Datasubset not found")
    return db_datasubset


@app.post("/datasubsets/", response_model=schemas.DataSubset)
def create_datasubset(
    category_id: int,
    datasubset: Annotated[schemas.DataSubsetCreate, Depends()],
    db: Session = Depends(get_db),
):
    db_datasubset = crud.get_datasubset_by_name(db, name=datasubset.name)
    if db_datasubset:
        raise HTTPException(status_code=400, detail="Datasubset already exists")

    return crud.create_datasubset(db=db, datasubset=datasubset, category_id=category_id)
