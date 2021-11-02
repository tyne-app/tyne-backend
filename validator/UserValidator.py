from starlette import status

from exception.exceptions import CustomError
from validator.UtilsValidator import UtilsValidator


class UserValidator:

    _utils_validator_ = UtilsValidator()

    @classmethod
    def validate_fields(cls, fields):

        invalid_data = {}

        if not cls._utils_validator_.validate_email(fields["email"]):
            invalid_data["email"] = cls._utils_validator_.INVALID_DATA_MESSAGE

        if not cls._utils_validator_.validate_not_empty(fields["password"]):
            # TODO: Mejorar logica de password
            invalid_data["password"] = cls._utils_validator_.INVALID_DATA_MESSAGE

        if invalid_data:
            raise CustomError(name="Error al validar los datos de entrada",
                              detail=invalid_data,
                              status_code=status.HTTP_400_BAD_REQUEST)

        return True
