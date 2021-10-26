from sqlalchemy.orm import Session

from dto.response.ClientResponse import ClientResponse
from repository.dao.ClientDao import ClientDao
from repository.entity.ClientEntity import ClientEntity


class ClientService:
    _client_dao_ = ClientDao()

    @classmethod
    def get_client_by_id(cls, client_id: int, db: Session):
        client: ClientEntity = cls._client_dao_.get_client(client_id=client_id, db=db)

        if client is not None:
            client_dto = ClientResponse()
            response = client_dto.map(client_entity=client)
            return response

        return None
