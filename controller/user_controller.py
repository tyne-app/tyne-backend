from fastapi import status, APIRouter, Response, Depends, Request, UploadFile, File
from sqlalchemy.orm import Session
from configuration.database import database
from dto.request.LoginUserRequest import LoginUserRequest
from dto.response.SimpleResponse import SimpleResponse
from service.JwtService import JwtService
from service.UserService import UserService

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
def login(response: Response, request: Request, loginRequest: LoginUserRequest,
          db: Session = Depends(database.get_data_base)):
    token = _service_.login_user(loginRequest=loginRequest, ip=request.client.host, db=db)

    if token is None:
        response.status_code = status.HTTP_404_NOT_FOUND

    return token


@user_controller.post(
    '/profile-image',
    status_code=status.HTTP_200_OK
)
def upload_profile_image(request: Request, response: Response, image: UploadFile = File(...),
                         db: Session = Depends(database.get_data_base)):

    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = request.headers['authorization']
    token_payload = _jwt_service_.verify_and_get_token_data(token=token)

    response = _service_.change_profile_image(token_payload.id_user, image.file, db)
    return response


@user_controller.delete(
    '/profile-image',
    status_code=status.HTTP_200_OK
)
def delete_profile_image(request: Request, response: Response, db: Session = Depends(database.get_data_base)):

    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = request.headers['authorization']
    token_payload = _jwt_service_.verify_and_get_token_data(token=token)

    _service_.delete_profile_image(token_payload.id_user, db)
    return SimpleResponse("Imagen borrada exitosamente")
