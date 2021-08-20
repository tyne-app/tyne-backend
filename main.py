import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from route.routes import routes  # TODO: Por definir
from route.local_route import local_router

api_local = FastAPI(
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    title="MS-API-Local",
    description="...",  # TODO: Definir descripción
    version="1.0.0"
)

class HandlerExceptionTest(Exception):
    def __init__(self, name: str):
        self.name = name

# TODO: Mejorar exception
'''
@api_local.exception_handler(HandlerExceptionTest)
async def api_exception_handler(request: Request, exc: HandlerExceptionTest):
    print("Reques en handler exceptioN!")
    print(request)
    print("Exc")
    print(exc)
    return JSONResponse(
        status_code=418,
        content={"message": f'Oops! {exc.name}'}
    )
'''
@api_local.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # TODO: Mejorar response de Excepcion valores invalidos
    # TODO: Esta función permite manejar la excepcion de datos inválidos en request o datos ausentes.
    print(exc.errors())  # TODO: Este podría servir para devolver un response más amigable a frontend
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"hola": exc.errors(), "body": exc.body})
    )

api_local.include_router(local_router)

if __name__ == "__main__":
    uvicorn.run("main:api_local", host="127.0.0.1", port=8001, reload=True)
