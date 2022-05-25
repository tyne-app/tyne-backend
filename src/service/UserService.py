from fastapi import UploadFile
from sqlalchemy.orm import Session
from starlette import status
from loguru import logger

from src.dto.request.LoginSocialRequest import LoginSocialRequest
from src.dto.request.LoginUserRequest import LoginUserRequest
from src.dto.response.UpdateProfileImageResponse import UpdateProfileImageDto
from src.dto.response.UserTokenResponse import UserTokenResponse
from src.dto.internal.TokenProfile import TokenProfile
from src.util.UserType import UserType
from src.repository.dao.ClientDao import ClientDao
from src.repository.dao.LocalDao import LocalDAO
from src.repository.dao.UserDao import UserDao
from src.repository.dao.ManagerDao import ManagerDao
from src.repository.entity.BranchEntity import BranchEntity
from src.repository.entity.ClientEntity import ClientEntity
from src.repository.entity.UserEntity import UserEntity
from src.repository.entity.ManagerEntity import ManagerEntity
from src.service.CloudinaryService import CloudinaryService
from src.service.JwtService import JwtService
from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions
from src.service.EmailService import EmailService
from src.util.EmailSubject import EmailSubject
from src.service.PasswordService import PasswordService
from src.dto.response.SimpleResponse import SimpleResponse
from src.exception.exceptions import CustomError


class UserService:
    _cloudinary_service_ = CloudinaryService()
    _user_dao_ = UserDao()
    _token_service = JwtService()
    _clientDao_ = ClientDao()
    _localDao_ = LocalDAO()
    _throwerExceptions = ThrowerExceptions()
    _email_service = EmailService()
    _password_service_ = PasswordService()
    _manager_dao = ManagerDao()

    async def login_user(self, login_request: LoginUserRequest, ip: str, db: Session):
        logger.info('login_user')

        login_request.validate_fields()

        user: UserEntity = self._get_user(email=login_request.email.lower(), is_social=False,
                                          password=login_request.password, db=db)

        return self._create_token_by_user(user=user, ip=ip, db=db)

    async def social_login_user(self, login_request: LoginSocialRequest, ip: str, db: Session) -> UserTokenResponse:
        logger.info("social_login_user")

        login_request.validate_fields()

        await self._token_service.decode_token_firebase(login_request.token)

        user: UserEntity = self._get_user(email=login_request.email, db=db, is_social=True)

        return self._create_token_by_user(user=user, ip=ip, db=db)

    def _get_user(self, email: str, db: Session, is_social: bool, password=None) -> UserEntity:
        logger.info("_get_user")

        user: UserEntity = self._user_dao_.user_login(email=email, db=db)

        if not user:
            raise CustomError(name="Credenciales incorrectas",
                              detail="Credenciales incorrectas",
                              status_code=status.HTTP_401_UNAUTHORIZED,
                              cause="Credenciales incorrectas")

        if not user.is_active:
            raise CustomError(name=Constants.CLIENT_UNAUTHORIZED,
                              detail="El usuario no está activado",
                              status_code=status.HTTP_401_UNAUTHORIZED,
                              cause="El usuario no está activado")

        if password:
            logger.info('Password exist')
            decrypted_password = self._password_service_.decrypt_password(user.password)

            if decrypted_password != password:
                raise CustomError(name="Credenciales incorrectas",
                                  detail="Credenciales incorrectas",
                                  status_code=status.HTTP_401_UNAUTHORIZED,
                                  cause="El usuario no está activado")

        logger.info('User available')
        return user

    def _create_token_by_user(self, user: UserEntity, ip: str, db: Session) -> UserTokenResponse:
        logger.info("_create_token_by_user")

        if user.id_user_type == UserType.MANAGER:
            logger.info("Is manager")
            branch: BranchEntity = self._localDao_.find_branch_by_email_user_manager(email=user.email, db=db)

            return self._create_token(id_user=user.id, id_branch_client=branch.id, rol=user.id_user_type, ip=ip,
                                      name=branch.manager.name, last_name=branch.manager.last_name)

        if user.id_user_type == UserType.CLIENT:
            logger.info("Is client")
            client: ClientEntity = self._clientDao_.find_client_by_email_user(email=user.email, db=db)

            return self._create_token(id_user=user.id, id_branch_client=client.id, rol=user.id_user_type, ip=ip,
                                      name=client.name, last_name=client.last_name)

        raise CustomError(name="Tipo de usuario no existente en el sistema",
                          detail="Tipo de usuario no existente en el sistema",
                          status_code=status.HTTP_401_UNAUTHORIZED,
                          cause="Tipo de usuario no existe")

    def _create_token(self, id_user: int, id_branch_client: int, rol: int,
                      ip: str, name: str, last_name: str) -> UserTokenResponse:
        logger.info("_create_token")

        return self._token_service.get_token(id_user=id_user,
                                             id_branch_client=id_branch_client,
                                             rol=rol, ip=ip, name=name,
                                             last_name=last_name)

    async def change_profile_image(self, user_id: int, file: UploadFile, db: Session):

        # Don't delete this try-except
        try:
            user = self._user_dao_.get_user(user_id=user_id, db=db)

            if user and user.image_url:
                await self._cloudinary_service_.delete_file(user.image_id)
        except:
            pass

        response_cloudinary = await self._cloudinary_service_.upload_image(file=file, user_id=user_id)
        user = self._user_dao_.update_profile_image(user_id=user_id,
                                                    url_image=response_cloudinary.metadata["secure_url"],
                                                    image_id=response_cloudinary.metadata["public_id"], db=db)

        response_dto = UpdateProfileImageDto()
        response_dto.url = user.image_url
        return response_dto

    async def delete_profile_image(self, user_id: int, db: Session):
        user: UserEntity = self._user_dao_.get_user(user_id, db)

        if user is None:
            await self._throwerExceptions.throw_custom_exception(name=Constants.USER_NOT_EXIST,
                                                                 detail=Constants.USER_NOT_EXIST,
                                                                 status_code=status.HTTP_204_NO_CONTENT)

        if user.image_id is None:
            await self._throwerExceptions.throw_custom_exception(name=Constants.USER_NOT_IMAGE_ERROR,
                                                                 detail=Constants.USER_NOT_IMAGE_ERROR,
                                                                 status_code=status.HTTP_400_BAD_REQUEST)

        await self._cloudinary_service_.delete_file(user.image_id)
        self._user_dao_.update_profile_image(user_id, None, None, db)

        return True

    def change_password(self, user_id: int, password: str, db: Session):
        self._user_dao_.change_password(user_id=user_id, password=password, db=db)
        return True

    def send_password_email(self, email: str, db: Session) -> SimpleResponse:
        logger.info('email: {}', email)

        token: str = self._user_token_by_email(email=email, is_active=True, db=db)

        self._email_service.send_email(user=Constants.USER,
                                       subject=EmailSubject.FORGOTTEN_PASSWORD,
                                       receiver_email=email,
                                       data=token)
        return SimpleResponse("Se ha enviado un correo para restablecer la contraseña")

    def restore_password(self, token: str, password: str, db: Session) -> SimpleResponse:
        logger.info("restore_password")

        token_profile: TokenProfile = self._token_service.decode_token_profile(token=token)

        self._user_dao_.change_password(user_id=token_profile.user_id, password=password, db=db)

        return SimpleResponse("Contraseña restaurada correctamente")

    def activate_user(self, token: str,
                      db: Session):
        logger.info("token: {}", token)
        token_profile: TokenProfile = self._token_service.decode_token_profile(token=token)

        self._user_dao_.activate_user(token_profile_activation=token_profile, db=db)

        return SimpleResponse("Cuenta activada correctamente")

    def retry_activation(self, email: str, db: Session) -> SimpleResponse:
        logger.info("email: {}", email)

        token: str = self._user_token_by_email(email=email, is_active=False, db=db)

        self._email_service.send_email(user=Constants.USER, subject=EmailSubject.RETRY_ACTIVATION,
                                       receiver_email=email, data=token)

        return SimpleResponse("Se ha enviado un correo para activar cuenta")

    def _user_token_by_email(self, email: str, is_active: bool, db: Session) -> str:
        logger.info("email: {}", email)

        user_entity: UserEntity = self._user_dao_.user_login(email=email, db=db)

        if user_entity is None:
            raise CustomError(name=Constants.USER_NO_AUTH,
                              detail="No existe usuario con este email",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="No existe usuario con este email")

        if user_entity.is_active != is_active:
            message: str = "activada" if is_active else "desactivada"

            raise CustomError(name=Constants.USER_NO_AUTH,
                              detail='Usuario debe tener cuenta %s' % message,
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="")

        token: str = self._token_service.get_token_profile(user_id=user_entity.id,
                                                           email=user_entity.email,
                                                           rol=user_entity.id_user_type)
        return token
