from sqlalchemy.orm import Session
from loguru import logger
from src.dto.request.ClientRequest import ClientRequest
from src.dto.request.ClientSocialRegistrationRequest import ClientSocialRegistrationRequest
from src.dto.response.ClientResponse import ClientResponse
from src.dto.response.SimpleResponse import SimpleResponse
from src.repository.dao.ClientDao import ClientDao
from src.repository.dao.UserDao import UserDao
from src.repository.entity.ClientEntity import ClientEntity
from src.repository.entity.UserEntity import UserEntity
from src.service.JwtService import JwtService
from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions
from src.validator.ClientValidator import ClientValidator
from src.service.EmailService import EmailService
from src.util.EmailSubject import EmailSubject
from src.service.PasswordService import PasswordService


class ClientService:
    _user_dao_ = UserDao()
    _client_dao_ = ClientDao()
    _client_validator_ = ClientValidator()
    _token_service = JwtService()
    _throwerExceptions = ThrowerExceptions()
    _email_service: EmailService = EmailService()
    _password_service_ = PasswordService()
    _created_client: str = "Cliente creado correctamente"

    # TODO: Se pueden hacer más general los to_entity() y validadores

    async def get_client_by_id(self, client_id: int, db: Session):
        client: ClientEntity = self._client_dao_.get_client_by_id(client_id=client_id, db=db)
        client_dto = ClientResponse()
        return client_dto.map(client_entity=client)

    async def create_client(self, client_request: ClientRequest, db: Session):
        logger.info("Inicio creación credenciales cliente")
        logger.info("cliete_request: {}", client_request)

        await self._client_validator_.validate_fields(
            client_request.__dict__)  # TODO: Lo que es validación puede ser más general

        client_request.password = self._password_service_.encrypt_password(client_request.password)

        user_entity: UserEntity = client_request.to_user_entity()
        client_entity: ClientEntity = client_request.to_client_entity()

        self._client_dao_.create_account(user_entity=user_entity, client_entity=client_entity, db=db)

        logger.info("Credenciales cliente creadas")
        logger.info("Cliente creado. Se enviará email de confirmación")

        activation_token: str = self._token_service.get_token_profile(user_id=user_entity.id,
                                                                      email=user_entity.email,
                                                                      rol=user_entity.id_user_type)

        self._email_service.send_email(user=Constants.CLIENT, subject=EmailSubject.CLIENT_WELCOME,
                                       receiver_email=client_request.email, data=activation_token)

        return SimpleResponse(self._created_client)  # TODO: Dejar estructura de respuesta igual para todo el proyecto

    async def create_client_social_networks(self, client_request: ClientSocialRegistrationRequest, db: Session):
        await client_request.validate_fields()

        token = await self._token_service.decode_token_firebase(client_request.token)
        logger.info("Se decodifica token")

        password_service = PasswordService()

        user_entity = client_request.to_user_entity(image_url=token.get("picture"),
                                                    password=password_service.generate_password())
        client_entity = client_request.to_client_entity()
        self._client_dao_.create_account(user_entity=user_entity, client_entity=client_entity, db=db)

        logger.info("Se crea cliente")

        activation_token: str = self._token_service.get_token_profile(user_id=user_entity.id,
                                                                      email=user_entity.email,
                                                                      rol=user_entity.id_user_type)

        self._email_service.send_email(user=Constants.CLIENT, subject=EmailSubject.CLIENT_WELCOME,
                                       receiver_email=client_request.email, data=activation_token)

        logger.info("Email enviado a correo de cliente")
        return SimpleResponse(self._created_client)
