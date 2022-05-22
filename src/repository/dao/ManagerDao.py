from sqlalchemy.orm import Session
from src.repository.entity.ManagerEntity import ManagerEntity
from src.repository.entity.UserEntity import UserEntity


class ManagerDao:

    def get_manager_by_email(self, email: str, db: Session) -> ManagerEntity:
        return db\
            .query(ManagerEntity)\
            .select_from(ManagerEntity)\
            .join(UserEntity, ManagerEntity.id_user == UserEntity.id)\
            .filter(UserEntity.email == email.lower()).first()
