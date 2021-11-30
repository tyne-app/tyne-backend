from fastapi import Request
from starlette import status
from dto.internal.Token import Token
from exception.exceptions import CustomError
from service.JwtService import JwtService


class AuthValidator:

    @classmethod
    def validate_token(self, request: Request):

        if 'authorization' not in request.headers:
            raise CustomError(name="Usuario no autorizado",
                              detail="Usuario no autorizado",
                              status_code=status.HTTP_401_UNAUTHORIZED,
                              cause="Usuario no autorizado")

        _jwt_service_ = JwtService()
        token_payload: Token = _jwt_service_.verify_and_get_token_data(token=request.headers['authorization'])
        return token_payload
