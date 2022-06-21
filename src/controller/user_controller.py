from fastapi import status, APIRouter, Response, Depends, Request, UploadFile, File
from sqlalchemy.orm import Session

from src.configuration.database import database
from src.dto.request.LoginSocialRequest import LoginSocialRequest
from src.dto.request.LoginUserRequest import LoginUserRequest
from src.dto.request.UserChangePasswordRequest import UserChangePasswordRequest
from src.dto.request.UserEmail import UserEmail
from src.dto.request.UserToken import UserToken
from src.dto.response.SimpleResponse import SimpleResponse
from src.service.JwtService import JwtService
from src.service.UserService import UserService

user_controller = APIRouter(
    prefix="/v1/users",
    tags=["Users"]
)

_service_ = UserService()
_jwt_service_ = JwtService()


@user_controller.post('/activation/retry/token', status_code=status.HTTP_200_OK)
def retry_activation_with_token(user_token: UserToken, db: Session = Depends(database.get_data_base)):
    return _service_.retry_by_email_from_expired_token(token=user_token.token, db=db)


@user_controller.post('/activation/retry/email', status_code=status.HTTP_200_OK)
async def retry_activation_with_email(user_email: UserEmail, db: Session = Depends(database.get_data_base)):
    return _service_.retry_activation(email=user_email.email, db=db)


@user_controller.post(
    '/activation',
    status_code=status.HTTP_200_OK
)
async def activate_user(request: Request, db: Session = Depends(database.get_data_base)):
    return _service_.activate_user(token=request.headers['authorization'], db=db)


@user_controller.post(
    '/login',
    status_code=status.HTTP_200_OK
)
async def login(response: Response,
                request: Request,
                login_request: LoginUserRequest,
                db: Session = Depends(database.get_data_base)):
    token = await _service_.login_user(login_request=login_request, ip=request.client.host, db=db)
    if token is None:
        response.status_code = status.HTTP_204_NO_CONTENT

    return token


@user_controller.post(
    '/social-login',
    status_code=status.HTTP_200_OK
)
async def social_login(response: Response,
                       request: Request,
                       login_request: LoginSocialRequest,
                       db: Session = Depends(database.get_data_base)):
    token = await _service_.social_login_user(login_request=login_request, ip=request.client.host, db=db)
    if token is None:
        response.status_code = status.HTTP_204_NO_CONTENT
    return token


@user_controller.post(
    '/profile-image',
    status_code=status.HTTP_200_OK
)
async def upload_profile_image(request: Request, response: Response, image: UploadFile = File(...),
                               db: Session = Depends(database.get_data_base)):
    token_payload = await _jwt_service_.verify_and_get_token_data(request)

    response = await _service_.change_profile_image(token_payload.id_user, image.file, db)
    return response


@user_controller.delete(
    '/profile-image',
    status_code=status.HTTP_200_OK
)
async def delete_profile_image(request: Request, response: Response, db: Session = Depends(database.get_data_base)):
    token_payload = await _jwt_service_.verify_and_get_token_data(request)
    await _service_.delete_profile_image(token_payload.id_user, db)
    return SimpleResponse("Imagen borrada exitosamente")


@user_controller.put(
    '/password',
    status_code=status.HTTP_200_OK
)
async def update_password(request: Request, response: Response, change_password: UserChangePasswordRequest,
                          db: Session = Depends(database.get_data_base)):
    token_payload = await _jwt_service_.verify_and_get_token_data(request)
    _service_.change_password(token_payload.id_user, change_password.password, db)
    return SimpleResponse("Contraseña actualizada correctamente")


@user_controller.post('/password/send-email', status_code=status.HTTP_200_OK)
def password_email(user_email: UserEmail, db: Session = Depends(database.get_data_base)):
    return _service_.send_password_email(email=user_email.email, db=db)


@user_controller.put('/password/restore', status_code=status.HTTP_202_ACCEPTED)
def restore_password(request: Request, password: UserChangePasswordRequest, db: Session = Depends(database.get_data_base)):
    return _service_.restore_password(token=request.headers['authorization'], password=password.password, db=db)
