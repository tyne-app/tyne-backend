from loguru import logger
from sqlalchemy.orm import Session
from starlette import status

from dto.request.ClientRequestDTO import ClientRequestDTO
from dto.request.ClientSocialRegistrationRequest import ClientSocialRegistrationRequest
from dto.response.ClientResponse import ClientResponse
from dto.response.SimpleResponse import SimpleResponse
from exception.exceptions import CustomError
from repository.dao.ClientDao import ClientDao
from repository.dao.UserDao import UserDao
from repository.entity.ClientEntity import ClientEntity
from repository.entity.UserEntity import UserEntity
from service.JwtService import JwtService
from service.LoginService import LoginService
from dto.dto import GenericDTO as wrapperDTO
from service.PasswordService import PasswordService
from validator.ClientValidator import ClientValidator


class ClientService:
    _user_dao_ = UserDao()
    _client_dao_ = ClientDao()
    _client_validator_ = ClientValidator()
    _login_service_ = LoginService()
    _tokenService_ = JwtService()

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

    def create_client_social_networks(self, client_request: ClientSocialRegistrationRequest, db: Session):

        # fields validations
        client_request.validate_fields()

        # verify if email exists
        user: UserEntity = self._user_dao_.verify_email(client_request.email, db)

        if not user:
            # try to verify the token and decode it
            token = self._tokenService_.decode_token_firebase(client_request.token)

            if token.email != client_request.email:
                raise CustomError(
                    name="Error al iniciar sesión",
                    detail="Error al iniciar sesión",
                    status_code=status.HTTP_400_BAD_REQUEST)

            # create client entity
            new_user = client_request.to_user_entity(image_url=token.picture,
                                                     password=PasswordService.generate_password())
            new_client = client_request.to_client_entity(user=new_user)
            self._client_dao_.create_client_v2(client=new_client, db=db)

            return SimpleResponse("Cliente creado correctamente")
        else:
            raise CustomError(
                name="Usuario ya existe",
                detail="Usuario ya existe en el sistema",
                status_code=status.HTTP_400_BAD_REQUEST)
