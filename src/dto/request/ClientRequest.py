from pydantic import BaseModel
from loguru import logger
from src.repository.entity.ClientEntity import ClientEntity
from datetime import datetime, timezone
from src.repository.entity.UserEntity import UserEntity
from src.util.UserType import UserType
from src.service.PasswordService import PasswordService


class ClientRequest(BaseModel):

    # _password_service_ = PasswordService() 

    name: str
    lastName: str
    birthDate: datetime
    email: str
    phone: str
    password: str

    def to_user_entity(self) -> UserEntity:
        logger.info("Creacion entidad usuario en client request")

        user_entity = UserEntity()
        user_entity.email = self.email.lower()
        # self.password = PasswordService.encrypt_password(self.password)
        user_entity.password = self.password
        user_entity.is_active = True
        user_entity.id_user_type = UserType.CLIENT
        user_entity.created_date = datetime.now(tz=timezone.utc)
        return user_entity

    def to_client_entity(self) -> ClientEntity:
        logger.info("Creacion de entidad cliente en client request")
        client_entity = ClientEntity()
        client_entity.name = self.name
        client_entity.last_name = self.lastName
        client_entity.birth_date = self.birthDate  # TODO: cambiar a snake_case. Hablar con frontend
        client_entity.phone = self.phone
        client_entity.created_date = datetime.now(tz=timezone.utc)
        client_entity.updated_date = datetime.now(tz=timezone.utc)
        return client_entity