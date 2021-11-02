from loguru import logger
from starlette import status

from exception.exceptions import CustomError
from repository.dao.UserDao import UserDao
from repository.dao.UserTypeDao import UserTypeDao
from validator.UserValidator import UserValidator


class LoginService:
    _user_dao_ = UserDao()
    _user_type_dao_ = UserTypeDao()
    _user_validator_ = UserValidator()

    @classmethod
    def create_user_login(cls, email, password, name_user_type, db):
        cls._user_validator_.validate_fields({"email": email, "password": password})
        user_type = cls._user_type_dao_.get_user_type_by_name(name_user_type, db)

        if not user_type.id:
            raise CustomError(
                name="Error LoginService",
                detail="user_type not find",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user_created = cls._user_dao_.create_user_login(email, password, user_type, db)

        if not user_created.id:
            raise CustomError(
                name="Error LoginService",
                detail="User not creted",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return user_created.id

    @classmethod
    def delete_user_login(cls, email, db):
        cls._user_dao_.delete_user_by_email(email, db)
