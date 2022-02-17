from loguru import logger
from src.dto.request.ClientRequest import ClientRequest
from src.repository.entity.UserEntity import UserEntity
from src.util.UserType import UserType
from datetime import datetime, timezone


class UserMapper:

    def to_user_entity(self, client_request: ClientRequest) -> UserEntity:
        logger.info("Creacion entidad usuario en user mapper")

        user_entity = UserEntity()
        user_entity.email = client_request.email
        user_entity.password = client_request.password
        user_entity.is_active = False
        user_entity.id_user_type = UserType.CLIENT
        user_entity.password = client_request.password
        user_entity.created_date = datetime.now(tz=timezone.utc)
        return user_entity
