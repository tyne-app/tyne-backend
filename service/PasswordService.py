import random
import string


class PasswordService:

    @staticmethod
    def generate_password():
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(20))
        return password
