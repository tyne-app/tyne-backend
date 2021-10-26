from fastapi import status
from datetime import datetime, timezone, timedelta
from dto.response.UserTokenResponse import UserTokenResponse
import jwt
from exception.exceptions import CustomError
from loguru import logger


class JwtService:

    KEY = "secret"
    ALGORITHM = "HS256"
    EXPIRED_KEY_WORD = "expired"
    SIGNATURE_EXPIRED_MSG = "Token expirado"
    ALGORITHM_KEY_WORD = "alg"
    ALGORITHM_MSG = "Token entrante no permitido"

    @classmethod
    def get_token(cls, id_user: int, id_branch_client: int, rol: int, ip: str):

        token = jwt.encode(
            {
                "id_user": id_user,
                "id_branch_client": id_branch_client,
                "rol": rol,
                "ip": ip,  # TODO: Hay que encriptar la ip más adelante
                "iss": "https://www.tyneapp.cl",
                "iat": datetime.now(tz=timezone.utc),
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30)
            },
            cls.KEY,
            algorithm=cls.ALGORITHM)

        token_response = UserTokenResponse()
        token_response.access_token = token

        return token_response

    def verify_and_get_token_data(self, token: str):
        try:
            decoded_token = jwt.decode(jwt=token, key=self.KEY, algorithms=self.ALGORITHM)
            if not decoded_token:
                raise CustomError(name="Error al verificar token",
                                  detail="",
                                  status_code=status.HTTP_400_BAD_REQUEST,
                                  cause="")

            return int(decoded_token['id_branch_client'])

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
