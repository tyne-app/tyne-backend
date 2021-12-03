from sqlalchemy.orm import Session
from repository.entity.UserTypeEntity import UserTypeEntity


class UserTypeDao:

    def get_user_type_by_name(self, name: str, db: Session):
        return db \
            .query(UserTypeEntity) \
            .filter(UserTypeEntity.name == name) \
            .first()
