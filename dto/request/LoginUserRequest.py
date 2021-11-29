from pydantic import BaseModel
from starlette import status

from util.Constants import Constants
from util.ThrowerExceptions import ThrowerExceptions
from validator.SharedValidator import SharedValidator


class LoginUserRequest(BaseModel):
    email: str
    password: str

    _throwerExceptions = ThrowerExceptions()

    async def validate_fields(self):
        validator = SharedValidator()

        if not validator.is_email_valid(self.email):
            await self._throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                                 detail=Constants.EMAIL_INVALID_ERROR,
                                                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not self.password:
            await self._throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                                 detail=Constants.PASSWORD_EMPTY_ERROR,
                                                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
