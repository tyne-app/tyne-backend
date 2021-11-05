from pydantic import BaseModel
from starlette import status
from exception.exceptions import CustomError
from validator.SharedValidator import SharedValidator


class LoginSocialRequest(BaseModel):
    email: str
    token: str

    def validate_fields(self):
        validator = SharedValidator()

        if not validator.is_email_valid(self.email):
            raise CustomError(name="Validación body",
                              detail="Email no es válido",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Email no es válido")

        if not self.token:
            raise CustomError(name="Validación body",
                              detail="Token no puede estar vacio",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Token no puede estar vacio")
