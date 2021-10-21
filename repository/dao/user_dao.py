from sqlalchemy.orm import Session
from repository.entity.UserEntity import UserEntity


class UserDao:

    @classmethod
    def login(cls, email: str, db: Session):
        try:
            user = db.query(UserEntity) \
                .filter(UserEntity.email == email) \
                .first()
            return user
        except Exception as error:
            raise error
