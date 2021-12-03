from fastapi import Request
from dto.internal.Token import Token
from service.JwtService import JwtService


class AuthValidator:

    async def validate_token(self, request: Request):
        _jwt_service_ = JwtService()
        token_payload: Token = await _jwt_service_.verify_and_get_token_data(request=request)
        return token_payload
