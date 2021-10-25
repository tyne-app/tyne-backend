from pydantic import BaseModel


class UserTokenResponse:
    access_token: str
