from sqlalchemy.orm import Session
from starlette import status

from dto.request.ClientRequestDTO import ClientRequestDTO
from dto.request.ClientSocialRegistrationRequest import ClientSocialRegistrationRequest
from dto.response.ClientResponse import ClientResponse
from dto.response.SimpleResponse import SimpleResponse
from repository.dao.ClientDao import ClientDao
from repository.dao.UserDao import UserDao
from repository.entity.ClientEntity import ClientEntity
from repository.entity.UserEntity import UserEntity
from service.JwtService import JwtService
from service.LoginService import LoginService
from service.PasswordService import PasswordService
from util.Constants import Constants
from util.ThrowerExceptions import ThrowerExceptions
from validator.ClientValidator import ClientValidator


class ClientService:
    _user_dao_ = UserDao()
    _client_dao_ = ClientDao()
    _client_validator_ = ClientValidator()
    _login_service_ = LoginService()
    _tokenService_ = JwtService()
    _throwerExceptions = ThrowerExceptions()

    @classmethod
    async def get_client_by_id(cls, client_id: int, db: Session):
        client: ClientEntity = cls._client_dao_.get_client_by_id(client_id=client_id, db=db)

        if client is None:
            await cls._throwerExceptions.throw_custom_exception(name=Constants.CLIENT_NOT_FOUND_ERROR_DETAIL,
                                                                detail=Constants.CLIENT_NOT_FOUND_ERROR_DETAIL,
                                                                status_code=status.HTTP_204_NO_CONTENT)

        client_dto = ClientResponse()
        response = client_dto.map(client_entity=client)
        return response

    @classmethod
    async def create_client(cls, client_req: ClientRequestDTO, db: Session):
        cls._client_validator_.validate_fields(client_req.__dict__)
        id_login_created = await cls._login_service_.create_user_login(client_req.email, client_req.password, "Cliente",
                                                                       db)
        client_is_created = cls._client_dao_.create_client(client_req, id_login_created, db)

        if not client_is_created:
            # TODO: Validar como hacer reversa si existe una excep no controlada
            cls._user_dao_.delete_user_by_id(id_login_created, db)
            cls._login_service_.delete_user_login(client_req.email, db)

            await cls._throwerExceptions.throw_custom_exception(name=Constants.CLIENT_CREATE_ERROR_DETAIL,
                                                                detail=Constants.CLIENT_CREATE_ERROR_DETAIL,
                                                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return client_is_created

    async def create_client_social_networks(self, client_request: ClientSocialRegistrationRequest, db: Session):

        # fields validations
        client_request.validate_fields()

        # verify if email exists
        user: UserEntity = self._user_dao_.verify_email(client_request.email, db)

        if not user:
            # try to verify the token and decode it
            token = self._tokenService_.decode_token_firebase(client_request.token)

            if token.email != client_request.email:
                await self._throwerExceptions.throw_custom_exception(name=Constants.LOGIN_ERROR,
                                                                     detail=Constants.LOGIN_ERROR,
                                                                     status_code=status.HTTP_400_BAD_REQUEST,
                                                                     cause=f"token.email: {token.email} es diferente a client_request.email: {client_request.email}")

            # create client entity
            new_user = client_request.to_user_entity(image_url=token.picture,
                                                     password=PasswordService.generate_password())
            new_client = client_request.to_client_entity(user=new_user)
            self._client_dao_.create_client_v2(client=new_client, db=db)

            return SimpleResponse("Cliente creado correctamente")
        else:
            await self._throwerExceptions.throw_custom_exception(name=Constants.USER_ALREADY_EXIST,
                                                                 detail=Constants.USER_ALREADY_EXIST,
                                                                 status_code=status.HTTP_400_BAD_REQUEST,
                                                                 cause=f"El usuario con id: {user.id} ya existe en el sistema")
