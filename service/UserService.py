from fastapi import UploadFile
from sqlalchemy.orm import Session
from starlette import status

from dto.request.LoginSocialRequest import LoginSocialRequest
from dto.request.LoginUserRequest import LoginUserRequest
from dto.response.UpdateProfileImageResponse import UpdateProfileImageDto
from dto.response.UserTokenResponse import UserTokenResponse
from enums.UserTypeEnum import UserTypeEnum
from repository.dao.ClientDao import ClientDao
from repository.dao.LocalDao import LocalDAO
from repository.dao.UserDao import UserDao
from repository.entity.BranchEntity import BranchEntity
from repository.entity.ClientEntity import ClientEntity
from repository.entity.UserEntity import UserEntity
from service.CloudinaryService import CloudinaryService
from service.JwtService import JwtService
from util.Constants import Constants
from util.ThrowerExceptions import ThrowerExceptions


class UserService:
    _cloudinary_service_ = CloudinaryService()
    _user_dao_ = UserDao()
    _tokenService_ = JwtService()
    _clientDao_ = ClientDao()
    _localDao_ = LocalDAO()
    _throwerExceptions = ThrowerExceptions()

    @classmethod
    async def login_user(cls, loginRequest: LoginUserRequest, ip: str, db: Session):

        id_branch_client = None
        name = None
        last_name = None
        loginRequest.validate_fields()

        tokenResponse: UserTokenResponse = None
        user: UserEntity = cls._user_dao_.verify_email(loginRequest.email, db)

        if user is not None:
            if user.is_active is not True:
                await cls._throwerExceptions.throw_custom_exception(name=Constants.CLIENT_UNAUTHORIZED,
                                                                    detail=Constants.TOKEN_NOT_EXIST_DETAIL,
                                                                    status_code=status.HTTP_401_UNAUTHORIZED)

            if user.password != loginRequest.password:
                await cls._throwerExceptions.throw_custom_exception(name=Constants.PASSWORD_INVALID_ERROR,
                                                                    detail=Constants.PASSWORD_INVALID_ERROR,
                                                                    status_code=status.HTTP_401_UNAUTHORIZED)

            if user.id_user_type == UserTypeEnum.encargado_local.value:
                branch: BranchEntity = cls._localDao_.find_branch_by_email_user_manager(email=loginRequest.email, db=db)
                if branch is not None:
                    id_branch_client = branch.id
                    name = branch.manager.name
                    last_name = branch.manager.last_name
            else:
                client: ClientEntity = cls._clientDao_.find_client_by_email_user(email=loginRequest.email, db=db)
                if client is not None:
                    id_branch_client = client.id
                    name = client.name
                    last_name = client.last_name
                pass

            if id_branch_client is None:
                await cls._throwerExceptions.throw_custom_exception(name=Constants.CLIENT_NOT_FOUND_ERROR_DETAIL,
                                                                    detail=Constants.CLIENT_NOT_FOUND_ERROR_DETAIL,
                                                                    status_code=status.HTTP_204_NO_CONTENT)

            tokenResponse = cls._tokenService_.get_token(id_user=user.id, id_branch_client=id_branch_client,
                                                         rol=user.id_user_type, ip=ip, name=name, last_name=last_name)

        return tokenResponse

    @classmethod
    async def social_login_user(cls, loginRequest: LoginSocialRequest, ip: str, db: Session):

        id_branch_client = None
        name = None
        last_name = None
        loginRequest.validate_fields()

        # try to verify the token and decode it
        token_firebase = cls._tokenService_.decode_token_firebase(loginRequest.token)

        tokenResponse: UserTokenResponse = None
        user: UserEntity = cls._user_dao_.verify_email(loginRequest.email, db)

        if user is not None:

            if token_firebase.email != loginRequest.email:
                await cls._throwerExceptions.throw_custom_exception(name=Constants.LOGIN_ERROR,
                                                                    detail=Constants.LOGIN_ERROR,
                                                                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if user.is_active is not True:
                await cls._throwerExceptions.throw_custom_exception(name=Constants.CLIENT_UNAUTHORIZED,
                                                                    detail=Constants.CLIENT_UNAUTHORIZED,
                                                                    status_code=status.HTTP_401_UNAUTHORIZED)

            if user.id_user_type == UserTypeEnum.encargado_local.value:
                branch: BranchEntity = cls._localDao_.find_branch_by_email_user_manager(email=loginRequest.email, db=db)
                if branch is not None:
                    id_branch_client = branch.id
                    name = branch.manager.name
                    last_name = branch.manager.last_name
            else:
                client: ClientEntity = cls._clientDao_.find_client_by_email_user(email=loginRequest.email, db=db)
                if client is not None:
                    id_branch_client = client.id
                    name = client.name
                    last_name = client.last_name
                pass

            if id_branch_client is None:
                await cls._throwerExceptions.throw_custom_exception(name=Constants.CLIENT_NOT_EXIST,
                                                                    detail=Constants.CLIENT_NOT_EXIST,
                                                                    status_code=status.HTTP_204_NO_CONTENT)

            tokenResponse = cls._tokenService_.get_token(id_user=user.id, id_branch_client=id_branch_client,
                                                         rol=user.id_user_type, ip=ip, name=name, last_name=last_name)

        return tokenResponse

    @classmethod
    def change_profile_image(cls, user_id: int, file: UploadFile, db: Session):

        # Don't delete this try-except
        try:
            user = cls._user_dao_.get_user(user_id=user_id, db=db)

            if user and user.image_url:
                cls._cloudinary_service_.delete_file(user.image_id)
        except:
            pass

        response_cloudinary = cls._cloudinary_service_.upload_image(file=file, user_id=user_id)
        user = cls._user_dao_.update_profile_image(user_id=user_id,
                                                   url_image=response_cloudinary.metadata["secure_url"],
                                                   image_id=response_cloudinary.metadata["public_id"], db=db)

        response_dto = UpdateProfileImageDto()
        response_dto.url = user.image_url
        return response_dto

    @classmethod
    async def delete_profile_image(cls, user_id: int, db: Session):
        user: UserEntity = cls._user_dao_.get_user(user_id, db)

        if user is None:
            await cls._throwerExceptions.throw_custom_exception(name=Constants.USER_NOT_EXIST,
                                                                detail=Constants.USER_NOT_EXIST,
                                                                status_code=status.HTTP_204_NO_CONTENT)

        if user.image_id is None:
            await cls._throwerExceptions.throw_custom_exception(name=Constants.USER_NOT_IMAGE_ERROR,
                                                                detail=Constants.USER_NOT_IMAGE_ERROR,
                                                                status_code=status.HTTP_400_BAD_REQUEST)

        cls._cloudinary_service_.delete_file(user.image_id)
        cls._user_dao_.update_profile_image(user_id, None, None, db)

        return True

    @classmethod
    def change_password(cls, user_id: int, password: str, db: Session):
        cls._user_dao_.change_password(user_id=user_id, password=password, db=db)
        return True
