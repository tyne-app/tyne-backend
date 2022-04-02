from pydantic import BaseModel
from starlette import status

from src.util.Constants import Constants
from src.validator.SharedValidator import SharedValidator
from src.exception.exceptions import CustomError


class LoginSocialRequest(BaseModel):
    email: str
    token: str

    def validate_fields(self):
        validator = SharedValidator()

        if not validator.is_email_valid(self.email):
            raise CustomError(name=Constants.INVALID_DATA_ERROR,
                              detail=Constants.EMAIL_INVALID_ERROR,
                              status_code=status.HTTP_400_BAD_REQUEST)

        if not self.token:
            raise CustomError(name=Constants.INVALID_DATA_ERROR,
                              detail=Constants.TOKEN_NOT_EXIST,
                              status_code=status.HTTP_400_BAD_REQUEST)
