from sqlalchemy.orm import Session
from starlette import status
from dto.request.LoginUserRequest import LoginUserRequest
from dto.response.UserTokenResponse import UserTokenResponse
from enums.UserTypeEnum import UserTypeEnum
from exception.exceptions import CustomError
from repository.dao.ClientDao import ClientDao
from repository.dao.LocalDAO import LocalDAO
from repository.dao.user_dao import UserDao
from repository.entity.BranchEntity import BranchEntity
from repository.entity.ClientEntity import ClientEntity
from repository.entity.UserEntity import UserEntity
from service.JwtService import JwtService


class UserService:

    @classmethod
    def login_user(cls, loginRequest: LoginUserRequest, ip: str, db: Session):

        id_branch_client = None
        loginRequest.validate_fields()

        tokenResponse: UserTokenResponse = None
        userDao = UserDao()
        user: UserEntity = userDao.login(loginRequest.email, db)

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
                localDao = LocalDAO()
                branch: BranchEntity = localDao.find_branch_by_email_user_manager(email=loginRequest.email, db=db)
                if branch is not None:
                    id_branch_client = branch.id
            else:
                clientDao = ClientDao()
                client: ClientEntity = clientDao.find_client_by_email_user(email=loginRequest.email, db=db)
                if client is not None:
                    id_branch_client = client.id
                pass

            if id_branch_client is None:
                raise CustomError(name="Usuario no existe",
                                  detail="No encontrado",
                                  status_code=status.HTTP_404_NOT_FOUND,
                                  cause="Usuario no existe")

            tokenService = JwtService()
            tokenResponse = tokenService.get_token(id_user=user.id, id_branch_client=id_branch_client,
                                                   rol=user.id_user_type, ip=ip)

        return tokenResponse
