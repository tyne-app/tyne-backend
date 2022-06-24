from pydantic import BaseModel


class UserToken(BaseModel):
    token: str
