from sqlalchemy.orm import Session
from starlette import status
from loguru import logger
from src.dto.request.ClientRequest import ClientRequest
from src.dto.request.ClientSocialRegistrationRequest import ClientSocialRegistrationRequest
from src.dto.response.ClientResponse import ClientResponse
from src.dto.response.SimpleResponse import SimpleResponse
from src.util.UserType import UserType
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
from src.service.EmailService import EmailService
from src.util.EmailSubject import EmailSubject
from src.mappers.ClientMapper import ClientMapper
from src.mappers.UserMapper import UserMapper


class ClientService:
    _user_dao_ = UserDao()
    _client_dao_ = ClientDao()
    _client_validator_ = ClientValidator()
    _login_service_ = LoginService()
    _tokenService_ = JwtService()
    _throwerExceptions = ThrowerExceptions()
    _email_service: EmailService = EmailService()
    _client_mapper = ClientMapper()
    _user_mapper = UserMapper()

    async def get_client_by_id(self, client_id: int, db: Session):
        client: ClientEntity = self._client_dao_.get_client_by_id(client_id=client_id, db=db)
        client_dto = ClientResponse()
        return client_dto.map(client_entity=client)

    async def create_client(self, client_req: ClientRequest, db: Session):
        logger.info("Inicio creación credenciales cliente")
        await self._client_validator_.validate_fields(client_req.__dict__)

        user_entity: UserEntity = self._user_mapper.to_user_entity(client_request=client_req)
        client_entity: ClientEntity = self._client_mapper.to_client_entity(client_request=client_req)
        self._client_dao_.create_account(user_entity=user_entity, client_entity=client_entity, db=db)

        logger.info("Credenciales cliente creadas")
        logger.info("Cliente creado. Se enviará email de confirmación")
        self._email_service.send_email(user=Constants.CLIENT, subject=EmailSubject.CLIENT_WELCOME,
                                       receiver_email=client_req.email)

    async def create_client_social_networks(self, client_request: ClientSocialRegistrationRequest, db: Session):
        # fields validations
        await client_request.validate_fields()

        # verify if email exists
        user: UserEntity = self._user_dao_.verify_email(client_request.email, db)

        if not user:
            # try to verify the token and decode it
            token = await self._tokenService_.decode_token_firebase(client_request.token)

            #if token.email != client_request.email:
            #    await self._throwerExceptions.throw_custom_exception(name=Constants.LOGIN_ERROR,
            #                                                         detail=[Constants.LOGIN_ERROR],
            #                                                         status_code=status.HTTP_400_BAD_REQUEST,
            #                                                         cause=f"token.email: {token.email} es diferente a client_request.email: {client_request.email}")
            # create client entity

            passWordService = PasswordService()
            new_user = client_request.to_user_entity(image_url=token.picture,
                                                     password=passWordService.generate_password())
            new_client = client_request.to_client_entity(user=new_user)
            self._client_dao_.create_client_v2(client=new_client, db=db)
            return SimpleResponse("Cliente creado correctamente")
        else:
            await self._throwerExceptions.throw_custom_exception(name=Constants.USER_ALREADY_EXIST,
                                                                 detail=[Constants.USER_ALREADY_EXIST],
                                                                 status_code=status.HTTP_400_BAD_REQUEST,
                                                                 cause=f"El usuario con id: {user.id} ya existe en el sistema")
