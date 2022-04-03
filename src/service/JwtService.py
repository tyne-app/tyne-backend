from datetime import datetime, timezone, timedelta

import jwt
from fastapi import status
from firebase_admin import auth
from loguru import logger

from src.configuration.Settings import Settings
from src.dto.internal.Token import Token
from src.dto.internal.TokenProfileActivation import TokenProfileActivation
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
                "ip": ip,  # TODO: Hay que encriptar la ip más adelante
                "iss": "https://www.tyneapp.cl",
                "iat": datetime.now(tz=timezone.utc),
                "exp": datetime.now(tz=timezone.utc) + timedelta(days=1000)
            },
            str(Settings.JWT_KEY),
            algorithm="HS256")

        tokenResponse = UserTokenResponse()
        tokenResponse.access_token = token
        return tokenResponse

    async def decode_token_firebase(self, token: str):
        logger.info("decode_token_firebase")
        try:
            auth.verify_id_token(token)
        except Exception as e:
            raise CustomError(name="Token login social inválido",
                              detail="Token login social inválido",
                              status_code=status.HTTP_401_UNAUTHORIZED)

    async def verify_and_get_token_data(self, request):
        try:
            if 'authorization' not in request.headers:
                await self._throwerExceptions.throw_custom_exception(name=Constants.TOKEN_NOT_EXIST,
                                                                     detail=Constants.TOKEN_NOT_EXIST_DETAIL,
                                                                     status_code=status.HTTP_401_UNAUTHORIZED,
                                                                     cause=Constants.TOKEN_NOT_EXIST_DETAIL)
            token_header = request.headers['authorization']

            decoded_token = jwt.decode(jwt=token_header, key=str(Settings.JWT_KEY), algorithms=self.ALGORITHM)
            if not decoded_token:
                await self._throwerExceptions.throw_custom_exception(name=Constants.TOKEN_VERIFY_ERROR,
                                                                     detail=Constants.TOKEN_VERIFY_ERROR,
                                                                     status_code=status.HTTP_401_UNAUTHORIZED,
                                                                     cause="decoded_token is None")

            token = Token(int(decoded_token['id_user']), int(decoded_token['id_branch_client']))
            return token

        except (jwt.ExpiredSignatureError, Exception) as error:
            # TODO: Deuda tecnica, refactorizar.
            if type(error) is CustomError:
                raise error

            logger.info("error: {}", error)
            logger.info("error.args: {}", error.args)

            message_error = error.args[0]
            content_detail = message_error

            if self.EXPIRED_KEY_WORD in message_error:
                content_detail = Constants.SIGNATURE_EXPIRED_MSG

            if self.ALGORITHM_KEY_WORD in message_error:
                content_detail = Constants.ALGORITHM_MSG

            await self._throwerExceptions.throw_custom_exception(name=Constants.TOKEN_DECODE_ERROR,
                                                                 detail=Constants.TOKEN_DECODE_ERROR,
                                                                 status_code=status.HTTP_400_BAD_REQUEST,
                                                                 cause=content_detail)

    async def verify_email_firebase(self, email: str):
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

    def get_token_profile_activation(self, email: str, rol: int, name: str, last_name: str):
        logger.info("get_token_profile_activation")

        return jwt.encode(
            {
                "email": email,
                "rol": rol,
                "name": name,
                "last_name": last_name,
                "iss": "https://www.tyneapp.cl",
                "iat": datetime.now(tz=timezone.utc),
                "exp": datetime.now(tz=timezone.utc) + timedelta(days=1)
            },
            str(Settings.JWT_KEY),
            algorithm="HS256")

    def decode_token_profile_activation(self, token: str):
        logger.info("decode_token_profile_activation")

        decoded_token = jwt.decode(token, str(Settings.JWT_KEY), algorithms=self.ALGORITHM)

        if not decoded_token:
            raise CustomError(name=Constants.TOKEN_VERIFY_ERROR,
                              detail=Constants.TOKEN_VERIFY_ERROR,
                              status_code=status.HTTP_401_UNAUTHORIZED,
                              cause="decoded_token is None")

        return TokenProfileActivation(decoded_token['email'],
                                      int(decoded_token['rol']),
                                      decoded_token['name'],
                                      decoded_token['last_name'])
