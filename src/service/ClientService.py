from sqlalchemy.orm import Session
from starlette import status

from src.dto.request.ClientRequest import ClientRequest
from src.dto.request.ClientSocialRegistrationRequest import ClientSocialRegistrationRequest
from src.dto.response.ClientResponse import ClientResponse
from src.dto.response.SimpleResponse import SimpleResponse
from src.enums.UserTypeEnum import UserTypeEnum
from src.repository.dao.ClientDao import ClientDao
from src.repository.dao.UserDao import UserDao
from src.repository.entity.ClientEntity import ClientEntity
from src.repository.entity.UserEntity import UserEntity
from src.service.JwtService import JwtService
from src.service.LoginService import LoginService
from src.service.PasswordService import PasswordService
from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions
from src.validator.ClientValidator import ClientValidator


class ClientService:
    _user_dao_ = UserDao()
    _client_dao_ = ClientDao()
    _client_validator_ = ClientValidator()
    _login_service_ = LoginService()
    _tokenService_ = JwtService()
    _throwerExceptions = ThrowerExceptions()

    async def get_client_by_id(self, client_id: int, db: Session):
        client: ClientEntity = self._client_dao_.get_client_by_id(client_id=client_id, db=db)
        client_dto = ClientResponse()
        return client_dto.map(client_entity=client)

    async def create_client(self, client_req: ClientRequest, db: Session):
        # validate fields
        await self._client_validator_.validate_fields(client_req.__dict__)

        # create user
        id_login_created = await self._login_service_.create_user_login(client_req.email, client_req.password,
                                                                        int(UserTypeEnum.cliente.value),
                                                                        db)
        if id_login_created:
            client_is_created = self._client_dao_.create_client(client_req, id_login_created, db)
            if not client_is_created:
                self._user_dao_.delete_user_by_id(id_login_created, db)
                self._login_service_.delete_user_login(client_req.email, db)
                await self._throwerExceptions.throw_custom_exception(name=Constants.CLIENT_CREATE_ERROR_DETAIL,
                                                                     detail=Constants.CLIENT_CREATE_ERROR_DETAIL,
                                                                     status_code=status.HTTP_400_BAD_REQUEST)

    async def create_client_social_networks(self, client_request: ClientSocialRegistrationRequest, db: Session):
        # fields validations
        await client_request.validate_fields()

        # verify if email exists
        user: UserEntity = self._user_dao_.verify_email(client_request.email, db)

        if not user:
            # try to verify the token and decode it
            token = await self._tokenService_.decode_token_firebase(client_request.token)

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
