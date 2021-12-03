from datetime import datetime

from sqlalchemy.orm import Session

from repository.entity.UserEntity import UserEntity
from repository.entity.UserTypeEntity import UserTypeEntity


class UserDao:

    def get_user(self, user_id: int, db: Session):
        return db.query(UserEntity) \
            .filter(UserEntity.id == user_id) \
            .first()

    def verify_email(self, email: str, db: Session):
        return db.query(UserEntity) \
            .filter(UserEntity.email == email) \
            .first()

    def update_profile_image(self, user_id: int, url_image: str, image_id: str, db: Session):
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

    def create_user(self, email: str, password: str, user_type: UserTypeEntity, db: Session):
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

    def delete_user_by_email(self, email: str, db: Session):
        db \
            .query(UserEntity) \
            .filter(UserEntity.email == email) \
            .delete()

    def delete_user_by_id(self, user_id: str, db: Session):
        db \
            .query(UserEntity) \
            .filter(UserEntity.id == user_id) \
            .delete()

    def change_password(self, user_id: int, password: str, db: Session):
        user = db.query(UserEntity) \
            .filter(UserEntity.id == user_id) \
            .first()

        if user:
            user.password = password
            db.commit()
            return user

        return None
