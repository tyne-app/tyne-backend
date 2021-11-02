from loguru import logger
from sqlalchemy.orm import Session
from starlette import status

from dto.request.ClientRequestDTO import ClientRequestDTO
from dto.response.ClientResponse import ClientResponse
from exception.exceptions import CustomError
from repository.dao.ClientDao import ClientDao
from repository.entity.ClientEntity import ClientEntity
from service.LoginService import LoginService
from dto.dto import GenericDTO as wrapperDTO
from validator.ClientValidator import ClientValidator


class ClientService:
    _client_dao_ = ClientDao()
    _client_validator_ = ClientValidator()
    _login_service_ = LoginService()

    @classmethod
    def get_client_by_id(cls, client_id: int, db: Session):
        client: ClientEntity = cls._client_dao_.get_client(client_id=client_id, db=db)

        if client is not None:
            client_dto = ClientResponse()
            response = client_dto.map(client_entity=client)
            return response

        return None

    @classmethod
    def create_client(cls, client_req: ClientRequestDTO, db: Session):
        response = wrapperDTO()

        id_login_created = cls._login_service_.create_user_login(client_req.email, client_req.password, "Cliente", db)

        cls._client_validator_.validate_fields(client_req.__dict__)
        client_is_created = cls._client_dao_.create_client(client_req, id_login_created, db)

        if not client_is_created:
            cls._login_service_.delete_user_login(client_req.email, db)
            raise CustomError(
                name="Error in create_client",
                detail="Client not created or updated",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response.data = [{"message": "Cliente creado correctamente"}]
        return response.__dict__
