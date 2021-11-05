from fastapi import status, APIRouter, Response, Request
from fastapi.params import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter  # TODO: Eliminar paquete, no funciona por alguna razón
from loguru import logger
from configuration.database.database import SessionLocal, get_data_base
from service.LocalService import LocalService
from dto.request.local_request_dto import NewAccount, NewBranch
from service.JwtService import JwtService


from service.MapboxService import MapBoxService
local_controller = APIRouter(
    prefix="/v1/locals",
    tags=["Local"]
)


@local_controller.get("/test") # TODO: ELIMINAAAAAAAAAAAAARRRRRRRRRRRRR
async def test_mapbox():
    map_box = MapBoxService()
    await map_box.get_latitude_longitude(address="avenida 10 de julio huamachuco 680", state_name="Santiago")
    # TODO: Para ocupar mapbox, obtener el string del State y el país por defecto Chile
    # TODO: Meterse a [features] --> Recorrer la lista
    # TODO: Por cada elemento, entrar a [context]
    # TODO: Dentro de context ubicar el id que su valor contenga la palabra place para la comuna y filtrarla con el State.name
    # TODO: Dentro de context ubicar el id que su valor contenga la palabra country para el pais y filtrar por el pais
    # TODO: AL ser True los 2 puntos anteriores, retornar el valor [center]
    pass


@local_controller.post("/register", status_code=status.HTTP_201_CREATED)
async def register_account(new_account: NewAccount, db: SessionLocal = Depends(get_data_base)):
    logger.info("new_account: {}", new_account)
    local_service = LocalService()
    account_created = await local_service.create_new_account(new_account=new_account, db=db)

    return account_created


@local_controller.get('/', status_code=status.HTTP_200_OK)  # TODO: response_model=BranchProfileLoginOutput
async def read_account(request: Request, response: Response, db: SessionLocal = Depends(get_data_base)):
    logger.info('login')

    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = request.headers['authorization']
    jwt_service = JwtService()
    token_payload = jwt_service.verify_and_get_token_data(token=token)

    local_service = LocalService()
    branch_profile = local_service.get_account_profile(branch_id=token_payload.id_branch_client, db=db)

    if branch_profile['data'] is None:
        response.status_code = status.HTTP_204_NO_CONTENT

    return branch_profile


@local_controller.post('/new-branch', status_code=status.HTTP_201_CREATED)  # TODO: response_model=NewBranchOutput
async def add_branch(request: Request, response: Response,
                     new_branch: NewBranch, db: SessionLocal = Depends(get_data_base)):
    logger.info('new_branch: {}', new_branch)

    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = request.headers['authorization']

    jwt_service = JwtService()
    token_payload = jwt_service.verify_and_get_token_data(token=token)

    local_service = LocalService()
    branch_profile = await local_service.add_new_branch(branch_id=token_payload.id_branch_client, new_branch=new_branch, db=db)
    return branch_profile
