from datetime import datetime, timezone, timedelta
from dto.response.UserTokenResponse import UserTokenResponse
import jwt


class JwtService:

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
