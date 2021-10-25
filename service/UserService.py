from fastapi import UploadFile
from sqlalchemy.orm import Session
from starlette import status
from dto.request.LoginUserRequest import LoginUserRequest
from dto.response.UpdateProfileImageDto import UpdateProfileImageDto
from dto.response.UserTokenResponse import UserTokenResponse
from enums.UserTypeEnum import UserTypeEnum
from exception.exceptions import CustomError
from repository.dao.ClientDao import ClientDao
from repository.dao.LocalDAO import LocalDAO
from repository.dao.UserDao import UserDao
from repository.entity.BranchEntity import BranchEntity
from repository.entity.ClientEntity import ClientEntity
from repository.entity.UserEntity import UserEntity
from service.CloudinaryService import CloudinaryService
from service.JwtService import JwtService


class UserService:
    _cloudinary_service_ = CloudinaryService()
    _user_dao_ = UserDao()
    _tokenService_ = JwtService()
    _clientDao_ = ClientDao()
    _localDao_ = LocalDAO()

    @classmethod
    def login_user(cls, loginRequest: LoginUserRequest, ip: str, db: Session):

        id_branch_client = None
        loginRequest.validate_fields()

        tokenResponse: UserTokenResponse = None
        user: UserEntity = cls._user_dao_.login(loginRequest.email, db)

        if user is not None:
            if user.is_active is not True:
                raise CustomError(name="Usuario desactivado",
                                  detail="Validación",
                                  status_code=status.HTTP_401_UNAUTHORIZED,
                                  cause="Usuario desactivado")

            if user.password != loginRequest.password:
                raise CustomError(name="Contraseña inválida",
                                  detail="Validación",
                                  status_code=status.HTTP_401_UNAUTHORIZED,
                                  cause="Contraseña inválida")

            if user.id_user_type == UserTypeEnum.encargado_local.value:
                branch: BranchEntity = cls._localDao_.find_branch_by_email_user_manager(email=loginRequest.email, db=db)
                if branch is not None:
                    id_branch_client = branch.id
            else:
                client: ClientEntity = cls._clientDao_.find_client_by_email_user(email=loginRequest.email, db=db)
                if client is not None:
                    id_branch_client = client.id
                pass

            if id_branch_client is None:
                raise CustomError(name="Usuario no existe",
                                  detail="No encontrado",
                                  status_code=status.HTTP_404_NOT_FOUND,
                                  cause="Usuario no existe")

            tokenResponse = cls._tokenService_.get_token(id_user=user.id, id_branch_client=id_branch_client,
                                                         rol=user.id_user_type, ip=ip)

        return tokenResponse

    @classmethod
    def change_profile_image(cls, user_id: int, file: UploadFile, db: Session):
        response = cls._cloudinary_service_.upload_image(file=file, user_id=user_id)
        user = cls._user_dao_.update_profile_image(user_id=user_id, url_image=response.metadata["secure_url"],
                                                   image_id=response.metadata["public_id"], db=db)

        response_dto = UpdateProfileImageDto(url=user.image_url)
        return response_dto

    @classmethod
    def delete_profile_image(cls, user_id: int, db: Session):
        user: UserEntity = cls._user_dao_.get_user(user_id, db)

        if user is None:
            raise CustomError(name="Usuario no existe",
                              detail="No encontrado",
                              status_code=status.HTTP_404_NOT_FOUND,
                              cause="Usuario no existe")

        if user.image_id is None:
            raise CustomError(name="Error eliminar imagen",
                              detail="Usuario no posee imagen de perfil",
                              status_code=status.HTTP_400_BAD_REQUEST,
                              cause="Usuario no existe")

        cls._cloudinary_service_.delete_file(user.image_id)
        cls._user_dao_.update_profile_image(user_id, None, None, db)

        return True
