from fastapi import status, APIRouter, Response, Request
from fastapi.params import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from loguru import logger
from configuration.database.database import SessionLocal, get_data_base
from service.LocalService import LocalService
from service.IntegrationService import IntegrationService
from dto.request.local_request_dto import NewAccount, NewBranch

local_controller = APIRouter(
    prefix="/v1/locals",
    tags=["Local"]
)

# TODO: Pasar a clase todas las rutas
# TODO: Validar schemas!!


@local_controller.post("/register", status_code=status.HTTP_201_CREATED)
async def register_account(new_account: NewAccount, db: SessionLocal = Depends(get_data_base)):
    logger.info("new_account: {}", new_account)
    local_service = LocalService()
    account_created = await local_service.create_new_account(new_account=new_account, db=db)

    return account_created

# TODO: ELIMINAR
# TODO: para esa ruta, es necesario los datos pre-login?
@local_controller.get('/pre-login/{email}', status_code=status.HTTP_200_OK) # TODO: response_model=BranchProfilePreLoginOutput
def read_account_pre_login(request: Request, response: Response,
                                 email: str, db: SessionLocal = Depends(get_data_base)):
    logger.info('email: {}', email)

    local_service = LocalService()
    account_pre_login = local_service.get_account_pre_login(email=email, db=db)

    return account_pre_login

# TODO: Para esta ruta, qué datos necesito retornar exactmente?
@local_controller.get('/{email}', status_code=status.HTTP_200_OK)  # TODO: response_model=BranchProfileLoginOutput
async def read_account(request: Request, response: Response, email: str, db: SessionLocal = Depends(get_data_base)):
    logger.info('email: {}', email)
    #TODO: Falta probar con token validar

    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = request.headers['authorization']
    integration_service = IntegrationService()
    await integration_service.validate_token(token=token)

    local_service = LocalService()
    branch_profile = local_service.get_account_profile(email=email, db=db)
    return branch_profile


@local_controller.post('/new-branch', status_code=status.HTTP_201_CREATED)  # TODO: response_model=NewBranchOutput
async def add_branch(request: Request, response: Response,
                     new_branch: NewBranch, db: SessionLocal = Depends(get_data_base)):
    logger.info('new_branch: {}', new_branch)

    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = request.headers['authorization']
    integration_service = IntegrationService()
    await integration_service.validate_token(token=token)

    branch_id = await integration_service.token_data(token=token)

    local_service = LocalService()
    branch_profile = local_service.add_new_branch(branch_id=branch_id, db=db)
    return branch_profile

    data = await add_new_branch(new_branch=new_branch, client_token=token)

    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data
