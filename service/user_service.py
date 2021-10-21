from sqlalchemy.orm import Session
from starlette import status
from dto.request.LoginUserRequest import LoginUserRequest
from dto.response.UserTokenResponse import UserTokenResponse
from exception.exceptions import CustomError
from repository.dao.user_dao import UserDao
from repository.entity.UserEntity import UserEntity
from service.jwt_service import JwtService


class UserService:

    @classmethod
    def login_user(cls, loginRequest: LoginUserRequest, db: Session):

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

            tokenService = JwtService()
            tokenResponse = tokenService.get_token()

        return tokenResponse
