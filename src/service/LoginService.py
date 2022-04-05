from starlette import status

from src.repository.dao.UserDao import UserDao
from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions
from src.validator.UserValidator import UserValidator


class LoginService: # TODO: No tiene uso, verificar si se incorporará en el futuro para respaldar y eliminar archivo.
    _user_dao_ = UserDao()
    _user_validator_ = UserValidator()
    _throwerExceptions_ = ThrowerExceptions()

    async def create_user_login(self, email, password, user_type: int, db):
        email = email.lower()
        await self._user_validator_.validate_fields({"email": email, "password": password})

        user_exist = self._user_dao_.verify_email(email, db)
        if user_exist:
            await self._throwerExceptions_.throw_custom_exception(name=Constants.USER_ALREADY_EXIST,
                                                                  detail=[Constants.USER_ALREADY_EXIST],
                                                                  status_code=status.HTTP_400_BAD_REQUEST)

        user_created = self._user_dao_.create_user(email, password, user_type, db)
        if not user_created:
            await self._throwerExceptions_.throw_custom_exception(name=Constants.USER_CREATE_ERROR,
                                                                  detail=[Constants.USER_CREATE_ERROR],
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
        return user_created.id


    def delete_user_login(self, email, db):  # TODO: No es borrado físico, solamente lógico dejando estado cuenta en False
        self._user_dao_.delete_user_by_email(email.lower(), db)
