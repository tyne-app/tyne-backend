import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from route import local_route, search_route

api_local = FastAPI(
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    title="MS-API-Local",
    description="...",  # TODO: Definir descripción
    version="1.0.0"
)

origins = ["*"]

api_local.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)


class HandlerExceptionTest(Exception):
    def __init__(self, name: str):
        self.name = name


def get_field_error(error: tuple):
    if len(error) == 2:
        return error[1]
    if len(error) == 3:
        return error[2]
    if len(error) == 4:
        return error[3]


@api_local.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error_array = exc.errors()
    error_detail_list = []

    for error in error_array:
        error_detail = {
            'field_error': get_field_error(error['loc']),
            'error_type': error['msg']
        }
        error_detail_list.append(error_detail)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'data': [], "error": error_detail_list})
    )

api_local.include_router(local_route.local_router)
api_local.include_router(search_route.search_router)


if __name__ == "__main__":
    uvicorn.run("main:api_local", host="127.0.0.1", port=8001, reload=True)
