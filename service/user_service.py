from sqlalchemy.orm import Session
from starlette import status
from dto.request.LoginUserRequest import LoginUserRequest
from exception.exceptions import CustomError
from repository.dao.user_dao import login


class UserService:

    @classmethod
    def login_user(cls, loginRequest: LoginUserRequest, db: Session):
        user = login(loginRequest.email, loginRequest.password, db)

        if user is not None:
            if user.is_active is not True:
                raise CustomError(name="Usuario desactivado",
                                  detail="Validación",
                                  status_code=status.HTTP_401_UNAUTHORIZED,
                                  cause="Usuario desactivado")

        return user

