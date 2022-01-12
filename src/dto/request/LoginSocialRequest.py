from pydantic import BaseModel
from starlette import status

from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions
from src.validator.SharedValidator import SharedValidator


class LoginSocialRequest(BaseModel):
    email: str
    token: str

    _throwerExceptions = ThrowerExceptions()

    async def validate_fields(self):
        validator = SharedValidator()

        if not validator.is_email_valid(self.email):
            await self._throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                                 detail=Constants.EMAIL_INVALID_ERROR,
                                                                 status_code=status.HTTP_400_BAD_REQUEST)

        if not self.token:
            await self._throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                                 detail=Constants.TOKEN_NOT_EXIST,
                                                                 status_code=status.HTTP_400_BAD_REQUEST)
