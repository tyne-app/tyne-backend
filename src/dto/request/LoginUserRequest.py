from pydantic import BaseModel
from starlette import status

from src.util.Constants import Constants
from src.validator.SharedValidator import SharedValidator
from src.exception.exceptions import CustomError


class LoginUserRequest(BaseModel):
    email: str
    password: str

    def validate_fields(self):
        validator = SharedValidator()

        if not validator.is_email_valid(self.email):
            raise CustomError(name=Constants.INVALID_DATA_ERROR,
                              detail=Constants.EMAIL_INVALID_ERROR,
                              status_code=status.HTTP_400_BAD_REQUEST)

        if not self.password:
            raise CustomError(name=Constants.INVALID_DATA_ERROR,
                              detail=Constants.PASSWORD_EMPTY_ERROR,
                              status_code=status.HTTP_400_BAD_REQUEST)
