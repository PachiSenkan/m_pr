from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import uvicorn

# from app.datasets import models

# from app import crud, schemas
# from app.database import engine, async_session_maker
from app.api.v1.routes.categories import router_categories
from app.api.v1.routes.datasets import router_datasets
from app.api.v1.routes.parameters import router_parameters

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router_categories)
app.include_router(router_datasets)
app.include_router(router_parameters)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
