import uvicorn
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials
from loguru import logger

from configuration.firebase_config import FirebaseConfig
from exception.exceptions import CustomError
from controller import business_controller, menu_controller, bank_controller, territory_controller, \
    user_controller, client_controller, reservation_controller

import firebase_admin

# from configuration.database import engine
from util.constants import Constants

api_local = FastAPI(
    docs_url="/v1/docs",
    title="MS-API-Local",
    description="...",  # TODO: Definir descripción
    version="1.0.0"
)

origins = ["*"]


@api_local.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder({
                "name": Constants.INTERNAL_ERROR,
                "details": Constants.INTERNAL_ERROR_DETAIL
            })
        )


api_local.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)


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


@api_local.exception_handler(CustomError)
async def custom_exception_handler(request: Request, exc: CustomError):
    logger.error(f" Error {exc.name} | cause: {exc.cause}")
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({
            "name": f"{exc.name}",
            "details": f"{exc.detail}"
        })
    )

# init firebase
FirebaseConfig.init_firebase()

api_local.include_router(bank_controller.bank_controller)
api_local.include_router(business_controller.business_controller)
api_local.include_router(client_controller.client_controller)
api_local.include_router(menu_controller.menu_controller)
api_local.include_router(reservation_controller.reservation_controller)
api_local.include_router(territory_controller.territory_controller)
api_local.include_router(user_controller.user_controller)

# engine.connect()

if __name__ == "__main__":
    uvicorn.run("main:api_local", host="127.0.0.1", port=8001, reload=True)
