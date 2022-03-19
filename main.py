import json

import uvicorn
from fastapi import status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from loguru import logger

from src.configuration.firebase.firebase_config import FirebaseConfig
from src.exception.exceptions import CustomError
from src.controller import business_controller, menu_controller, bank_controller, territory_controller, \
    user_controller, client_controller, reservation_controller

from src.exception.ThrowerExceptions import ThrowerExceptions
from src.configuration.api.api_config import setup_app, add_middlewares

app = setup_app()
app = add_middlewares(app)


def get_field_error(error: tuple):
    if len(error) == 2:
        return error[1]
    if len(error) == 3:
        return error[2]
    if len(error) == 4:
        return error[3]


@app.exception_handler(RequestValidationError)
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


_throwerExceptions = ThrowerExceptions()


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        error_detail = {
            "URL": f"{request.url}",
            "query_params": f"{request.query_params}",
            "path_params": f"{request.path_params}",
            "cause": f"{e}",
        }
        logger.exception(e)
        logger.error(json.dumps(error_detail, indent=4))
        return await _throwerExceptions.response_internal_exception()


@app.exception_handler(CustomError)
async def custom_exception_handler(request: Request, exc: CustomError):
    error_detail = {
        "URL": f"{request.url}",
        "query_params": f"{request.query_params}",
        "path_params": f"{request.path_params}",
        "custom_error": f"{exc.__dict__}",
    }
    logger.error(json.dumps(error_detail, indent=4))

    return await _throwerExceptions.response_custom_exception(exc)


firebase_config = FirebaseConfig()
firebase_config.init_firebase()

app.include_router(bank_controller.bank_controller)
app.include_router(business_controller.business_controller)
app.include_router(client_controller.client_controller)
app.include_router(menu_controller.menu_controller)
app.include_router(reservation_controller.reservation_controller)
app.include_router(territory_controller.territory_controller)
app.include_router(user_controller.user_controller)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
