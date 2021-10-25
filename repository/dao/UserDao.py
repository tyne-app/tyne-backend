from sqlalchemy.orm import Session
from starlette import status
from exception.exceptions import CustomError
from repository.entity.UserEntity import UserEntity
from repository.entity.UserTypeEntity import UserTypeEntity  #no eliminar o muere todo


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

