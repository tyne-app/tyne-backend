from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status
from exception.exceptions import CustomError
from repository.entity.UserEntity import UserEntity
from loguru import logger
from repository.entity.UserTypeEntity import UserTypeEntity  # no eliminar o muere todo


class UserDao:

    @classmethod
    def get_user(cls, user_id: int, db: Session):
        try:
            user = db.query(UserEntity) \
                .filter(UserEntity.id == user_id) \
                .first()
            return user
        except Exception as error:
            raise error

    @classmethod
    def login(cls, email: str, db: Session):
        try:
            user = db.query(UserEntity) \
                .filter(UserEntity.email == email) \
                .first()
            return user
        except Exception as error:
            raise error

    @classmethod
    def update_profile_image(cls, user_id: int, url_image: str, image_id: str, db: Session):
        try:
            user: UserEntity = db.query(UserEntity) \
                .filter(UserEntity.id == user_id) \
                .first()

            if user:
                user.image_url = url_image
                user.image_id = image_id
                db.commit()
                return user

            raise CustomError(name="Usuario no existe",
                              detail="No existe el usuario " + str(user_id),
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="")

        except Exception as error:
            raise error

    @classmethod
    def create_user_login(cls, email: str, password: str, user_type: UserTypeEntity, db: Session):
        try:
            user_entity = UserEntity()
            user_entity.email = email
            user_entity.password = password
            user_entity.created_date = datetime.now()
            user_entity.is_active = True
            user_entity.id_user_type = user_type.id

            db.add(user_entity)
            db.flush()

            return user_entity

        except SQLAlchemyError as error:
            logger.error(error)
            raise CustomError(name="Error create_user",
                              detail="BD error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause=error.__cause__)

        except Exception as error:
            logger.error(error)
            raise CustomError(name="Error create_user",
                              detail="BD error",
                              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              cause=error.__cause__)
