from fastapi import status
from datetime import datetime, timezone, timedelta

from dto.internal.Token import Token
from dto.response.UserTokenResponse import UserTokenResponse
import jwt
from exception.exceptions import CustomError
from loguru import logger
from firebase_admin import auth


class JwtService:

    KEY = "AAmfjZRE563ewniu834Z-e45422-344"
    ALGORITHM = "HS256"
    EXPIRED_KEY_WORD = "expired"
    SIGNATURE_EXPIRED_MSG = "Token expirado"
    ALGORITHM_KEY_WORD = "alg"
    ALGORITHM_MSG = "Token entrante no permitido"

    @classmethod
    def get_token(cls, id_user: int, id_branch_client: int, rol: int, ip: str, name: str, last_name: str):
        key = "secret"
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
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30)
            },
            key,
            algorithm="HS256")

        tokenResponse = UserTokenResponse()
        tokenResponse.access_token = token
        return tokenResponse

    @classmethod
    def decode_token(cls, token: str):
        print(token)
        decoded_token = auth.verify_id_token(token)
        print(decoded_token)

    def verify_and_get_token_data(self, token: str):
        try:
            decoded_token = jwt.decode(jwt=token, key=self.KEY, algorithms=self.ALGORITHM)
            if not decoded_token:
                raise CustomError(name="Error al verificar token",
                                  detail="",
                                  status_code=status.HTTP_400_BAD_REQUEST,
                                  cause="")

            token = Token(int(decoded_token['id_user']), int(decoded_token['id_branch_client']))
            return token

        except (jwt.ExpiredSignatureError, Exception) as error:
            logger.info("error: {}", error)
            logger.info("error.args: {}", error.args)
            content_detail = None
            message_error = error.args[0]

            if self.EXPIRED_KEY_WORD in message_error:
                content_detail = self.SIGNATURE_EXPIRED_MSG
            if self.ALGORITHM_KEY_WORD in message_error:
                content_detail = self.ALGORITHM_MSG
            else:
                content_detail = message_error
            raise CustomError(name="Error al decodificar token",
                              detail=content_detail,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="")
