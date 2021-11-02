from starlette import status

from exception.exceptions import CustomError
from validator.UtilsValidator import UtilsValidator


class ClientValidator:
    _utils_validator_ = UtilsValidator()

    @classmethod
    def validate_fields(cls, fields):
        invalid_data = {}

        if not cls._utils_validator_.validate_phone(fields["phone"]):
            invalid_data["phone"] = cls._utils_validator_.INVALID_DATA_MESSAGE

        if not cls._utils_validator_.validate_not_empty(fields["name"]):
            invalid_data["name"] = cls._utils_validator_.INVALID_DATA_MESSAGE

        if invalid_data:
            raise CustomError(name="Error al validar los datos de entrada",
                              detail=invalid_data,
                              status_code=status.HTTP_400_BAD_REQUEST)

        return True
