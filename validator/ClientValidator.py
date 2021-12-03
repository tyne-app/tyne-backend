from starlette import status

from util.Constants import Constants
from util.ThrowerExceptions import ThrowerExceptions
from validator.UtilsValidator import UtilsValidator


class ClientValidator:
    _utils_validator_ = UtilsValidator()
    _throwerExceptions = ThrowerExceptions()

    async def validate_fields(self, fields):
        invalid_data = {}

        if not self._utils_validator_.validate_phone(fields["phone"]):
            invalid_data["phone"] = self._utils_validator_.INVALID_DATA_MESSAGE

        if not self._utils_validator_.validate_not_empty(fields["name"]):
            invalid_data["name"] = self._utils_validator_.INVALID_DATA_MESSAGE

        if invalid_data:
            await self._throwerExceptions.throw_custom_exception(name=Constants.INVALID_DATA_ERROR,
                                                                 detail=invalid_data,
                                                                 status_code=status.HTTP_400_BAD_REQUEST)

        return True
