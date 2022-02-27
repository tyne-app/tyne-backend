from pydantic import BaseModel


class UserChangePasswordRequest(BaseModel):
    password: str
