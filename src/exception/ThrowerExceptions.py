from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from src.exception.exceptions import CustomError
from src.util.Constants import Constants

'''
    Esta clasese invoca dentro de los servicios llamando al método throw_custom_exception
    para que luego sea capturado por el middleware de excepciones y este mismo middleware
    llama denuevo a esta clase ThrowerExceptions para que se genere la respuesta.
    Vuelta innecesara, puede mejorar el código invocando solamente a CustomError()
'''
class ThrowerExceptions:

    async def throw_custom_exception(self,
                                     name=Constants.INTERNAL_ERROR,
                                     detail=None,
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     cause=""):
        if detail is None:
            detail = [Constants.INTERNAL_ERROR_DETAIL]
        raise CustomError(name=name,
                          detail=detail,
                          status_code=status_code,
                          cause=cause)

    async def response_custom_exception(self, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder({
                "name": f"{exc.name}",
                "details": exc.detail
            })
        )

    async def response_internal_exception(self):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder({
                "name": Constants.INTERNAL_ERROR,
                "details": Constants.INTERNAL_ERROR_DETAIL
            })
        )
