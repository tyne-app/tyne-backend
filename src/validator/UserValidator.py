from starlette import status

from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions
from src.validator.UtilsValidator import UtilsValidator


class UserValidator:
    _utils_validator_ = UtilsValidator()
    _throwerExceptions = ThrowerExceptions()

    async def validate_fields(self, fields):
        invalid_data = {}
        if not self._utils_validator_.validate_email(fields["email"]):
            invalid_data["email"] = self._utils_validator_.INVALID_DATA_MESSAGE
        if not self._utils_validator_.validate_password(fields["password"]):
            # TODO: Mejorar logica de password
            invalid_data["password"] = self._utils_validator_.INVALID_DATA_PASSWORD
        if invalid_data:
            await self._throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                                 detail=invalid_data,
                                                                 status_code=status.HTTP_400_BAD_REQUEST)
