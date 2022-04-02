from fastapi import UploadFile
from sqlalchemy.orm import Session
from starlette import status
from loguru import logger

from src.dto.request.LoginSocialRequest import LoginSocialRequest
from src.dto.request.LoginUserRequest import LoginUserRequest
from src.dto.response.UpdateProfileImageResponse import UpdateProfileImageDto
from src.dto.response.UserTokenResponse import UserTokenResponse
from src.util.UserType import UserType
from src.repository.dao.ClientDao import ClientDao
from src.repository.dao.LocalDao import LocalDAO
from src.repository.dao.UserDao import UserDao
from src.repository.entity.BranchEntity import BranchEntity
from src.repository.entity.ClientEntity import ClientEntity
from src.repository.entity.UserEntity import UserEntity
from src.service.CloudinaryService import CloudinaryService
from src.service.JwtService import JwtService
from src.util.Constants import Constants
from src.exception.ThrowerExceptions import ThrowerExceptions
from src.service.EmailService import EmailService
from src.util.EmailSubject import EmailSubject
from src.service.PasswordService import PasswordService
from src.dto.response.SimpleResponse import SimpleResponse
from src.exception.exceptions import CustomError
from src.dto.internal.TokenFirebase import TokenFirebase


class UserService:
    _cloudinary_service_ = CloudinaryService()
    _user_dao_ = UserDao()
    _token_service = JwtService()
    _clientDao_ = ClientDao()
    _localDao_ = LocalDAO()
    _throwerExceptions = ThrowerExceptions()
    _email_service = EmailService()
    _password_service_ = PasswordService()

    async def login_user(self, login_request: LoginUserRequest, ip: str, db: Session):
        logger.info('login_user')

        login_request.validate_fields()
        await self._token_service.verify_email_firebase(login_request.email)

        user: UserEntity = self._get_user(email=login_request.email, password=login_request.password, db=db)

        return self._create_token_by_user(user=user, ip=ip, db=db)

    async def social_login_user(self, login_request: LoginSocialRequest, ip: str, db: Session) -> UserTokenResponse:
        logger.info("social_login_user")

        login_request.validate_fields()

        await self._token_service.decode_token_firebase(login_request.token)

        user: UserEntity = self._get_user(email=login_request.email, db=db)

        return self._create_token_by_user(user=user, ip=ip, db=db)

    def _get_user(self, email: str, db: Session, password=None) -> UserEntity:
        logger.info("_get_user")

        user: UserEntity = self._user_dao_.user_login(email=email, db=db)

        if not user:
            raise CustomError(name="Credenciales incorrectas",
                              detail="Credenciales incorrectas",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Credenciales incorrectas")

        if not user.is_active:
            raise CustomError(name=Constants.CLIENT_UNAUTHORIZED,
                              detail=Constants.TOKEN_NOT_EXIST_DETAIL,
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

    async def send_email_forgotten_password(self, email: str, db: Session):
        logger.info('email: {}', email)
        is_user: bool = self._user_dao_.send_email_forgotten_password(email=email, db=db)

        if not is_user:
            await self._throwerExceptions.throw_custom_exception(name=Constants.USER_NOT_FOUND,
                                                                 detail=Constants.USER_NOT_FOUND_DETAIL,
                                                                 status_code=status.HTTP_400_BAD_REQUEST)

        self._email_service.send_email(user=Constants.USER,
                                       subject=EmailSubject.FORGOTTEN_PASSWORD,
                                       receiver_email=email)

    def activate_user(self, token: str, db: Session):
        logger.info("token: {}", token)
        token_profile_activation = self._token_service.decode_token_profile_activation(token=token)

        if token_profile_activation.rol == UserType.CLIENT:
            logger.info("Is client")
            self._user_dao_.activate_client_user(token_profile_activation=token_profile_activation, db=db)

        if token_profile_activation.rol == UserType.MANAGER:
            logger.info("Is manager")
            self._user_dao_.activate_manager_user(token_profile_activation=token_profile_activation, db=db)

        return SimpleResponse("Cuenta activada correctamente")
