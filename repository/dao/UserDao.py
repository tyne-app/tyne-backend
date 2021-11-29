from datetime import datetime

from sqlalchemy.orm import Session

from repository.entity.UserEntity import UserEntity
from repository.entity.UserTypeEntity import UserTypeEntity  # no eliminar o muere todo


class UserDao:

    @classmethod
    def get_user(cls, user_id: int, db: Session):
        return db.query(UserEntity) \
            .filter(UserEntity.id == user_id) \
            .first()

    @classmethod
    def verify_email(cls, email: str, db: Session):
        return db.query(UserEntity) \
            .filter(UserEntity.email == email) \
            .first()

    @classmethod
    def update_profile_image(cls, user_id: int, url_image: str, image_id: str, db: Session):
        user: UserEntity = db \
            .query(UserEntity) \
            .filter(UserEntity.id == user_id) \
            .first()

        if user:
            user.image_url = url_image
            user.image_id = image_id
            db.commit()
            return user

        return None

    @classmethod
    def create_user(cls, email: str, password: str, user_type: UserTypeEntity, db: Session):
        user_entity = UserEntity()
        user_entity.email = email
        user_entity.password = password
        user_entity.created_date = datetime.now()
        user_entity.is_active = True
        user_entity.id_user_type = user_type.id

        db.add(user_entity)
        db.flush()
        db.commit()

        return user_entity

    @classmethod
    def delete_user_by_email(cls, email: str, db: Session):
        db \
            .query(UserEntity) \
            .filter(UserEntity.email == email) \
            .delete()

    @classmethod
    def delete_user_by_id(cls, user_id: str, db: Session):
        db \
            .query(UserEntity) \
            .filter(UserEntity.id == user_id) \
            .delete()

    @classmethod
    def change_password(cls, user_id: int, password: str, db: Session):
        user = db.query(UserEntity) \
            .filter(UserEntity.id == user_id) \
            .first()

        if user:
            user.password = password
            db.commit()
            return user

        return None
