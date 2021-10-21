from fastapi import status, APIRouter, Response, Depends
from sqlalchemy.orm import Session
from configuration.database import database
from dto.request.LoginUserRequest import LoginUserRequest
from service.user_service import UserService

user_controller = APIRouter(
    prefix="/v1/users",
    tags=["Users"]
)


@user_controller.post(
    '/login',
    status_code=status.HTTP_200_OK
)
def login(response: Response, loginRequest: LoginUserRequest, db: Session = Depends(database.get_data_base)):
    service = UserService()
    token = service.login_user(loginRequest=loginRequest, db=db)

    if token is None:
        response.status_code = status.HTTP_404_NOT_FOUND

    return token

