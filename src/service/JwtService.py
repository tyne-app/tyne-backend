from datetime import datetime, timezone, timedelta

import jwt
from fastapi import status
from firebase_admin import auth
from loguru import logger

from src.configuration.Settings import Settings
from src.dto.internal.Token import Token
from src.dto.internal.TokenProfile import TokenProfile
from src.dto.response.UserTokenResponse import UserTokenResponse
from src.exception.ThrowerExceptions import ThrowerExceptions
from src.exception.exceptions import CustomError
from src.util.Constants import Constants


class JwtService:
    _throwerExceptions = ThrowerExceptions()

    ALGORITHM = "HS256"
    EXPIRED_KEY_WORD = "expired"
    ALGORITHM_KEY_WORD = "alg"
    SIGNATURE_EXPIRED_MSG = "Token expirado"
    ALGORITHM_MSG = "Token entrante no permitido"

    def get_token(self, id_user: int, id_branch_client: int, rol: int, ip: str, name: str, last_name: str):
        token = jwt.encode(
            {
                "id_user": id_user,
                "id_branch_client": id_branch_client,
                "rol": rol,
                "name": name,
                "last_name": last_name,
                "iss": "https://tyne.cl",
                "iat": datetime.now(tz=timezone.utc),
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30)
            },
            str(Settings.JWT_KEY),
            algorithm="HS256")

        tokenResponse = UserTokenResponse()
        tokenResponse.access_token = token
        return tokenResponse

    async def decode_token_firebase(self, token: str):
        logger.info("decode_token_firebase")
        try:
            return auth.verify_id_token(token)

        except Exception as e:
            raise CustomError(name="Token login social inválido",
                              detail="Token login social inválido",
                              status_code=status.HTTP_401_UNAUTHORIZED)

    async def verify_and_get_token_data(self, request):
        try:
            if 'authorization' not in request.headers:
                raise Exception(Constants.TOKEN_NOT_EXIST)

            token_header = request.headers['authorization']

            decoded_token = jwt.decode(jwt=token_header, key=str(Settings.JWT_KEY), algorithms=self.ALGORITHM)
            if not decoded_token:
                raise Exception(Constants.TOKEN_VERIFY_ERROR)

            token = Token(int(decoded_token['id_user']), int(decoded_token['id_branch_client']),
                          int(decoded_token['rol']))
            return token
        except Exception as error:
            token = request.headers['authorization']
            logger.info("token: {}", token)
            logger.error("error: {}", error)

            await self._throwerExceptions.throw_custom_exception(name=Constants.TOKEN_INVALID_ERROR,
                                                                 detail=Constants.TOKEN_INVALID_ERROR,
                                                                 status_code=status.HTTP_401_UNAUTHORIZED)

    async def verify_email_firebase(self, email: str):  # TODO: No se ocupa ahora, eliminar si pruebas login salen bien.
        is_valid = False
        try:
            auth.get_user_by_email(email)
            is_valid = True
            logger.info("Usuario registrado con redes sociales")
        except Exception as e:
            logger.error("Exception: {}", e)
            logger.error("Exception dictionary: {}", e.__dict__)
        finally:
            if is_valid:
                raise CustomError(name=Constants.USER_EXIST_FIREBASE,
                                  detail=Constants.USER_EXIST_FIREBASE,
                                  status_code=status.HTTP_401_UNAUTHORIZED)

    def get_token_profile(self, user_id: int, email: str, rol: int):
        logger.info("get_token_profile")

        return jwt.encode(
            {
                "user_id": user_id,
                "email": email,
                "rol": rol,
                "iss": "https://www.tyne.cl",
                "iat": datetime.now(tz=timezone.utc),
                "exp": datetime.now(tz=timezone.utc) + timedelta(days=1)
            },
            str(Settings.JWT_KEY),
            algorithm="HS256")

    def decode_token_profile(self, token: str):
        logger.info("decode_token_profile")

        decoded_token = jwt.decode(token, str(Settings.JWT_KEY), algorithms=self.ALGORITHM)

        if not decoded_token:
            raise CustomError(name=Constants.TOKEN_VERIFY_ERROR,
                              detail=Constants.TOKEN_VERIFY_ERROR,
                              status_code=status.HTTP_401_UNAUTHORIZED,
                              cause="decoded_token is None")

        return TokenProfile(user_id=int(decoded_token['user_id']),
                            email=decoded_token['email'],
                            rol=int(decoded_token['rol']))
