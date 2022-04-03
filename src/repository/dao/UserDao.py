from datetime import datetime
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from sqlalchemy.engine import Row
from src.exception.exceptions import CustomError
from src.repository.entity.UserEntity import UserEntity
from src.repository.entity.ManagerEntity import ManagerEntity
from src.repository.entity.BranchEntity import BranchEntity
from src.repository.entity.ClientEntity import ClientEntity
from src.dto.internal.TokenProfileActivation import TokenProfileActivation


class UserDao:

    def get_user(self, user_id: int, db: Session):
        return db.query(UserEntity) \
            .filter(UserEntity.id == user_id) \
            .first()

    def user_login(self, email: str, db: Session) -> UserEntity:
        return db.query(UserEntity) \
            .filter(UserEntity.email == email) \
            .filter(UserEntity.is_active) \
            .first()

    def verify_email(self, email: str, db: Session):  # TODO: Es necesario esto?
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

    def create_user(self, email: str, password: str, user_type: int, db: Session):
        user_entity = UserEntity()
        user_entity.email = email
        user_entity.password = password
        user_entity.created_date = datetime.now()
        user_entity.is_active = True
        user_entity.id_user_type = user_type

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

    def send_email_forgotten_password(self, email: str, db: Session) -> bool:
        return db.query(exists().where(UserEntity.email == email)).scalar()

    def get_email_by_branch(self, branch_id: int, db: Session) -> str:
        branch_email: Row = db.query(UserEntity.email) \
            .join(ManagerEntity, ManagerEntity.id_user == UserEntity.id) \
            .join(BranchEntity, BranchEntity.manager_id == ManagerEntity.id) \
            .filter(BranchEntity.id == branch_id).first()
        return branch_email[0]  # TODO: Ver forma de obtener email mas directa

    def get_email_by_cient(self, client_id: int, db: Session) -> str:

        client_email: Row = db.query(UserEntity.email) \
            .join(ClientEntity, ClientEntity.id_user == UserEntity.id) \
            .filter(ClientEntity.id == client_id).first()
        return client_email[0]

    def activate_client_user(self, token_profile_activation: TokenProfileActivation, db: Session):
        user: UserEntity = db.query(UserEntity).join(ClientEntity, ClientEntity.id_user == UserEntity.id) \
            .filter(UserEntity.id_user_type == token_profile_activation.rol) \
            .filter(UserEntity.email == token_profile_activation.email) \
            .filter(UserEntity.is_active == False) \
            .filter(ClientEntity.name == token_profile_activation.name) \
            .filter(ClientEntity.last_name == token_profile_activation.last_name).first()

        if not user:
            raise CustomError(name="El usuario no existe o ya esta activo",
                              detail="El usuario no existe o ya esta activo",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="El usuario no existe o ya esta activo")
        user.is_active = True
        db.commit()

    def activate_manager_user(self, token_profile_activation: TokenProfileActivation, db: Session):
        user: UserEntity = db.query(UserEntity).join(ManagerEntity, ManagerEntity.id_user == UserEntity.id) \
            .filter(UserEntity.id_user_type == token_profile_activation.rol) \
            .filter(UserEntity.email == token_profile_activation.email) \
            .filter(UserEntity.is_active == False) \
            .filter(ManagerEntity.name == token_profile_activation.name) \
            .filter(ManagerEntity.last_name == token_profile_activation.last_name).first()

        if not user:
            raise CustomError(name="El usuario no existe o ya esta activo",
                              detail="El usuario no existe o ya esta activo",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="El usuario no existe o ya esta activo")
        user.is_active = True
        db.commit()
