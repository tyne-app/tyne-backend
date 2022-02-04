from fastapi import status, APIRouter, Response, Depends, Request, UploadFile, File
from sqlalchemy.orm import Session

from src.configuration.database import database
from src.dto.request.LoginSocialRequest import LoginSocialRequest
from src.dto.request.LoginUserRequest import LoginUserRequest
from src.dto.request.UserChangePasswordRequest import UserChangePasswordRequest
from src.dto.response.SimpleResponse import SimpleResponse
from src.service.JwtService import JwtService
from src.service.UserService import UserService

user_controller = APIRouter(
    prefix="/v1/users",
    tags=["Users"]
)

_service_ = UserService()
_jwt_service_ = JwtService()


@user_controller.post(
    '/login',
    status_code=status.HTTP_200_OK
)
async def login(response: Response,
                request: Request,
                loginRequest: LoginUserRequest,
                db: Session = Depends(database.get_data_base)):
    token = await _service_.login_user(loginRequest=loginRequest, ip=request.client.host, db=db)

    if token is None:
        response.status_code = status.HTTP_204_NO_CONTENT

    return token


@user_controller.post(
    '/social-login',
    status_code=status.HTTP_200_OK
)
async def social_login(response: Response,
                       request: Request,
                       loginRequest: LoginSocialRequest,
                       db: Session = Depends(database.get_data_base)):
    token = await _service_.social_login_user(loginRequest=loginRequest, ip=request.client.host, db=db)
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


@user_controller.post('/forgotten-password/{email}', status_code=status.HTTP_200_OK)
async def forgotten_password(email: str, db: Session = Depends(database.get_data_base)):
    await _service_.send_email_forgotten_password(email=email, db=db)
    return SimpleResponse("Se ha enviado un correo para restablecer la contraseña")