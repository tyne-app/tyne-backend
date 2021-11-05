import re


class UtilsValidator:
    NUMBER_AND_WORD_REGEX = re.compile(r"[A-Za-z0-9\sáéíóúÁÉÍÓÚñ]+")
    NUMBER_REGEX = re.compile(r"[0-9]+")
    PHONE_REGEX = re.compile(r"\+569[0-9]{8}")
    EMAIL_REGEX = re.compile(r"[A-Za-z0-9\.]+@[A-Za-z0-9]+\.?[A-Za-z]+")
    INVALID_DATA_MESSAGE = "Formato no válido"

    def validate_email(self, email):
        return re.fullmatch(self.EMAIL_REGEX, email)

    def validate_password(self, password):
        return True

    def validate_phone(self, phone):
        return re.fullmatch(self.PHONE_REGEX, phone)

    def validate_not_empty(self, value):
        if value is None:
            return False
        return len(value) > 0
