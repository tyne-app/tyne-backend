from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from exception.exceptions import CustomError
from util.Constants import Constants


class ThrowerExceptions:

    @classmethod
    async def throw_custom_exception(cls,
                                     name=Constants.INTERNAL_ERROR,
                                     detail=Constants.INTERNAL_ERROR_DETAIL,
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     cause=""):
        raise CustomError(name=name,
                          detail=detail,
                          status_code=status_code,
                          cause=cause)

    @classmethod
    async def response_custom_exception(cls, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder({
                "name": f"{exc.name}",
                "details": f"{exc.detail}"
            })
        )

    @classmethod
    async def response_internal_exception(cls):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder({
                "name": Constants.INTERNAL_ERROR,
                "details": Constants.INTERNAL_ERROR_DETAIL
            })
        )
