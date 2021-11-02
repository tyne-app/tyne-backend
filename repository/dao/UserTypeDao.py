from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from loguru import logger
from starlette import status

from exception.exceptions import CustomError
from repository.entity.UserTypeEntity import UserTypeEntity


class UserTypeDao:

    @classmethod
    def get_user_type_by_name(cls, name: str, db: Session):
        try:
            return db\
                .query(UserTypeEntity)\
                .filter(UserTypeEntity.name == name)\
                .first()

        except SQLAlchemyError as error:
            logger.error(error)
            raise CustomError(name="Error get_user_type_by_name",
                              detail="BD error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause=error.__cause__)

        except Exception as error:
            logger.error(error)
            raise CustomError(name="Error get_user_type_by_name",
                              detail="BD error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause=error.__cause__)
