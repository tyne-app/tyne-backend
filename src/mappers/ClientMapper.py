from loguru import logger
from src.dto.request.ClientRequest import ClientRequest
from src.repository.entity.ClientEntity import ClientEntity
from datetime import datetime, timezone


class ClientMapper:

    def to_client_entity(self, client_request: ClientRequest) -> ClientEntity:
        logger.info("Creacion de entidad cliente en mapper cliente")
        client_entity = ClientEntity()
        client_entity.name = client_request.name
        client_entity.birth_date = client_request.birthDate  # TODO: cambiar a snake_case. Hablar con frontend
        client_entity.phone = client_request.phone
        client_entity.created_date = datetime.now(tz=timezone.utc)
        client_entity.updated_date = datetime.now(tz=timezone.utc)
        return client_entity
