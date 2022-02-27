from src.util.Constants import Constants
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

'''
    Se debería lanzar CustomError para que se capte por el middleware y este retorne un JSON con el error
'''


class CustomError(Exception):
    def __init__(self, name, status_code, detail=Constants.INTERNAL_ERROR_DETAIL, cause=''):
        super().__init__()
        self.name = name
        self.status_code = status_code
        self.detail = detail
        self.cause = cause

    def response_custom_exception(self):
        return JSONResponse(
            status_code=self.status_code,
            content=jsonable_encoder({
                "name": f"{self.name}",
                "details": self.detail
            })
        )