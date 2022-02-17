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


class UserService:
    _cloudinary_service_ = CloudinaryService()
    _user_dao_ = UserDao()
    _tokenService_ = JwtService()
    _clientDao_ = ClientDao()
    _localDao_ = LocalDAO()
    _throwerExceptions = ThrowerExceptions()
    _email_service = EmailService()

    async def login_user(self, loginRequest: LoginUserRequest, ip: str, db: Session):

        id_branch_client = None
        name = None
        last_name = None
        await loginRequest.validate_fields()

        tokenResponse: UserTokenResponse = None
        user: UserEntity = self._user_dao_.verify_email(loginRequest.email, db)

        if user is not None:
            if user.is_active is not True:
                await self._throwerExceptions.throw_custom_exception(name=Constants.CLIENT_UNAUTHORIZED,
                                                                     detail=Constants.TOKEN_NOT_EXIST_DETAIL,
                                                                     status_code=status.HTTP_401_UNAUTHORIZED)

            if user.password != loginRequest.password:
                await self._throwerExceptions.throw_custom_exception(name=Constants.PASSWORD_INVALID_ERROR,
                                                                     detail=Constants.PASSWORD_INVALID_ERROR,
                                                                     status_code=status.HTTP_401_UNAUTHORIZED)

            if user.id_user_type == UserType.MANAGER:
                branch: BranchEntity = self._localDao_.find_branch_by_email_user_manager(email=loginRequest.email,
                                                                                         db=db)
                if branch is not None:
                    id_branch_client = branch.id
                    name = branch.manager.name
                    last_name = branch.manager.last_name
            else:
                client: ClientEntity = self._clientDao_.find_client_by_email_user(email=loginRequest.email, db=db)
                if client is not None:
                    id_branch_client = client.id
                    name = client.name
                    last_name = client.last_name
                pass

            if id_branch_client is None:
                await self._throwerExceptions.throw_custom_exception(name=Constants.CLIENT_NOT_FOUND_ERROR_DETAIL,
                                                                     detail=Constants.CLIENT_NOT_FOUND_ERROR_DETAIL,
                                                                     status_code=status.HTTP_204_NO_CONTENT)

            tokenResponse = self._tokenService_.get_token(id_user=user.id, id_branch_client=id_branch_client,
                                                          rol=user.id_user_type, ip=ip, name=name, last_name=last_name)

        return tokenResponse

    async def social_login_user(self, loginRequest: LoginSocialRequest, ip: str, db: Session):

        id_branch_client = None
        name = None
        last_name = None
        await loginRequest.validate_fields()

        # try to verify the token and decode it
        token_firebase = await self._tokenService_.decode_token_firebase(loginRequest.token)

        tokenResponse: UserTokenResponse = None
        user: UserEntity = self._user_dao_.verify_email(loginRequest.email, db)

        if user is not None:

            # if token_firebase.email != loginRequest.email:
            #    await self._throwerExceptions.throw_custom_exception(name=Constants.LOGIN_ERROR,
            #                                                         detail=Constants.LOGIN_ERROR,
            #                                                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if user.is_active is not True:
                await self._throwerExceptions.throw_custom_exception(name=Constants.CLIENT_UNAUTHORIZED,
                                                                     detail=Constants.CLIENT_UNAUTHORIZED,
                                                                     status_code=status.HTTP_401_UNAUTHORIZED)

            if user.id_user_type == UserType.MANAGER:
                branch: BranchEntity = self._localDao_.find_branch_by_email_user_manager(email=loginRequest.email,
                                                                                         db=db)
                if branch is not None:
                    id_branch_client = branch.id
                    name = branch.manager.name
                    last_name = branch.manager.last_name
            else:
                client: ClientEntity = self._clientDao_.find_client_by_email_user(email=loginRequest.email, db=db)
                if client is not None:
                    id_branch_client = client.id
                    name = client.name
                    last_name = client.last_name
                pass

            if id_branch_client is None:
                await self._throwerExceptions.throw_custom_exception(name=Constants.CLIENT_NOT_EXIST,
                                                                     detail=Constants.CLIENT_NOT_EXIST,
                                                                     status_code=status.HTTP_204_NO_CONTENT)

            tokenResponse = self._tokenService_.get_token(id_user=user.id, id_branch_client=id_branch_client,
                                                          rol=user.id_user_type, ip=ip, name=name, last_name=last_name)

        return tokenResponse

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
