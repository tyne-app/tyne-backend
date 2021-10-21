from datetime import datetime, timezone, timedelta
from dto.response.UserTokenResponse import UserTokenResponse
import jwt


class JwtService:

    @classmethod
    def get_token(cls):
        token = jwt.encode(
            {
                "id_user": "1",
                "id_branch": "0",
                "id_restaurant": "0",
                "name": "",
                "last_name": "",
                "rol": "customer",
                "ip": "196.168.94.62",
                "iss": "https://www.tyneapp.cl",
                "iat": datetime.now(tz=timezone.utc),
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30)
            },
            "MIGEAgEAMBAGByqGSM49AgEGBS",
            algorithm="HS256")

        tokenResponse = UserTokenResponse()
        tokenResponse.access_token = token
        return tokenResponse
