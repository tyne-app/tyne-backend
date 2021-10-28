from pydantic import BaseModel
from starlette import status
from exception.exceptions import CustomError
from validator.SharedValidator import SharedValidator


class LoginUserRequest(BaseModel):
    email: str
    password: str

    def validate_fields(self):
        validator = SharedValidator()

        if not validator.is_email_valid(self.email):
            raise CustomError(name="Validación body",
                              detail="Email no es válido",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Email no es válido")

        if not self.password:
            raise CustomError(name="Validación body",
                              detail="Contraseña no puede estar vacia",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Contraseña no puede estar vacia")