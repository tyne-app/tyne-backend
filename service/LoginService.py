from starlette import status

from repository.dao.UserDao import UserDao
from repository.dao.UserTypeDao import UserTypeDao
from util.Constants import Constants
from util.ThrowerExceptions import ThrowerExceptions
from validator.UserValidator import UserValidator
from dto.response.ClientCreateResponse import ClientCreateResponse


class LoginService:
    _user_dao_ = UserDao()
    _user_type_dao_ = UserTypeDao()
    _user_validator_ = UserValidator()
    _throwerExceptions = ThrowerExceptions()

    async def create_user_login(self, email, password, name_user_type, db):
        await self._user_validator_.validate_fields({"email": email, "password": password})

        user_exist = self._user_dao_.verify_email(email, db)
        if user_exist:
            await self._throwerExceptions.throw_custom_exception(name=Constants.USER_ALREADY_EXIST,
                                                                 detail=Constants.USER_ALREADY_EXIST,
                                                                 status_code=status.HTTP_400_BAD_REQUEST)

        user_type = self._user_type_dao_.get_user_type_by_name(name_user_type, db)
        if not user_type:
            await self._throwerExceptions.throw_custom_exception(name=Constants.USER_CREATE_ERROR,
                                                                 detail=Constants.USER_TYPE_MOT_FOUND,
                                                                 status_code=status.HTTP_400_BAD_REQUEST)

        user_created = self._user_dao_.create_user(email, password, user_type, db)
        if not user_created:
            await self._throwerExceptions.throw_custom_exception(name=Constants.USER_CREATE_ERROR,
                                                                 detail=Constants.USER_CREATE_ERROR,
                                                                 status_code=status.HTTP_400_BAD_REQUEST)
        return user_created.id

    def delete_user_login(self, email, db):
        self._user_dao_.delete_user_by_email(email, db)
