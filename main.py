import uvicorn
from fastapi import FastAPI
from route.routes import routes

api_local = FastAPI(
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    title="MS-API-Local",
    description="...",  # TODO: Definir descripción
    version="1.0.0"
)

api_local.include_router(routes)

if __name__ == "__main__":
    uvicorn.run("main:api_local", host="127.0.0.1", port=8000, reload=True)
