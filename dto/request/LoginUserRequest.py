from pydantic import BaseModel


class LoginUserRequest(BaseModel):
    email: str
    password: str

