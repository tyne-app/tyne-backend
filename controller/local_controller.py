from fastapi import status, APIRouter, Response, Request
from fastapi.params import Depends
from loguru import logger
from configuration.database.database import SessionLocal, get_data_base
from service.LocalService import LocalService
from dto.request.local_request_dto import NewAccount

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

'''
@local_controller.get('/pre-login/{email}', status_code=status.HTTP_200_OK, response_model=BranchProfilePreLoginOutput)
async def read_account_pre_login(request: Request, response: Response, email: str):
    logger.info('email: {}', email)

    data = await get_branch_pre_login(email=email)

    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data


@local_controller.get('/{email}', status_code=status.HTTP_200_OK, response_model=BranchProfileLoginOutput)
async def read_account(request: Request, response: Response, email: str):
    logger.info('email: {}', email)
    #TODO: Falta probar con token validar

    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    valid_token = await validate_token(client_token=request.headers['authorization'])

    if 'error' in valid_token:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    data = await get_branch_profile(email=email)

    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data


@local_controller.post('/new-branch', status_code=status.HTTP_201_CREATED, response_model=NewBranchOutput)
async def add_branch(request: Request, response: Response, new_branch: AddBranch):
    logger.info('')

    if 'authorization' not in request.headers:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}

    token = request.headers['authorization']
    valid_token = await validate_token(client_token=request.headers['authorization'])

    if 'error' in valid_token:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'error': 'Usuario no autorizado'}


    # TODO: Refactorizar eliminando campo type_lega_representative, se agrega en backend.
    data = await add_new_branch(new_branch=new_branch, client_token=token)

    if 'data' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return data
'''''