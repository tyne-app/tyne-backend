import re

EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')


class SharedValidator:

    @classmethod
    def is_email_valid(cls, email: str):
        is_valid = False

        if re.fullmatch(EMAIL_REGEX, email):
            is_valid = True

        print(is_valid)

        return is_valid
