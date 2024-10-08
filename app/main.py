from fastapi import FastAPI
import uvicorn

from app.datasets.routers import (
    router_categories,
    router_datasets,
    router_parameters,
)


app = FastAPI()

app.include_router(router_categories)
app.include_router(router_datasets)
app.include_router(router_parameters)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
